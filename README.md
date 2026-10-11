# naming-is-hard

There are only two hard things in computer science: cache invalidation,
naming things, and off-by-one errors. This Claude Code plugin takes on
the second. It holds a rule Claude follows while it names commands,
settings, flags, and other parts of software, so a person understands
each name on first read. Claude loads the rule on its own when it names
something; to ask for names directly, type
`/naming-is-hard:naming-is-hard DESCRIPTION`. Claude Code 2.1.296 also
accepts the short `/naming-is-hard`. The plugin has two reviews you run
yourself:
`/naming-is-hard:review-internal-names` for names experts read, and
`/naming-is-hard:review-user-facing-names` for names users see. Work in
progress.
