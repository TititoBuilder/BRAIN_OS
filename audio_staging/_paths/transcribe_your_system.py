import json, whisper, torch

MP3 = r"C:\BRAIN_OS\audio_staging\_paths\your_system.mp3"
OUT = r"C:\BRAIN_OS\audio_staging\_paths\your_system.json"
KEY = "your_system"

print("CUDA available:", torch.cuda.is_available())
print("loading model...")
model = whisper.load_model("base", device="cuda" if torch.cuda.is_available() else "cpu")

print("transcribing (word timestamps)...")
result = model.transcribe(MP3, word_timestamps=True, verbose=False)

# Flatten word-level timestamps from segments into a flat words[] list,
# matching the format the existing path transcripts + app karaoke expect.
words = []
for seg in result.get("segments", []):
    for w in seg.get("words", []):
        words.append({
            "word": w["word"].strip(),
            "start": round(w["start"], 2),
            "end": round(w["end"], 2),
        })

out = {
    "machine_key": KEY,
    "language": result.get("language", "en"),
    "duration": round(words[-1]["end"], 2) if words else 0,
    "text": result.get("text", "").strip(),
    "words": words,
}

open(OUT, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=2))
print("DONE. words:", len(words), "duration:", out["duration"], "s")
print("saved:", OUT)
