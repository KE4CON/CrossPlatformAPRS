namespace Aprs.Desktop.ViewModels;

public sealed class MainWindowViewModel
{
    public MainWindowViewModel(MapViewModel map)
    {
        Map = map;
        StationList = new StationListViewModel(map);
    }

    public MapViewModel Map { get; }

    public StationListViewModel StationList { get; }

    public static MainWindowViewModel CreateDesignTime()
    {
        return new MainWindowViewModel(MapViewModel.CreateDesignTime());
    }
}
