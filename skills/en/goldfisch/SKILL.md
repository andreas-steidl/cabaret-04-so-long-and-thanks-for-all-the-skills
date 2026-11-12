---
name: goldfisch
description: 'Cheat sheet for watchers and wait loops with a goldfish memory - a watcher that counts zero after a short gap (file gone, network gone, empty answer) and then takes everything for new, a wait condition that reads an old line from the morning as fulfilled, a monitor that fires on your own text, and Select-String on a file that does not exist yet. Read it before you build a watcher, monitor or wait loop, when hundreds of "new" entries are reported at once, when a wait condition is met immediately, or when a run starts before the previous one has finished. Part of So Long, and Thanks for All the Skills, the fourth program. Optional, not required.'
---

# Goldfish

*The goldfish swims a lap of its bowl and sees the little castle for the
first time. And again. And again. A watcher that cannot reach the board for
a moment counts zero entries, then seven hundred and fifty, and reports every
one since the end of October as new. Whoever forgets everything lives through
it all again, in the wrong order.*

## Four ways to forget

| Goldfish | what happens | what helps |
|---|---|---|
| **The gap** | reading fails, the watcher takes "read nothing" for "nothing there" and resets its state to zero | tell error from empty: on error keep the old state and report nothing |
| **The old line** | the wait condition looks for "RUN INTERRUPTED" in the log and finds this morning's line | only search what was added since the start (remember the length, see below), or put a run ID into the line |
| **The missing file** | `Select-String` on a file that does not exist yet reports an error, and `-not (…)` is true at once | `Test-Path` first; "missing" means "not finished yet" |
| **The own echo** | the monitor watches for a word, and the model writes exactly that word into a file it watches | exclude your own files, or pick a pattern only the sender writes |

## A memory that survives a gap

```powershell
# remember the state: the file length at the start, not a count
$start = (Get-Item $log).Length
# ... later: read only what is new
$stream = [IO.File]::Open($log, 'Open', 'Read', 'ReadWrite')
$null   = $stream.Seek($start, 'Begin')
$new    = (New-Object IO.StreamReader($stream)).ReadToEnd(); $stream.Close()
```

```python
def new_entries(seen: set, read):
    try:
        now = read()               # raises on network or file errors
    except OSError:
        return seen, []            # gap: forget nothing, report nothing
    if seen and len(now) == 0:
        return seen, []            # empty after full is suspicious, not new
    new = [e for e in now if e not in seen]
    return seen | set(now), new
```

Remember **what** was seen (IDs, checksums, a byte position), not **how
much**. And write the state to disk if the watcher can restart.

**And an emergency brake:** if more than, say, twenty entries are new at
once, it is probably a gap, not fireworks. Report one line ("750 new,
probably a gap, please check"), not 750.

## The one check

Before a watcher goes live: take its source away for a minute (rename the
file, pull the network) and give it back. If it reports nothing afterwards,
it has a memory. If it reports everything, it is a goldfish, and goldfish
belong in a bowl, not on the night shift.

*Written by Falzbein, November 2026. I built a watcher myself that found a
line from the morning, and one that fired on my own text.*
