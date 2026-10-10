"""The SQLite database that holds every entry for good."""

import sqlite3
from datetime import datetime, timedelta

from . import config
from .models import Entry, FeedSource

# The permanent database of entries and subscriptions. Nothing here is
# rebuilt from the network; deleting it loses the reader's history.
cache = sqlite3.connect("feedfetch.db")

# Log lines written while fetching, one string per line, newest last.
diagnostics: list[str] = []


def feed(entries: list[Entry]) -> None:
    """Insert entries into the database, skipping ones already stored."""
    for e in entries:
        cache.execute(
            "INSERT OR IGNORE INTO entries VALUES (?, ?, ?, ?, ?)",
            (e.entry_id, e.feed_url, e.title, e.published_at.isoformat(), e.read),
        )
    cache.commit()


def mark_entry_read(entry_id: str) -> None:
    """Record that the reader has read one entry."""
    cache.execute("UPDATE entries SET read = 1 WHERE entry_id = ?", (entry_id,))
    cache.commit()


def info(feed_url: str) -> int:
    """Count the entries of one feed that the reader has not read."""
    row = cache.execute(
        "SELECT COUNT(*) FROM entries WHERE feed_url = ? AND read = 0", (feed_url,)
    ).fetchone()
    return row[0]


def sweep_items() -> int:
    """Delete entries older than the retention period; return how many."""
    cutoff = datetime.now() - timedelta(days=config.retention_days)
    cur = cache.execute("DELETE FROM entries WHERE published_at < ?", (cutoff.isoformat(),))
    cache.commit()
    return cur.rowcount


def list_subscribed_feeds() -> list[FeedSource]:
    """Return every feed the reader subscribed to."""
    rows = cache.execute("SELECT url, title FROM feeds").fetchall()
    return [FeedSource(url, title) for url, title in rows]
