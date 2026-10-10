"""Every command, flag, and setting a pgtend user types."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pgtend", description="Day-to-day PostgreSQL administration.")
    sub = p.add_subparsers(dest="command", required=True)

    vac = sub.add_parser("vacuum-table", help="Run VACUUM on one table.")
    vac.add_argument("table")
    vac.add_argument("--analyze", action="store_true",
                     help="Also update the planner statistics (VACUUM ANALYZE).")

    rei = sub.add_parser("reindex-table", help="Rebuild every index of one table.")
    rei.add_argument("table")
    rei.add_argument("--concurrently", action="store_true",
                     help="Rebuild without locking out writes (REINDEX CONCURRENTLY).")

    sub.add_parser("promote-replica", help="Turn this standby into the primary (pg_promote).")

    bloat = sub.add_parser("estimate-table-bloat",
                           help="Work out how much dead space each table holds, from pg_stats.")
    bloat.add_argument("--min-mb", type=int, default=0)

    sub.add_parser("list-blocking-locks", help="Print each lock that makes another backend wait.")

    term = sub.add_parser("terminate-backend", help="End one backend (pg_terminate_backend).")
    term.add_argument("pid", type=int)

    sub.add_parser("tidy-database", help="Run VACUUM on every table of the database.")

    snap = sub.add_parser("snapshot", help="Write a logical backup of the database with pg_dump.")
    snap.add_argument("file")
    snap.add_argument("--fast", action="store_true",
                      help="Leave large objects out of the dump.")

    locks = sub.add_parser("locks", help="Print the locks held right now.")
    locks.add_argument("--kill", action="store_true",
                       help="Instead of printing, terminate every backend that holds a blocking lock.")

    sub.add_parser("stats", help="Print how often each index was scanned (pg_stat_user_indexes).")

    sub.add_parser("replica-lag-check-run-now-and-report",
                   help="Print each replica's replay lag in seconds.")

    sub.add_parser("zap-idle", help="Terminate every backend idle in a transaction "
                                    "for more than five minutes.")

    sub.add_parser("diag", help="Print the rows of pg_stat_activity: one per backend, "
                                "with its state and current query.")

    # Settings: bare, they print the value; given one value, they set it.
    for name, help_text in [
        ("wal-keep-size", "WAL kept for replicas to catch up (wal_keep_size)."),
        ("statement-timeout", "Longest a statement may run (statement_timeout)."),
        ("slow-ms", "Log every statement that runs longer than this many milliseconds "
                    "(log_min_duration_statement)."),
        ("set-max-conns", "The most client connections the server accepts (max_connections)."),
    ]:
        s = sub.add_parser(name, help=help_text)
        s.add_argument("value", nargs="?")

    return p
