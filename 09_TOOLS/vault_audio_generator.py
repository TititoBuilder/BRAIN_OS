"""
vault_audio_generator.py — Vault Node Audio Generator
Converts HIGH priority BRAIN_OS vault .md files into spoken audio.

Pipeline per file:
  1. Read .md file from vault
  2. Call Claude API to convert to natural spoken narration script
  3. Run Kokoro TTS (am_heart voice) to generate .mp3
  4. Save to converted/ folder for Drive upload

Usage:
    python vault_audio_generator.py --dry-run
    python vault_audio_generator.py
    python vault_audio_generator.py --skip-existing
    python vault_audio_generator.py --limit 5
    python vault_audio_generator.py --file "07_SYSTEM/Cristian_Principles.md"
"""

import argparse
import os
import sys
import json
import time
import urllib.request
import urllib.error
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# ── Config ─────────────────────────────────────────────────────────────────────
BRAIN_OS_ROOT = Path(r"C:\BRAIN_OS")
PROJECT_ROOT  = Path(r"C:\Dev\Projects\soccer-content-generator")
OUTPUT_DIR    = PROJECT_ROOT / "converted" / "vault_audio"
ENV_FILE      = PROJECT_ROOT / ".env"
TTS_SCRIPT    = PROJECT_ROOT / "tts_local.py"
PYTHON_EXE    = Path(r"C:\Knowledge\CA\venv\Scripts\python.exe")
TTS_VOICE     = "af_heart"
DELAY_SECONDS = 3

# ── HIGH priority vault nodes ──────────────────────────────────────────────────
HIGH_PRIORITY_NODES = [
    # 07_SYSTEM
    "07_SYSTEM/Cristian_Principles.md",
    "07_SYSTEM/Trigger_Architecture.md",
    "07_SYSTEM/Session_Protocol.md",
    "07_SYSTEM/MCP_Registry.md",
    "07_SYSTEM/Project_Directory.md",
    "07_SYSTEM/Tools_Registry.md",
    "07_SYSTEM/Master_Control.md",
    "07_SYSTEM/Active_Environments.md",
    "07_SYSTEM/KNOWLEDGE_INGESTION_PROTOCOL_V2.md",
    # 02_AGENTS
    "02_AGENTS/Content_Orchestrator.md",
    "02_AGENTS/Data_Orchestrator.md",
    "02_AGENTS/Video_Orchestrator.md",
    "02_AGENTS/DaVinci_Resolve_MCP.md",
    "02_AGENTS/Resolve_Editing_Agent.md",
    "02_AGENTS/BDF_Memory_Agent.md",
    # 02_PROJECTS
    "02_PROJECTS/BDF_Agent_Pipeline.md",
    "02_PROJECTS/BDF_Book_System.md",
    "02_PROJECTS/Resolve_MCP_Server.md",
    "02_PROJECTS/Read_Along_App.md",
    "02_PROJECTS/CristianConstruction.md",
    # 04_WORKFLOWS
    "04_WORKFLOWS/BDF_Video_Production_Flow.md",
    "04_WORKFLOWS/BDF_Knowledge_Build_Flow.md",
    # 01_DOMAINS
    "01_DOMAINS/AI_Engineering.md",
    "01_DOMAINS/Creative_Systems.md",
    # 05_MEMORY
    "05_MEMORY/Memory_Index.md",
    "05_MEMORY/LanceDB_Vector_Store.md",
    # 08_TRIGGERS
    "08_TRIGGERS/Trigger_Architecture.md" if False else "07_SYSTEM/Trigger_Architecture.md",
    "08_TRIGGERS/Trigger_Session_Close.md",
    "08_TRIGGERS/Trigger_Render_Complete.md",
    "08_TRIGGERS/Trigger_BDF_Queue_Check.md",
]

# Deduplicate
HIGH_PRIORITY_NODES = list(dict.fromkeys(HIGH_PRIORITY_NODES))

NARRATION_PROMPT = """You are converting a technical knowledge document into a natural spoken audio script.
The listener is Cristian, a developer learning about his own systems while driving or at the gym.

Rules:
- Write in second person: "You built..." "Your system..."
- Convert all wiki-links [[Like_This]] to plain text "Like This"
- Convert markdown headers to natural spoken transitions: "Let's talk about..."
- Convert bullet lists to flowing sentences
- Skip frontmatter (tags, dates) entirely
- Skip raw code blocks — describe what the code does instead
- Length: aim for 3-5 minutes of speech (~400-600 words)
- Tone: clear, direct, conversational — like a knowledgeable colleague explaining your own work back to you
- Start with: "Here's what you need to know about [topic]..."

Output only the spoken script — no headers, no markdown, no preamble."""


def load_api_key() -> str:
    load_dotenv(ENV_FILE)
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        print("[vault_audio] ERROR: ANTHROPIC_API_KEY not found")
        sys.exit(1)
    return key


def md_to_script(md_content: str, filename: str, api_key: str) -> str:
    """Convert markdown content to spoken narration script via Claude API."""
    if len(md_content) > 8000:
        md_content = md_content[:8000] + "\n\n[...content truncated...]"

    payload = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "system": NARRATION_PROMPT,
        "messages": [{
            "role": "user",
            "content": f"Document: {filename}\n\n{md_content}\n\nGenerate the spoken audio script now."
        }]
    }

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["content"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        print(f"[vault_audio] API error {e.code}: {e.read().decode()}")
        sys.exit(1)


def run_tts(script: str, output_mp3: Path) -> bool:
    """Synthesize script to MP3 using tts_local.py."""
    temp_txt = output_mp3.with_suffix(".txt")
    temp_txt.write_text(script, encoding="utf-8")

    result = subprocess.run(
        [str(PYTHON_EXE), str(TTS_SCRIPT), str(temp_txt), "--voice", TTS_VOICE],
        capture_output=True, text=True,
        encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}
    )

    # tts_local.py appends _af_heart_audio to stem
    actual = output_mp3.parent / (output_mp3.stem + f"_{TTS_VOICE}_audio.mp3")
    if result.returncode == 0 and actual.exists():
        actual.rename(output_mp3)
        return True

    print(f"[vault_audio] TTS failed: {result.stderr[-200:]}")
    return False


def slug(filepath: str) -> str:
    """Convert path to flat filename slug."""
    return Path(filepath).stem.lower().replace(" ", "_")


def output_exists(filepath: str) -> bool:
    mp3 = OUTPUT_DIR / f"{slug(filepath)}_audio.mp3"
    return mp3.exists()


def main():
    parser = argparse.ArgumentParser(description="Generate audio for vault HIGH priority nodes")
    parser.add_argument("--dry-run",       action="store_true")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--limit",         type=int, default=None)
    parser.add_argument("--file",          help="Process single file (relative to BRAIN_OS root)")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Single file mode
    if args.file:
        files = [args.file]
    else:
        files = HIGH_PRIORITY_NODES.copy()
        if args.skip_existing:
            files = [f for f in files if not output_exists(f)]
        if args.limit:
            files = files[:args.limit]

    print(f"[vault_audio] {len(files)} files to process")
    print(f"[vault_audio] Output: {OUTPUT_DIR}")
    print()

    if args.dry_run:
        for i, f in enumerate(files, 1):
            exists = "✓" if output_exists(f) else "·"
            print(f"  {i:02d}. [{exists}] {f}")
        print(f"\n[vault_audio] Dry run — nothing processed.")
        return

    api_key = load_api_key()
    success, failed = [], []

    for i, filepath in enumerate(files, 1):
        md_path = BRAIN_OS_ROOT / filepath
        if not md_path.exists():
            print(f"  {i}/{len(files)} ⚠️  NOT FOUND: {filepath}")
            failed.append(filepath)
            continue

        print(f"  {i}/{len(files)} {Path(filepath).stem}")

        md_content = md_path.read_text(encoding="utf-8", errors="ignore")
        print(f"    → generating script ({len(md_content.split())} words)...")
        script = md_to_script(md_content, Path(filepath).name, api_key)
        print(f"    → script: {len(script.split())} words")

        output_mp3 = OUTPUT_DIR / f"{slug(filepath)}_audio.mp3"
        print(f"    → synthesizing...")
        if run_tts(script, output_mp3):
            size_mb = output_mp3.stat().st_size / (1024 * 1024)
            print(f"    ✅ {output_mp3.name} ({size_mb:.1f} MB)")
            success.append(filepath)
        else:
            print(f"    ❌ TTS failed")
            failed.append(filepath)

        if i < len(files):
            time.sleep(DELAY_SECONDS)

    print()
    print("=" * 55)
    print(f"  VAULT AUDIO COMPLETE")
    print(f"  Success: {len(success)}/{len(files)}")
    if failed:
        print(f"  Failed:  {len(failed)}")
        for f in failed:
            print(f"    - {f}")
    print("=" * 55)


if __name__ == "__main__":
    main()
