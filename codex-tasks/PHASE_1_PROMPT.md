# Codex Prompt — Phase 1 APRS Core Protocol

Read `AGENTS.md` and `codex-tasks/MASTER_TASK_LIST.md`.

Implement Phase 1 tasks only:
- Task 1.1 Raw AX.25/APRS text line parser
- Task 1.2 Position packet parser
- Task 1.3 Status/comment/telemetry parser
- Task 1.4 Messages/bulletins/announcements/queries parser
- Task 1.5 Objects/items parser
- Task 1.6 Weather parser

Requirements:
- Keep all protocol parsing in `Aprs.Core`.
- Add strong models for packet types.
- Parser must not throw on malformed packets.
- Add unit tests with sample packets.
- Preserve unknown packets as raw/unknown packet models.

Run:
- `dotnet build`
- `dotnet test`

Summarize changed files, behavior, and test results.
