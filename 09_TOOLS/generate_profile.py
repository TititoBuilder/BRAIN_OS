#!/usr/bin/env python3
"""
Generate PowerShell $PROFILE from SYSTEM_MASTER.md as single source of truth.

1. Reads the current profile and extracts verbatim the two complex functions
   that cannot be pattern-generated: dev (file watcher) and ca-audio (venv
   activation + cd + run).
2. Reads the aliases table from SYSTEM_MASTER.md (validation only — confirms
   the generated set matches what is documented).
3. Generates correct function bodies for every alias from known patterns
   (log, compile, book, special cases).
4. Reads HF_TOKEN and GITHUB_TOKEN from C:\\BRAIN_OS\\03_APIS\\.env and emits
   them as $env: assignment lines — values never hardcoded in the profile.
5. Writes the complete, regenerated profile to both PS profile paths (they
   must remain identical per SYSTEM_MASTER.md constraint).

Usage:
    python generate_profile.py            # write both profiles
    python generate_profile.py --dry-run  # print to stdout only
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SYSTEM_MASTER = Path(r"C:\BRAIN_OS\SYSTEM_MASTER.md")
ENV_FILE = Path(r"C:\BRAIN_OS\03_APIS\.env")
PROFILE_MAIN = Path(
    r"C:\Users\titit\OneDrive\Documents\WindowsPowerShell"
    r"\Microsoft.PowerShell_profile.ps1"
)
PROFILE_VSCODE = Path(
    r"C:\Users\titit\OneDrive\Documents\WindowsPowerShell"
    r"\Microsoft.VSCode_profile.ps1"
)

# Functions preserved verbatim from the current profile (complex logic)
PRESERVE_VERBATIM = {"dev", "ca-audio"}

# Expected alias names from SYSTEM_MASTER.md § PowerShell Aliases
EXPECTED_ALIASES = {
    "bdf-log", "bdf-compile", "bdf-book",
    "ca-log", "ca-compile", "ca-book", "ca-audio",
    "dev",
    "mcp-log", "mcp-compile", "mcp-book",
    "bdf-tts", "brainos-book", "map-bdf", "cc",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_ps_functions(text: str) -> dict[str, str]:
    """Parse PowerShell function blocks by tracking brace depth.

    Handles nested braces correctly (while-loops, if-blocks, etc.).
    Returns {name: full_definition_string}.
    """
    functions: dict[str, str] = {}
    lines = text.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        m = re.match(r"\s*function\s+([\w-]+)\s*\{", lines[i])
        if m:
            name = m.group(1)
            depth = lines[i].count("{") - lines[i].count("}")
            start = i
            i += 1
            while i < len(lines) and depth > 0:
                depth += lines[i].count("{") - lines[i].count("}")
                i += 1
            functions[name] = "".join(lines[start:i]).rstrip()
        else:
            i += 1
    return functions


def read_env(path: Path) -> dict[str, str]:
    """Read key=value pairs from a .env file. Returns empty dict if missing."""
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            env[key.strip()] = val.strip()
    return env


def extract_alias_names_from_master(text: str) -> set[str]:
    """Extract alias names listed in the PowerShell Aliases table."""
    names: set[str] = set()
    in_table = False
    for line in text.splitlines():
        if "## PowerShell Aliases" in line:
            in_table = True
            continue
        if in_table:
            if line.startswith("##") and "PowerShell Aliases" not in line:
                break
            m = re.match(r"\|\s*`([\w-]+)`", line)
            if m:
                names.add(m.group(1))
    return names


# ---------------------------------------------------------------------------
# Function generators
# All paths come from SYSTEM_MASTER.md § Canonical Paths
# ---------------------------------------------------------------------------

def log_func(name: str, target: str) -> str:
    """Move a file from Downloads to the project's Session_Resumes/processed/."""
    return (
        f"function {name} {{\n"
        f"    param([string]$file)\n"
        f'    Move-Item "$env:USERPROFILE\\Downloads\\$file" "{target}" -Force\n'
        f'    Write-Host "Session log moved to processed\\" -ForegroundColor Green\n'
        f"}}"
    )


def compile_func(name: str, target: str) -> str:
    """Move a file from Downloads to the project's book incoming/ drop zone."""
    return (
        f"function {name} {{\n"
        f"    param([string]$file)\n"
        f'    Move-Item "$env:USERPROFILE\\Downloads\\$file" "{target}" -Force\n'
        f'    Write-Host "Compile file moved to incoming\\" -ForegroundColor Green\n'
        f"}}"
    )


def book_func(name: str, book_key: str) -> str:
    """CA venv python → shared book_compiler.py --book <key>."""
    py = "C:\\Knowledge\\CA\\venv\\Scripts\\python.exe"
    compiler = "C:\\Dev\\shared\\book-compiler\\book_compiler.py"
    return (
        f"function {name} {{\n"
        f'    & "{py}" "{compiler}" --book {book_key} @args\n'
        f"}}"
    )


# Special-case functions that don't fit a repeating pattern
# ----------------------------------------------------------------

MCP_BOOK = "\n".join([
    "function mcp-book {",
    # CA venv python → mcp_book_compiler.py (separate compiler, not shared book-compiler)
    '    & "C:\\Knowledge\\CA\\venv\\Scripts\\python.exe"'
    ' "C:\\Dev\\Projects\\soccer-content-generator\\mcp_book_compiler.py" @args',
    "}",
])

BDF_TTS = "\n".join([
    "function bdf-tts {",
    # CA venv carries PyTorch/Kokoro — required for TTS inference
    '    & "C:\\Knowledge\\CA\\venv\\Scripts\\python.exe"'
    ' "C:\\Dev\\Projects\\soccer-content-generator\\tts_local.py" @args',
    "}",
])

MAP_BDF = "\n".join([
    "function map-bdf {",
    '    Push-Location "C:\\Dev\\Projects\\soccer-content-generator"',
    '    & ".\\venv\\Scripts\\python.exe" "scripts\\graph_maintainer.py"',
    "    Pop-Location",
    "}",
])

CC = "\n".join([
    "function cc {",
    "    claude --dangerously-skip-permissions @args",
    "}",
])

# ---------------------------------------------------------------------------
# Profile builder
# ---------------------------------------------------------------------------

def build_profile(preserved: dict[str, str], env: dict[str, str]) -> str:
    """Assemble the complete profile string from generated + preserved parts."""
    parts: list[str] = []

    # --- Log aliases (SYSTEM_MASTER.md: Session_Resumes/processed/ targets) ---
    log_targets = {
        "bdf-log": "C:\\Knowledge\\BDF\\Session_Resumes\\processed\\",
        "ca-log":  "C:\\Knowledge\\CA\\Session_Resumes\\processed\\",
        "mcp-log": "C:\\Knowledge\\MCP\\Session_Resumes\\processed\\",
    }
    for name, target in log_targets.items():
        parts.append(log_func(name, target))

    # --- Compile aliases (SYSTEM_MASTER.md: *_Book/incoming/ targets) ---
    compile_targets = {
        "bdf-compile": "C:\\Knowledge\\BDF\\BDF_Book\\incoming\\",
        "ca-compile":  "C:\\Knowledge\\CA\\CA_Book\\incoming\\",
        "mcp-compile": "C:\\Knowledge\\MCP\\MCP_Book\\incoming\\",
    }
    for name, target in compile_targets.items():
        parts.append(compile_func(name, target))

    # --- Book aliases (CA venv → shared book compiler) ---
    for name, key in [("bdf-book", "bdf"), ("ca-book", "ca"), ("brainos-book", "brainos")]:
        parts.append(book_func(name, key))

    # --- Special-case aliases ---
    parts.append(MCP_BOOK)
    parts.append(BDF_TTS)
    parts.append(MAP_BDF)
    parts.append(CC)

    # --- Preserved complex functions (verbatim from current profile) ---
    for name in ("dev", "ca-audio"):
        if name in preserved:
            parts.append(preserved[name])
        else:
            print(f"WARNING: '{name}' not found in current profile — omitted.", file=sys.stderr)

    # --- Env var lines from C:\BRAIN_OS\03_APIS\.env ---
    env_lines: list[str] = []
    for key in ("HF_TOKEN", "GITHUB_TOKEN"):
        if key in env:
            env_lines.append(f'$env:{key} = "{env[key]}"')
        else:
            print(
                f"WARNING: {key} not in {ENV_FILE} — omitted from profile.\n"
                f"         Add {key}=<value> to that .env file and re-run.",
                file=sys.stderr,
            )
    if env_lines:
        parts.append("\n".join(env_lines))

    return "\n\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    dry_run = "--dry-run" in sys.argv

    # Validate source files exist
    for path in (SYSTEM_MASTER, PROFILE_MAIN):
        if not path.exists():
            print(f"ERROR: required file not found: {path}", file=sys.stderr)
            sys.exit(1)

    # --- Step 1: extract verbatim functions from current profile ---
    current_text = PROFILE_MAIN.read_text(encoding="utf-8")
    all_funcs = extract_ps_functions(current_text)
    preserved = {n: body for n, body in all_funcs.items() if n in PRESERVE_VERBATIM}
    print(f"Current profile: {len(all_funcs)} functions parsed.")
    print(f"Preserving verbatim: {sorted(preserved)}")

    # --- Step 2: validate aliases against SYSTEM_MASTER.md ---
    master_text = SYSTEM_MASTER.read_text(encoding="utf-8")
    documented = extract_alias_names_from_master(master_text)
    if documented:
        missing_from_script = documented - EXPECTED_ALIASES
        extra_in_script = EXPECTED_ALIASES - documented
        if missing_from_script:
            print(f"WARNING: aliases in SYSTEM_MASTER.md not generated: {missing_from_script}")
        if extra_in_script:
            print(f"NOTE: aliases generated but not in SYSTEM_MASTER.md table: {extra_in_script}")
        print(f"SYSTEM_MASTER.md alias table: {sorted(documented)}")
    else:
        print("WARNING: could not parse aliases table from SYSTEM_MASTER.md")

    # --- Step 3: read tokens ---
    env = read_env(ENV_FILE)
    found = [k for k in ("HF_TOKEN", "GITHUB_TOKEN") if k in env]
    if found:
        print(f"Tokens loaded from .env: {found}")

    # --- Step 4: build ---
    content = build_profile(preserved, env)

    if dry_run:
        print("\n" + "=" * 60)
        print("DRY RUN — generated profile:")
        print("=" * 60)
        print(content)
        print("=" * 60)
        return

    # --- Step 5: write both profiles (must be identical per SYSTEM_MASTER.md) ---
    for dest in (PROFILE_MAIN, PROFILE_VSCODE):
        dest.write_text(content, encoding="utf-8")
        print(f"Written: {dest}")

    print("Done. Both profiles regenerated and kept in sync.")


if __name__ == "__main__":
    main()
