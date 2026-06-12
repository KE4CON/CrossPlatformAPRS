using Aprs.Desktop.ViewModels;
using Xunit;

namespace Aprs.Tests;

public sealed class MainWindowViewModelTests
{
    [Fact]
    public void CreateDesignTime_InitializesMapFirstShellViewModels()
    {
        var viewModel = MainWindowViewModel.CreateDesignTime();

        Assert.NotNull(viewModel.Map);
        Assert.NotNull(viewModel.StationList);
        Assert.NotNull(viewModel.RawPacketLog);
    }

    [Fact]
    public void CreateDesignTime_KeepsFeaturePanelViewModelsAvailable()
    {
        var viewModel = MainWindowViewModel.CreateDesignTime();

        Assert.NotNull(viewModel.MessageCenter);
        Assert.NotNull(viewModel.ObjectManager);
        Assert.NotNull(viewModel.Weather);
        Assert.NotNull(viewModel.DecodedEventLog);
        Assert.NotNull(viewModel.EventMonitor);
        Assert.NotNull(viewModel.Replay);
        Assert.NotNull(viewModel.RfDiagnostics);
        Assert.NotNull(viewModel.Alerts);
    }
}
