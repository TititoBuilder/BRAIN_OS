"""
claude_monitor.py — Real-time Claude API Cost Monitor
======================================================
Pulls live usage data from the Anthropic Admin API and surfaces
spend by model, daily burn rate, projected month-end cost, and
threshold alerts — all before the invoice surprises you.

Setup
-----
    pip install anthropic python-dotenv rich requests

    # .env
    ANTHROPIC_ADMIN_KEY=sk-ant-admin-...   # from console.anthropic.com → API Keys (Admin)
    DAILY_BUDGET_USD=5.00                  # alert when daily spend exceeds this
    MONTHLY_BUDGET_USD=80.00              # alert when monthly projection exceeds this

    # Telegram alert settings
    TELEGRAM_BOT_TOKEN=your-bot-token
    TELEGRAM_CHAT_ID=your-chat-id

Run once:
    python claude_monitor.py

Run on a schedule (cron — every hour):
    0 * * * * /path/to/venv/bin/python /path/to/claude_monitor.py >> /var/log/claude_monitor.log 2>&1
"""

from __future__ import annotations

import os
import sys
import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import TypedDict

import anthropic
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Try importing rich for terminal output; fall back to plain print gracefully
# ---------------------------------------------------------------------------
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    RICH = True
    console = Console()
except ImportError:
    RICH = False
    console = None  # type: ignore

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ADMIN_KEY: str        = os.getenv("ANTHROPIC_ADMIN_KEY", "")
DAILY_BUDGET: float   = float(os.getenv("DAILY_BUDGET_USD", "5.00"))
MONTHLY_BUDGET: float = float(os.getenv("MONTHLY_BUDGET_USD", "80.00"))
LOG_DIR = Path(os.getenv("LOG_DIR", str(Path.home() / ".claude_monitor")))
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Notification: uses existing Telegram bot from soccer-content-generator
# TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID — same vars, no new bot needed

logging.basicConfig(
    filename=str(LOG_DIR / "monitor.log"),
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Pricing table — update when Anthropic changes rates
# Source: https://anthropic.com/pricing
# ---------------------------------------------------------------------------
MODEL_PRICING: dict[str, dict[str, float]] = {
    "claude-sonnet-4-6":       {"input": 3.00,  "output": 15.00},
    "claude-sonnet-4":         {"input": 3.00,  "output": 15.00},
    "claude-haiku-4-5":        {"input": 0.80,  "output": 4.00},
    # Fallback for unrecognised models
    "__default__":             {"input": 3.00,  "output": 15.00},
}


def price_per_million(model: str) -> dict[str, float]:
    for key in MODEL_PRICING:
        if key in model:
            return MODEL_PRICING[key]
    return MODEL_PRICING["__default__"]


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------
class ModelStats(TypedDict):
    input_tokens: int
    output_tokens: int
    requests: int
    cost_usd: float


# ---------------------------------------------------------------------------
# Core: parse usage from Anthropic console CSV export
# ---------------------------------------------------------------------------
CSV_PATH = Path(os.getenv(
    "ANTHROPIC_CSV",
    str(Path.home() / "Downloads" / "anthropic_usage.csv")
))


def load_csv(path: Path, start: datetime, end: datetime) -> dict[str, ModelStats]:
    """
    Parses the CSV exported from console.anthropic.com → Cost → Export.

    Actual Anthropic CSV schema (confirmed):
        usage_date_utc, model, workspace, api_key, usage_type,
        context_window, token_type, cost_usd, list_price_usd,
        cost_type, inference_geo, speed

    Each row = one token_type entry (input_no_cache / output / etc.)
    with cost_usd already calculated by Anthropic.
    """
    import csv

    stats: dict[str, ModelStats] = {}

    if not path.exists():
        raise FileNotFoundError(
            f"CSV not found at {path}\n"
            f"  Go to console.anthropic.com > Cost > Export\n"
            f"  Save the file to: {path}\n"
            f"  Or set ANTHROPIC_CSV=/your/path/anthropic_usage.csv in .env"
        )

    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Date column is usage_date_utc in format YYYY-MM-DD
            raw_date = row.get("usage_date_utc", "").strip()
            try:
                row_dt = datetime.strptime(raw_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except ValueError:
                continue

            if not (start <= row_dt <= end):
                continue

            model      = row.get("model",      "unknown").strip()
            token_type = row.get("token_type", "").strip()       # input_no_cache / output / etc.
            api_key    = row.get("api_key",    "unknown").strip() # which integration called it

            try:
                cost = float(row.get("cost_usd", 0) or 0)
            except ValueError:
                cost = 0.0

            if model not in stats:
                stats[model] = ModelStats(
                    input_tokens=0, output_tokens=0, requests=0, cost_usd=0.0
                )

            # Accumulate tokens by type — Anthropic doesn't give raw token
            # counts in this export, only cost. We track rows as a proxy.
            if "input" in token_type:
                stats[model]["input_tokens"]  += 1  # row count proxy
            elif "output" in token_type:
                stats[model]["output_tokens"] += 1  # row count proxy

            stats[model]["requests"]  += 1
            stats[model]["cost_usd"]  += cost

    return stats


def fetch_usage(start: datetime, end: datetime) -> dict[str, ModelStats]:
    """
    Reads usage from the exported CSV.
    Download a fresh export from console.anthropic.com whenever you need updated numbers.
    """
    return load_csv(CSV_PATH, start, end)
# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------
def compute_summary(stats: dict[str, ModelStats], today_stats: dict[str, ModelStats]) -> dict:
    total_monthly  = sum(m["cost_usd"] for m in stats.values())
    total_today    = sum(m["cost_usd"] for m in today_stats.values())
    total_tokens   = sum(m["input_tokens"] + m["output_tokens"] for m in stats.values())

    now = datetime.now(timezone.utc)
    days_elapsed   = now.day
    days_in_month  = 30  # conservative
    projected_monthly = (total_monthly / days_elapsed) * days_in_month if days_elapsed else 0

    # Which model is the biggest spender?
    top_model = max(stats, key=lambda m: stats[m]["cost_usd"], default="none")

    return {
        "total_monthly":        round(total_monthly, 4),
        "total_today":          round(total_today, 4),
        "total_tokens":         total_tokens,
        "projected_monthly":    round(projected_monthly, 2),
        "days_elapsed":         days_elapsed,
        "top_model":            top_model,
        "daily_budget":         DAILY_BUDGET,
        "monthly_budget":       MONTHLY_BUDGET,
        "daily_over_budget":    total_today   >= DAILY_BUDGET,
        "monthly_over_budget":  projected_monthly >= MONTHLY_BUDGET,
    }


# ---------------------------------------------------------------------------
# Output: rich table (pretty terminal) or plain text (log / CI)
# ---------------------------------------------------------------------------
def render_rich(
    stats: dict[str, ModelStats],
    summary: dict,
    period_label: str,
) -> None:
    assert RICH and console

    # ── Header panel ──────────────────────────────────────────────────────
    status_color = "red" if summary["monthly_over_budget"] else \
                   "yellow" if summary["daily_over_budget"] else "green"
    header = Text()
    header.append("Claude Cost Monitor  ", style="bold")
    header.append(f"({period_label})", style="dim")
    console.print(Panel(header, border_style=status_color, padding=(0, 1)))

    # ── Summary cards ─────────────────────────────────────────────────────
    console.print()
    console.print(
        f"  [bold]Monthly total[/bold]   ${summary['total_monthly']:.4f}   "
        f"[dim]Projected: ${summary['projected_monthly']:.2f} / ${MONTHLY_BUDGET:.2f}[/dim]"
    )
    daily_flag = " [bold red]⚠ OVER BUDGET[/bold red]" if summary["daily_over_budget"] else ""
    console.print(
        f"  [bold]Today's spend[/bold]   ${summary['total_today']:.4f}"
        f"  [dim]Budget: ${DAILY_BUDGET:.2f}[/dim]{daily_flag}"
    )
    console.print(
        f"  [bold]Tokens consumed[/bold] {summary['total_tokens']:,}"
    )
    console.print()

    # ── Per-model breakdown table ─────────────────────────────────────────
    table = Table(
        box=box.SIMPLE_HEAD,
        show_header=True,
        header_style="bold",
        min_width=80,
    )
    table.add_column("Model",          style="cyan",  no_wrap=True)
    table.add_column("Requests",       justify="right")
    table.add_column("Input (M tok)",  justify="right")
    table.add_column("Output (M tok)", justify="right")
    table.add_column("Cost (USD)",     justify="right", style="yellow")
    table.add_column("% of total",     justify="right")

    total_cost = summary["total_monthly"] or 1  # avoid div/0

    for model, m in sorted(stats.items(), key=lambda x: -x[1]["cost_usd"]):
        pct = (m["cost_usd"] / total_cost) * 100
        table.add_row(
            model,
            f"{m['requests']:,}",
            f"{m['input_tokens']  / 1_000_000:.3f}",
            f"{m['output_tokens'] / 1_000_000:.3f}",
            f"${m['cost_usd']:.4f}",
            f"{pct:.1f}%",
        )

    console.print(table)

    # ── Alerts ────────────────────────────────────────────────────────────
    if summary["daily_over_budget"]:
        console.print(
            f"  [bold red]ALERT[/bold red] Daily spend ${summary['total_today']:.2f} "
            f"exceeds budget ${DAILY_BUDGET:.2f}"
        )
    if summary["monthly_over_budget"]:
        console.print(
            f"  [bold red]ALERT[/bold red] Projected month-end "
            f"${summary['projected_monthly']:.2f} exceeds budget ${MONTHLY_BUDGET:.2f}"
        )

    console.print()


def render_plain(stats: dict[str, ModelStats], summary: dict, period_label: str) -> None:
    sep = "-" * 70
    print(f"\n{sep}")
    print(f"  Claude Cost Monitor  ({period_label})")
    print(sep)
    print(f"  Monthly total   : ${summary['total_monthly']:.4f}")
    print(f"  Today spend     : ${summary['total_today']:.4f}  (budget: ${DAILY_BUDGET:.2f})")
    print(f"  Projected MTD   : ${summary['projected_monthly']:.2f}  (budget: ${MONTHLY_BUDGET:.2f})")
    print(f"  Tokens consumed : {summary['total_tokens']:,}")
    print(sep)
    print(f"  {'Model':<30} {'Requests':>10} {'Cost':>12} {'%':>8}")
    print(f"  {'-'*30} {'-'*10} {'-'*12} {'-'*8}")
    total_cost = summary["total_monthly"] or 1
    for model, m in sorted(stats.items(), key=lambda x: -x[1]["cost_usd"]):
        pct = (m["cost_usd"] / total_cost) * 100
        print(f"  {model:<30} {m['requests']:>10,} ${m['cost_usd']:>10.4f} {pct:>7.1f}%")
    if summary["daily_over_budget"]:
        print(f"\n  !! ALERT: daily spend ${summary['total_today']:.2f} > budget ${DAILY_BUDGET:.2f}")
    if summary["monthly_over_budget"]:
        print(f"  !! ALERT: projected ${summary['projected_monthly']:.2f} > budget ${MONTHLY_BUDGET:.2f}")
    print(sep + "\n")


# ---------------------------------------------------------------------------
# Persistence — log snapshot to JSON for trend tracking
# ---------------------------------------------------------------------------
def save_snapshot(summary: dict, stats: dict[str, ModelStats]) -> None:
    snapshot_file = LOG_DIR / "snapshots.jsonl"
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "models": {
            model: dict(m) for model, m in stats.items()
        },
    }
    with snapshot_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


# ---------------------------------------------------------------------------
# Alerts via Telegram — same bot already used by clip_watcher.py
# Uses TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID from .env (no new credentials)
# ---------------------------------------------------------------------------
def send_alert(subject: str, body: str) -> None:
    """
    Sends a Telegram message using the existing soccer bot credentials.
    Silently skips if TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID are not set.
    """
    token   = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        log.warning("Telegram not configured — set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")
        return

    import urllib.request
    import urllib.error

    url  = f"https://api.telegram.org/bot{token}/sendMessage"
    text = f"*{subject}*\n\n{body}"
    data = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}).encode()

    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                print("[ALERT SENT] Telegram")
                log.info("Telegram alert sent to chat_id: %s", chat_id)
    except urllib.error.URLError as exc:
        log.warning("Telegram alert failed: %s", exc)
        print(f"[ALERT ERROR] {exc}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    now   = datetime.now(timezone.utc)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    month_start = today.replace(day=1)

    log.info("Fetching monthly usage (%s – %s)", month_start.date(), now.date())

    try:
        monthly_stats = fetch_usage(start=month_start, end=now)
        today_stats   = fetch_usage(start=today,       end=now)
    except EnvironmentError as exc:
        print(f"[CONFIG ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        log.error("Usage fetch failed: %s", exc)
        print(f"[API ERROR] {exc}", file=sys.stderr)
        sys.exit(1)

    summary = compute_summary(monthly_stats, today_stats)
    period  = f"{month_start.strftime('%b %d')} – {now.strftime('%b %d, %Y')}"

    if RICH:
        render_rich(monthly_stats, summary, period)
    else:
        render_plain(monthly_stats, summary, period)

    save_snapshot(summary, monthly_stats)
    log.info(
        "Snapshot saved — monthly $%.4f, today $%.4f, projected $%.2f",
        summary["total_monthly"],
        summary["total_today"],
        summary["projected_monthly"],
    )

    # Send Telegram alert if any threshold is breached
    alerts = []
    if summary["daily_over_budget"]:
        alerts.append(
            f"DAILY BUDGET EXCEEDED\n"
            f"  Spent today : ${summary['total_today']:.2f}\n"
            f"  Daily limit : ${DAILY_BUDGET:.2f}\n"
            f"  Top model   : {summary['top_model']}"
        )
    if summary["monthly_over_budget"]:
        alerts.append(
            f"MONTH-END PROJECTION OVER BUDGET\n"
            f"  Projected   : ${summary['projected_monthly']:.2f}\n"
            f"  Monthly cap : ${MONTHLY_BUDGET:.2f}\n"
            f"  Days elapsed: {summary['days_elapsed']}"
        )
    if alerts:
        body = "\n\n".join(alerts) + f"\n\nFull monthly spend: ${summary['total_monthly']:.4f}"
        subject = f"Claude Budget Alert — ${summary['total_today']:.2f} today"
        send_alert(subject, body)


if __name__ == "__main__":
    main()
