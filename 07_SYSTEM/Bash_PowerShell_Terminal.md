---
tags: [tool, terminal, bash, powershell, command-line, shell]
created: 2026-05-03
updated: 2026-05-03
---

# Bash & PowerShell — Terminal Environments

**What They Are:** Command-line shells for executing commands, running scripts, and system automation

**Primary Terminal:** Windows PowerShell (what you use most)

**Secondary:** Bash (Git Bash, WSL, occasionally used)

---

## The Two Shells You Work With

### Windows PowerShell
**Platform:** Windows native  
**Language:** Microsoft's scripting language  
**Command Style:** Verb-Noun cmdlets (e.g., `Get-Content`, `Move-Item`)  
**What You Use It For:** 
- Git operations (commit, push, pull)
- File operations (move, copy, delete)
- Python venv activation
- Running scripts
- System administration

**How to Open:**
- Win+X → Terminal (default)
- VS Code integrated terminal (default)
- Start menu → "PowerShell"

### Bash (Bourne Again Shell)
**Platform:** Unix/Linux native, available on Windows via Git Bash or WSL  
**Language:** Unix shell scripting  
**Command Style:** Terse abbreviations (e.g., `cat`, `ls`, `mv`)  
**What You Use It For:**
- Git operations (when in Git Bash)
- Unix-style scripting
- Linux-compatible commands

**How to Open:**
- Git Bash application
- WSL (Windows Subsystem for Linux)
- VS Code integrated terminal (select Bash from dropdown)

---

## Why Commands Fail Between Shells

**The Problem You've Experienced:**

When other Claude sessions tell you to run `mv` or `ls`, but you're in PowerShell, the commands fail or behave unexpectedly.

**Why:** PowerShell and Bash are **different languages**. They don't share syntax.

### Example (From This Session):

**Other chat said:**
```bash
mv /path/to/file.txt C:\BRAIN_OS\
```

**Failed because:** 
- `mv` is Bash native
- You're in PowerShell
- PowerShell has `mv` as an **alias** but it maps to `Move-Item` cmdlet
- The path format `/path/to/` is Unix-style, not Windows

**Should have been:**
```powershell
Move-Item C:\Users\titit\Downloads\file.txt C:\BRAIN_OS\
```

---

## Command Translation Table

**Your Daily Commands - PowerShell vs Bash:**

| Task | PowerShell (What You Use) | Bash (Git Bash/WSL) | Notes |
|------|---------------------------|---------------------|-------|
| List files | `Get-ChildItem` or `ls` or `dir` | `ls` | PowerShell has `ls` alias |
| Change directory | `Set-Location` or `cd` | `cd` | Works in both |
| Move file | `Move-Item` or `mv` | `mv` | PowerShell has `mv` alias |
| Copy file | `Copy-Item` or `cp` | `cp` | PowerShell has `cp` alias |
| Remove file | `Remove-Item` or `rm` | `rm` | PowerShell has `rm` alias |
| Print file content | `Get-Content` or `cat` | `cat` | PowerShell has `cat` alias |
| Create directory | `New-Item -ItemType Directory` or `mkdir` | `mkdir` | PowerShell has `mkdir` alias |
| Find text in files | `Select-String` | `grep` | Different command entirely |
| Current directory | `Get-Location` or `pwd` | `pwd` | PowerShell has `pwd` alias |
| Clear screen | `Clear-Host` or `cls` or `clear` | `clear` | PowerShell has aliases |
| Environment variables | `$env:VARIABLE` | `$VARIABLE` | Different syntax |
| Command history | `Get-History` or `history` | `history` | PowerShell has alias |

---

## PowerShell-Specific Concepts

### Cmdlets (Command-lets)
**Format:** Verb-Noun

**Common Verbs:**
- `Get` - Retrieve information
- `Set` - Modify settings
- `New` - Create something
- `Remove` - Delete something
- `Copy` - Duplicate
- `Move` - Relocate
- `Test` - Check condition

**Examples:**
```powershell
Get-ChildItem C:\BRAIN_OS     # List files
Set-Location C:\Dev           # Change directory
New-Item -ItemType File test.md  # Create file
Remove-Item old.txt           # Delete file
Copy-Item src.txt dst.txt     # Copy file
Move-Item file.txt C:\New\    # Move file
Test-Path C:\BRAIN_OS         # Check if path exists
```

### Aliases
PowerShell has built-in aliases that mimic Unix commands:

```powershell
ls    → Get-ChildItem
cd    → Set-Location
pwd   → Get-Location
cat   → Get-Content
mv    → Move-Item
cp    → Copy-Item
rm    → Remove-Item
mkdir → New-Item -ItemType Directory
```

**Key insight:** When you type `ls` in PowerShell, you're actually running `Get-ChildItem` underneath.

### Pipeline
PowerShell passes **objects** through the pipeline, not just text:

```powershell
Get-ChildItem C:\BRAIN_OS | Where-Object {$_.Extension -eq ".md"}
```

This filters for .md files by checking the Extension **property** of each file object.

Bash would use text parsing:
```bash
ls /c/BRAIN_OS | grep ".md"
```

---

## Bash-Specific Concepts

### Terse Commands
Bash commands are short and cryptic:

```bash
ls      # List
cd      # Change directory
pwd     # Print working directory
cat     # Concatenate (show file content)
grep    # Search text
find    # Find files
awk     # Text processing
sed     # Stream editor
```

### Pipes and Text Processing
Bash passes **text** through pipes:

```bash
cat file.txt | grep "pattern" | wc -l
```

This shows file content → filters for "pattern" → counts lines.

### Path Format
**Bash (Unix-style):**
```bash
/c/Users/titit/BRAIN_OS
/mnt/c/BRAIN_OS  # WSL format
```

**PowerShell (Windows-style):**
```powershell
C:\Users\titit\BRAIN_OS
```

---

## When to Use Which Shell

### Use PowerShell When:
- ✅ Working on Windows (your daily work)
- ✅ Managing files in C:\ drives
- ✅ Running Python scripts
- ✅ Git operations (works fine in PowerShell)
- ✅ System administration on Windows
- ✅ You need object-oriented pipeline

### Use Bash When:
- ✅ Following Linux/Unix tutorials
- ✅ Running shell scripts from open-source projects (often .sh files)
- ✅ Working with Linux servers (SSH)
- ✅ Using WSL (Windows Subsystem for Linux)
- ✅ You need Unix-specific tools (awk, sed, grep with advanced features)

### Your Default: PowerShell
**Why:** You're on Windows, working with Windows paths, and PowerShell handles everything you need.

**When Bash appears:** Mostly when following tutorials or past Claude sessions that default to Unix conventions.

---

## Common PowerShell Commands (Your Daily Use)

### File Operations
```powershell
# List files
Get-ChildItem
ls                    # Alias
dir                   # Alias

# List with details
Get-ChildItem -Force  # Show hidden files
ls -Recurse          # List recursively (all subdirectories)

# Change directory
Set-Location C:\BRAIN_OS
cd C:\BRAIN_OS       # Alias

# Current directory
Get-Location
pwd                  # Alias

# Move file
Move-Item source.txt C:\Destination\
mv source.txt C:\Destination\  # Alias

# Copy file
Copy-Item source.txt destination.txt
cp source.txt destination.txt  # Alias

# Delete file
Remove-Item file.txt
rm file.txt          # Alias

# Create directory
New-Item -ItemType Directory -Path C:\New\Folder
mkdir C:\New\Folder  # Alias

# Create file
New-Item -ItemType File -Path test.txt
```

### Git Operations
```powershell
# Status
git status

# Add files
git add .
git add filename.txt

# Commit
git commit -m "message"

# Push
git push origin main

# Pull
git pull origin main

# View log
git log
git log --oneline

# Diff
git diff
git diff HEAD~1
```

### Python venv Activation
```powershell
# Activate venv (BDF example)
C:\Dev\Projects\soccer-content-generator\venv\Scripts\Activate.ps1

# OR if in project directory
.\venv\Scripts\Activate.ps1

# Deactivate
deactivate
```

### Finding Python
```powershell
# Find Python executable
where.exe python

# Check Python version
python --version

# Check which Python is active
Get-Command python
```

### Searching Files
```powershell
# Search for text in files (like grep)
Select-String -Path *.md -Pattern "kokoro"

# Search recursively
Get-ChildItem -Recurse | Select-String "pattern"

# Find files by name
Get-ChildItem -Recurse -Filter "*.md"
```

---

## Common Bash Commands (Reference)

### File Operations
```bash
# List files
ls
ls -la              # List all, long format

# Change directory
cd /c/BRAIN_OS

# Current directory
pwd

# Move file
mv source.txt /c/destination/

# Copy file
cp source.txt destination.txt

# Delete file
rm file.txt

# Create directory
mkdir new_folder

# Create file
touch test.txt
```

### Text Processing
```bash
# Show file content
cat file.txt

# Search in files
grep "pattern" file.txt
grep -r "pattern" .    # Recursive search

# Count lines
wc -l file.txt

# First/last lines
head file.txt          # First 10 lines
tail file.txt          # Last 10 lines
tail -f log.txt        # Follow log file
```

---

## Environment Variables

### PowerShell
```powershell
# View all environment variables
Get-ChildItem Env:

# Get specific variable
$env:PATH
$env:USERPROFILE

# Set temporary variable (current session only)
$env:MY_VAR = "value"

# Set permanent variable (requires admin)
[System.Environment]::SetEnvironmentVariable("MY_VAR", "value", "User")
```

### Bash
```bash
# View all environment variables
env
printenv

# Get specific variable
echo $PATH
echo $HOME

# Set temporary variable
export MY_VAR="value"

# Set permanent variable (add to ~/.bashrc)
echo 'export MY_VAR="value"' >> ~/.bashrc
source ~/.bashrc
```

---

## VS Code Terminal Integration

### Default Terminal: PowerShell

**Open terminal:** Ctrl+` (backtick)

### Switching Between Shells

**In integrated terminal:**
1. Click dropdown arrow (next to + icon)
2. Select shell type:
   - PowerShell (default)
   - Git Bash
   - Command Prompt
   - WSL (if installed)

**Multiple terminals:**
- Click + to open new terminal
- Different shells can run simultaneously
- Switch between them with dropdown

### Setting Default Shell

**File → Preferences → Settings → search "terminal default"**

Or manually:
```json
{
  "terminal.integrated.defaultProfile.windows": "PowerShell"
}
```

---

## Scripting

### PowerShell Scripts (.ps1)
```powershell
# hello.ps1
Write-Host "Hello from PowerShell"
$name = "Cristian"
Write-Host "Welcome, $name"
```

**Run script:**
```powershell
.\hello.ps1
```

**Execution policy (if blocked):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Bash Scripts (.sh)
```bash
#!/bin/bash
# hello.sh
echo "Hello from Bash"
name="Cristian"
echo "Welcome, $name"
```

**Run script:**
```bash
bash hello.sh
# OR make executable first
chmod +x hello.sh
./hello.sh
```

---

## Identifying Which Shell You're In

### Visual Indicators

**PowerShell:**
```
PS C:\BRAIN_OS>
```
- `PS` prefix
- Windows-style paths (C:\)

**Bash:**
```
user@computer:/c/BRAIN_OS$
```
- No `PS` prefix
- Unix-style paths (/c/)
- Username@computername format

### Programmatic Check

**PowerShell:**
```powershell
$PSVersionTable
# Shows PowerShell version info
```

**Bash:**
```bash
echo $SHELL
# Shows /bin/bash or similar
```

---

## Troubleshooting

### "Command not recognized" in PowerShell

**Problem:** Typed a Bash command in PowerShell

**Example:**
```powershell
grep "pattern" file.txt
# Error: grep is not recognized
```

**Solution:** Use PowerShell equivalent:
```powershell
Select-String -Pattern "pattern" file.txt
```

### Path format errors

**Problem:** Using Unix paths in PowerShell

**Example:**
```powershell
cd /c/BRAIN_OS
# Might work due to path translation, but not guaranteed
```

**Solution:** Use Windows paths:
```powershell
cd C:\BRAIN_OS
```

### Script execution blocked

**Problem:**
```powershell
.\script.ps1
# Error: running scripts is disabled on this system
```

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Real-World Examples (From Your Workflow)

### This Session - File Operations

**What you ran:**
```powershell
cd C:\BRAIN_OS
Move-Item "$env:USERPROFILE\Downloads\VS_Code.md" "07_SYSTEM\" -Force
git add 07_SYSTEM/VS_Code.md
git commit -m "feat: document VS Code"
git push origin main
```

**What other chats sometimes suggest (Bash-style):**
```bash
cd /c/BRAIN_OS
mv ~/Downloads/VS_Code.md 07_SYSTEM/
git add 07_SYSTEM/VS_Code.md
git commit -m "feat: document VS Code"
git push origin main
```

**Both work, but PowerShell is your native environment.**

### Python venv Activation

**PowerShell (what you use):**
```powershell
C:\Dev\Projects\soccer-content-generator\venv\Scripts\Activate.ps1
```

**Bash (if you were in Git Bash):**
```bash
source /c/Dev/Projects/soccer-content-generator/venv/bin/activate
```

**Notice:** Different activation scripts for different shells.

---

## Quick Reference

### Most Used PowerShell Commands (Your Workflow)

```powershell
# Navigation
cd C:\BRAIN_OS
ls
pwd

# File operations
Move-Item file.txt destination\
Copy-Item file.txt copy.txt
Remove-Item file.txt

# Git
git status
git add .
git commit -m "message"
git push origin main
git diff HEAD~1

# Python
where.exe python
python script.py
.\venv\Scripts\Activate.ps1

# Search
Select-String -Path *.md -Pattern "search term"

# VS Code
code .
code C:\BRAIN_OS
```

---

## Connected Tools

### Integration Points

**VS Code:**
- Integrated terminal defaults to PowerShell
- Can switch to Bash via dropdown
- Terminal shares working directory with VS Code

**Git:**
- Works in both PowerShell and Bash
- Same commands, same results
- Git Bash provides Unix environment on Windows

**Python:**
- venv activation differs per shell
- Python commands (python, pip) work in both
- Path format depends on shell

**Claude Code:**
- Runs in terminal (PowerShell by default)
- `claude` command works in both shells
- Execution environment is terminal-agnostic

---

## When Chats Give You Commands

**If command starts with:**
- `Get-`, `Set-`, `New-`, `Remove-` → **PowerShell**
- `ls`, `cd`, `pwd`, `cat`, `grep`, `mv` without context → **Could be either** (check your terminal)
- Path like `/c/` or `/mnt/c/` → **Bash/Unix**
- Path like `C:\` → **PowerShell/Windows**

**Rule of thumb:**
- You're almost always in PowerShell
- If command fails, translate to PowerShell equivalent
- Refer to command translation table above

---

## Learning Resources

**PowerShell:**
- Built-in help: `Get-Help <command>`
- Examples: `Get-Help Get-ChildItem -Examples`
- Update help: `Update-Help` (run as admin)

**Bash:**
- Manual pages: `man <command>`
- Online: tldr.sh for quick examples

---

## Connected to
- [[Tools_Registry]]
- [[VS_Code]]
- [[Git_Workflow]]
- [[Python_Development]]
