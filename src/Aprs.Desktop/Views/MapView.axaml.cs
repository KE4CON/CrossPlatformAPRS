using Avalonia;
using Avalonia.Controls;
using Avalonia.Media;
using Aprs.Desktop.ViewModels;
using Aprs.Services;
using System.ComponentModel;

namespace Aprs.Desktop.Views;

public sealed partial class MapView : UserControl
{
    private MapViewModel? currentViewModel;

    public MapView()
    {
        InitializeComponent();
        DataContextChanged += (_, _) => AttachViewModel();
        SizeChanged += (_, _) => RenderMarkers();
    }

    private void AttachViewModel()
    {
        if (currentViewModel is not null)
        {
            currentViewModel.PropertyChanged -= ViewModel_PropertyChanged;
        }

        currentViewModel = DataContext as MapViewModel;
        if (currentViewModel is not null)
        {
            currentViewModel.PropertyChanged += ViewModel_PropertyChanged;
        }

        RenderMarkers();
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
            RenderMarkers();
        }
    }

    private void RenderMarkers()
    {
        MarkerCanvas.Children.Clear();

        if (DataContext is not MapViewModel viewModel)
        {
            EmptySelectionPanel.IsVisible = true;
            StationDetailsPanel.IsVisible = false;
            return;
        }

        EmptySelectionPanel.IsVisible = !viewModel.HasSelectedStation && !viewModel.HasSelectedObject && !viewModel.HasSelectedWeather;
        StationDetailsPanel.IsVisible = viewModel.HasSelectedStation;

        foreach (var marker in viewModel.Markers)
        {
            var markerButton = CreateMarkerButton(marker, ReferenceEquals(marker, viewModel.SelectedStation));
            markerButton.Click += (_, _) =>
            {
                viewModel.SelectStation(marker);
                RenderMarkers();
            };

            var left = MarkerCanvas.Bounds.Width * marker.MapLeftPercent / 100;
            var top = MarkerCanvas.Bounds.Height * marker.MapTopPercent / 100;
            Canvas.SetLeft(markerButton, Math.Max(8, left - 14));
            Canvas.SetTop(markerButton, Math.Max(8, top - 14));

            MarkerCanvas.Children.Add(markerButton);
        }

        foreach (var marker in viewModel.WeatherMarkers)
        {
            var markerButton = CreateWeatherMarkerButton(marker, ReferenceEquals(marker, viewModel.SelectedWeather));
            markerButton.Click += (_, args) =>
            {
                args.Handled = true;
                viewModel.SelectWeather(marker);
                RenderMarkers();
            };

            var left = MarkerCanvas.Bounds.Width * marker.MapLeftPercent / 100;
            var top = MarkerCanvas.Bounds.Height * marker.MapTopPercent / 100;
            Canvas.SetLeft(markerButton, Math.Max(8, left - 15));
            Canvas.SetTop(markerButton, Math.Max(8, top - 15));

            MarkerCanvas.Children.Add(markerButton);
        }

        foreach (var marker in viewModel.ObjectMarkers)
        {
            var markerButton = CreateObjectMarkerButton(marker, ReferenceEquals(marker, viewModel.SelectedObject));
            markerButton.Click += (_, args) =>
            {
                args.Handled = true;
                viewModel.SelectObject(marker);
                RenderMarkers();
            };

            var left = MarkerCanvas.Bounds.Width * marker.MapLeftPercent / 100;
            var top = MarkerCanvas.Bounds.Height * marker.MapTopPercent / 100;
            Canvas.SetLeft(markerButton, Math.Max(8, left - 16));
            Canvas.SetTop(markerButton, Math.Max(8, top - 16));

            MarkerCanvas.Children.Add(markerButton);
        }
    }

    private void ClearSelectionButton_Click(object? sender, Avalonia.Interactivity.RoutedEventArgs e)
    {
        if (DataContext is MapViewModel viewModel)
        {
            viewModel.ClearSelection();
            RenderMarkers();
        }
    }

    private static Button CreateMarkerButton(StationMarkerViewModel marker, bool isSelected)
    {
        var symbol = new Border
        {
            Width = 28,
            Height = 28,
            CornerRadius = new CornerRadius(14),
            Background = GetMarkerBrush(marker),
            BorderBrush = isSelected ? new SolidColorBrush(Color.FromRgb(250, 204, 21)) : Brushes.White,
            BorderThickness = new Thickness(isSelected ? 3 : 2),
            Child = new TextBlock
            {
                Text = marker.SymbolLabel,
                FontWeight = FontWeight.Bold,
                Foreground = Brushes.White,
                FontSize = marker.SymbolLabel.Length > 1 ? 10 : 13,
                HorizontalAlignment = Avalonia.Layout.HorizontalAlignment.Center,
                VerticalAlignment = Avalonia.Layout.VerticalAlignment.Center
            }
        };

        var label = new Border
        {
            Background = new SolidColorBrush(Color.FromArgb(230, 248, 250, 252)),
            BorderBrush = new SolidColorBrush(Color.FromRgb(203, 213, 225)),
            BorderThickness = new Thickness(1),
            CornerRadius = new CornerRadius(3),
            Padding = new Thickness(5, 2),
            Child = new TextBlock
            {
                Text = marker.DisplayName,
                FontSize = 11,
                Foreground = new SolidColorBrush(Color.FromRgb(15, 23, 42))
            }
        };

        return new Button
        {
            Background = Brushes.Transparent,
            BorderBrush = Brushes.Transparent,
            Padding = new Thickness(0),
            Content = new StackPanel
            {
                Spacing = 3,
                Children =
                {
                    symbol,
                    label
                }
            }
        };
    }

    private static Button CreateObjectMarkerButton(ObjectMarkerViewModel marker, bool isSelected)
    {
        var symbol = new Border
        {
            Width = 30,
            Height = 30,
            CornerRadius = new CornerRadius(4),
            Background = GetObjectMarkerBrush(marker),
            BorderBrush = isSelected ? new SolidColorBrush(Color.FromRgb(250, 204, 21)) : Brushes.White,
            BorderThickness = new Thickness(isSelected ? 3 : 2),
            Opacity = marker.IsInactive ? 0.58 : 1,
            Child = new TextBlock
            {
                Text = marker.SymbolLabel,
                FontWeight = FontWeight.Bold,
                Foreground = Brushes.White,
                FontSize = marker.SymbolLabel.Length > 1 ? 10 : 13,
                HorizontalAlignment = Avalonia.Layout.HorizontalAlignment.Center,
                VerticalAlignment = Avalonia.Layout.VerticalAlignment.Center
            }
        };

        var label = new Border
        {
            Background = new SolidColorBrush(Color.FromArgb(230, 255, 251, 235)),
            BorderBrush = new SolidColorBrush(Color.FromRgb(202, 138, 4)),
            BorderThickness = new Thickness(1),
            CornerRadius = new CornerRadius(3),
            Padding = new Thickness(5, 2),
            Child = new TextBlock
            {
                Text = marker.ObjectName,
                FontSize = 11,
                Foreground = new SolidColorBrush(Color.FromRgb(63, 44, 9))
            }
        };

        return new Button
        {
            Background = Brushes.Transparent,
            BorderBrush = Brushes.Transparent,
            Padding = new Thickness(0),
            Content = new StackPanel
            {
                Spacing = 3,
                Children =
                {
                    symbol,
                    label
                }
            }
        };
    }

    private static Button CreateWeatherMarkerButton(WeatherStationMarkerViewModel marker, bool isSelected)
    {
        var symbol = new Border
        {
            Width = 30,
            Height = 30,
            CornerRadius = new CornerRadius(15),
            Background = marker.IsStale
                ? new SolidColorBrush(Color.FromRgb(100, 116, 139))
                : new SolidColorBrush(Color.FromRgb(2, 132, 199)),
            BorderBrush = isSelected ? new SolidColorBrush(Color.FromRgb(250, 204, 21)) : Brushes.White,
            BorderThickness = new Thickness(isSelected ? 3 : 2),
            Opacity = marker.IsStale ? 0.68 : 1,
            Child = new TextBlock
            {
                Text = marker.SymbolLabel,
                FontWeight = FontWeight.Bold,
                Foreground = Brushes.White,
                FontSize = 10,
                HorizontalAlignment = Avalonia.Layout.HorizontalAlignment.Center,
                VerticalAlignment = Avalonia.Layout.VerticalAlignment.Center
            }
        };

        var label = new Border
        {
            Background = new SolidColorBrush(Color.FromArgb(230, 240, 249, 255)),
            BorderBrush = new SolidColorBrush(Color.FromRgb(14, 116, 144)),
            BorderThickness = new Thickness(1),
            CornerRadius = new CornerRadius(3),
            Padding = new Thickness(5, 2),
            Child = new TextBlock
            {
                Text = marker.DisplayName,
                FontSize = 11,
                Foreground = new SolidColorBrush(Color.FromRgb(12, 74, 110))
            }
        };

        return new Button
        {
            Background = Brushes.Transparent,
            BorderBrush = Brushes.Transparent,
            Padding = new Thickness(0),
            Content = new StackPanel
            {
                Spacing = 3,
                Children =
                {
                    symbol,
                    label
                }
            }
        };
    }

    private static IBrush GetMarkerBrush(StationMarkerViewModel marker)
    {
        return marker.AgeState switch
        {
            StationLifecycleState.Hidden => new SolidColorBrush(Color.FromRgb(71, 85, 105)),
            StationLifecycleState.Expired => new SolidColorBrush(Color.FromRgb(100, 116, 139)),
            _ => GetSymbolBrush(marker)
        };
    }

    private static IBrush GetSymbolBrush(StationMarkerViewModel marker)
    {
        return marker.MarkerIconKey switch
        {
            "home" => new SolidColorBrush(Color.FromRgb(37, 99, 235)),
            "car" => new SolidColorBrush(Color.FromRgb(22, 101, 52)),
            "truck" => new SolidColorBrush(Color.FromRgb(21, 128, 61)),
            "weather" => new SolidColorBrush(Color.FromRgb(2, 132, 199)),
            "digipeater" => new SolidColorBrush(Color.FromRgb(147, 51, 234)),
            "repeater" => new SolidColorBrush(Color.FromRgb(190, 18, 60)),
            "object" => new SolidColorBrush(Color.FromRgb(202, 138, 4)),
            _ => new SolidColorBrush(Color.FromRgb(37, 99, 235))
        };
    }

    private static IBrush GetObjectMarkerBrush(ObjectMarkerViewModel marker)
    {
        if (marker.IsKilled || marker.LifecycleState == AprsObjectLifecycleState.Killed)
        {
            return new SolidColorBrush(Color.FromRgb(100, 116, 139));
        }

        if (marker.LifecycleState == AprsObjectLifecycleState.Expired)
        {
            return new SolidColorBrush(Color.FromRgb(120, 113, 108));
        }

        return marker.ObjectType == AprsManagedObjectType.Item
            ? new SolidColorBrush(Color.FromRgb(217, 119, 6))
            : new SolidColorBrush(Color.FromRgb(202, 138, 4));
    }

    private void MapSurface_PointerPressed(object? sender, Avalonia.Input.PointerPressedEventArgs e)
    {
        if (DataContext is not MapViewModel viewModel || MarkerCanvas.Bounds.Width <= 0 || MarkerCanvas.Bounds.Height <= 0)
        {
            return;
        }

        var point = e.GetPosition(MarkerCanvas);
        var xPercent = point.X / MarkerCanvas.Bounds.Width * 100;
        var yPercent = point.Y / MarkerCanvas.Bounds.Height * 100;
        if (viewModel.HandleMapClick(xPercent, yPercent))
        {
            RenderMarkers();
            e.Handled = true;
        }
    }
}
