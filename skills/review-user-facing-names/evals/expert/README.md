# pgtend

pgtend is a command-line tool for database administrators who run
PostgreSQL in production. Its users know PostgreSQL's own terms
(vacuum, WAL, replica, backend) and expect a tool to use them.

```
pgtend vacuum-table orders --analyze
pgtend list-blocking-locks
pgtend statement-timeout 30s
```

Settings work the same way: bare, they print the value; given one
value, they set it.
