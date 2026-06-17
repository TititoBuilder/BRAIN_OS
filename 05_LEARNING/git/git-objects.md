# Git Object Model

## Four object types
- blob   ? file contents only (no name, no path)
- tree   ? folder snapshot (lists blobs + subtrees by name)
- commit ? points to one tree + one parent + author + message
- tag    ? named pointer to a commit (Phase 2)

## SHA = the address
Every object is named by SHA-1 hash of its contents.
Same content = same hash. Git never duplicates data.

## One file change = four new objects
file change -> new blob -> new tree -> new parent trees -> new commit
Old objects untouched. History is immutable.

## Commands
git cat-file -t <hash>   show object type
git cat-file -p <hash>   show object contents
git log --oneline -5     show recent commits

## Live example (BRAIN_OS)
commit a2ea9b8 points to tree bde83ae
tree bde83ae lists all root folders as subtrees + files as blobs
CLAUDE.md = blob be9f966 ? unchanged across commits = stored once
