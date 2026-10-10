"""Download feeds and turn them into entries."""

import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urlsplit, urlunsplit

from . import config, store
from .models import Entry


def normalize_feed_url(url: str) -> str:
    """Lower-case the scheme and host and drop a trailing slash."""
    parts = urlsplit(url.strip())
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))


def fetch_feed(url: str) -> bytes:
    """Download one feed's XML."""
    req = urllib.request.Request(url, headers={"User-Agent": config.USER_AGENT})
    with urllib.request.urlopen(req, timeout=config.http_timeout_seconds) as resp:
        return resp.read()


def handle_data(url: str, xml: bytes) -> list[Entry]:
    """Parse a feed's XML into entries, newest first."""
    root = ET.fromstring(xml)
    data2 = []
    for item in root.iter("item"):
        data2.append(
            Entry(
                entry_id=item.findtext("guid") or item.findtext("link"),
                feed_url=url,
                title=item.findtext("title") or "",
                published_at=datetime.fromisoformat(item.findtext("pubDate")),
            )
        )
    data2.sort(key=lambda e: e.published_at, reverse=True)
    return data2[: config.MAX]


class FeedManager:
    """Fetches subscribed feeds over HTTP and stores what they hold."""

    def refresh(self, url: str, purge: bool = False) -> None:
        """Fetch a feed and store its new entries.

        With purge=True it fetches nothing: it deletes every stored entry
        of the feed instead.
        """
        url = normalize_feed_url(url)
        if purge:
            store.cache.execute("DELETE FROM entries WHERE feed_url = ?", (url,))
            store.cache.commit()
            return
        try:
            store.feed(handle_data(url, fetch_feed(url)))
        except OSError as err:
            store.diagnostics.append(f"{url}: {err}")
