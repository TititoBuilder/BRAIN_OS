# OPERATIONS

Bucket index. Infrastructure and shared components. Nothing here ships to a
customer; everything here is depended on by something that does.
Source of truth is the filesystem. This file is a view, not a copy.

## Projects

### BRAIN_OS
- Path: `C:\BRAIN_OS`
- Nav: none — TODO create BRAINOS_Nav.md
- The graph. Knowledge layer and AI-readable operating layer. Not a project.
- Tooling in `09_TOOLS\` (30 files, 6 layers). Zero internal Python imports —
  architecturally decoupled by design.

### Knowledge (knowledge-base repo)
- Path: `C:\Knowledge`
- Nav: none — TODO create Knowledge_Nav.md
- Repo: github.com/TititoBuilder/knowledge-base
- Hosts the CANONICAL AI/TTS venv at `C:\Knowledge\CA\venv`
  (PyTorch nightly cu128, verified for RTX 5070 Ti sm_120 Blackwell).
- DO NOT relocate. DO NOT install CPU-only torch here — breaks GPU inference
  across all AI projects.

### obs-mcp-server
- Path: `C:\Users\titit\Projects\obs-mcp-server`
- Nav: [[OBS_Nav]]
- MCP server for OBS Studio. (obs = OBS Studio, never Obsidian.)

### resolve-mcp-server
- Path: `C:\Users\titit\Projects\resolve-mcp-server`
- Nav: [[ResolveMCP_Nav]]
- MCP server for DaVinci Resolve. Namespace: `davinci-resolve`.

### brain-audio (shared package)
- Path: `C:\Dev\shared\brain-audio`
- Nav: none — TODO create BrainAudio_Nav.md
- TTS normalizer. Consumed by CA_Book (CONTENT).
- Vault knowledge node (not code): `C:\BRAIN_OS\02_PROJECTS\brain-audio` — linked, not duplicated.

### book-compiler (shared package)
- Path: `C:\Dev\shared\book-compiler`
- Nav: none — TODO create BookCompiler_Nav.md

## Fragility points (blast radius)
- `gdrive_credentials.json` / `gdrive_token.json` — shared by 4-6 scripts.
  Copies exist in `C:\Knowledge\CA\CA_Book\`. Consolidation is an open queue item.
- `soccer-content-generator\.env` — shared by 4-6 scripts.
- Drive file IDs: `C:\BRAIN_OS\09_TOOLS\drive_index.json`.

## Notes
- Shared packages live here, not in a consumer's bucket. Assigning a shared
  component to one consumer would misrepresent its blast radius.
- `00_NAV\SYSTEM_Rules.md` (4594 bytes) is not a nav file. Likely belongs in
  `07_SYSTEM\`. Flagged, not moved.

---

## Complete Repo Inventory — August 14 2026
Discovered using Get-ChildItem with -Force flag (required — .git is hidden on Windows).
Previous inventories missed repos because -Force was omitted.

| Repo | Root | Notes |
|---|---|---|
| BRAIN_OS | C:\BRAIN_OS | Vault + tooling |
| cc-landing | C:\Dev\cc-landing | CristianConstruction landing page — at Dev root, NOT Dev\Projects |
| CristianConstruction | C:\Dev\CristianConstruction | Business OS — at Dev root |
| custom-agent | C:\Dev\Projects\custom-agent | TTS agent |
| gig_tracker | C:\Dev\Projects\gig_tracker\gig_tracker | NESTED — inner folder is the git root |
| soccer-content-generator | C:\Dev\Projects\soccer-content-generator | BDF pipeline |
| book-compiler | C:\Dev\shared\book-compiler | Shared — CA book audio compiler |
| brain-audio | C:\Dev\shared\brain-audio | Shared package — installed editable in BDF/CA/read-along |
| knowledge-base | C:\Knowledge | Entire Knowledge folder is a repo |
| obs-mcp-server | C:\Users\titit\Projects\obs-mcp-server | OBS Studio bridge |
| read-along-app | C:\Users\titit\Projects\read-along-app | Vercel + Railway |
| resolve-mcp-server | C:\Users\titit\Projects\resolve-mcp-server | DaVinci bridge |

**Discovery command (always use -Force):**
```powershell
Get-ChildItem C:\Dev, C:\Knowledge, C:\Users\titit\Projects, C:\BRAIN_OS -Recurse -Depth 3 -Force -Filter ".git" -Directory -ErrorAction SilentlyContinue | ForEach-Object { $_.Parent.FullName } | Sort-Object
```

**Key findings:**
- C:\Dev\ root has repos NOT inside Projects\ — always scan Dev root, not just Dev\Projects
- C:\Dev\shared\ contains two shared packages invisible to previous scans
- C:\Knowledge is itself a git repo — not just a venv host
- gig_tracker has a nested path — git root is the INNER gig_tracker folder