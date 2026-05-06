---
tags: [tool, development, ide, vscode, extensions]
created: 2026-05-03
updated: 2026-05-03
---

# VS Code — Primary Development Environment

**What It Is:** Visual Studio Code - Microsoft's free, open-source code editor

**Primary Uses:**
- BRAIN_OS file browsing and editing (all .md files)
- Python development (BDF, Custom Agent, Read-Along App)
- Git operations and version control
- Markdown documentation
- Multi-project workspace management

**Location:** Installed system-wide, accessible via `code` command

---

## Core Workflows

### Opening BRAIN_OS Workspace
```powershell
# From anywhere
code C:\BRAIN_OS

# From BRAIN_OS directory
cd C:\BRAIN_OS
code .
```

**Result:** Entire vault opens as workspace, file tree visible, full text search enabled

### Multi-Folder Workspace (Simultaneous Projects)
```
File → Add Folder to Workspace
```

**Example workspace:**
- C:\BRAIN_OS (knowledge vault)
- C:\Dev\Projects\soccer-content-generator (BDF)
- C:\Dev\CristianConstruction (Custom Agent)
- C:\Users\titit\Projects\read-along-app (Read-Along)

**Save workspace:** File → Save Workspace As → `my-workspace.code-workspace`

### Integrated Terminal
**Open:** Ctrl+` (backtick)

**Switch terminal type:**
- Default: PowerShell
- Also available: Bash (Git Bash), Command Prompt, WSL

**Multiple terminals:** Click + icon to open additional terminals

---

## Installed Extensions

### Python Development Suite

**ms-python.python**
- Core Python language support
- Syntax highlighting, IntelliSense
- Detects Python interpreters (system + venvs)

**ms-python.vscode-pylance**
- Fast type checking
- Auto-imports
- IntelliSense (smarter than base Python extension)

**ms-python.debugpy**
- Python debugger
- Breakpoints, variable inspection, call stack
- F5 to start debugging

**ms-python.vscode-python-envs**
- Manage virtual environments
- See all venvs: BDF venv, CA venv, Read-Along venv
- Switch between them: Ctrl+Shift+P → "Python: Select Interpreter"

**ms-python.black-formatter** ⭐ NEW
- Auto-format Python code on save
- Consistent style across all projects
- Configure: Settings → "Format On Save" → Enable

**charliermarsh.ruff** ⭐ NEW
- Fast Python linter (replaces flake8, isort)
- Catches errors, style issues
- Auto-fix many issues

---

### Git & Version Control

**eamodio.gitlens**
- See who changed each line (inline blame)
- Navigate commit history
- Compare branches, files
- Hover over line → see last commit that touched it

**mhutchie.git-graph**
- Visual git history tree
- See branches, merges, commits
- Right-click commits → checkout, revert, cherry-pick

**fabiospampinato.vscode-open-in-github** ⭐ NEW
- Jump from code to GitHub page
- Right-click file → "Open in GitHub"
- Works for lines, files, repos

---

### Markdown & Documentation

**yzhang.markdown-all-in-one** ⭐ NEW
- Auto-generate table of contents
- Keyboard shortcuts (Ctrl+B for bold, Ctrl+I for italic)
- Auto-complete lists
- Format tables

**bierner.markdown-preview-enhanced** ⭐ NEW
- Better Markdown preview (Ctrl+Shift+V)
- Mermaid diagram support
- Export to PDF, HTML
- Math equations (LaTeX)

**willasm.obsidian-md-vsc**
- Obsidian vault integration
- Wiki-link support ([[link]] syntax)
- Preview Obsidian files in VS Code

---

### Productivity & Workflow

**anthropic.claude-code**
- Claude Code integration
- AI pair programming
- Terminal-based coding agent

**gruntfuggly.todo-tree**
- Finds all TODO comments in codebase
- Sidebar view of all TODOs
- Click to jump to location
- Supports: TODO, FIXME, HACK, NOTE

**usernamehw.errorlens**
- Shows errors/warnings inline (no hover needed)
- Color-coded by severity
- Faster error spotting

**emeraldwalk.runonsave**
- Auto-run commands when files save
- Example: Auto-format, run tests, compile

**alefragnani.project-manager** ⭐ NEW
- Save project contexts
- Switch between BDF, CA, Read-Along instantly
- Sidebar: Quick access to saved projects

---

### UI & Appearance

**pkief.material-icon-theme**
- File/folder icons for visual scanning
- Python files = Python icon
- Markdown files = M icon
- Folders color-coded by type

**ms-vscode.powershell**
- PowerShell language support
- Syntax highlighting for .ps1 files
- Integrated terminal PowerShell

---

## Key Features

### File Search
- **Ctrl+P:** Quick file open (fuzzy search)
- **Ctrl+Shift+F:** Search across entire workspace
- **Ctrl+Shift+H:** Find and replace across files

### Multi-Cursor Editing
- **Ctrl+D:** Select next occurrence of word
- **Ctrl+Shift+L:** Select all occurrences
- **Alt+Click:** Add cursor at click location

### Zen Mode
- **Ctrl+K Z:** Distraction-free coding
- Hides sidebar, panels, status bar
- Press Esc twice to exit

### Split Editor
- **Ctrl+\\:** Split editor vertically
- **Ctrl+K Ctrl+\\:** Split horizontally
- Drag tabs between splits

---

## Python-Specific Workflows

### Virtual Environment Detection
VS Code auto-detects venvs in project directories:
- BDF: `C:\Dev\Projects\soccer-content-generator\venv\`
- Custom Agent: Currently shares BDF venv (needs separation)
- Read-Along: `C:\Users\titit\Projects\read-along-app\venv\`

**Switch interpreter:**
1. Click Python version in status bar (bottom right)
2. OR Ctrl+Shift+P → "Python: Select Interpreter"
3. Choose project's venv

**Indicator:** Status bar shows active interpreter

### Debugging Python
1. Open Python file
2. Set breakpoint: Click left of line number (red dot appears)
3. F5 to start debugging
4. Step through: F10 (step over), F11 (step into), Shift+F11 (step out)
5. Inspect variables in Debug sidebar

### Running Python Files
- **Terminal method:** Integrated terminal, `python script.py`
- **Right-click method:** Right-click file → "Run Python File in Terminal"
- **Debug method:** F5 (runs with debugger)

---

## BRAIN_OS-Specific Workflows

### Opening Vault
```powershell
code C:\BRAIN_OS
```

**File tree shows:**
- 01_DOMAINS/
- 02_PROJECTS/
- 07_SYSTEM/
- 08_TEMPLATES/
- 10_CHATS/

### Creating/Editing Markdown Files
- Ctrl+N → new file
- Save as .md
- Markdown syntax highlighting automatic
- Preview: Ctrl+Shift+V

### Wiki-Link Navigation
With `willasm.obsidian-md-vsc`:
- [[link]] syntax recognized
- Ctrl+Click to follow link
- Auto-complete wiki-links

### Full-Vault Search
- Ctrl+Shift+F
- Search term: finds across all .md files
- Results show in sidebar with context
- Click result to jump to file/line

---

## Git Workflows in VS Code

### Viewing Changes
- **Source Control sidebar:** Ctrl+Shift+G
- See modified files
- Click file → diff view (side-by-side comparison)

### Staging & Committing
1. Source Control sidebar
2. Hover over file → click + (stage)
3. Enter commit message
4. Ctrl+Enter or click ✓ (commit)

### Viewing History (GitLens)
- Click line → see last commit in inline blame
- Right-click file → "Open File History"
- See all commits that touched file

### Viewing Graph (Git Graph)
- Status bar → "Git Graph" button
- OR Command Palette → "Git Graph: View Git Graph"
- Visual tree of all commits, branches

---

## Recommended Settings

**Auto-save:**
```
File → Auto Save (check to enable)
```

**Format on save:**
```
Settings → "Format On Save" → Enable
```

**Show hidden files:**
```
Settings → "Files: Exclude" → Remove patterns you want visible
```

**Integrated terminal default:**
```
Settings → "Terminal › Integrated › Default Profile: Windows" → PowerShell
```

---

## Keyboard Shortcuts (Essential)

| Action | Shortcut |
|--------|----------|
| Command Palette | Ctrl+Shift+P |
| Quick File Open | Ctrl+P |
| Toggle Terminal | Ctrl+` |
| Toggle Sidebar | Ctrl+B |
| Search in Files | Ctrl+Shift+F |
| Git Source Control | Ctrl+Shift+G |
| New File | Ctrl+N |
| Save File | Ctrl+S |
| Close Editor | Ctrl+W |
| Split Editor | Ctrl+\\ |
| Zen Mode | Ctrl+K Z |
| Markdown Preview | Ctrl+Shift+V |

---

## Project-Specific Usage

### BDF Platform
**Open:** `code C:\Dev\Projects\soccer-content-generator`

**Active venv:** `soccer-content-generator\venv\`

**Key files:**
- Python scripts for card generation
- Video compilation automation
- Book compilation

### Custom Agent
**Open:** `code C:\Dev\CristianConstruction`

**Active venv:** Currently shares BDF venv (needs separation)

**Key files:**
- `ca_audio.py` (Kokoro TTS)
- `book_compiler.py` (session → chapters)
- Telegram bot integration

### Read-Along App
**Open:** `code C:\Users\titit\Projects\read-along-app`

**Active venv:** `read-along-app\venv\`

**Key files:**
- Whisper transcription backend
- React frontend
- FastAPI server

### BRAIN_OS
**Open:** `code C:\BRAIN_OS`

**No venv** (pure Markdown vault)

**Usage:**
- Create/edit knowledge nodes
- Search across entire knowledge base
- Navigate wiki-links
- Maintain documentation

---

## Troubleshooting

### Extension Not Working
1. Ctrl+Shift+P → "Developer: Reload Window"
2. If still broken: Uninstall → reinstall extension

### Python Interpreter Not Detected
1. Ctrl+Shift+P → "Python: Select Interpreter"
2. If venv not listed: Click "Enter interpreter path"
3. Navigate to `venv\Scripts\python.exe`

### Terminal Not Opening
1. Check default shell: Settings → Terminal → Default Profile
2. Try different shell: Click dropdown in terminal panel
3. Reload window: Ctrl+Shift+P → "Developer: Reload Window"

### Git Not Showing Changes
1. Ensure folder is git repository: `git status` in terminal
2. Refresh: Source Control sidebar → refresh icon
3. Check .gitignore isn't excluding files

---

## Performance Tips

**For large workspaces (like BRAIN_OS with many files):**

1. **Exclude unnecessary folders from search:**
   Settings → "Search: Exclude" → Add patterns like `**/node_modules`, `**/.git`

2. **Disable file watchers for large directories:**
   Settings → "Files: Watcher Exclude" → Add `**/.git/objects/**`

3. **Close unused editors:**
   Ctrl+W to close current, Ctrl+K W to close all

---

## Integration with Other Tools

### Claude Code Integration
- Extension: `anthropic.claude-code`
- Terminal command: `claude`
- Works within VS Code terminal
- AI pair programming in same environment

### Obsidian Integration
- Extension: `willasm.obsidian-md-vsc`
- Open BRAIN_OS in both VS Code and Obsidian
- Edit in VS Code, view graph in Obsidian
- Wiki-links work in both

### Git Integration
- Native git support
- GitLens extension for advanced features
- Git Graph for visual history
- All git operations possible without leaving VS Code

---

## When to Use VS Code vs Obsidian vs PowerShell

**VS Code:**
- Writing/editing Python code
- Multi-file project work
- Git operations with visual diff
- Debugging Python
- Markdown editing with preview

**Obsidian:**
- Graph view of BRAIN_OS
- Quick note-taking
- Wiki-link navigation
- Visual knowledge exploration

**PowerShell:**
- Quick file operations (move, copy)
- Git commands (commit, push)
- Running scripts
- System administration

**Often all three are open simultaneously** for different aspects of workflow.

---

## Connected to
- [[Tools_Registry]]
- [[BRAIN_OS]]
- [[Python_Development]]
- [[Git_Workflow]]
- [[Obsidian]]
