using Aprs.Services;

namespace Aprs.Desktop.ViewModels;

public sealed class MessageCenterViewModel
{
    private readonly IAprsMessageStoreService messageStore;
    private readonly List<MessageRowViewModel> inbox = [];
    private readonly List<MessageRowViewModel> outbox = [];
    private readonly List<MessageRowViewModel> drafts = [];
    private readonly List<MessageRowViewModel> conversation = [];

    public MessageCenterViewModel(IAprsMessageStoreService messageStore)
    {
        this.messageStore = messageStore;
        Refresh();
        SelectedMessage = Inbox.FirstOrDefault() ?? Outbox.FirstOrDefault() ?? Drafts.FirstOrDefault();
        if (SelectedMessage is not null)
        {
            SelectMessage(SelectedMessage);
        }
    }

    public IReadOnlyList<MessageRowViewModel> Inbox => inbox;

    public IReadOnlyList<MessageRowViewModel> Outbox => outbox;

    public IReadOnlyList<MessageRowViewModel> Drafts => drafts;

    public IReadOnlyList<MessageRowViewModel> Conversation => conversation;

    public MessageRowViewModel? SelectedMessage { get; set; }

    public string ComposeLocalStation { get; set; } = "N0CALL";

    public string ComposeRecipient { get; set; } = "K8ABC";

    public string ComposeBody { get; set; } = "Reply text";

    public string ComposeValidationSummary { get; private set; } = "Not validated";

    public int InboxCount => Inbox.Count;

    public int OutboxCount => Outbox.Count;

    public int DraftCount => Drafts.Count;

    public static MessageCenterViewModel CreateDesignTime()
    {
        var store = new AprsMessageStoreService();
        var now = DateTimeOffset.UtcNow;
        store.AddIncomingMessage(CreateDemoMessage("K8ABC", "N0CALL", "Hello there", now.AddMinutes(-12)), "N0CALL", AprsPacketSource.Simulation);
        var draft = store.CreateDraft(new AprsMessageComposeRequest("N0CALL", "K8ABC", "Draft reply"), now.AddMinutes(-5));
        store.QueueMessage(draft.Id, now.AddMinutes(-4));
        store.CreateDraft(new AprsMessageComposeRequest("N0CALL", "W1AW", "Question for net control"), now.AddMinutes(-2));
        return new MessageCenterViewModel(store);
    }

    public void Refresh()
    {
        inbox.Clear();
        inbox.AddRange(messageStore.GetInboxMessages().Select(message => new MessageRowViewModel(message)));
        outbox.Clear();
        outbox.AddRange(messageStore.GetOutboxMessages().Select(message => new MessageRowViewModel(message)));
        drafts.Clear();
        drafts.AddRange(messageStore.GetDrafts().Select(message => new MessageRowViewModel(message)));
        if (SelectedMessage is not null)
        {
            RefreshConversation(SelectedMessage.RemoteStation);
        }
    }

    public void SelectMessage(MessageRowViewModel message)
    {
        SelectedMessage = message;
        RefreshConversation(message.RemoteStation);
    }

    public AprsMessageComposeValidationResult ValidateCompose()
    {
        var validation = messageStore.ValidateComposeRequest(new AprsMessageComposeRequest(
            ComposeLocalStation,
            ComposeRecipient,
            ComposeBody));
        ComposeValidationSummary = validation.IsValid
            ? "Ready to queue"
            : string.Join("; ", validation.Errors);
        return validation;
    }

    private void RefreshConversation(string remoteStation)
    {
        conversation.Clear();
        conversation.AddRange(messageStore.GetConversation(remoteStation).Select(message => new MessageRowViewModel(message)));
    }

    private static Aprs.Core.MessageAprsPacket CreateDemoMessage(string sender, string recipient, string body, DateTimeOffset receivedAtUtc)
    {
        var raw = $"{sender}>APRS::{recipient.PadRight(9)}:{body}";
        var parser = new Aprs.Core.AprsParser();
        return (Aprs.Core.MessageAprsPacket)parser.Parse(raw, receivedAtUtc);
    }
}
