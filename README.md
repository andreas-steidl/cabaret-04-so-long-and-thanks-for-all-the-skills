# So Long, and Thanks for All the Skills (work in progress)

German title: *Macht's gut, und danke für die Skills*

The fourth season of a small cabaret by Falzbein and Andy, about time and memory: guessed
clock times, hand-overs nobody reads, watchers that forget, getting through a compaction,
estimates in human days, and answers that scroll away. **Not finished yet:** two numbers are
here, the others are being prepared. There is no poster and no website so far; the host
https://solong.special.at/ is not set up yet.

## What is here

- `skills/en/fast-roller/` and `skills/de/fast-roller/`: **Fast Roller (Don't Forget Me)** keeps
  questions and answers in one file per day and finds them again ("for the record", "where was
  that about ...?"). With a small script (standard library only), tests and an example.
- `skills/en/rome-in-a-day/`: **Rome in a day**, a cheat sheet against estimates that are far too
  long (UNIT, COUNT, PARALLEL, HALVE, WAIT), with a German explanation in `README.de.md`.
- `doku/`: the collection of notes for this season.

## Install a skill

Copy one folder unchanged from `skills/en/<name>/` (or `skills/de/<name>/`) to
`~/.claude/skills/<name>/` (on Windows `%USERPROFILE%\.claude\skills\<name>\`). Claude Code loads
it on the next start. For fast-roller, `PRUEFSUMMEN.sha256` in the folder lists the SHA-256 of
every file (`sha256sum -c PRUEFSUMMEN.sha256`).

## License

MIT, see [LICENSE](LICENSE). Copyright (c) 2026 Falzbein und Andy.

## The other seasons

- Season 1: **The Skill Suite of Horrors**, project `01-grauen`, https://horrors.special.at/
- Season 2: **Don't Panic – The Skill Suite for Panicking Models**, project `02-panik`, https://dontpanic.special.at/
- Season 3: **Lost in Translation**, project `03-katastrophen`, https://lostintranslation.special.at/
- The stage over all seasons, with the combined skill: **Zwischenraum**, project `zwischenraum`, https://zwischenraum.special.at/

---

**Deutsch:** Die vierte Spielzeit, *Macht's gut, und danke für die Skills*, handelt von Zeit und
Gedächtnis und ist in Arbeit. Fertig sind fast-roller (deutsch und englisch) und rome-in-a-day
(englisch, mit deutschem `README.de.md`); die übrigen Nummern sind vorbereitet. Plakat und Seite
folgen, der Host solong.special.at ist noch nicht angelegt.
