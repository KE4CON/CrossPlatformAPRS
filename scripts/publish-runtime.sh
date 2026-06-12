#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <runtime-identifier>" >&2
  exit 2
fi

RID="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOLUTION="$REPO_ROOT/CrossPlatformAprs.sln"
PROJECT="$REPO_ROOT/src/Aprs.Desktop/Aprs.Desktop.csproj"
OUTPUT="$REPO_ROOT/artifacts/publish/$RID"

case "$RID" in
  win-x64|osx-arm64|osx-x64|linux-x64|linux-arm64)
    ;;
  *)
    echo "Unsupported runtime identifier: $RID" >&2
    exit 2
    ;;
esac

echo "Publishing APRS Command for $RID"
dotnet restore "$SOLUTION"
dotnet build "$SOLUTION" -c Release --no-restore
dotnet test "$SOLUTION" -c Release --no-build
dotnet publish "$PROJECT" -c Release -r "$RID" --self-contained true -o "$OUTPUT" /p:PublishSingleFile=false /p:DebugType=none /p:DebugSymbols=false

echo "APRS Command publish output: $OUTPUT"
