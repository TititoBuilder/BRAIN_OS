# Git Phase 4 ? Remote and Collaboration

## Three things in your Git world
1. Local repo: C:\BRAIN_OS\.git\
2. GitHub: github.com/TititoBuilder/BRAIN_OS
3. origin/main: Git local cached snapshot of GitHub

"Your branch is up to date with origin/main" = compared against cache, NOT live GitHub.
git fetch updates the cache. git pull = fetch + merge.

## Remote commands
git fetch              update origin/main snapshot, no merge
git pull               fetch + merge into current branch
git push               send local commits to GitHub, move origin/main forward
git remote -v          show where origin points

## Reading pointers
git log --oneline --graph --all -3
  HEAD -> main    where you are locally
  origin/main     Git cached snapshot of GitHub
  origin/HEAD     GitHub default branch pointer
All three aligned = perfect sync.

## Safety commands
git revert <hash>         new commit that undoes a previous one (safe, history preserved)
git reset --hard <hash>   move HEAD back, discard everything after (destructive)
git reflog                black box recorder ? every HEAD position ever

## Recovery pattern
git reflog -10            find the position you want
git reset --hard HEAD@{N} go back to that exact moment
Nothing truly lost while reflog has it (90 day default retention).

## Live example (BRAIN_OS)
git remote -v -> origin = https://github.com/TititoBuilder/BRAIN_OS.git
git reflog showed full session history:
  merge, checkouts, commits, conflict resolution ? all recorded
