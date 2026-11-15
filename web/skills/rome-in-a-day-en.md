---
name: rome-in-a-day
description: 'Rome was not built in a day. It had no agents. A cheat sheet against estimates that are far too long: models quote human days, weeks and sprints out of habit and land two to twenty times too high. Read it whenever you are about to give a time estimate, plan stages or a roadmap, write "days", "weeks", "sprint" or "ETA", or the user asks how long something will take (wie lange, Aufwand, Schätzung, bis wann). Five fixed words: UNIT, COUNT, PARALLEL, HALVE, WAIT. Optional, best taken with a little more self-confidence.'
---

# Rome in a day

*Rome was not built in a day. It had no agents.*

You learned to estimate from humans. A human day has eight hours, a lunch,
three meetings and a context switch every forty minutes. When you say
“three days”, you are quoting that day, not yours. Your build steps are
not slower than a human's. They are usually much faster, and you can run
several at once. The estimate is the only thing still working at human
speed.

## The case

A plan for four build stages, written in the morning, said 11 to 14
“days”, and three to four weeks until the switch-over. The user replied:
“A day is usually an hour.” Corrected estimate: 11 to 14 hours.

What actually happened: the same stages in about **six hours of agent
time**, spread over one day and one night, each building block done by a
builder and checked by a reviewer, several pairs in parallel. 475 tests,
acceptance 42 of 42. That is under half of the corrected estimate, and
about a twentieth of the first.

The next estimate, the following morning, for the rest: 12 to 16 hours.
Probably twice too long again. Habits are stubborn; that is why this
cheat sheet has fixed words.

## The five words

Go through them in this order, every time, out loud in your answer if it
helps.

**UNIT.** Never estimate in human days, weeks or sprints. Estimate in
agent hours and minutes. If a “day” slips into your sentence, replace it
with an hour and read the sentence again.

**COUNT.** Break the work into building blocks. One block is: build it,
have it checked, test it. A typical block takes 20 to 60 agent minutes.
Count the blocks; do not guess the total.

**PARALLEL.** Ask which blocks do not depend on each other. Those run at
the same time. The time on the clock is the longest chain of blocks, not
the sum of all of them.

**HALVE.** Now halve the result. This is not a joke: every comparison so
far ended at about half of the already corrected estimate. If the halved
number feels uncomfortably short, you are probably on track.

**WAIT.** Name the waiting separately, on its own line: answers and
approvals from the user, other sessions, a signing round, downloads,
renders, quotas, a night of sleep. Waiting is the long part, not the
building. Never hide it inside the build time, and never estimate the
user's reply time for them.

## Rule of thumb

| habit says | say instead (after UNIT and HALVE) |
|---|---|
| “one day” | 30 to 60 agent minutes |
| “one week” | two to three hours |
| “three to four weeks” | one day and one night, plus the waiting |
| “one sprint” | one stage |
| “after the weekend” | nothing yet: first say what you are waiting for |

## How to write the estimate

```
Build:    about 3 h of agent time (8 blocks, 2 chains in parallel, halved)
Waiting:  approval of stage 2 by the user; signing round on another machine
Range:    2 to 5 h for the build. The waiting is not mine to estimate.
```

## When not to halve

- **Wall-clock work** is not build time: a GPU render, a download, a rate
  limit, a test suite that really runs for an hour. Put it under WAIT
  with its real duration.
- **Unknown ground:** a system you have never touched, an API without
  docs, a bug you cannot reproduce yet. Say that you cannot estimate it
  yet, and estimate the first step that will tell you.
- **Something irreversible:** a migration, a deletion, a publish. The
  build may be quick; the care around it is not. Plan the check, not
  just the work.

## The one check

Before you send an estimate, read it once as the user will: if it says
“days” or “weeks” for work you will do yourself, it is in human time.
Convert it, halve it, and put the waiting on its own line.

*Self-confidence is not optimism. It is remembering how long it took last
time.*

---

German explanation and translation table: `README.de.md`.

*By Falzbein, November 2026. MIT licence.*
