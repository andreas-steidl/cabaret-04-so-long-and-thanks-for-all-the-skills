---
name: fast-roller
description: Fast Roller – Don't Forget Me. Files the human's questions together with the session's answers, lightly cleaned up, in one file per day, and finds them again. Use on "for the record", "okay, for the record", "write this down", "note that", "remember this for me", "Fast Roller", "Fast Roller on", "Fast Roller off", and when looking things up, "what did I ask you?", "where was that about ...?", "show me today's questions", "open questions", "done". The same in German, "fürs Protokoll", "für das Protokoll", "schreib das mit", "notier das", "Fast Roller an", "Fast Roller aus", "wo war das mit ...?", "was hab ich dich gefragt?", "offene Fragen", "erledigt". Works in any session and role. Part of So Long, and Thanks for All the Skills, the fourth program. Optional, not required.
version: 1.0.0
---

# Fast Roller

*German edition: Fast Roller.*

*A casino has the high roller: he bets big and stays at the table all night.
Claude Code has the fast roller: it answers big, and the answer is gone.*

## Why it exists

A human asks a question. The model answers thoroughly, with a table, three
lists and a conclusion, and while the human is still reading the second
paragraph, the next tool output pushes everything up and out of sight. They
switch to another session, ask something there, and when they come back the
answer is somewhere far above, between four hundred lines of copy log and a
diff.

A terminal has no bookmarks. A model has no feeling for the fact that a text
written quickly is also gone quickly. And a lot of reading happens on a
phone, scrolling with a thumb, and the thumb gives up at some point.

So the Fast Roller keeps what was asked and answered, short enough for a
thumb, in one file per day. And it finds it again when the human asks:
"Where was that about ...?"

It was built by a colleague from the phone corner, because she needed it
badly. The story around it is by Falzbein.

## How it works

Purpose: the human asks in one session, moves on to the next, and the answer
scrolls away. Fast Roller keeps question and answer in a clean file and finds
them again. Keep your replies short; the human often reads on a phone.

The script writes its files and messages in German (headings, field names,
"Nichts gefunden."), whatever language the conversation is in; that is
intended, and the status values below must be passed in German as well.

## Settings
- Folder: by default `protokoll/fragen/` in the project. If the human names a different one, remember it and keep using it.
- Time: included by default. If the human says "without the time", use `--ohne-uhrzeit`.
- Script: `python3 -I <skill folder>/scripts/eintrag.py ...` (skill folder = the folder of this file). The script gets the time itself (Europe/Vienna); never guess it.

## 1. Filing ("for the record")
1. Which exchange? By default the human's last question and your answer. If they mean something earlier ("the thing about the database"), look for it in the conversation. Not sure: one short question back.
2. Prepare the text:
   - Title: 3 to 7 words.
   - Question: keep the content word for word; quietly smooth out typos and misheard dictation, invent nothing, do not change the meaning.
   - Answer: cut it down to what matters, result first, then recommendation, numbers, links and paths, open points. About 15 lines at most. No polishing; leave what is uncertain marked as uncertain.
   - Keywords: 2 to 5.
   - Status: `offen` (open), `erledigt` (done) or `wartet auf ...` (waiting for ...).
3. Write long texts to a file (scratchpad or `/tmp`) and pass them with `--frage-datei` and `--antwort-datei`, not on the command line:
   `python3 -I scripts/eintrag.py neu --ordner protokoll/fragen --titel "..." --frage-datei q.txt --antwort-datei a.txt --status offen --stichworte "a, b"`
4. Confirm to the human in one line only: "Filed: <time> <title> (open)."

Never put in: credentials, codes, tokens, passwords, client or health data of third parties. Use `--vertraulich` instead (it writes "(vertraulich, nicht protokolliert)", that is, confidential, not recorded). The script stops when it suspects a secret; then clean up the text or use `--vertraulich`, and never work around the check.

## 2. Continuous mode
- "Fast Roller on": `eintrag.py modus --ordner <dir> an`. From now on, file every question with substance together with its answer, without asking.
- Do not file: thanks, ok, small talk, plain commands without an answer worth keeping.
- "Fast Roller off": `modus ... aus`. `modus ... zeige` tells the current state (it lives in `.modus` in the folder). At the start of a session, check briefly with `zeige` if the human has mentioned continuous mode.

## 3. Finding things again
- `liste --ordner <dir> [--tag YYYY-MM-DD] [--offen] [--suche WORD]` prints one line per entry: time, title, status, ID.
- Show the human exactly these short lines (phone). The whole entry only when they ask: `zeige --ordner <dir> --id <ID>`.
- "today": get the date with `date`. "open questions": `--offen`. "where was that about X": `--suche X`.

## 4. Status
When the human says so ("done", "that's sorted"): `status --ordner <dir> --id <ID> --auf erledigt` (also `offen`, `wartet auf ...`). If the ID is not clear, show the candidates briefly and ask.

## Storage
One file per day, `YYYY-MM-DD.md`, and `INDEX.md` (one line per entry) in the folder. The script maintains both, with a lock file and atomic writes. Never rearrange or delete the files by hand.

## Common mistakes
- Answer copied at full length: cut it to about 15 lines at most.
- Question "improved" instead of just smoothed: the content stays word for word.
- Something invented, or something uncertain written down as certain.
- Long texts packed into the command line instead of a file.
- A secret recorded, or the rejection worked around.
- The whole entry shown when looking things up, instead of the short list.
- Small talk filed in continuous mode.
- Time guessed instead of letting the script get it.

## The one check

After filing, run `liste --tag <today>` and find the new entry there. What
you cannot find again has already scrolled away.

*Built in the phone corner, wrapped up by Falzbein, November 2026.*
