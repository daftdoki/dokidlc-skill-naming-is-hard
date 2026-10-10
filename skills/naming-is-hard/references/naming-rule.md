# Naming commands, subcommands, flags, and settings

A command line is a sentence with the program as its subject:
`bak rebuild-catalog` reads "bak rebuilds the catalog." Name each command
so that sentence is true and plain.

The examples come from `bak`, a backup tool.

## The shape

- **Command or subcommand:** a verb, then its object. The verb is what
  the command does when it runs:
  - it prints what is already stored: `show` (`show-retention-days`)
  - it works out a result and prints it: the verb of that work
    (`estimate-restore-time`, `find-corrupt-snapshots`)
  - it changes or writes something: that change (`rebuild-catalog`,
    `prune-expired-snapshots`, `mark-job-reviewed`)
- **Setting:** the noun of the property it controls, with no verb. Bare,
  it prints the value; given one value, it sets it:
  `progress-bar-visibility off`, `retention-days 30`. A setting takes at
  most one value; anything that takes a name and a value is two commands
  (`show-alert-limits`, `set-alert-limit NAME VALUE`). Settings are the
  one exception to the sentence.
- **Flag:** names what the command keeps or adds: `--metadata-only`. A
  flag that changes what the command does, not just how much, is a
  separate command with its own name: `bak list-jobs --purge` becomes
  `purge-finished-jobs`.
- **Argument as object:** an argument can complete the sentence.
  `bak restore SNAPSHOT` reads "bak restores SNAPSHOT", so `restore`
  needs no noun of its own. It holds only when the argument is the thing
  acted on.
- **Subcommand:** stands on its own, without its parent's words. It shows
  up alone in logs and errors.
- **Verb:** a plain verb a newcomer knows: `evaluate`, not `sweep`;
  `find`, not `grep`.
- **Length:** three words is the sweet spot. Use four only when the
  fourth word adds clarity worth its length; more than four almost never.

## The object

- End on the head noun, the kind of thing. Put the words that say which
  kind of the head noun in front of it: `snapshot-index`,
  `max-parallel-jobs`, `integrity-checks` (a kind of check), not
  `snapshot-checks` (the thing checked). Name the kind even when only
  one kind exists today, because a second kind would leave the first
  without one.
- Add those words until nothing else fits the name, then stop. Two
  words before the head is the most a reader parses easily; when you
  need more, use one word for the group.
- The head noun names what the thing contains, not what it is for:
  `job-logs`, not `diagnostics`.

## Outside a command line

The rule applies to every name a person reads, through these mappings.

- **In code:** a function or method is a command, so "the code VERBs
  OBJECT" is a true sentence and its verb follows the three cases in The
  shape. A parameter is a flag: one that changes what the function
  does, not just how much, is its own function. A variable, constant,
  attribute, field, or config key is an object or a setting. A class
  is an object that names the kind of thing each instance is; a suffix
  that names no kind (`Manager`, `Handler`, `Helper`, `Data`, `Info`)
  fails The object: `JobManager` becomes `JobQueue` or `JobScheduler`,
  whichever the class is.
- **In an interface:** a button or menu item is a command. A label on a
  value, or a toggle, is a setting.

## The words

- One role per word: a word that is a noun in one name is a noun in
  every name. Forms of a word count as their own words: "restore" can
  be the verb in `restore-snapshot` while "restored" modifies
  `show-restored-files`. One form doing two jobs is what fails.
- Name for the audience of the surface. A setting or command a person
  outside the field types uses the word that person knows
  (`retention-limit`), even when the field has a more exact term. A
  name experts read uses the field's term (`max-chunk-entropy`): a plain
  or invented word that hides a term they know fails, the same as jargon
  fails a newcomer.
- A word's meanings include the ones it already has in the field. In
  backups, "differential" names a kind of backup, so `differential` is
  taken before the project uses it for anything else.
- Use the project's existing term for a thing, and its spelling, while
  that term passes every check. A term that fails a check is renamed
  everywhere at once: `bak` once called its schedules "cron knobs";
  they became `backup-schedules` in every name and every document.
- When a word fails, the interface wins: rename to the word the person
  already sees on screen and in the output, and change the internal
  names to match.

## Product names

A product's, plugin's, or skill's own name may be playful: a backup
product can be called `squirrel`. Every name a person types or reads to
get work done inside it follows the rest of this rule:
`squirrel restore-snapshot`, not `squirrel dig-up`.

## Done when

Every name passes all four:
1. `PROGRAM NAME` read aloud is a sentence, or the name is a setting.
2. Nothing else fits the object, in the project or in the field.
3. Removing any word loses meaning.
4. Each word has the same role here as in every other name.
