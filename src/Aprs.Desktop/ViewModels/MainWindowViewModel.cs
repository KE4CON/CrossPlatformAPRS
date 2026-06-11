namespace Aprs.Desktop.ViewModels;

public sealed class MainWindowViewModel
{
    public MainWindowViewModel(MapViewModel map)
        : this(map, GpsStatusViewModel.CreateDesignTime())
    {
    }

    public MainWindowViewModel(MapViewModel map, GpsStatusViewModel gpsStatus)
    {
        Map = map;
        StationList = new StationListViewModel(map);
        GpsStatus = gpsStatus;
    }

    public MapViewModel Map { get; }

    public StationListViewModel StationList { get; }

    public GpsStatusViewModel GpsStatus { get; }

    public static MainWindowViewModel CreateDesignTime()
    {
        return new MainWindowViewModel(MapViewModel.CreateDesignTime());
    }
}
