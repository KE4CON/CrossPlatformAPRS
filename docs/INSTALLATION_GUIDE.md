# APRS Command Installation Guide

This guide explains how normal users can install or run APRS Command. Packaged installers are planned for later work. Until then, use a published folder or run from source.

The detailed installer/package strategy is tracked in `docs/INSTALLER_AND_PACKAGE_PLAN.md`.

## Windows

1. Download the future Windows x64 package or use the `win-x64` publish output.
2. Extract the folder to a user-writable location such as your profile folder.
3. Run the APRS Command executable.
4. Allow user data folders to be created under your application data area.
5. If Windows blocks an unsigned development build, review the file source before allowing it.

Required permissions:

- user-writable configuration and log folders
- network access for APRS-IS receive
- optional serial access for hardware TNCs

## macOS Apple Silicon

1. Use the `osx-arm64` publish output.
2. Place APRS Command in a user-writable folder or future application bundle.
3. Start the app.
4. If macOS warns about an unsigned development build, only open it if you trust the build source.

Future packages should handle signing and notarization.

## macOS Intel

1. Use the `osx-x64` publish output.
2. Follow the same steps as macOS Apple Silicon.
3. Verify Intel support remains part of the build you downloaded.

## Linux x64

1. Use the `linux-x64` publish output.
2. Extract it into your home directory or another user-writable location.
3. Run the desktop executable from a terminal or future `.desktop` launcher.
4. Ensure the app data folder is writable.

Serial port permissions may require adding your user to a group such as `dialout`, depending on the distribution.

## Linux ARM64

1. Use the `linux-arm64` publish output.
2. Extract it to user-writable storage.
3. Run the app from a terminal first so launch errors are visible.
4. Keep map cache and logs on storage with enough free space.

## Raspberry Pi 5 / Linux ARM64

1. Use `linux-arm64`.
2. Prefer a high-quality SD card or external storage for maps and logs.
3. Verify desktop libraries required by Avalonia are installed by your distribution.
4. Add your user to the serial device group if using USB TNC hardware.
5. Test receive-only before connecting any transmit path.

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
