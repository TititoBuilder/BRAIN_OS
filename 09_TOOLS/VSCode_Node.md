---
tags: [tools, vscode, editor, dev-environment]
status: active
dependencies: []
parent: "[[09_TOOLS_INDEX]]"
children:
  - "[[VSCode_Python_Group]]"
  - "[[VSCode_Git_Group]]"
  - "[[VSCode_AI_Group]]"
  - "[[VSCode_UI_Group]]"
  - "[[VSCode_Shell_Group]]"
  - "[[VSCode_Automation_Group]]"
  - "[[VSCode_Markdown_Group]]"
---

# VS Code Node

Visual Studio Code — primary code editor for all BRAIN_OS projects.
Installed extensions as of 2026-04-28.

---

## Python Group
Extensions for Python development, environments, and debugging.

| Extension | Version | Purpose |
|---|---|---|
| ms-python.python | 2026.4.0 | Core Python language support |
| ms-python.vscode-pylance | 2026.2.1 | Fast type checker & IntelliSense (Pyright) |
| ms-python.debugpy | 2026.4.0 | Python debugger (DAP) |
| ms-python.vscode-python-envs | 1.28.0 | Virtual environment manager |

## Git Group
Extensions for Git workflow and history visualization.

| Extension | Version | Purpose |
|---|---|---|
| eamodio.gitlens | 17.12.2 | Inline blame, history explorer, worktrees |
| mhutchie.git-graph | 1.30.0 | Visual branch/commit graph |

## AI Group
AI coding assistants and in-editor agents.

| Extension | Version | Purpose |
|---|---|---|
| anthropic.claude-code | 2.1.121 | Claude Code CLI integration & agent panel |
| github.copilot-chat | 0.45.1 | GitHub Copilot inline chat |

## UI / Productivity Group
Visual enhancements and editor productivity tools.

| Extension | Version | Purpose |
|---|---|---|
| pkief.material-icon-theme | 5.34.0 | File/folder icon theme |
| usernamehw.errorlens | 3.28.0 | Inline error & warning annotations |
| gruntfuggly.todo-tree | 0.0.226 | TODO/FIXME/HACK tag sidebar tree |

## Shell Group
Shell language support.

| Extension | Version | Purpose |
|---|---|---|
| ms-vscode.powershell | 2025.4.0 | PowerShell language support & debugger |

## Automation Group
File-event automation inside VS Code.

| Extension | Version | Purpose |
|---|---|---|
| emeraldwalk.runonsave | 1.0.3 | Run shell commands on file save |

## Markdown / Docs Group
Obsidian-compatible Markdown editing in VS Code.

| Extension | Version | Purpose |
|---|---|---|
| willasm.obsidian-md-vsc | 1.3.0 | Obsidian Markdown preview & [[wikilinks]] |

---

## Setup Notes
- Extensions installed to: `C:\Users\titit\.vscode\extensions\`
- Python envs managed via `ms-python.vscode-python-envs` — virtual envs per project
- `runonsave` used to auto-trigger bridge restarts or test runners on save
- `claude-code` extension connects to the Claude Code CLI daemon
