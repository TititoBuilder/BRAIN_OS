# INGESTION COMMANDS — BDF Session Compiles
# Execute from Claude Code in C:\BRAIN_OS
# Date: 2026-05-05

# ============================================================
# STEP 1: Copy compile files to BRAIN_OS/10_CHATS/
# ============================================================
# Run these from Win+X Terminal (PowerShell), NOT Claude Code terminal

# Copy all 5 compiles to BRAIN_OS
Copy-Item "C:\[SOURCE_PATH]\20260318_session_compile.md" "C:\BRAIN_OS\10_CHATS\"
Copy-Item "C:\[SOURCE_PATH]\20260315_session_compile_style_transfer.md" "C:\BRAIN_OS\10_CHATS\"
Copy-Item "C:\[SOURCE_PATH]\20260401_session_compile.md" "C:\BRAIN_OS\10_CHATS\"
Copy-Item "C:\[SOURCE_PATH]\20260315_session_compile_twitter.md" "C:\BRAIN_OS\10_CHATS\"
Copy-Item "C:\[SOURCE_PATH]\20260315_session_compile_story_kling.md" "C:\BRAIN_OS\10_CHATS\"

# ============================================================
# STEP 2: Append Avatar Pipeline patch
# ============================================================
# This appends all new sections to existing BDF_Avatar_Pipeline.md
Get-Content "C:\[SOURCE_PATH]\BDF_Avatar_Pipeline_PATCH.md" | Add-Content "C:\BRAIN_OS\04_WORKFLOWS\BDF_Avatar_Pipeline.md"

# ============================================================
# STEP 3: Git commit
# ============================================================
cd C:\BRAIN_OS
git add .
git commit -m "feat: ingest 5 BDF session compiles Feb-April 2026

- 20260318: age scale system, gpt-image-1, GPT-4o fixes, generate_psg5.py
- 20260315 (style): gpt-image-1 migration + character sheet factory
- 20260315 (twitter): Twitter API v2 integration + dashboard
- 20260315 (kling): story generator + Kling animation + avatar decisions
- 20260401: Telegram 3-bug fix + asyncio architectural rule
- BDF_Avatar_Pipeline.md: patched with all missing systems"

# ============================================================
# STEP 4: Verify
# ============================================================
git log --oneline -5
Get-Content "C:\BRAIN_OS\04_WORKFLOWS\BDF_Avatar_Pipeline.md" | Select-String "gpt-image-1|age scale|T-pose"
