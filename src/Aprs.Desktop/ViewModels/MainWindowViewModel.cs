using System.Collections.ObjectModel;

namespace Aprs.Desktop.ViewModels;

public sealed class MainWindowViewModel
{
    private MainWindowViewModel(IEnumerable<PaneViewModel> panes)
    {
        Panes = new ObservableCollection<PaneViewModel>(panes);
    }

    public ObservableCollection<PaneViewModel> Panes { get; }

    public static MainWindowViewModel CreateDesignTime()
    {
        return new MainWindowViewModel(
        [
            new PaneViewModel("Map", "Live APRS station positions", "Map display will appear here."),
            new PaneViewModel("Station List", "Latest heard stations", "Station data will appear after packets are received."),
            new PaneViewModel("Raw Packet Monitor", "Incoming APRS packet lines", "Raw packet traffic will appear here."),
            new PaneViewModel("Messages", "APRS messages and acknowledgements", "Message conversations will appear here."),
            new PaneViewModel("Objects", "APRS objects and items", "Objects and items will appear here."),
            new PaneViewModel("Weather", "Weather packet summaries", "Weather reports will appear here."),
            new PaneViewModel("Settings", "Connection and safety settings", "Configuration controls will appear here.")
        ]);
    }
}
