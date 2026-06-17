---
knowledge_os_status: Learning
---

# Git — Understanding the Tool That Protects Your Work

Here's what you need to know about Git — not as a list of commands, but as a system you can reason about. By the end of this lesson you will understand why Git works the way it does, and you will never have to memorize a command again because the logic will tell you what to run.

---

## Part One — What Git Actually Is

Git is not a backup tool. It is not a sync tool. It is a content-addressable database that stores snapshots of your project over time.

Let's break that down.

When you save a file on your computer, you overwrite the previous version. It is gone. Git does the opposite — it never overwrites anything. Every time you take a snapshot, Git adds new data to its database and leaves everything else untouched. That means every state your project has ever been in is preserved forever, and you can go back to any of them at any time.

The database lives in a hidden folder called dot-git inside your project folder. That folder is what makes a directory a repository. Remove it and Git forgets everything — the folder is just a folder again. Keep it and you have the full history of every change ever made.

When people say repository, or repo for short, they mean a project folder that Git is tracking. Your BRAIN OS vault is a repo. Your Read Along app is a repo. Your CristianConstruction project is a repo. Each one has its own dot-git folder with its own independent history.

---

## Part Two — How Git Stores Data

Git stores four types of objects. Everything in the entire system is one of these four things.

The first is a blob. A blob stores the raw contents of a file — nothing else. No filename. No path. Just the bytes. If two files in your project have identical contents, Git stores only one blob for both of them. It never duplicates data.

The second is a tree. A tree represents a folder. It contains a list of filenames paired with the blob or tree that corresponds to each one. So a tree for your root folder would list every file and subfolder, each pointing to its blob or subtree.

The third is a commit. A commit points to one tree — the snapshot of your entire project at that moment. It also points to its parent commit, which is the previous snapshot. And it stores your name, the date, and your commit message. That chain of parent pointers is your project's history.

The fourth is a tag. A tag is a named pointer to a specific commit. Think of it as a label you pin to a moment in history — like version one point zero, or stable release.

Now here is the part that makes Git fast and safe. Every object is identified by a hash of its contents. Git takes everything inside an object, runs it through a mathematical function, and produces a forty-character fingerprint. That fingerprint is the object's address in the database. Change one byte anywhere in the object and the fingerprint changes completely.

This is why your commit hashes look the way they do — things like three-six-two-c-c-b-zero. That is not a random identifier. That is a mathematical fingerprint of everything in that commit. Two commits with the same hash are guaranteed to have identical contents. That is how Git detects corruption and guarantees integrity.

It also means Git is extremely storage-efficient. If your README file did not change between one hundred commits, all one hundred commits point to the same single blob. Git stores it once.

---

## Part Three — The Staging Area

Most version control systems have two zones — your working files and the database. Git has three.

The first zone is your working directory. These are the actual files you see and edit on your computer. When you open a file in VS Code and change something, you are working in this zone.

The second zone is the staging area, also called the index. This is Git's preparation area for the next commit. It sits between your working files and the database. Nothing goes into a commit without passing through here first.

The third zone is the repository — the dot-git database of permanent snapshots.

Here is how data moves between them.

When you run git add followed by a filename, you are taking that file from your working directory and placing a copy of it in the staging area. You are saying — this is what I want in the next snapshot. You can add multiple files one at a time, building exactly the commit you want.

When you run git commit, Git takes everything in the staging area, builds a tree from it, wraps it in a commit object with your message, and writes it permanently to the database. The staging area does not clear — it stays as your current snapshot until the next change.

This three-zone design is intentional. It lets you work on ten things at once but commit them as separate, focused snapshots. One commit for the bug fix. One commit for the documentation update. One commit for the new feature. Each one tells a clean story.

This is why the discipline of adding by explicit filename matters. When you run git add with a specific file, you are making a deliberate choice about what story this commit tells. Adding everything at once with a shortcut bypasses that intention and produces commits that mix unrelated changes — which makes the history harder to read and the bugs harder to find.

---

## Part Four — Reading Status and Differences

Before you commit anything, you need to see what state you are in. Two commands give you that picture.

Git status shows you which files have changed since the last commit, and which of those changes are currently in the staging area. You will see two sections — changes not staged for commit, and changes staged for commit. The first section is your working directory. The second is what will go into the next commit if you run it right now.

Git diff shows you the actual lines that changed. Run it without arguments and you see the difference between your working directory and the staging area. Run it with the flag double-dash-cached and you see the difference between the staging area and the last commit — meaning exactly what would be written if you committed right now.

Reading a diff takes one minute to learn. Lines starting with a minus sign were removed. Lines starting with a plus sign were added. Lines with no prefix are context — they show surrounding code so you know where you are in the file.

The habit to build is this: run git status before every add, and run git diff double-dash-cached before every commit. Never commit blind. Verify the state before writing to history.

---

## Part Five — Branching

A branch is a pointer to a commit. That is all it is. Not a copy of your project. Not a separate folder. Just a lightweight pointer — a name that says this is where I am working right now.

When you create a branch, Git creates a new pointer at your current commit and that is it. The entire operation takes milliseconds and costs almost no storage. This is why Git encourages branching freely — it is genuinely cheap.

Here is why branching matters in practice. Imagine you are about to rewrite a script that runs every time you close a session. If that script breaks, your entire session close workflow is dead until you fix it. If you work directly on your main branch, that risk is real. If you work on a separate branch, your main branch stays untouched until you are confident the work is ready.

The workflow goes like this. You create a new branch with git checkout dash-b followed by a name. You do your work and commit it to that branch. Your main branch does not see any of those commits — it stays exactly where it was. When you are satisfied, you switch back to main and run git merge followed by your branch name. Git finds the point where the two branches diverged and combines the work. Then you delete the branch because it served its purpose. The commits live in main forever. The branch was just the workspace — temporary scaffolding that you take down when the building is done.

Branch names should describe the work. Fix slash something for bug fixes. Feat slash something for new features. Chore slash something for maintenance. The slash is just a naming convention — it helps you organize when you have many branches.

---

## Part Six — Merge Conflicts

Sometimes when you merge, Git cannot figure out how to combine two sets of changes automatically. This happens when both branches edited the same lines in the same file. Git does not guess which version is correct — it stops and asks you to decide.

This is called a merge conflict, and it looks more alarming than it is.

Git marks the conflicting section in the file with three sets of markers. A line of seven less-than signs followed by the word HEAD marks the start of your local version. A line of seven equals signs divides your version from the incoming version. A line of seven greater-than signs followed by a commit hash marks the end of the incoming version.

Your job is simple. Open the file, find the markers, decide which version to keep — or combine them if both have useful content — then delete all three marker lines. Save the file. Run git add on it. Run git commit. The conflict is resolved and the merge completes.

The mental model to hold is that Git is protecting you. It found a genuine ambiguity and refused to make a choice on your behalf. That is the correct behavior. Once you understand what the markers mean, resolving a conflict takes less than two minutes.

---

## Part Seven — Reading History

Git stores the complete history of your project, and it gives you tools to read it at any level of detail.

Git log shows you the commit history. Add the flag double-dash-oneline to see one line per commit — the hash and the message. This is your project timeline. Newest commits at the top, oldest at the bottom.

To see the history of a specific file, add double-dash followed by the filename. Git filters the log to show only commits that touched that file. This is how you answer the question — when did this behavior change? You do not read through hundreds of commits. You filter to the ten or twenty that touched the relevant file.

Git show followed by a commit hash shows you the full details of that commit — the message, the author, the date, and the complete diff of every line that changed. This is how you go from knowing which commit is suspicious to seeing exactly what it did.

Git blame followed by a filename shows you each line of the file annotated with the commit that last touched it, along with the author and date. This is not about assigning fault — it is about finding which commit introduced a specific line of code, so you can understand the context and history behind it.

Git bisect is for when you have a bug and you know it did not exist at some earlier point. You tell Git which commit was good and which commit is bad. Git checks out the commit exactly halfway between them. You test whether the bug exists. You tell Git good or bad. Git checks out the halfway point of the remaining range. You repeat until Git identifies the exact first bad commit. This is a binary search — it finds the answer in logarithmic time rather than linear time. For one hundred commits, you find the culprit in seven steps.

---

## Part Eight — Remote Repositories and Synchronization

Your local repository and GitHub are two separate things that you keep in sync manually.

Your local repo is the dot-git folder on your machine. GitHub is a server that hosts a copy of that same repo. When you push, you send your local commits to GitHub. When you pull, you download GitHub's commits to your local machine.

There is a third thing that surprises people. Git maintains a local cache of what GitHub looks like. It is called origin slash main. When Git tells you your branch is up to date with origin slash main, it is not checking GitHub live — it is comparing against this cached snapshot. The cache updates when you fetch or pull.

Git fetch downloads new commits from GitHub and updates the cache, but does not merge anything into your working branch. It is a safe read operation. Git pull is fetch followed by merge — it downloads and integrates in one step.

The name origin is just a shortcut. It is the default name Git gives to the remote you cloned from. When you run git push, Git expands origin to the full URL of your GitHub repository.

---

## Part Nine — Recovery Tools

Three commands exist specifically for when things go wrong.

Git revert creates a new commit that undoes the changes from a previous commit. Your history is preserved — you can see both the original commit and the reverting commit. This is the safe way to undo something that has already been pushed to GitHub.

Git reset moves your branch pointer backward to an earlier commit. With the flag double-dash-hard, it also discards all the changes after that point. This is destructive — use it only on commits that have not been pushed, or when you are absolutely certain you want to erase the work.

Git reflog is your ultimate safety net. It records every position HEAD has ever been at — every commit, every checkout, every merge, every reset. Even if you run git reset double-dash-hard and lose commits, reflog still has a record of where you were before. You can use it to recover anything that happened in the last ninety days.

The habit is this: before any destructive operation, run git reflog to see the current state. After the operation, if something went wrong, run git reflog again to find the position you want to recover, and use git reset to go back there.

---

## Part Ten — Your Workflow Principles

Everything in this lesson connects to five principles that make Git work for a serious project.

First — every project gets a remote at creation. Your local dot-git is one machine. One drive failure and it is gone. The remote is your backup, your deploy trigger, and your safety net. Create the remote the same day you create the project.

Second — add by explicit filename. You now understand why. The staging area exists so you build commits with intention. Adding everything at once produces noisy history that is hard to read and hard to debug.

Third — audio and generated files never get committed. Git tracks text. Binary files like audio, images, and compiled artifacts inflate your repository and cannot be meaningfully diffed. They belong in cloud storage with their IDs tracked in a JSON index. Your dot-gitignore file is the enforcement mechanism.

Fourth — one commit per concern. A commit that fixes a bug and adds a feature and updates documentation is three commits collapsed into one. Future you cannot undo just the bug fix without also undoing the feature. Small, focused commits with clear messages are a gift to yourself six months from now.

Fifth — verify before write. Git status before every add. Git diff double-dash-cached before every commit. Never commit blind. The two seconds you spend verifying save the ten minutes you spend recovering from a mistake.

Git is a tool that rewards understanding over memorization. Once you see that it is a database of snapshots identified by hashes, the commands stop being arbitrary. Push sends snapshots to the cloud. Pull downloads them. Branch creates a new pointer. Merge combines two lines of snapshots. Everything follows from the model.

That is Git.
