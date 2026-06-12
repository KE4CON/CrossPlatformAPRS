namespace AprsCommand.Contracts;

public enum ContractSourceTrustLevel
{
    Unknown,
    Untrusted,
    External,
    OperatorConfigured,
    Local,
    Internal
}
