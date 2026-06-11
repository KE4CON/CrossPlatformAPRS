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
            DirewolfProfileViewModel.CreateDesignTime())
    {
    }

    public MainWindowViewModel(
        MapViewModel map,
        GpsStatusViewModel gpsStatus,
        MessageCenterViewModel messageCenter,
        ObjectManagerViewModel objectManager,
        DirewolfProfileViewModel direwolfProfile)
    {
        Map = map;
        StationList = new StationListViewModel(map);
        GpsStatus = gpsStatus;
        MessageCenter = messageCenter;
        ObjectManager = objectManager;
        DirewolfProfile = direwolfProfile;
        Map.AttachObjectManager(ObjectManager);
    }

    public MapViewModel Map { get; }

    public StationListViewModel StationList { get; }

    public GpsStatusViewModel GpsStatus { get; }

    public MessageCenterViewModel MessageCenter { get; }

    public ObjectManagerViewModel ObjectManager { get; }

    public DirewolfProfileViewModel DirewolfProfile { get; }

    public static MainWindowViewModel CreateDesignTime()
    {
        return new MainWindowViewModel(MapViewModel.CreateDesignTime());
    }
}
