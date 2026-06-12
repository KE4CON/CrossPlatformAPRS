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
            EventMonitorViewModel.CreateDesignTime(),
            MessageCenterViewModel.CreateDesignTime(),
            ObjectManagerViewModel.CreateDesignTime(),
            DirewolfProfileViewModel.CreateDesignTime(),
            PortStatusViewModel.CreateDesignTime(),
            IGateStatusViewModel.CreateDesignTime(),
            DigipeaterStatusViewModel.CreateDesignTime(),
            WeatherViewModel.CreateDesignTime(),
            ReplayViewModel.CreateDesignTime(),
            RfDiagnosticsViewModel.CreateDesignTime(),
            AlertRulesViewModel.CreateDesignTime(),
            GeofenceEditorViewModel.CreateDesignTime(),
            SimulationViewModel.CreateDesignTime(),
            TrainingModeViewModel.CreateDesignTime())
    {
    }

    public MainWindowViewModel(
        MapViewModel map,
        GpsStatusViewModel gpsStatus,
        RawPacketLogViewModel rawPacketLog,
        DecodedEventLogViewModel decodedEventLog,
        EventMonitorViewModel eventMonitor,
        MessageCenterViewModel messageCenter,
        ObjectManagerViewModel objectManager,
        DirewolfProfileViewModel direwolfProfile,
        PortStatusViewModel portStatus,
        IGateStatusViewModel iGateStatus,
        DigipeaterStatusViewModel digipeaterStatus,
        WeatherViewModel weather,
        ReplayViewModel replay,
        RfDiagnosticsViewModel rfDiagnostics,
        AlertRulesViewModel alerts,
        GeofenceEditorViewModel geofences,
        SimulationViewModel simulation,
        TrainingModeViewModel training)
    {
        Map = map;
        StationList = new StationListViewModel(map);
        GpsStatus = gpsStatus;
        RawPacketLog = rawPacketLog;
        DecodedEventLog = decodedEventLog;
        EventMonitor = eventMonitor;
        MessageCenter = messageCenter;
        ObjectManager = objectManager;
        DirewolfProfile = direwolfProfile;
        PortStatus = portStatus;
        IGateStatus = iGateStatus;
        DigipeaterStatus = digipeaterStatus;
        Weather = weather;
        Replay = replay;
        RfDiagnostics = rfDiagnostics;
        Alerts = alerts;
        Geofences = geofences;
        Simulation = simulation;
        Training = training;
        Map.AttachObjectManager(ObjectManager);
    }

    public MapViewModel Map { get; }

    public StationListViewModel StationList { get; }

    public GpsStatusViewModel GpsStatus { get; }

    public RawPacketLogViewModel RawPacketLog { get; }

    public DecodedEventLogViewModel DecodedEventLog { get; }

    public EventMonitorViewModel EventMonitor { get; }

    public MessageCenterViewModel MessageCenter { get; }

    public ObjectManagerViewModel ObjectManager { get; }

    public DirewolfProfileViewModel DirewolfProfile { get; }

    public PortStatusViewModel PortStatus { get; }

    public IGateStatusViewModel IGateStatus { get; }

    public DigipeaterStatusViewModel DigipeaterStatus { get; }

    public WeatherViewModel Weather { get; }

    public ReplayViewModel Replay { get; }

    public RfDiagnosticsViewModel RfDiagnostics { get; }

    public AlertRulesViewModel Alerts { get; }

    public GeofenceEditorViewModel Geofences { get; }

    public SimulationViewModel Simulation { get; }

    public TrainingModeViewModel Training { get; }

    public static MainWindowViewModel CreateDesignTime()
    {
        return new MainWindowViewModel(MapViewModel.CreateDesignTime());
    }
}
