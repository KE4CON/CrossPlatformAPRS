# APRS Command Installation Guide

This guide explains how normal users can install or run APRS Command. Packaged installers are planned for later work. Until then, use a published folder or run from source.

The detailed installer/package strategy is tracked in `docs/INSTALLER_AND_PACKAGE_PLAN.md`.

Portable packages are written under `artifacts/packages/` when package scripts are run. Each package has a matching SHA256 checksum under `artifacts/checksums/`.

## Windows

1. Download `APRS-Command-win-x64.zip` or use the `win-x64` publish output.
2. Extract the folder to a user-writable location such as your profile folder.
3. Run the APRS Command executable.
4. Allow user data folders to be created under your application data area.
5. If Windows blocks an unsigned development build, review the file source before allowing it.

Required permissions:

- user-writable configuration and log folders
- network access for APRS-IS receive
- optional serial access for hardware TNCs

## macOS Apple Silicon

1. Use `APRS-Command-osx-arm64.tar.gz` or the `osx-arm64` publish output.
2. Extract APRS Command to a user-writable folder or future application bundle.
3. Start the app.
4. If macOS warns about an unsigned development build, only open it if you trust the build source.

Future packages should handle signing and notarization.

## macOS Intel

1. Use `APRS-Command-osx-x64.tar.gz` or the `osx-x64` publish output.
2. Follow the same steps as macOS Apple Silicon.
3. Verify Intel support remains part of the build you downloaded.

## Linux x64

1. Use `APRS-Command-linux-x64.tar.gz` or the `linux-x64` publish output.
2. Extract it into your home directory or another user-writable location.
3. Run the desktop executable from a terminal or future `.desktop` launcher.
4. Ensure the app data folder is writable.

Serial port permissions may require adding your user to a group such as `dialout`, depending on the distribution.

## Linux ARM64

1. Use `APRS-Command-linux-arm64.tar.gz` or the `linux-arm64` publish output.
2. Extract it to user-writable storage.
3. Run the app from a terminal first so launch errors are visible.
4. Keep map cache and logs on storage with enough free space.

## Raspberry Pi 5 / Linux ARM64

1. Use `APRS-Command-linux-arm64.tar.gz`.
2. Prefer a high-quality SD card or external storage for maps and logs.
3. Verify desktop libraries required by Avalonia are installed by your distribution.
4. Add your user to the serial device group if using USB TNC hardware.
5. Test receive-only before connecting any transmit path.

## Verify Checksums

When checksum files are provided, compare the package SHA256 value before running APRS Command:

```bash
cd artifacts/packages
shasum -a 256 APRS-Command-linux-x64.tar.gz
cat ../checksums/APRS-Command-linux-x64.tar.gz.sha256
```

The values should match.

## Build From Source

Install the .NET 10 SDK, then run:

```bash
dotnet restore
dotnet build
dotnet run --project src/Aprs.Desktop
```

## Map Cache and Storage Notes

Offline map tiles can use significant space. Choose a map cache folder that:

- has enough free space
- is writable by your user
- is not on a nearly full system disk
- is backed up only if you need map/cache persistence

## Troubleshooting Launch Problems

If APRS Command will not start:

1. Run it from a terminal to see error output.
2. Confirm the .NET 10 SDK or runtime is installed when running from source.
3. Confirm the app folder is not read-only.
4. Confirm the application data folder is writable.
5. Check logs under the configured `logs/` folder.
6. On Linux, install missing desktop libraries reported by the terminal.
7. On macOS, review security prompts for unsigned development builds.
