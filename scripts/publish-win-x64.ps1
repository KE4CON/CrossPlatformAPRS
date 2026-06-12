param(
    [string]$RuntimeIdentifier = "win-x64"
)

$ErrorActionPreference = "Stop"

$supported = @("win-x64")
if ($supported -notcontains $RuntimeIdentifier) {
    throw "Unsupported runtime identifier for this script: $RuntimeIdentifier"
}

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptRoot "..")
$solution = Join-Path $repoRoot "CrossPlatformAprs.sln"
$project = Join-Path $repoRoot "src/Aprs.Desktop/Aprs.Desktop.csproj"
$output = Join-Path $repoRoot "artifacts/publish/$RuntimeIdentifier"

Write-Host "Publishing APRS Command for $RuntimeIdentifier"
dotnet restore $solution
dotnet build $solution -c Release --no-restore
dotnet test $solution -c Release --no-build
dotnet publish $project -c Release -r $RuntimeIdentifier --self-contained true -o $output /p:PublishSingleFile=false /p:DebugType=none /p:DebugSymbols=false

Write-Host "APRS Command publish output: $output"
