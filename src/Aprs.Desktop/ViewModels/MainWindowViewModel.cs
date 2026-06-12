namespace Aprs.Desktop.ViewModels;

using Aprs.Services;

public sealed class MainWindowViewModel
{
    public MainWindowViewModel(MapViewModel map)
        : this(
            map,
            GpsStatusViewModel.CreateDesignTime(),
            RawPacketLogViewModel.CreateDesignTime(),
            DecodedEventLogViewModel.CreateDesignTime(),
            MessageCenterViewModel.CreateDesignTime(),
            ObjectManagerViewModel.CreateDesignTime(),
            DirewolfProfileViewModel.CreateDesignTime(),
            PortStatusViewModel.CreateDesignTime(),
            IGateStatusViewModel.CreateDesignTime(),
            DigipeaterStatusViewModel.CreateDesignTime(),
            WeatherViewModel.CreateDesignTime(),
            ReplayViewModel.CreateDesignTime())
    {
    }

    public MainWindowViewModel(
        MapViewModel map,
        GpsStatusViewModel gpsStatus,
        RawPacketLogViewModel rawPacketLog,
        DecodedEventLogViewModel decodedEventLog,
        MessageCenterViewModel messageCenter,
        ObjectManagerViewModel objectManager,
        DirewolfProfileViewModel direwolfProfile,
        PortStatusViewModel portStatus,
        IGateStatusViewModel iGateStatus,
        DigipeaterStatusViewModel digipeaterStatus,
        WeatherViewModel weather,
        ReplayViewModel replay)
    {
        Map = map;
        StationList = new StationListViewModel(map);
        GpsStatus = gpsStatus;
        RawPacketLog = rawPacketLog;
        DecodedEventLog = decodedEventLog;
        MessageCenter = messageCenter;
        ObjectManager = objectManager;
        DirewolfProfile = direwolfProfile;
        PortStatus = portStatus;
        IGateStatus = iGateStatus;
        DigipeaterStatus = digipeaterStatus;
        Weather = weather;
        Replay = replay;
        Map.AttachObjectManager(ObjectManager);
    }

    public MapViewModel Map { get; }

    public StationListViewModel StationList { get; }

    public GpsStatusViewModel GpsStatus { get; }

    public RawPacketLogViewModel RawPacketLog { get; }

    public DecodedEventLogViewModel DecodedEventLog { get; }

    public MessageCenterViewModel MessageCenter { get; }

    public ObjectManagerViewModel ObjectManager { get; }

    public DirewolfProfileViewModel DirewolfProfile { get; }

    public PortStatusViewModel PortStatus { get; }

    public IGateStatusViewModel IGateStatus { get; }

    public DigipeaterStatusViewModel DigipeaterStatus { get; }

    public WeatherViewModel Weather { get; }

    public ReplayViewModel Replay { get; }

    public static MainWindowViewModel CreateDesignTime()
    {
        return new MainWindowViewModel(MapViewModel.CreateDesignTime());
    }
}
