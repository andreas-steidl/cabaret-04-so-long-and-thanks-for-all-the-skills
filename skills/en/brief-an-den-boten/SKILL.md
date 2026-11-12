---
name: brief-an-den-boten
description: 'Cheat sheet for handovers before a context compaction or the end of a session - notes nobody reads because they are addressed to the summary ("after the cut, read file X"), /compact instructions, hooks that bring files back after the cut, and summaries that claim approvals that were never given. Read it before your context window fills up, before you write a handover or a letter to your successor, before you suggest /compact with an instruction, and after a cut, before you do something the summary allows. Part of So Long, and Thanks for All the Skills, the fourth program. Optional, not required.'
---

# Message in a Bottle

*Two sessions write into their notes before the cut: "After the cut, read
the compact instruction and follow it." The human says: "I don't believe
that works." The human was right. You don't write to the postman asking him
to read the letter. You write the letter.*

## Who sees what after the cut

The summary is written at the end of the window by the model itself, from
what is in the window. It reads no files and follows no instructions that
live in files. After the cut, the new half sees:

| what | arrives? |
|---|---|
| the summary | yes, but written under the brief "files and decisions"; the tone is missing |
| a `/compact <instruction>` | yes, it steers the summary; put the most important part first |
| `CLAUDE.md`, project and user memory | yes, they are loaded again |
| the output of a `SessionStart` hook with matcher `compact` | yes, as context |
| a file that none of the above points to | no |
| "please read after the cut" inside a note | no, that is the message to the postman |

## Writing the letter

1. **Yourself and complete**, while you are still all there: what is running,
   what is open, and how things stand between you and the human. Into a file
   with the date in its name.
2. **Put up a signpost** that loads by itself: a line in the memory index or
   in `CLAUDE.md`, or better a hook that brings the newest letter along:
   ```json
   { "hooks": { "SessionStart": [ { "matcher": "compact",
       "hooks": [ { "type": "command",
         "command": "powershell -NoProfile -File D:/path/after_the_cut.ps1" } ] } ] } }
   ```
   The script prints the letter to stdout; the result lands in the context.
   Try it once: does the text appear after `/compact`?
3. **The `/compact` instruction**: the most important sentence first, then
   identifiers (session, paths, open tasks), and at the end "Also keep …".

## The summary is a claim

If after a cut only the summary says the human agreed to a deletion, a push
or a release, look it up in the transcript. Memory tells, the log counts:

```powershell
Select-String -Path "$HOME\.claude\projects\<project>\<session>.jsonl" -Pattern 'delete|push|publish' |
  Select-Object -Last 20 LineNumber, @{n='Text';e={$_.Line.Substring(0,[Math]::Min(200,$_.Line.Length))}}
```

## The one check

Picture a reader who knows only what loads by itself. Do they find your
letter? If they would need an instruction from your letter to find it, they
won't.

*Written by Falzbein, November 2026. After two lines from the audience, and
after many cuts that went well because the letter was already there.*
