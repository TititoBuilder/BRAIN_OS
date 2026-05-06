---
tags: [book, project]
book_project: mcp
book_status: active
created: 2026-05-05
updated: 2026-05-05
domain: AI_Engineering
---

# MCP Book System

Technical knowledge book for the Resolve MCP bridge, DaVinci Resolve Free tier patterns, and Windows pipeline engineering.

## Pipeline
```
Session log → mcp-compile <file> → incoming\ → mcp-book
→ mcp_book_compiler.py → chapters\ → stitch → MCP_Master_Book.txt
```

**Commands:**
```powershell
mcp-compile "session_log.txt"   # routes to incoming\
mcp-book                         # compiles + stitches
```

## File Locations
| Component | Path |
|---|---|
| Compiler | `C:\Dev\Projects\soccer-content-generator\mcp_book_compiler.py` |
| Chapters (canonical) | `C:\Knowledge\MCP\MCP_Book\chapters\` |
| Incoming | `C:\Knowledge\MCP\MCP_Book\incoming\` |
| Processed | `C:\Knowledge\MCP\MCP_Book\_processed\` |
| Review | `C:\Knowledge\MCP\MCP_Book\_review\` |
| Rejected | `C:\Knowledge\MCP\MCP_Book\_rejected\` |
| Audio | `C:\Knowledge\MCP\MCP_Book\audio\` |
| Master book (derived) | `C:\Knowledge\MCP\MCP_Book\BDF_Master_Book.txt` |
| Session resumes | `C:\Knowledge\MCP\Session_Resumes\` |

## Chapter Inventory
| File | Topic | Size |
|---|---|---|
| ch01_resolve_free_tier_nils | Resolve Free NoneType inventory + guard patterns | ~16 KB |
| ch02_bridge_reload_discipline | Mandatory reload command, UTF-8 encoding | ~16 KB |
| ch03_windows_encoding_patterns | cp1252 vs UTF-8, subprocess env, ASCII rules | ~16 KB |
| ch04_mcp_bridge_architecture | Two-process design, 14 tools, timeline state | ~16 KB |

**Total: 4 chapters, clean numbering ✅**

## Differences vs BDF/CA
| Property | MCP Book |
|---|---|
| Format | `.txt` |
| Count | 4 chapters |
| Compiler | `mcp_book_compiler.py` (in BDF project) |
| venv | BDF venv |
| Post-processing | TBD — verify if TTS/Drive sync is wired |

## Connected Nodes
- [[Resolve_MCP_Server]]
- [[BDF_Book_System]]
- [[PowerShell_Aliases]]
