# soccer-content-generator — dependency context
_updated: 2026-05-24T17:59:42.743421+00:00_
_nodes: 98_

## Clip_Pipeline
- **clip_config.py** (4.5 KB)
- **clip_parser.py** (11.5 KB) — internal: `clip_config`
- **clip_watcher.py** (30.8 KB) — internal: `clip_config`, `clip_parser`, `src.soccer_bot`
- **mcp_ingest.py** (34.7 KB) — internal: `src.agent.clip_name_parser`; external: `httpx`

## Data_Fetch
- **fixture_calendar.py** (36.1 KB) — external: `dotenv`, `requests`
- **src/api_data_fetcher.py** (9.2 KB) — external: `dotenv`, `requests`
- **src/football_api.py** (5.9 KB) — external: `requests`
- **src/football_api_client.py** (7.9 KB) — internal: `base_client`, `config`
- **src/match_data_fetcher.py** (28.0 KB) — external: `dotenv`, `requests`
- **src/news_api_client.py** (6.5 KB) — internal: `base_client`

## Infrastructure
- **dashboard_api.py** (81.4 KB) `[HEADER ONLY - read on demand]`
  - `class GenerateRequest(BaseModel)`
  - `def initialize_vector_store()`
  - `def get_db()`
  - `def load_content_queue()`
  - `def save_content_queue(queue)`
  - `async def startup_event()`
  - `async def health()`
  - `async def get_queue()`
  - `async def approve_queue_item(id)`
  - `async def reject_queue_item(id)`
  - `async def generate(req)`
  - `async def get_fixtures()`
  - `async def get_players()`
  - `async def get_stats()`
  - `async def generate(req)`
  - `class GenerateRequest(BaseModel)`
  - `def initialize_vector_store()`
  - `async def startup_event()`
  - `async def status()`
  - `async def generate(req)`
  - `def get_db()`
  - `def load_content_queue()`
  - `def save_content_queue(queue)`
  - `class GenerateRequest(BaseModel)`
  - `def health_check()`
  - `def get_fixtures(days, min_hype)`
  - `def get_queue(status, limit)`
  - `def approve_post(item_id)`
  - `def reject_post(item_id)`
  - `def get_stats()`
  - `def get_players()`
  - `def get_competitions()`
  - `def trigger_discovery()`
  - `async def generate_content(request)`
  - `def publish_post(item_id)`
  - `def _load_queue()`
  - `def _save_queue(queue)`
  - `def _find_post(queue, post_id)`
  - `def hub_status()`
  - `def get_assets()`
  - `def save_assets(payload)`
  - `def increment_asset_usage(asset_id)`
  - `def hub_queue()`
  - `def hub_approve(post_id)`
  - `def hub_reject(post_id)`
  - `class EditRequest(BaseModel)`
  - `def hub_edit(post_id, body)`
  - `class RateRequest(BaseModel)`
  - `def hub_rate(post_id, body)`
  - `def hub_send_telegram(post_id)`
  - `class HubGenerateRequest(BaseModel)`
  - `def hub_generate(body)`
  - `def hub_clip_status()`
  - `def hub_telegram_sync()`
- **database_manager.py** (9.1 KB) — external: `pandas`
- **lancedb_integrator.py** (14.9 KB) — external: `lancedb`, `pandas`, `sentence_transformers`
- **rebuild_lancedb.py** (20.0 KB) — internal: `vector_store`; external: `dotenv`, `lancedb`, `pandas`
- **src/database.py** (7.3 KB)
- **src/knowledge_manager.py** (8.4 KB) — internal: `vector_store`; external: `PyPDF2`
- **src/vector_store.py** (4.4 KB) — external: `lancedb`

## Intelligence
- **src/agent/knowledge_enricher.py** (7.3 KB)
- **src/agent/memory.py** (3.8 KB)
- **src/content_agent.py** (11.2 KB) — internal: `database`, `knowledge_manager`, `soccer_bot`
- **src/quality_agent.py** (15.7 KB) — internal: `database`, `knowledge_manager`
- **src/rag_pipeline.py** (7.0 KB) — external: `anthropic`, `dotenv`
- **src/research_agent.py** (10.4 KB) — internal: `api_data_fetcher`, `database`, `knowledge_manager`
- **src/soccer_bot.py** (32.6 KB) — external: `anthropic`, `dotenv`

## Media
- **generate_avatar.py** (12.7 KB) — internal: `avatar_character_profiles`; external: `dotenv`, `requests`
- **kling_agent.py** (16.9 KB) — external: `dotenv`, `requests`
- **src/card_composer.py** (25.4 KB) — external: `PIL`
- **src/image_agent.py** (36.5 KB) — internal: `src.card_composer`; external: `PIL`, `dotenv`, `requests`
- **src/media_agent.py** (43.9 KB) — external: `dotenv`, `requests`
- **src/video_generator.py** (10.9 KB) — external: `PIL`, `moviepy`

## Orchestration
- **bot_service.py** (11.9 KB) — external: `dotenv`
- **pipeline.py** (7.7 KB)
- **trigger_watcher.py** (14.6 KB)

## Output_Pipeline
- **converter.py** (20.3 KB)
- **export_pipeline.py** (13.3 KB)
- **mcp_book_compiler.py** (28.3 KB) — external: `anthropic`, `dotenv`
- **src/publishers/instagram_publisher.py** (5.9 KB) — internal: `src.formatters.platform_formatter`, `src.publishers.base_publisher`; external: `requests`
- **src/publishers/publisher_router.py** (10.1 KB) — internal: `src.publishers.base_publisher`
- **src/publishers/tiktok_publisher.py** (7.6 KB) — internal: `src.formatters.platform_formatter`, `src.publishers.base_publisher`; external: `requests`
- **src/publishers/youtube_publisher.py** (8.5 KB) — internal: `src.formatters.platform_formatter`, `src.publishers.base_publisher`
- **src/twitter_publisher.py** (13.8 KB) — external: `tweepy`
- **tts_local.py** (16.5 KB) — external: `dotenv`

## Scripts
- **scripts/cleanup_lancedb_duplicates.py** (1.0 KB) — external: `dotenv`, `lancedb`
- **scripts/database_exporter.py** (10.5 KB) — external: `pandas`
- **scripts/distill_session.py** (10.7 KB) — external: `anthropic`, `dotenv`
- **scripts/drive_cleanup.py** (7.0 KB) — internal: `drive_sync`
- **scripts/drive_sync.py** (19.8 KB)
- **scripts/graph_maintainer.py** (17.1 KB)
- **scripts/ingest_international_break.py** (7.1 KB) — internal: `vector_store`; external: `dotenv`
- **scripts/ingest_ucl_2026.py** (6.9 KB) — internal: `src.knowledge_manager`; external: `dotenv`
- **scripts/ingest_ucl_r16_second_legs.py** (5.4 KB) — internal: `vector_store`; external: `dotenv`
- **scripts/ingest_worldcup_2026.py** (3.7 KB) — internal: `knowledge_manager`; external: `dotenv`
- **scripts/knowledge_watcher.py** (3.1 KB) — internal: `vector_store`; external: `dotenv`

## UI_Entry
- **media_hub.py** (38.6 KB)
- **src/enhanced_terminal_ui.py** (55.4 KB) `[HEADER ONLY - read on demand]`
  - `class QueueStatus`
  - `def publish_post(post, twitter_publisher, youtube_publisher)`
  - `def get_platform_icon(post)`
  - `class ContentQueue`
  - `  def __init__(self, queue_path)`
  - `  def _load_queue(self)`
  - `  def _save_queue(self)`
  - `  def _save(self)`
  - `  def add(self, content, hashtags, content_type, topic, platform, media_path, video_path, title, cost)`
  - `  def get_by_id(self, post_id)`
  - `  def get_pending(self)`
  - `  def get_telegram_pending(self)`
  - `  def get_youtube_pending(self)`
  - `  def get_twitter_pending(self)`
  - `  def get_by_status(self, status)`
  - `  def approve(self, post_id)`
  - `  def edit_and_approve(self, post_id, new_content)`
  - `  def reject(self, post_id, reason)`
  - `  def mark_telegram_pending(self, post_id)`
  - `  def skip(self, post_id)`
  - `  def get_stats(self)`
  - `def clear_screen()`
  - `def print_header(title)`
  - `def print_divider()`
  - `def print_post_card(post, index, total)`
  - `def print_queue_summary(queue)`
  - `def run_review_queue(queue, twitter_publisher, youtube_publisher, filter_platform)`
  - `def sync_telegram_approvals(queue, twitter_publisher, youtube_publisher, approver)`
  - `def view_youtube_queue(queue, youtube_publisher)`
  - `def open_media_hub()`
  - `def print_content_type_menu()`
  - `def print_platform_menu()`
  - `def generate_single(queue, bot, media_agent)`
  - `def generate_batch(queue, bot, media_agent)`
  - `def view_avatar_library(media_agent)`
  - `def view_system_status(bot, media_agent, twitter_publisher, youtube_publisher)`
  - `def print_main_menu(queue)`
  - `def main()`

## uncategorized
- **avatar_character_profiles.py** (65.1 KB) `[HEADER ONLY - read on demand]`
- **bulk_player_generator.py** (11.0 KB)
- **check_queue.py** (1.8 KB)
- **conftest.py** (0.1 KB)
- **content_queue.py** (5.1 KB)
- **create_avatar_library.py** (21.2 KB) — external: `dotenv`, `requests`
- **diagnose_api.py** (4.5 KB) — external: `requests`
- **ingest_ucl_knowledge.py** (4.8 KB) — internal: `knowledge_manager`
- **obs_mcp.py** (7.4 KB) — external: `dotenv`, `fastapi`, `fastapi.middleware.cors`, `pydantic`, `simpleobsws`, `uvicorn`
- **obs_relay.py** (11.4 KB)
- **session_close.py** (4.5 KB)
- **soccer_knowledge_ingester.py** (0.0 KB)
- **src/__init__.py** (0.0 KB)
- **src/agent/__init__.py** (0.1 KB)
- **src/agent/clip_name_parser.py** (14.1 KB)
- **src/agent/pattern_detector.py** (6.4 KB)
- **src/agents/news_image_agent.py** (13.1 KB) — external: `bs4`, `requests`
- **src/base_client.py** (4.8 KB) — external: `requests`
- **src/competitions_api.py** (3.8 KB) — external: `requests`
- **src/config.py** (2.9 KB) — external: `dotenv`
- **src/cost_tracker.py** (5.9 KB)
- **src/data/__init__.py** (0.0 KB)
- **src/data/ingestion/__init__.py** (0.0 KB)
- **src/data/ingestion/schedule_manager.py** (9.7 KB)
- **src/data/ingestion/ucl_ingester.py** (7.5 KB)
- **src/date_injector.py** (1.1 KB)
- **src/formatters/__init__.py** (0.0 KB)
- **src/formatters/platform_formatter.py** (6.0 KB)
- **src/gallery_matcher.py** (1.9 KB)
- **src/knowledge_ui_component.py** (10.2 KB)
- **src/player_memory.py** (2.7 KB)
- **src/publishers/__init__.py** (0.0 KB)
- **src/publishers/base_publisher.py** (6.6 KB)
- **src/soccer_knowledge_ingester.py** (41.0 KB) — internal: `vector_store`; external: `pandas`
- **src/topic_router.py** (53.2 KB) `[HEADER ONLY - read on demand]`
  - `class RoutedQuery`
  - `class TopicRouter`
  - `  def __init__(self)`
  - `  def _get_match_fetcher(self)`
  - `  def _get_competitions_api(self)`
  - `  def route(self, topic, context, content_type)`
  - `  def _handle_team(self, result, team_name, content_type)`
  - `  def _handle_player(self, result, player_name, content_type)`
  - `  def _handle_competition(self, result, comp_name)`
  - `  def _detect_players(self, text)`
  - `  def _detect_teams(self, text)`
  - `  def _detect_competitions(self, text)`
- **src/ucl_bridge.py** (4.8 KB) — internal: `src.vector_store`
- **src/youtube_api_client.py** (8.1 KB) — internal: `base_client`, `config`
- **story_generator.py** (12.2 KB) — external: `anthropic`, `dotenv`
- **sync_brain.py** (19.4 KB)
- **telegram_approver.py** (20.8 KB) — external: `dotenv`, `telegram`
- **test_football_data_org.py** (4.3 KB) — external: `dotenv`, `requests`
- **test_football_data_org2.py** (3.2 KB) — external: `dotenv`, `requests`
- **test_ucl.py** (0.5 KB) — external: `dotenv`, `requests`
