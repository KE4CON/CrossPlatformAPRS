using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;
using Aprs.Desktop.Composition;
using Aprs.Desktop.ViewModels;
using Aprs.Desktop.Views;

namespace Aprs.Desktop;

public sealed partial class App : Application
{
    private DesktopRuntime? runtime;

    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
    {
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            if (Design.IsDesignMode)
            {
                // The XAML previewer uses sample data only.
                desktop.MainWindow = new MainWindow
                {
                    DataContext = MainWindowViewModel.CreateDesignTime()
                };
            }
            else
            {
                // Real runtime: construct services and the live view models.
                runtime = DesktopRuntime.Create();
                desktop.MainWindow = new MainWindow
                {
                    DataContext = runtime.MainViewModel
                };
                runtime.Start();

                desktop.ShutdownRequested += OnShutdownRequested;
            }
        }

        base.OnFrameworkInitializationCompleted();
    }

    private async void OnShutdownRequested(object? sender, ShutdownRequestedEventArgs e)
    {
        if (runtime is not null)
        {
            await runtime.DisposeAsync();
            runtime = null;
        }
    }
}
