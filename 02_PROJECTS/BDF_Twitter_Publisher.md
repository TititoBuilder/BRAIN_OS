---
tags: [bdf, pipeline, live]
updated: 2026-05-01
parent: "[[BDF_Soccer_Bot]]"
---

# BDF Twitter Publisher

This document covers how the BDF pipeline posts to Twitter/X, which credentials it requires, how the approval flow connects `telegram_approver.py` to `twitter_publisher.py`, and what rate-limit and formatting constraints are enforced.

---

## TwitterPublisher (src/twitter_publisher.py)

`TwitterPublisher` is the sole class responsible for all outbound Twitter operations in the BDF pipeline. It is instantiated on demand by `dashboard_api.py` (on approval) and by the background polling loop in `telegram_approver.py`. It is never run as a standalone service.

### Credentials

The class reads five environment variables from `.env` at initialisation. Key names only — values are never logged:

| Variable | Purpose |
|---|---|
| `TWITTER_BEARER_TOKEN` | OAuth 2.0 app-only bearer token — used by tweepy.Client (v2) |
| `TWITTER_API_KEY` | OAuth 1.0a consumer key — used by both Client and API |
| `TWITTER_API_SECRET` | OAuth 1.0a consumer secret |
| `TWITTER_ACCESS_TOKEN` | OAuth 1.0a user access token |
| `TWITTER_ACCESS_TOKEN_SECRET` | OAuth 1.0a user access token secret |

If any of the five values is missing, `_setup_client` prints a warning and leaves `self.client = None`. All publish methods check `self.client` first and return an error dict rather than raising.

### API Client Setup

Two tweepy objects are initialised. The `tweepy.Client` (API v2) handles tweet creation. The `tweepy.API` (API v1.1) handles media uploads — Twitter's v2 API does not support direct media upload, so images and videos go through the v1.1 endpoint before the tweet is posted. Both are configured with `wait_on_rate_limit=True`, which means the library blocks and retries rather than raising an exception when rate limits are hit.

### Text Formatting and Limits

`create_tweet_text` enforces a hard cap of 200 characters on all outgoing tweets (not the Twitter-maximum of 280). This is a deliberate editorial choice to leave room for images and to keep posts punchy. The method takes up to 3 hashtags, builds a hashtag string, calculates remaining space for the body, and applies `_trim_to_limit` which looks for the last sentence boundary within the available window. If no boundary is found it cuts at the last word boundary and appends an ellipsis. The final string is hard-capped at 200 characters in all cases.

### Publishing Methods

`publish_tweet(content, image_path)` is the standard method called by the approval flow. It accepts a content dict with keys `content`, `hashtags`, `title`, and optionally `image_path`. If an image path is provided and the file exists, it uploads the image using the v1.1 API and attaches the `media_id` to the tweet. Returns a result dict with `success`, `tweet_id`, `tweet_url`, `tweet_text`, `has_image`, and `published_at` on success, or `{"error": ...}` on failure.

`publish_video_tweet(caption, video_path)` handles MP4 uploads using chunked upload (`media_category="tweet_video"`, `chunked=True`). Twitter rejects single-part video uploads above a few MB, so the chunked path is mandatory for any real video clip. This method is called by `clip_watcher.py` and `mcp_ingest.py` when posting DaVinci exports.

`create_thread` splits long content into up to 5 tweets with `(1/n)` numbering, posting each as a reply to the previous.

### Known Issues

The `tweet_url` returned in the result uses the generic path `https://twitter.com/user/status/{tweet_id}` rather than the authenticated account's actual username because the account handle is not stored in the publisher. Links work when corrected manually.

---

## Telegram Approval Flow

The approval lifecycle for content destined for Twitter runs through two components: `telegram_approver.py` (the gating layer) and `twitter_publisher.py` (the execution layer).

### Send Phase

When a post is approved for Telegram review — either via the dashboard's "Send to Telegram" button or via the terminal UI's T-key — `TelegramApprover.send_for_review` fires a non-blocking message to the configured Telegram chat. The message includes the post title, platform, character count bar, body preview (capped at 600 chars), and hashtags. Three inline keyboard buttons are attached: `✅ APPROVE — Publish`, `❌ REJECT — Skip`, and `✏️ Edit & Requeue`. The callback data format is `action:post_id` (e.g. `approve:post_abc123def456`). The post's queue status is set to `telegram_pending`.

### Sync Phase

Telegram decisions are collected either by calling `sync_decisions()` (Option 8 in the terminal) or by the background polling loop started via `start_background_polling`. The background loop runs in a daemon thread with a 30-second sleep cycle, polling for new `callback_query` updates using a cursor (`_last_update_id`) that prevents double-processing.

A critical architecture constraint is that `self.bot` (a `telegram.Bot` instance) belongs to the main thread's event loop. The background thread creates its own `Bot` instance and its own `asyncio` event loop. Attempting to share `self.bot` across threads causes `RuntimeError: Event loop is closed` and connection pool exhaustion.

### Approval to Publish

When a decision of `approve` is received, the approver calls `queue.approve(post_id)` and then constructs a `post_dict` from the queue entry using `getattr` (not `dict.get`, because queue entries can be either dicts or class instances depending on the call path). It then calls `twitter_publisher.publish_tweet(post_dict)`. A failure in `publish_tweet` is caught and logged as a warning rather than propagated — the approval is already recorded and the post will not be lost.

---

## Dashboard Approval Flow

The React dashboard at `localhost:5173` approves posts via `POST /queue/{post_id}/approve` or `POST /queue/{post_id}/approve` (hub route). The hub approve endpoint:

1. Sets the post status to `approved` and saves the queue.
2. Attempts to run the card compositor (`compose_bdf_card`) using any available image.
3. Calls `TwitterPublisher().publish_tweet(post_dict, image_path=final_image_path)`.
4. Saves the `tweet_url` back to the queue entry if publishing succeeds.
5. Returns `{"success": True, "tweet_url": ...}`. Twitter errors are returned as warnings, not HTTP 500s, so the approval is never lost.

---

## Connected to

- [[BDF_Canvas]]
- [[Tools_Registry]]
- [[LanceDB_Vector_Store]]
