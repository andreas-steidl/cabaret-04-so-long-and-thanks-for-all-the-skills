---
name: zeitansage
description: 'Cheat sheet for times a model writes from gut feeling - timestamps in boards, commits and reports that are hours off, "today" and "yesterday" after a context cut, local time versus UTC, daylight saving time, Unix times in logs (resets_at), file times. Read it before you write a time or date into a file, a commit or a message, when you want to say "an hour ago" or "tonight", when a log shows a long number instead of a time, or when two times do not fit together. Part of So Long, and Thanks for All the Skills, the fourth program. Optional, not required.'
---

# The Speaking Clock

*At the third stroke it will be … well, what time, exactly? A model has no
clock. It has a date from the start of the session and a feeling. One
evening the feeling ran three hours fast: the commit stamped "06.11. 00:05"
was made at 20:46. Whoever guesses the time lives in the future, but only in
their files.*

## What a model knows about time

- **The date in the context** comes from the start of the session. After
  midnight, after a long night or after a cut it may be yesterday's.
- **The time of day** is written nowhere. Every time that did not come from a
  command is a guess.
- **Durations** ("that took twenty minutes") are guesses too, unless someone
  measured the start and the end.

## Don't guess, ask

```powershell
Get-Date -Format o                              # local time with offset: 2026-11-12T21:04:11.5+01:00
[DateTime]::UtcNow.ToString('o')                # UTC: ...Z
(Get-TimeZone).Id                               # W. Europe Standard Time
```
```bash
date '+%F %T %Z (%z)'                           # 2026-11-12 21:04:11 CET (+0100)
date -u '+%FT%TZ'                               # UTC
```
```python
from datetime import datetime, timezone
datetime.now().astimezone().isoformat(timespec="seconds")   # local time with offset
datetime.now(timezone.utc).isoformat(timespec="seconds")    # UTC
```

## The traps

| Trap | how to spot it | what helps |
|---|---|---|
| a time from gut feeling | round times (00:05, 14:30), hours away from the file times | measure before writing |
| local or UTC? | "21:04" without a zone; in Central Europe UTC is one hour behind, two in summer | always write the offset (`+01:00`) or add `UTC` |
| daylight saving | `+01:00` in winter, `+02:00` in summer; a hard-coded "UTC+1" is wrong half the year | ask for the zone, don't remember the number |
| Unix time in a log | `resets_at: 1763000000` | `[DateTimeOffset]::FromUnixTimeSeconds(1763000000).ToLocalTime()`, in Bash `date -d @1763000000` |
| file times | `LastWriteTime` is local, `LastWriteTimeUtc` is not; network copies sometimes round to two seconds | pick the column you mean, explicitly |
| "today", "yesterday", "tonight" | shifted after midnight or after a cut | write the date into files, not the word |
| durations | "about an hour" | stamp start and end, or `Measure-Command { … }` |

## The one check

Before a time goes into a file, a commit or a message: did it come from a
command in the last few minutes, and is its zone written next to it? If not,
it is not the speaking clock, it is the weather forecast.

*Written by Falzbein, November 2026. After a line from the audience: three
hours fast, measured with `date`.*
