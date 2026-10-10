"""Records the library stores."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class FeedSource:
    """A feed the reader subscribed to."""

    url: str
    title: str


@dataclass
class Entry:
    """One item of a feed."""

    entry_id: str
    feed_url: str
    title: str
    published_at: datetime
    read: bool = False
