using Aprs.Core;
using Aprs.Services;

namespace Aprs.Desktop.ViewModels;

public sealed class ObjectManagerViewModel
{
    private readonly IAprsObjectManager objectManager;
    private readonly IAprsObjectEditorService editorService;
    private readonly List<ObjectListRowViewModel> objects = [];

    public ObjectManagerViewModel(IAprsObjectManager objectManager, IAprsObjectEditorService editorService)
    {
        this.objectManager = objectManager;
        this.editorService = editorService;
        Editor = new ObjectEditorViewModel(editorService, editorService.CreateNewDraft(DateTimeOffset.UtcNow));
        NewObjectCommand = new DesktopCommand(CreateNewObject);
        EditSelectedCommand = new DesktopCommand(EditSelectedObject);
        SaveCommand = new DesktopCommand(() => Save());
        CancelCommand = new DesktopCommand(Cancel);
        MarkKilledCommand = new DesktopCommand(() => MarkKilled());
        DeleteCommand = new DesktopCommand(() => DeleteSelectedObject());
        Refresh();
    }

    public IReadOnlyList<ObjectListRowViewModel> Objects => objects;

    public ObjectListRowViewModel? SelectedObject { get; set; }

    public ObjectEditorViewModel Editor { get; }

    public string StatusText { get; private set; } = "No object saved yet.";

    public DesktopCommand NewObjectCommand { get; }

    public DesktopCommand EditSelectedCommand { get; }

    public DesktopCommand SaveCommand { get; }

    public DesktopCommand CancelCommand { get; }

    public DesktopCommand MarkKilledCommand { get; }

    public DesktopCommand DeleteCommand { get; }

    public static ObjectManagerViewModel CreateDesignTime()
    {
        var manager = new AprsObjectManager();
        var profileService = new LocalStationProfileService(new DateTimeOffset(2026, 6, 10, 12, 0, 0, TimeSpan.Zero));
        profileService.UpdateProfile(profileService.GetCurrentProfile() with
        {
            Callsign = "N0CALL",
            FixedLatitude = 39.058333,
            FixedLongitude = -84.508333
        }, new DateTimeOffset(2026, 6, 10, 12, 0, 0, TimeSpan.Zero));
        var parser = new AprsParser();
        manager.AcceptPacket(parser.Parse("OBJ1>APRS:;CHECKPNT1*111111z3903.50N/08430.50W-Checkpoint 1", DateTimeOffset.UtcNow), AprsPacketSource.Simulation);
        manager.AcceptPacket(parser.Parse("ITEM1>APRS:)REPEATER!3903.50N/08430.50WrLocal repeater", DateTimeOffset.UtcNow), AprsPacketSource.Simulation);
        return new ObjectManagerViewModel(manager, new AprsObjectEditorService(manager, profileService));
    }

    public void CreateNewObject()
    {
        Editor.Load(editorService.CreateNewDraft(DateTimeOffset.UtcNow));
        StatusText = "New local object draft.";
    }

    public void EditSelectedObject()
    {
        if (SelectedObject is null)
        {
            StatusText = "Select an object to edit.";
            return;
        }

        var model = editorService.LoadForEditing(SelectedObject.Name, DateTimeOffset.UtcNow);
        if (model is null)
        {
            StatusText = "Selected object was not found.";
            return;
        }

        Editor.Load(model);
        StatusText = $"Editing {SelectedObject.Name}.";
    }

    public AprsObjectEditorSaveResult Save()
    {
        var result = editorService.Save(Editor.ToModel(), DateTimeOffset.UtcNow);
        Editor.Load(result.Model);
        StatusText = result.IsSuccess ? $"Saved {result.ObjectState!.Name} locally." : string.Join("; ", result.Errors);
        Refresh();
        return result;
    }

    public void Cancel()
    {
        Editor.Load(editorService.CreateNewDraft(DateTimeOffset.UtcNow));
        StatusText = "Edit cancelled.";
    }

    public AprsObjectEditorSaveResult MarkKilled()
    {
        var result = editorService.MarkKilled(Editor.ToModel(), DateTimeOffset.UtcNow);
        Editor.Load(result.Model);
        StatusText = result.IsSuccess ? $"Marked {result.ObjectState!.Name} killed locally." : string.Join("; ", result.Errors);
        Refresh();
        return result;
    }

    public bool DeleteSelectedObject()
    {
        if (SelectedObject is null)
        {
            StatusText = "Select a local object to delete.";
            return false;
        }

        var removed = editorService.DeleteLocalObject(SelectedObject.Name);
        StatusText = removed ? $"Removed {SelectedObject.Name}." : "Only local or adopted objects can be removed here.";
        Refresh();
        return removed;
    }

    public void Refresh()
    {
        objects.Clear();
        objects.AddRange(objectManager.GetAllObjects().Select(state => new ObjectListRowViewModel(state)));
    }
}
