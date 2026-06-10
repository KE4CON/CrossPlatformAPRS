using Avalonia;
using Avalonia.Controls;
using Avalonia.Media;
using Aprs.Desktop.ViewModels;
using Aprs.Services;

namespace Aprs.Desktop.Views;

public sealed partial class MapView : UserControl
{
    public MapView()
    {
        InitializeComponent();
        DataContextChanged += (_, _) => RenderMarkers();
        SizeChanged += (_, _) => RenderMarkers();
    }

    private void RenderMarkers()
    {
        MarkerCanvas.Children.Clear();

        if (DataContext is not MapViewModel viewModel)
        {
            return;
        }

        foreach (var marker in viewModel.Markers)
        {
            var markerButton = CreateMarkerButton(marker);
            markerButton.Click += (_, _) => viewModel.SelectStation(marker);

            var left = MarkerCanvas.Bounds.Width * marker.MapLeftPercent / 100;
            var top = MarkerCanvas.Bounds.Height * marker.MapTopPercent / 100;
            Canvas.SetLeft(markerButton, Math.Max(8, left - 14));
            Canvas.SetTop(markerButton, Math.Max(8, top - 14));

            MarkerCanvas.Children.Add(markerButton);
        }
    }

    private static Button CreateMarkerButton(StationMarkerViewModel marker)
    {
        var symbol = new Border
        {
            Width = 28,
            Height = 28,
            CornerRadius = new CornerRadius(14),
            Background = GetMarkerBrush(marker),
            BorderBrush = Brushes.White,
            BorderThickness = new Thickness(2),
            Child = new TextBlock
            {
                Text = marker.SymbolLabel,
                FontWeight = FontWeight.Bold,
                Foreground = Brushes.White,
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

    private static IBrush GetMarkerBrush(StationMarkerViewModel marker)
    {
        return marker.AgeState switch
        {
            StationLifecycleState.Active => new SolidColorBrush(Color.FromRgb(22, 101, 52)),
            StationLifecycleState.Stale => new SolidColorBrush(Color.FromRgb(180, 83, 9)),
            StationLifecycleState.Expired => new SolidColorBrush(Color.FromRgb(100, 116, 139)),
            StationLifecycleState.Hidden => new SolidColorBrush(Color.FromRgb(71, 85, 105)),
            _ => new SolidColorBrush(Color.FromRgb(37, 99, 235))
        };
    }
}
