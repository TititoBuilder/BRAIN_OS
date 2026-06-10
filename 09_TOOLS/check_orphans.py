import json, os
STAGING = r"C:\BRAIN_OS\audio_staging"
idx = json.load(open("drive_index.json", encoding="utf-8"))["index"]
mp3s = {f[:-4] for f in os.listdir(STAGING) if f.endswith(".mp3")}

orphans = ["2026-05-28_1417_bdf_ca_brain_os_audio", "cristianconstruction_audio",
           "knowledge_ingestion_protocol_v2_audio", "read_along_app_audio"]

for o in orphans:
    base = o[:-6]  # strip _audio
    print(f"\n{o}.mp3")
    print(f"  this name indexed?        {o in idx}")
    print(f"  base '{base}' indexed?    {base in idx}")
    print(f"  base '{base}'.mp3 exists? {base in mp3s}")
    # any index key that contains the base (catches naming variants)
    related = [k for k in idx if base.replace('_','') in k.replace('_','') or k.replace('_','') in base.replace('_','')]
    print(f"  related index keys:       {related[:5]}")
