# Git Phase 3 ? History and Inspection

## Core commands

git log --oneline -10
  Recent commits newest-first. Type: description pattern = conventional commits.

git log --oneline -- <file>
  Every commit that ever touched one file.
  -- tells Git: everything after this is a filepath, not a branch name.

git show <hash>
  Full diff of one commit. - line = removed. + line = added.
  Commit message explains WHY. Diff shows WHAT.

git blame <file> -L <start>,<end>
  Shows which commit last touched each line + author + date.
  Not fault-finding ? it is suspect-finding when debugging.

git bisect start
git bisect bad               current commit is broken
git bisect good <hash>       this commit was working
git bisect good/bad          test midpoint, tell Git result
git bisect reset             return to HEAD when done
  Binary search ? finds breaking commit in log2(N) steps not N steps.

## Conventional commits (your pattern)
fix:      bug fix
feat:     new feature
chore:    maintenance
session:  session close archive
queue:    queue update

## Debugging workflow
1. git log --oneline -- <file>     narrow to commits touching that file
2. git show <hash>                 inspect suspects
3. git bisect                      binary search if history is long

## Live example (BRAIN_OS)
git log --oneline -- 09_TOOLS/session_close.py  -> 8 commits
git show 552e973  -> encoding fix: added encoding="utf-8" to subprocess.run()
git blame 09_TOOLS/session_close.py -L 50,60
  -> line 53 last touched by 3744890e on 2026-05-19
  -> rest of block written by 0ed986d8 on 2026-05-13
