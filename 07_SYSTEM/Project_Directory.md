---
tags: [system, reference, live]
updated: 2026-05-20
---

# Project Directory

Quick reference for all active projects, paths, and how 
to open each one correctly.

> Rule: always open Win+X → Terminal first. Navigate to 
> the project directory. Then run claude. Never cd from 
> one active venv into another project.

---

## soccer-content-generator
- Path: `C:\Dev\Projects\soccer-content-generator`
- Purpose: BDF soccer content pipeline — clips, queue, 
  dashboard, Twitter publishing
- Session close lives here: `python session_close.py`
- Open with: `cd C:\Dev\Projects\soccer-content-generator && claude`

---

## book-compiler (shared)
- Path: `C:\Dev\shared\book-compiler`
- Purpose: Shared plugin-architecture book compiler for all BRAIN_OS books (BDF, CA, BRAIN_OS)
- Entry: `python book_compiler.py --book [bdf|ca|brainos]`
- Venv: always `C:\Knowledge\CA\venv`
- Aliases: `bdf-book` · `ca-book` · `brainos-book`
- See: [[Book_Compiler_Shared]]
- Added: 2026-05-20