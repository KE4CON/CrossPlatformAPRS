using Avalonia.Controls;
using Aprs.Desktop.ViewModels;
using Aprs.Services;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.ComponentModel;
using System.IO;
using System.Linq;
using Mapsui;
using Mapsui.Layers;
using Mapsui.Projections;
using Mapsui.Styles;
using Mapsui.Tiling;
using Mapsui.Tiling.Layers;
using BruTile.MbTiles;
using SQLite;

namespace Aprs.Desktop.Views;

public sealed partial class MapView : UserControl
{
    private MapViewModel? currentViewModel;
    private GenericCollectionLayer<List<IFeature>>? markerLayer;
    private bool mapInitialized;
    private bool hasFitToData;

    public MapView()
    {
        InitializeComponent();
        Loaded += (_, _) => InitializeMap();
        DataContextChanged += (_, _) => AttachViewModel();
    }

    private void InitializeMap()
    {
        if (mapInitialized)
        {
            return;
        }

        mapInitialized = true;

        var map = MapControl.Map;
        map.Layers.Add(CreateBaseLayer());

        markerLayer = new GenericCollectionLayer<List<IFeature>>
        {
            Name = "APRS markers"
        };
        map.Layers.Add(markerLayer);

        map.Info += OnMapInfo;

        RefreshFeatures();

        // With no live stations to fit to (e.g. running offline), open the view over
        // the area the offline tiles actually cover, so the map isn't blank on launch.
        if (!hasFitToData && offlineExtent is { } coverage)
        {
            hasFitToData = true;
            map.Navigator.ZoomToBox(coverage);
        }
    }

    // Offline-first base map: if an "offline.mbtiles" raster tile file is present next
    // to the application, use it so the map works with no internet (for field use).
    // Otherwise fall back to online OpenStreetMap tiles.
    private MRect? offlineExtent;

    private ILayer CreateBaseLayer()
    {
        try
        {
            var mbtilesPath = Path.Combine(AppContext.BaseDirectory, "offline.mbtiles");
            if (File.Exists(mbtilesPath))
            {
                // Register the native SQLite provider used to read the .mbtiles file.
                SQLitePCL.Batteries_V2.Init();
                var source = new MbTilesTileSource(
                    new SQLiteConnectionString(mbtilesPath, false),
                    type: MbTilesType.BaseLayer);
                var extent = source.Schema.Extent;
                offlineExtent = new MRect(extent.MinX, extent.MinY, extent.MaxX, extent.MaxY);
                Console.Error.WriteLine(
                    $"[Map] Using offline tiles: {mbtilesPath} "
                    + $"(extent {extent.MinX:0},{extent.MinY:0} .. {extent.MaxX:0},{extent.MaxY:0})");
                return new TileLayer(source) { Name = "Offline (MBTiles)" };
            }

            Console.Error.WriteLine(
                $"[Map] No offline.mbtiles found at {mbtilesPath}; using online OpenStreetMap.");
        }
        catch (Exception exception)
        {
            Console.Error.WriteLine(
                $"[Map] Offline tiles failed to load ({exception.GetType().Name}: {exception.Message}); "
                + "using online OpenStreetMap.");
        }

        return OpenStreetMap.CreateTileLayer();
    }

    private void AttachViewModel()
    {
        if (currentViewModel is not null)
        {
            currentViewModel.PropertyChanged -= ViewModel_PropertyChanged;
            currentViewModel.Markers.CollectionChanged -= Markers_CollectionChanged;
        }

        currentViewModel = DataContext as MapViewModel;
        if (currentViewModel is not null)
        {
            currentViewModel.PropertyChanged += ViewModel_PropertyChanged;
            currentViewModel.Markers.CollectionChanged += Markers_CollectionChanged;
        }

        UpdatePanels();
        RefreshFeatures();
    }

    private void Markers_CollectionChanged(object? sender, NotifyCollectionChangedEventArgs e)
    {
        RefreshFeatures();
    }

    private void ViewModel_PropertyChanged(object? sender, PropertyChangedEventArgs e)
    {
        if (e.PropertyName is nameof(MapViewModel.SelectedStation)
            or nameof(MapViewModel.SelectedStationDetails)
            or nameof(MapViewModel.HasSelectedStation)
            or nameof(MapViewModel.SelectedObject)
            or nameof(MapViewModel.ObjectMarkers)
            or nameof(MapViewModel.ObjectMarkerCount)
            or nameof(MapViewModel.SelectedWeather)
            or nameof(MapViewModel.WeatherMarkers)
            or nameof(MapViewModel.WeatherMarkerCount))
        {
            UpdatePanels();
            RefreshFeatures();
        }
    }

    private void UpdatePanels()
    {
        if (DataContext is not MapViewModel viewModel)
        {
            EmptySelectionPanel.IsVisible = true;
            StationDetailsPanel.IsVisible = false;
            return;
        }

        EmptySelectionPanel.IsVisible =
            !viewModel.HasSelectedStation && !viewModel.HasSelectedObject && !viewModel.HasSelectedWeather;
        StationDetailsPanel.IsVisible = viewModel.HasSelectedStation;
    }

    private void RefreshFeatures()
    {
        if (markerLayer is null || DataContext is not MapViewModel viewModel)
        {
            return;
        }

        var features = new List<IFeature>();

        foreach (var marker in viewModel.Markers)
        {
            var selected = ReferenceEquals(marker, viewModel.SelectedStation);
            var feature = MakeFeature(marker.MapLeftPercent, marker.MapTopPercent);
            AddStationStyles(feature, marker, selected);
            feature.Styles.Add(LabelFor(marker.DisplayName));
            feature["station"] = marker;
            features.Add(feature);
        }

        foreach (var marker in viewModel.WeatherMarkers)
        {
            var selected = ReferenceEquals(marker, viewModel.SelectedWeather);
            var color = marker.IsStale ? new Color(100, 116, 139) : new Color(2, 132, 199);
            var feature = MakeFeature(marker.MapLeftPercent, marker.MapTopPercent);
            feature.Styles.Add(DotStyle(color, SymbolType.Ellipse, selected));
            feature.Styles.Add(LabelFor(marker.DisplayName));
            feature["weather"] = marker;
            features.Add(feature);
        }

        foreach (var marker in viewModel.ObjectMarkers)
        {
            var selected = ReferenceEquals(marker, viewModel.SelectedObject);
            var feature = MakeFeature(marker.MapLeftPercent, marker.MapTopPercent);
            feature.Styles.Add(DotStyle(ObjectColor(marker), SymbolType.Rectangle, selected));
            feature.Styles.Add(LabelFor(marker.ObjectName));
            feature["object"] = marker;
            features.Add(feature);
        }

        markerLayer.Features.Clear();
        markerLayer.Features.AddRange(features);
        markerLayer.DataHasChanged();

        FitToDataOnce(features);
    }

    // APRS symbol sheets (aprs.fi set by OH7LZB), bundled as embedded resources.
    // Each sheet is a 16-column grid of 64px cells indexed by symbol code (0x21..0x7E).
    private const string PrimarySheet = "embedded://Aprs.Desktop.aprs-symbols-64-0.png";
    private const string SecondarySheet = "embedded://Aprs.Desktop.aprs-symbols-64-1.png";
    private const string OverlaySheet = "embedded://Aprs.Desktop.aprs-symbols-64-2.png";
    private const int CellSize = 64;
    private const double IconScale = 0.45;          // 64px * 0.45 ~= 29px on screen
    private const double SelectedIconScale = 0.55;

    private static PointFeature MakeFeature(double leftPercent, double topPercent)
    {
        // The view model encodes position as a whole-planet percentage (see
        // PlaceholderMapCoordinateConverter): longitude = x*360-180, latitude = 90-y*180.
        // Recover the real coordinate and project to Web Mercator for Mapsui.
        var longitude = (leftPercent / 100.0 * 360.0) - 180.0;
        var latitude = 90.0 - (topPercent / 100.0 * 180.0);
        var (mercatorX, mercatorY) = SphericalMercator.FromLonLat(longitude, latitude);
        return new PointFeature(new MPoint(mercatorX, mercatorY));
    }

    private static bool TryRegion(char code, out BitmapRegion region)
    {
        region = null!;
        if (code < '!' || code > '~')
        {
            return false;
        }

        var index = code - '!';
        region = new BitmapRegion((index % 16) * CellSize, (index / 16) * CellSize, CellSize, CellSize);
        return true;
    }

    private static void AddStationStyles(PointFeature feature, StationMarkerViewModel marker, bool selected)
    {
        var table = marker.SymbolTableIdentifier;
        var code = marker.SymbolCode;

        // No usable APRS symbol: fall back to the colored category dot.
        if (table is null || code is null || !TryRegion(code.Value, out var region))
        {
            feature.Styles.Add(DotStyle(StationColor(marker), SymbolType.Ellipse, selected));
            return;
        }

        if (selected)
        {
            feature.Styles.Add(new SymbolStyle
            {
                SymbolType = SymbolType.Ellipse,
                Fill = new Brush(new Color(250, 204, 21, 170)),
                Outline = new Pen(new Color(202, 138, 4), 2),
                SymbolScale = 0.7
            });
        }

        var scale = selected ? SelectedIconScale : IconScale;
        var sheet = table.Value == '/' ? PrimarySheet : SecondarySheet;
        feature.Styles.Add(new ImageStyle
        {
            Image = new Mapsui.Styles.Image { Source = sheet, BitmapRegion = region },
            SymbolScale = scale
        });

        // For overlay symbols (table id other than '/' or '\'), draw the overlay
        // character glyph on top of the base symbol.
        if (marker.Overlay is char overlay && TryRegion(overlay, out var overlayRegion))
        {
            feature.Styles.Add(new ImageStyle
            {
                Image = new Mapsui.Styles.Image { Source = OverlaySheet, BitmapRegion = overlayRegion },
                SymbolScale = scale
            });
        }
    }

    private static SymbolStyle DotStyle(Color color, SymbolType symbolType, bool selected)
    {
        return new SymbolStyle
        {
            SymbolType = symbolType,
            Fill = new Brush(color),
            Outline = new Pen(selected ? new Color(250, 204, 21) : Color.White, selected ? 3 : 2),
            SymbolScale = selected ? 0.9 : 0.7
        };
    }

    private static LabelStyle LabelFor(string label)
    {
        return new LabelStyle
        {
            Text = label,
            ForeColor = new Color(15, 23, 42),
            BackColor = new Brush(new Color(248, 250, 252, 230)),
            Halo = new Pen(Color.White, 1),
            Offset = new Offset(0, 22),
            Font = new Font { Size = 11 }
        };
    }

    private void FitToDataOnce(IReadOnlyCollection<IFeature> features)
    {
        if (hasFitToData || features.Count == 0)
        {
            return;
        }

        var points = features.OfType<PointFeature>().Select(f => f.Point).ToList();
        if (points.Count == 0)
        {
            return;
        }

        var minX = points.Min(p => p.X);
        var minY = points.Min(p => p.Y);
        var maxX = points.Max(p => p.X);
        var maxY = points.Max(p => p.Y);

        hasFitToData = true;

        if (maxX - minX < 1 && maxY - minY < 1)
        {
            // Single point (or all coincident): center and zoom to a regional resolution.
            MapControl.Map.Navigator.CenterOnAndZoomTo(new MPoint(minX, minY), 611);
            return;
        }

        var box = new MRect(minX, minY, maxX, maxY).Grow((maxX - minX + maxY - minY) * 0.08);
        MapControl.Map.Navigator.ZoomToBox(box);
    }

    private void OnMapInfo(object? sender, MapInfoEventArgs e)
    {
        if (DataContext is not MapViewModel viewModel || markerLayer is null)
        {
            return;
        }

        var feature = e.GetMapInfo(new ILayer[] { markerLayer })?.Feature;
        if (feature is not null)
        {
            if (feature["station"] is StationMarkerViewModel station)
            {
                viewModel.SelectStation(station);
                UpdatePanels();
                RefreshFeatures();
                return;
            }

            if (feature["object"] is ObjectMarkerViewModel objectMarker)
            {
                viewModel.SelectObject(objectMarker);
                UpdatePanels();
                RefreshFeatures();
                return;
            }

            if (feature["weather"] is WeatherStationMarkerViewModel weather)
            {
                viewModel.SelectWeather(weather);
                UpdatePanels();
                RefreshFeatures();
                return;
            }
        }

        // Empty-map click: convert the world position back to the view model's
        // normalized percentage space and forward it (used for placing/moving objects).
        var world = e.WorldPosition;
        if (world is null)
        {
            return;
        }

        var (longitude, latitude) = SphericalMercator.ToLonLat(world.X, world.Y);
        var xPercent = (longitude + 180.0) / 360.0 * 100.0;
        var yPercent = (90.0 - latitude) / 180.0 * 100.0;
        if (viewModel.HandleMapClick(xPercent, yPercent))
        {
            UpdatePanels();
            RefreshFeatures();
        }
    }

    private void ClearSelectionButton_Click(object? sender, Avalonia.Interactivity.RoutedEventArgs e)
    {
        if (DataContext is MapViewModel viewModel)
        {
            viewModel.ClearSelection();
            UpdatePanels();
            RefreshFeatures();
        }
    }

    private static Color StationColor(StationMarkerViewModel marker)
    {
        return marker.AgeState switch
        {
            StationLifecycleState.Hidden => new Color(71, 85, 105),
            StationLifecycleState.Expired => new Color(100, 116, 139),
            _ => marker.MarkerIconKey switch
            {
                "home" => new Color(37, 99, 235),
                "car" => new Color(22, 101, 52),
                "truck" => new Color(21, 128, 61),
                "weather" => new Color(2, 132, 199),
                "digipeater" => new Color(147, 51, 234),
                "repeater" => new Color(190, 18, 60),
                "object" => new Color(202, 138, 4),
                _ => new Color(37, 99, 235)
            }
        };
    }

    private static Color ObjectColor(ObjectMarkerViewModel marker)
    {
        if (marker.IsKilled || marker.LifecycleState == AprsObjectLifecycleState.Killed)
        {
            return new Color(100, 116, 139);
        }

        if (marker.LifecycleState == AprsObjectLifecycleState.Expired)
        {
            return new Color(120, 113, 108);
        }

        return marker.ObjectType == AprsManagedObjectType.Item
            ? new Color(217, 119, 6)
            : new Color(202, 138, 4);
    }
}
