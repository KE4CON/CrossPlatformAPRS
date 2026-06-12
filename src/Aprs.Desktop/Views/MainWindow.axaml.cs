using Avalonia.Controls;
using Avalonia.Interactivity;
using Aprs.Desktop.ViewModels;

namespace Aprs.Desktop.Views;

public sealed partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    private void Help_Click(object? sender, RoutedEventArgs e)
    {
        var helpWindow = new HelpWindow
        {
            DataContext = HelpViewModel.CreateDefault()
        };

        helpWindow.Show(this);
    }
}
