---
tags: [project, book, shared, plugin]
project: book-compiler
status: active
created: 2026-05-20
updated: 2026-05-20
parent: "[[Project_Directory]]"
---

# Book Compiler — Shared Plugin Architecture

> System context: See `C:\BRAIN_OS\SYSTEM_MASTER.md` for hardware, paths, venvs, and cross-project rules.

Single canonical book compiler serving all BRAIN_OS books via a plugin architecture.
Replaces the per-project `book_compiler.py` copies that previously lived inside each project root.

Root: `C:\Dev\shared\book-compiler\`

---

## Architecture

Single entry point with `--book` flag selects which book config to load:

```powershell
C:\Knowledge\CA\venv\Scripts\python.exe book_compiler.py --book [bdf|ca|brainos|mcp]
```

**Book configs** (one JSON per book):

| Config | Path |
|---|---|
| BDF | `C:\Dev\shared\book-compiler\books\bdf.json` |
| CA | `C:\Dev\shared\book-compiler\books\ca.json` |
| BRAIN_OS | `C:\Dev\shared\book-compiler\books\brainos.json` |

---

## Runtime Rule

Always use `C:\Knowledge\CA\venv\Scripts\python.exe` — never system Python or project-specific venvs.

---

## Aliases (PowerShell profile)

| Alias | Equivalent |
|---|---|
| `bdf-book` | `--book bdf` via CA venv |
| `ca-book` | `--book ca` via CA venv |
| `brainos-book` | `--book brainos` via CA venv |

---

## MCP Integration

`mcp.json` added 2026-05-20 — book compiler exposed as MCP plugin.

---

## Migration Note (2026-05-20)

`book_compiler.py` was previously duplicated in each project:
- `C:\Dev\Projects\soccer-content-generator\book_compiler.py` — **deleted** (stale copy)
- `C:\Knowledge\CA\CA_Book\book_compiler.py` — verify separately

All book compilation now routes through this shared plugin.

---

## Connected to

- [[BDF_Book_System]]
- [[CA_Book_System]]
- [[Project_Directory]]
- [[Tools_Registry]]
