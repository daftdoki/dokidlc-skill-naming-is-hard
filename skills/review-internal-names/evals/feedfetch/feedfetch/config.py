"""Settings the library reads at start-up."""

USER_AGENT = "feedfetch/0.4 (+https://example.org/feedfetch)"

# Seconds to wait for a feed server before giving up.
http_timeout_seconds = 20

# Entries older than this many days are deleted by the cleanup job.
retention_days = 90

# The most entries kept for one feed; older ones are dropped first.
MAX = 50
