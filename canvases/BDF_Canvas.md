## Image Pipeline

**Current architecture (as of 2026-04-30): DaVinci Resolve exports + card_[composer.py](http://composer.py)**

| Stage | Tool |
|---|---|
| Video/clip editing | DaVinci Resolve (Free license) |
| Still frame export | DaVinci render bridge via `resolve-mcp-server` (TCP 9000) |
| Card compositing | `card_[composer.py](http://composer.py)` + Pillow |
| Output | Branded image cards saved to `src/images/cards/` (gitignored) |

> ⚠️ **DEPRECATED:** `gpt-image-1` (OpenAI image generation) was the previous
> image source. It was replaced by DaVinci exports. Any reference to `gpt-image-1`
> in old documentation or the cheat sheet is stale — do not restore.

The `card_[composer.py](http://composer.py)` takes DaVinci-exported stills and applies branding
overlays, text, and layout. Pillow handles all compositing. No external image
API calls in the current pipeline.

---

## Google Drive Sync

Both the BDF and CA book compilers share a **single Google OAuth credential**
living inside the BDF project root.

| File | Path |
|---|---|
| OAuth client | `C:\Dev\Projects\soccer-content-generator\gdrive_credentials.json` |
| OAuth token | `C:\Dev\Projects\soccer-content-generator\gdrive_token.json` |

Both files are gitignored. **Never duplicate them** — one Google account,
one token, both compilers reference the BDF path directly.

**BDF sync target (Google Drive):**

| Content | Drive path |
|---|---|
| Chapter audio (.mp3) | `BDF_Book_Audio\chapters\` |
| Session audio | `BDF_Book_Audio\` |

**CA sync target (Google Drive):**

| Content | Drive path |
|---|---|
| Chapter audio (.wav) | `CA_Book_Audio\chapters\` |
| Master book (.txt) | `CA_Book_Audio\CA_Master_Book.txt` |

CA sync fires automatically on every `ca-book` run.
For bulk CA re-sync (after major expansion): run `ca_bulk_[upload.py](http://upload.py)` from
`C:\Users\titit\Downloads\` using the BDF venv.

**Token refresh (applies to both compilers):**

```powershell
cd C:\Dev\Projects\soccer-content-generator
Remove-Item gdrive_token.json
python -c "import book_compiler; book_compiler.get_drive_service()"
# Browser opens → approve → token refreshed
```

---

## Connected to
