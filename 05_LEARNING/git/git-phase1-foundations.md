# Git Phase 1 ? Foundations

## Topic 1: Object Model
Four object types ? everything in Git is one of these:
- blob   ? file contents only (no name, no path)
- tree   ? folder snapshot (lists blobs + subtrees by name)
- commit ? points to one tree + one parent + author + message
- tag    ? named pointer to a commit

SHA = the address. Every object named by hash of its contents.
Same content = same hash. Git never duplicates data.
One file change = four new objects: blob -> tree -> parent trees -> commit.
Old objects untouched. History is immutable.

Commands:
  git cat-file -t <hash>   show object type
  git cat-file -p <hash>   show object contents
  git log --oneline -5     show recent commits

## Topic 2: Staging Area
Three zones: working directory -> staging area -> repository
git add   = move file from working dir into staging area (builds next commit)
git commit = snapshot the staging area into the repository permanently

git status        shows what is modified vs staged
git diff --cached shows exactly what is staged right now

Why explicit filenames: git add -A dumps everything ? staging area
exists so you build commits intentionally, one concern at a time.

## Topic 3: Merge Conflicts
Diverged branches = both sides moved forward independently:
          A -- your commit
         /
... -- base
         \
          B -- remote commit

git pull = git fetch + git merge combined.
Conflict markers:
  <<<<<<< HEAD       your version
  =======            divider
  >>>>>>> <hash>     remote version

Resolution: pick one side, delete markers, git add, git commit, git push.

## Topic 4: .gitignore ? coming next

## Key commands learned live
  git cat-file -t <hash>
  git cat-file -p <hash>
  git log --oneline -5
  git status
  git diff <file>
  git diff --cached
  git add <explicit-filename>
  git pull
  git push
  git check-ignore -v <file>

## Topic 4: .gitignore
Tells Git which files to never track.
Only works on UNTRACKED files ? already committed files need git rm --cached.

Pattern rules:
  *.mp3                    any .mp3 anywhere in repo
  audio_staging/*.mp3      .mp3 directly inside audio_staging only
  audio_staging/**/*.mp3   .mp3 inside audio_staging at any depth
  !important.mp3           un-ignore this specific file
  Untitled*.canvas         wildcard prefix match

Three rules that bite people:
1. gitignore only works on untracked files
2. First match wins ? order matters
3. Negation ! must come AFTER the ignore rule, not before

gitignore does NOT support regex ? glob patterns only.

Commands:
  git check-ignore -v <file>   verify why a file is ignored
  git rm --cached <file>       untrack a committed file without deleting it
