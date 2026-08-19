---
tags: [project, landing, vercel, static]
status: dormant
parent: "[[02_PROJECTS/Custom_Agent_TTS]]"
---
# CC Landing — Custom Agent lead page

Static single-file landing page. One `index.html` (13 KB), no framework, no
build step, no `package.json`. Title: **Custom Agent — Free Estimate**.

| Item | Detail |
|---|---|
| Root | `C:\Dev\cc-landing` |
| Repo | github.com/TititoBuilder/cc-landing |
| Deploy | Vercel — `.vercel/` links the project; `git push` publishes |
| Venv | none (no Python) |
| Last commit | 2026-04-10 — dormant since |

## Naming trap (read this first)

Three names collide on this one repo:

- The **repo** is `cc-landing`.
- The **content** is Custom Agent — renamed twice (Skilltrade → Custom Agent,
  commits `e6c9051`, `5f05a45`, `0514a0c`).
- `CC_` **everywhere else in the vault** means CristianConstruction
  (`CC_Nav.md`, `C:\Dev\CristianConstruction`). This page has nothing to do
  with the construction business.

Same class of trap as `obs` (OBS Studio) vs `obsidian` (the note app). The repo
name is a fossil from an earlier identity. Resolve by name through
`09_TOOLS\artifact_paths.py` / `project_paths.py` rather than guessing from
the prefix.

## Relationship

Marketing surface for **custom-agent** (`C:\Dev\Projects\custom-agent`), the
TTS agent project. See [[Custom_Agent_TTS]]. The landing page captures estimate
requests; the agent is the product behind it.

## Known gaps

- No `<h1>` in the markup — only a `<title>`.
- No meta description — search results and link previews render blank.
- Dormant since 2026-04-10; unverified whether the Vercel deployment is live.
