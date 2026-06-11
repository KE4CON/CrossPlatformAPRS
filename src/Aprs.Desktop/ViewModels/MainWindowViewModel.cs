namespace Aprs.Desktop.ViewModels;

public sealed class MainWindowViewModel
{
    public MainWindowViewModel(MapViewModel map)
        : this(map, GpsStatusViewModel.CreateDesignTime(), MessageCenterViewModel.CreateDesignTime())
    {
    }

    public MainWindowViewModel(MapViewModel map, GpsStatusViewModel gpsStatus, MessageCenterViewModel messageCenter)
    {
        Map = map;
        StationList = new StationListViewModel(map);
        GpsStatus = gpsStatus;
        MessageCenter = messageCenter;
    }

    public MapViewModel Map { get; }

    public StationListViewModel StationList { get; }

    public GpsStatusViewModel GpsStatus { get; }

    public MessageCenterViewModel MessageCenter { get; }

    public static MainWindowViewModel CreateDesignTime()
    {
        return new MainWindowViewModel(MapViewModel.CreateDesignTime());
    }
}
