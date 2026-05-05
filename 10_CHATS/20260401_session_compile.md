# SESSION COMPILE — April 1, 2026
**Project:** BreakingDown Futbol (BDF)
**Type:** Bug Fix + Feature Planning
**Machine:** Predator (C:\Dev\Projects\soccer-content-generator)
**Compiled:** 2026-05-05
**Status:** Ready for ingestion

---

## WHAT WAS BUILT

### Problem Solved
Telegram APPROVE/REJECT buttons were tapping but zero posts published to Twitter.
Posts piling up in Telegram with no action taken. Root: 3 compounding bugs in
`src/telegram_approver.py`.

### Milestone Achieved
Pipeline confirmed live end-to-end:
`Telegram tap → background thread (within 5s) → Twitter publish`
- Terminal: `INFO:telegram_approver: Auto-published post post_1722547007_32`
- Twitter @tititoluli1987: went from 6 → 10 posts this session

### New Scripts
- `experiment1_pixabay.py` — tests 5 soccer search terms, downloads top 3 images per term to `test_results/experiment1/`
- `experiment2_news_images.py` — scrapes `og:image` from ESPN, Sky Sports, BBC Sport, Goal.com for Mbappe / Haaland / Yamal / Real Madrid vs Man City

---

## KEY DECISIONS

| Decision | Detail |
|---|---|
| Architectural rule | ONE THREAD = ONE EVENT LOOP = ONE BOT INSTANCE |
| Image pipeline strategy | 5 sources: Pixabay, Unsplash, NewsImageAgent, DALL-E 3, Kling AI |
| Visual review workflow | Two-stage: terminal preview + Telegram approval |
| Next experiments | Run experiment1 + experiment2 → results → design real pipeline |

---

## TECHNICAL KNOWLEDGE

### Bug 1 — `.get()` on class instance
```python
# WRONG — Post objects are not dicts, .get() raises AttributeError silently
post.get("platform")

# CORRECT
getattr(post, "platform", None)
```

### Bug 2 — Shared bot across threads (event loop collision)
```python
# WRONG — self.bot belongs to main thread's event loop
# Background thread using it: RuntimeError: Event loop is closed

# CORRECT — Create fresh bot inside thread
def start_background_polling(self):
    def thread_worker():
        thread_bot = TelegramBot(token=self.token)  # ← fresh instance
        asyncio.run(self._async_sync_on_bot(thread_bot))
    threading.Thread(target=thread_worker).start()
```

### Bug 3 — Connection pool exhaustion (consequence of Bug 2)
- Failed requests didn't release connections
- Pool filled with dead connections — every new request timed out
- **Fix:** Resolved automatically once Bug 2 was fixed

### Architectural Rule (proven)
```
ONE THREAD = ONE EVENT LOOP = ONE BOT INSTANCE
Never share asyncio objects across threads.
```

### Files Modified
- `src/telegram_approver.py` — complete rewrite, 3 fixes, full comments
  - `start_background_polling`: creates `thread_bot` inside thread
  - `_async_sync`: simplified wrapper calling `_async_sync_on_bot(self.bot)`
  - `_async_sync_on_bot`: new method, accepts `bot` param, thread-safe
  - approve handler: `getattr()` replaces `.get()`, removed platform filter
  - Added `success/reject/edit` logger.info lines for terminal confirmation

### Install Required
```powershell
pip install beautifulsoup4 pillow --break-system-packages
```

---

## PENDING (from this session)
1. Run `experiment1_pixabay.py` — judge image quality
2. Run `experiment2_news_images.py` — judge player photo relevance
3. Report results → design real image selection pipeline
4. Experiment 3: DALL-E 3 style test
5. Experiment 4: full waterfall composite test

---

## BRAIN_OS ROUTING

| Knowledge | Target File | Action |
|---|---|---|
| Telegram 3-bug fix + root causes | `02_PROJECTS/BDF_Agent_Pipeline.md` | ADD — bug fix record |
| ONE THREAD = ONE EVENT LOOP rule | `02_PROJECTS/BDF_Agent_Pipeline.md` | ADD — architectural rule |
| `getattr()` vs `.get()` on class instances | `02_PROJECTS/BDF_Agent_Pipeline.md` | ADD — Python pattern |
| Thread-safe bot pattern | `02_PROJECTS/BDF_Agent_Pipeline.md` | ADD — code pattern |
| Image pipeline 5-source strategy | `04_WORKFLOWS/BDF_Social_Media_Flow.md` | ADD — new section |
| experiment1 + experiment2 scripts | `04_WORKFLOWS/BDF_Social_Media_Flow.md` | ADD — scripts reference |
| Pipeline milestone (6→10 tweets confirmed) | `02_PROJECTS/BDF_Canvas.md` | ADD — milestone log |
