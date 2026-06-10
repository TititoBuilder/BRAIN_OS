import json, os

keys = ["davinci_resolve_mcp", "resolve_mcp_server",
        "resolve_editing_agent", "model_context_protocol"]
base = r"C:\BRAIN_OS\audio_staging"

texts = {}
for k in keys:
    path = os.path.join(base, k + ".json")
    if not os.path.exists(path):
        print(f"[MISSING] {k}.json not in audio_staging")
        continue
    t = json.load(open(path, encoding="utf-8")).get("text", "")
    texts[k] = t.strip()
    print(f"\n=== {k}  (len {len(t)}) ===")
    print(t[:260])

print("\n--- pairwise check ---")
ks = list(texts.keys())
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        a, b = texts[ks[i]], texts[ks[j]]
        shared = len(os.path.commonprefix([a, b]))
        flag = "  <-- HIGH OVERLAP" if shared > 150 else ""
        print(f"{ks[i]} vs {ks[j]}: identical={a==b}, shared_prefix={shared}{flag}")
