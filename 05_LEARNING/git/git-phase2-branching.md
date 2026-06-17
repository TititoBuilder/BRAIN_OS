# Git Phase 2 ? Branching

## Core concept
A branch is a pointer to a commit ? not a copy of the repo.
Creating a branch costs nothing ? one line in .git/refs/heads/.
Work on a branch is invisible to main until YOU merge it.

## Full branch workflow
git checkout -b <name>       create + switch to new branch
git checkout main            switch back to main
git merge <name>             bring branch work into main
git branch -d <name>         delete after merge (scaffold down)

## Key rules
- Uncommitted changes follow you across branch switches
- Commit first to isolate work to a branch
- git log --oneline main..<branch>  shows unmerged commits ? safe-to-delete check
- Empty output = branch has nothing main does not ? safe to delete

## Visualizing history
git log --oneline --graph --all -6
Shows forks, merges, HEAD position, local vs remote pointers.

## Naming convention
fix/<what>       bug fixes
feat/<what>      new features
chore/<what>     maintenance

## Branches are temporary scaffolds
Create -> build -> merge -> delete.
The work lives in main forever. The branch was just the workspace.

## Live example (BRAIN_OS)
Branch: fix/session-close
Commit: remove stale --project BDF docstring
Merged into main as 362ccb0
Branch deleted after merge ? clean.

Old stale branch found: broken-state-2026-05-05
Checked with: git log --oneline main..broken-state-2026-05-05
Output empty = no unmerged work = safe to delete. Deleted.
