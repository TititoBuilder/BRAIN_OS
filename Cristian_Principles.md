The Principle of Verified Reality (The Sync Rule)
Context: Any system bridging local logic and remote state.

Global Pulse Check — Use account-level Change Tokens (changes().getStartPageToken()), not folder modifiedTime, to detect out-of-band drift. Folder timestamps are shallow and don't propagate. The token is a single lightweight API call that acts as a global dirty flag.
Session-Anchor TTL — TTL values are not magic numbers. Derive them from Max_Session_Duration + Buffer. For BRAIN_OS: 4 hours (3h max session + 1h buffer). One fresh sync per session, zero interruptions mid-flow.
Config Centralization — System sensitivity constants (TTL, token storage) belong in C:\BRAIN_OS\BRAIN_OS_CONFIG.json, not buried in project scripts. Global constants at the OS root; logic at the project root.

Proof: bdf_drive_manifest.json is a Security Log, not Ground Truth. It is only as reliable as its last sync. The TTL and Pulse Check together define when "cached" becomes "ghost."
