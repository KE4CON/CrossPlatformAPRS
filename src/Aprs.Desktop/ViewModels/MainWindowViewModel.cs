namespace Aprs.Desktop.ViewModels;

using Aprs.Services;

public sealed class MainWindowViewModel
{
    public MainWindowViewModel(MapViewModel map)
        : this(map, GpsStatusViewModel.CreateDesignTime(), MessageCenterViewModel.CreateDesignTime(), ObjectManagerViewModel.CreateDesignTime())
    {
    }

    public MainWindowViewModel(MapViewModel map, GpsStatusViewModel gpsStatus, MessageCenterViewModel messageCenter, ObjectManagerViewModel objectManager)
    {
        Map = map;
        StationList = new StationListViewModel(map);
        GpsStatus = gpsStatus;
        MessageCenter = messageCenter;
        ObjectManager = objectManager;
    }

    public MapViewModel Map { get; }

    public StationListViewModel StationList { get; }

    public GpsStatusViewModel GpsStatus { get; }

    public MessageCenterViewModel MessageCenter { get; }

    public ObjectManagerViewModel ObjectManager { get; }

    public static MainWindowViewModel CreateDesignTime()
    {
        return new MainWindowViewModel(MapViewModel.CreateDesignTime());
    }
}
