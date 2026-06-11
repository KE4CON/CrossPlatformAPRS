namespace Aprs.Desktop.ViewModels;

using Aprs.Services;

public sealed class MainWindowViewModel
{
    public MainWindowViewModel(MapViewModel map)
        : this(
            map,
            GpsStatusViewModel.CreateDesignTime(),
            MessageCenterViewModel.CreateDesignTime(),
            ObjectManagerViewModel.CreateDesignTime(),
            DirewolfProfileViewModel.CreateDesignTime(),
            PortStatusViewModel.CreateDesignTime())
    {
    }

    public MainWindowViewModel(
        MapViewModel map,
        GpsStatusViewModel gpsStatus,
        MessageCenterViewModel messageCenter,
        ObjectManagerViewModel objectManager,
        DirewolfProfileViewModel direwolfProfile,
        PortStatusViewModel portStatus)
    {
        Map = map;
        StationList = new StationListViewModel(map);
        GpsStatus = gpsStatus;
        MessageCenter = messageCenter;
        ObjectManager = objectManager;
        DirewolfProfile = direwolfProfile;
        PortStatus = portStatus;
        Map.AttachObjectManager(ObjectManager);
    }

    public MapViewModel Map { get; }

    public StationListViewModel StationList { get; }

    public GpsStatusViewModel GpsStatus { get; }

    public MessageCenterViewModel MessageCenter { get; }

    public ObjectManagerViewModel ObjectManager { get; }

    public DirewolfProfileViewModel DirewolfProfile { get; }

    public PortStatusViewModel PortStatus { get; }

    public static MainWindowViewModel CreateDesignTime()
    {
        return new MainWindowViewModel(MapViewModel.CreateDesignTime());
    }
}
