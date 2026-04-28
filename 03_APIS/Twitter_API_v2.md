# API: Twitter API v2

## Purpose
Publishes approved BDF posts (text + media card) to the @BreakingDownFutbol Twitter account.

## Used by projects
- BDF

## Limits and rules
- Rate limits: `wait_on_rate_limit=True` set in tweepy Client; v1.1 media upload has its own tier
- Cost: $0 (included in current Twitter developer plan)
- Legal constraints:
  - No broadcast footage (DMCA) — video clips never attached to tweets
  - Self-imposed 200-char hard cap on tweet text (stricter than Twitter's 280); enforced in `create_tweet_text()`
  - Max 3 hashtags per post

## Credentials
- `TWITTER_BEARER_TOKEN`
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`

## Connected agents
- [[BDF_Automation_Agent]]

## Inputs
- Text string (≤200 chars, ≤3 hashtags) from `create_tweet_text()`
- Media: card image uploaded via tweepy API v1.1 `media_upload()`, media_id attached to v2 tweet
- Approval gate: post must be `telegram_pending → approved` before `twitter_publisher.py` fires

## Outputs
- Tweet ID returned on success; logged to content queue
- `twitter_publisher.py` wraps `tweepy.Client.create_tweet()` + `tweepy.API.media_upload()`
