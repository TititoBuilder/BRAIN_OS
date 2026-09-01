"""
category: Vault & Sync
vault_paths.py — The one definition of which directories are not vault content.

vault_index.py and compile_session.py must agree on this set or their file
lists diverge: one scanner sees a file the other does not. They previously
held separate copies with a comment asking a human to keep them in sync.

Membership is by path segment at any depth, not by prefix, so a venv nested
below the top level is excluded too.

Verified 2026-08-27: .obsidian, audio_staging, and root _archive hold zero
.md files; only 02_PROJECTS/_archive does, with two.

Import as a sibling:
    from vault_paths import SKIP_DIRS
"""

SKIP_DIRS = {
    "venv",
    ".git",
    ".obsidian",
    "_archive",
    "audio_staging",
    "__pycache__",
    "node_modules",
}


if __name__ == "__main__":
    print(f"{len(SKIP_DIRS)} excluded directory names:")
    for d in sorted(SKIP_DIRS):
        print(" ", d)
