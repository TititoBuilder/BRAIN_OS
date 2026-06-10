import os
files = {
    "kokoro_tts":     r"02_AGENTS\CA_Kokoro_TTS.md",
    "message_queues": r"00_DASHBOARD\Queue.md",
}
for key, rel in files.items():
    p = os.path.join(r"C:\BRAIN_OS", rel)
    txt = open(p, encoding="utf-8").read()
    has_key = f"knowledge_os_machine_key: {key}" in txt
    # body = content after frontmatter (after second ---)
    parts = txt.split("---", 2)
    body = parts[2] if len(parts) > 2 else txt
    print(f"=== {key}  ({rel}) ===")
    print("  declares this machine_key in frontmatter:", has_key)
    print("  total length:", len(txt), "| body length:", len(body.strip()))
    print("  body preview:", body.strip()[:200].replace(chr(10), " "))
    print()
