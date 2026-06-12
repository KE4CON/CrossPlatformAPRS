#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <runtime-identifier>" >&2
  exit 2
fi

RID="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PUBLISH_DIR="$REPO_ROOT/artifacts/publish/$RID"
PACKAGES_DIR="$REPO_ROOT/artifacts/packages"
CHECKSUMS_DIR="$REPO_ROOT/artifacts/checksums"
RELEASE_NOTES_DIR="$REPO_ROOT/artifacts/release-notes"
STAGING_ROOT="$REPO_ROOT/artifacts/package-staging"
STAGING_DIR="$STAGING_ROOT/APRS-Command-$RID"
PACKAGE_BASENAME="APRS-Command-$RID"

case "$RID" in
  win-x64)
    PACKAGE_PATH="$PACKAGES_DIR/$PACKAGE_BASENAME.zip"
    ;;
  osx-arm64|osx-x64|linux-x64|linux-arm64)
    PACKAGE_PATH="$PACKAGES_DIR/$PACKAGE_BASENAME.tar.gz"
    ;;
  *)
    echo "Unsupported runtime identifier: $RID" >&2
    exit 2
    ;;
esac

echo "Packaging APRS Command portable build for $RID"
"$SCRIPT_DIR/publish-runtime.sh" "$RID"

mkdir -p "$PACKAGES_DIR" "$CHECKSUMS_DIR" "$RELEASE_NOTES_DIR" "$STAGING_ROOT"
rm -rf "$STAGING_DIR" "$PACKAGE_PATH" "$CHECKSUMS_DIR/$(basename "$PACKAGE_PATH").sha256"
mkdir -p "$STAGING_DIR"

cp -R "$PUBLISH_DIR"/. "$STAGING_DIR"/
mkdir -p "$STAGING_DIR/docs" "$STAGING_DIR/packaging"

cp "$REPO_ROOT/README.md" "$STAGING_DIR/README.md"
cp "$REPO_ROOT/docs/QUICK_START.md" "$STAGING_DIR/QUICK_START.md"
cp "$REPO_ROOT/docs/INSTALLATION_GUIDE.md" "$STAGING_DIR/INSTALLATION_GUIDE.md"
cp "$REPO_ROOT/docs/SAFETY_AND_TRANSMIT_GUIDE.md" "$STAGING_DIR/SAFETY_AND_TRANSMIT_GUIDE.md"
cp "$REPO_ROOT/docs/TROUBLESHOOTING.md" "$STAGING_DIR/TROUBLESHOOTING.md"
cp "$REPO_ROOT/docs/RELEASE_NOTES_TEMPLATE.md" "$RELEASE_NOTES_DIR/RELEASE_NOTES_TEMPLATE.md"

if [[ -f "$REPO_ROOT/LICENSE" ]]; then
  cp "$REPO_ROOT/LICENSE" "$STAGING_DIR/LICENSE"
elif [[ -f "$REPO_ROOT/LICENSE.md" ]]; then
  cp "$REPO_ROOT/LICENSE.md" "$STAGING_DIR/LICENSE.md"
else
  printf 'APRS Command license: TBD\n' > "$STAGING_DIR/LICENSE_PLACEHOLDER.txt"
fi

if [[ -d "$REPO_ROOT/packaging/templates" ]]; then
  cp -R "$REPO_ROOT/packaging/templates" "$STAGING_DIR/packaging/templates"
fi

cat > "$STAGING_DIR/VERSION.txt" <<EOF
APRS Command
Version: 0.0.0-dev
Runtime: $RID
Package: $(basename "$PACKAGE_PATH")
Build date: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
Safe defaults: APRS-IS transmit disabled; RF transmit disabled; iGate disabled; digipeater disabled; beaconing disabled; weather beaconing disabled; REST API disabled; WebSocket disabled; file hooks disabled; plugin loading disabled; replay/simulation/training cannot transmit.
EOF

if [[ "$RID" == linux-* ]]; then
  cp "$REPO_ROOT/packaging/templates/aprs-command.desktop.template" "$STAGING_DIR/aprs-command.desktop.template"
fi

case "$RID" in
  win-x64)
    (cd "$STAGING_ROOT" && zip -qr "$PACKAGE_PATH" "APRS-Command-$RID")
    ;;
  *)
    (cd "$STAGING_ROOT" && tar -czf "$PACKAGE_PATH" "APRS-Command-$RID")
    ;;
esac

if command -v shasum >/dev/null 2>&1; then
  (cd "$PACKAGES_DIR" && shasum -a 256 "$(basename "$PACKAGE_PATH")" > "$CHECKSUMS_DIR/$(basename "$PACKAGE_PATH").sha256")
elif command -v sha256sum >/dev/null 2>&1; then
  (cd "$PACKAGES_DIR" && sha256sum "$(basename "$PACKAGE_PATH")" > "$CHECKSUMS_DIR/$(basename "$PACKAGE_PATH").sha256")
else
  echo "No SHA256 tool found. Install shasum or sha256sum." >&2
  exit 1
fi

echo "APRS Command package output: $PACKAGE_PATH"
echo "APRS Command checksum output: $CHECKSUMS_DIR/$(basename "$PACKAGE_PATH").sha256"
