# API: Football Data APIs

## Purpose
Fetches live match results, standings, squad data, and competition fixtures for BDF content generation.

## Used by projects
- BDF

## Limits and rules
- Rate limits:
  - football-data.org: 10 requests/min (free tier)
  - TheSportsDB / api-football: ~30 requests/min
- Cost: $0 (free tiers used; monitored in cost_tracker.py)
- Legal constraints: 100 calls/day hard cap (self-imposed across all football API clients)

## Credentials
- `FOOTBALL_DATA_API_KEY` — sent as header `X-Auth-Token` (football-data.org)
- `API_FOOTBALL_KEY` — TheSportsDB / api-football

## Connected agents
- [[BDF_Research_Agent]]

## Inputs

**football-data.org:**
- BASE_URL: `https://api.football-data.org/v4`
- UCL competition ID: `2001`
- Endpoints used: `/competitions/{id}/matches`, `/competitions/{id}/standings`, `/teams/{id}`

**TheSportsDB / api-football:**
- BASE_URL: `https://www.thesportsdb.com/api/v1/json`
- UCL competition ID: `2` (api-football), `2001` (football-data.org)
- Endpoints used: `/v1/json/1/eventsseason.php`, `/v1/json/1/searchteams.php`

## Outputs
- Match objects: score, date, teams, competition name
- Standings: position, points, GD per team
- Consumed by schedule_manager.py to determine ContentWindow and topic priority
