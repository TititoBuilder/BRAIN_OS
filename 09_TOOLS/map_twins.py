import json, os
STAGING = r"C:\BRAIN_OS\audio_staging"
idx = json.load(open("drive_index.json", encoding="utf-8"))["index"]

# find all *_audio.mp3 files and their non-audio twin
mp3s = [f for f in os.listdir(STAGING) if f.endswith(".mp3")]
keys_present = {f[:-4] for f in mp3s}  # strip .mp3

twins = []
for f in sorted(keys_present):
    if f.endswith("_audio"):
        base = f[:-6]  # strip _audio
        if base in keys_present:
            twins.append((base, f))  # (plain, _audio)

print(f"twin pairs found: {len(twins)}\n")
print(f"{'plain':32s} {'_audio':38s} INDEX REFERENCES")
print("-" * 95)
for base, audio in twins:
    in_base  = base  in idx
    in_audio = audio in idx
    if in_base and not in_audio:
        verdict = f"plain  (keep {base})  -> _audio is residue"
    elif in_audio and not in_base:
        verdict = f"_audio (keep {audio})  -> plain is residue"
    elif in_base and in_audio:
        verdict = "BOTH indexed (!) -- investigate"
    else:
        verdict = "NEITHER indexed -- both residue?"
    print(f"{base:32s} {audio:38s} {verdict}")
