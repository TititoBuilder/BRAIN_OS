# FLAGS.txt — Field Manual
Location: C:\BRAIN_OS\FLAGS.txt
Updated: 2026-08-10

---

## What FLAGS.txt Is

Your personal study syllabus, generated from your own codebase.
Every line is something that surprised you, confused you, or revealed
a gap while working on real code. It is not a to-do list. It is a
record of where your understanding ended and the unknown began.

---

## File Format

One flag per line. Seven pipe-separated columns. No exceptions.

    DATE | REPO | TYPE | THING | WHAT I EXPECTED | WHAT HAPPENED | QUESTION/ACTION

Rules:
- One entry per line — press Enter after every flag
- Seven columns separated by | (pipe character)
- Add | FIXED at the end when resolved
- Never split one flag across two lines
- Edit in VS Code, never in the terminal

---

## Column Definitions

### DATE
Format: YYYY-MM-DD
When you found it. Patterns emerge over time. If CMD flags keep
appearing every session, that's a signal you need terminal drills,
not theory. If DESIGN flags cluster around one repo, that repo
has structural debt.

### REPO
The repo or tool where the flag appeared.
Examples: BRAIN_OS, custom-agent, resolve-mcp-server, POWERSHELL
If one repo generates most flags, that repo needs the most attention.

### TYPE
The category. This is the most important column — you sort by it
at the end of every session to decide what to study next.

    RISK    Work that could be lost or exposed. Fix immediately.
            Examples: unpushed commits, secrets in history,
            untracked work, OneDrive sync conflicts

    DESIGN  Something structurally wrong that should be fixed.
            Examples: hardcoded paths, backup files instead of
            git tags, nested repos, duplicate copies of a project

    CMD     A command, flag, or tool behavior you could not explain.
            Examples: git diff A..B vs A...B, Select-String syntax,
            why -Force is needed to find .git folders

    CONCEPT A git/python/system idea you only half understand.
            Examples: what a merge base is, how LF/CRLF conversion
            works, what HEAD actually points to

    CODE    Code in your own repos you cannot explain.
            Examples: a function you wrote 3 months ago and no
            longer recognize, a pattern you copied without understanding

### THING
The specific subject. Short enough to search for later.
Examples: "hardcoded absolute paths", "git diff A...B", "venv location"

### WHAT I EXPECTED
What you thought would happen before you ran the command or read
the code. "Unknown" is a valid answer. Guessing wrong is more
useful than not guessing — the gap between expectation and reality
is where learning happens.

### WHAT HAPPENED
The reality. One sentence. What git actually did, what the output
actually showed, what the code actually does.

### QUESTION/ACTION
What you do with this flag:
- A question to research: "what is a merge base?"
- A fix to apply: "apply .env pattern"
- A decision: "delete and rely on git log"
- Status: FIXED (with date)

---

## Type Sort — What Each Distribution Means

At the end of every session, count your flags by TYPE.
The distribution tells you what to do next.

    Mostly RISK     → Fix today before anything else. Stop all
                      other work until RISK flags are cleared.

    Mostly CMD      → You need terminal drills, not theory.
                      Open FreeCodeCamp Relational Database cert.
                      Drill only the flagged commands, not the
                      whole curriculum linearly.

    Mostly CONCEPT  → Read git internals before writing more
                      automation. Study: objects, refs, index,
                      merge base, HEAD.

    Mostly CODE     → Your problem is documentation, not knowledge.
                      Write a README per repo, 10 lines each,
                      before adding any new features.

    Mostly DESIGN   → Stop adding features. Refactor the churn
                      hot spots from Phase 2 archaeology first.

---

## Session Workflow

1. Open FLAGS.txt in VS Code at the start of every session
2. Review open flags — are any now answerable?
3. Work the lesson or direction
4. Log flags as they appear — don't batch at the end
5. At session close: sort by TYPE, count each group
6. Top 3 open flags become the next session's opening moves
7. Commit FLAGS.txt to BRAIN_OS before closing

---

## Example Entries

    2026-08-10 | BRAIN_OS | RISK | ahead 7, never pushed | thought it was synced | 7 commits only on laptop | push immediately | FIXED
    2026-08-10 | custom-agent | DESIGN | hardcoded absolute paths | works locally | breaks on other machines | apply .env + pathlib pattern | FIXED
    2026-08-10 | POWERSHELL | CMD | typed filepath as command | thought PS would open it | PS tried to execute it | use: code <path> to open files
    2026-08-10 | BRAIN_OS | CONCEPT | git diff A..B vs A...B | thought they were the same | symmetric difference vs range | study git diff mechanics

---

## What FLAGS.txt Is Not

- Not a task manager (use your 4-bucket system for tasks)
- Not a journal (one line per flag, no prose)
- Not a trophy case (FIXED flags stay in the file as history)
- Not optional (skipping it means repeating the same gaps forever)

