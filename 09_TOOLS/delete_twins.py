import json, os
STAGING = r"C:\BRAIN_OS\audio_staging"
idx = json.load(open("drive_index.json", encoding="utf-8"))["index"]
mp3s = {f[:-4] for f in os.listdir(STAGING) if f.endswith(".mp3")}

deleted, skipped = [], []
for f in sorted(mp3s):
    if f.endswith("_audio"):
        base = f[:-6]
        if base in mp3s and f not in idx and base in idx:
            for ext in (".mp3", ".json"):
                p = os.path.join(STAGING, f + ext)
                if os.path.exists(p):
                    os.remove(p)
                    deleted.append(os.path.basename(p))

print(f"deleted: {len(deleted)} files")
# verify: no _audio twins remain that should be gone
remaining = [f for f in os.listdir(STAGING) if f.endswith("_audio.mp3")]
print(f"_audio.mp3 files still in staging: {len(remaining)}")
if remaining:
    for r in remaining: print("   still present:", r)
# sanity: confirm a few plain twins still exist (we kept them)
for k in ["master_control", "cristian_principles", "trigger_architecture"]:
    print(f"  kept {k}.mp3:", os.path.exists(os.path.join(STAGING, k + ".mp3")))
