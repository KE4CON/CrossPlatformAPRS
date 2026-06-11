# Feature Scope — Ham Radio APRS Only

This project is limited to amateur-radio APRS features.

Out of scope for now:
- ICS forms
- Public-service resource map
- T-card resource tracking
- Non-amateur-radio fleet tracking

In scope:
- APRS station tracking
- APRS-IS
- RF/TNC support
- Messaging
- Objects/items
- Weather packets
- Local/weather station input from common personal weather station systems and weather station software
- Common weather observation normalization for APRS weather display and optional safe weather beaconing
- GPS/mobile operation
- Digipeater/iGate support
- Offline maps
- Logging/replay
- Diagnostics
- Training/simulation

Weather scope notes:
- Phase 10 is not only APRS weather display. It also includes local weather station input, common weather data normalization, APRS weather packet formatting, and safe optional weather beacon transmit.
- Local/offline-capable weather sources should be preferred when possible.
- Internet/cloud weather APIs are optional and must use user-provided credentials where required.
- Weather credentials/tokens must not be stored in plain text if avoidable.
- Weather transmit features must be disabled by default, keep APRS-IS weather transmit separate from RF weather transmit, and must never transmit stale data.
