import json, os
STAGING = r"C:\BRAIN_OS\audio_staging"
idx = json.load(open("drive_index.json", encoding="utf-8"))["index"]
mp3s = {f[:-4] for f in os.listdir(STAGING) if f.endswith(".mp3")}

to_delete = []
for f in sorted(mp3s):
    if f.endswith("_audio"):
        base = f[:-6]
        if base in mp3s and f not in idx and base in idx:
            for ext in (".mp3", ".json"):
                p = os.path.join(STAGING, f + ext)
                if os.path.exists(p):
                    to_delete.append(p)

print(f"files that WOULD be deleted: {len(to_delete)}")
for p in to_delete:
    print("  ", os.path.basename(p))
print("\nDRY RUN -- nothing deleted. Review, then we execute.")
