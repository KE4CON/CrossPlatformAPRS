namespace Aprs.Desktop.ViewModels;

public sealed class MainWindowViewModel
{
    public MainWindowViewModel(MapViewModel map)
    {
        Map = map;
    }

    public MapViewModel Map { get; }

    public static MainWindowViewModel CreateDesignTime()
    {
        return new MainWindowViewModel(MapViewModel.CreateDesignTime());
    }
}
