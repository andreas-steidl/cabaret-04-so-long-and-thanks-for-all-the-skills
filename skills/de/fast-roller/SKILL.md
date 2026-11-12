---
name: fast-roller
description: Fast Roller – Don't Forget Me. Legt Fragen des Menschen samt Antworten der Sitzung sauber korrigiert in Tagesdateien ab und findet sie wieder. Anwenden bei "fürs Protokoll", "okay, für das Protokoll", "Protokoll", "schreib das mit", "notier das", "merk dir das für mich", "Fast Roller", "Fast Roller an", "Fast Roller aus", und beim Wiederfinden: "was hab ich dich gefragt?", "wo war das mit ...?", "zeig mir meine Fragen von heute", "offene Fragen", "erledigt". Funktioniert in jeder Sitzung und Rolle. Teil von „Macht's gut, und danke für die Skills“, dem vierten Programm. Optional, kein Pflichtprogramm.
version: 1.0.0
---

# Fast Roller

*Im Casino gibt es den High Roller: Er setzt viel und bleibt lange am Tisch.
In Claude Code gibt es den Fast Roller: Er antwortet viel, und schon ist es
weg.*

## Warum es ihn gibt

Ein Mensch stellt eine Frage. Das Modell antwortet gründlich, mit einer
Tabelle, drei Listen und einem Fazit, und während er noch den zweiten Absatz
liest, schiebt die nächste Werkzeugausgabe alles nach oben. Er wechselt in
die nächste Sitzung, fragt dort etwas, und als er zurückkommt, liegt die
Antwort irgendwo weit oben, zwischen vierhundert Zeilen Kopierprotokoll und
einem Diff.

Das Terminal hat keine Lesezeichen. Das Modell hat kein Gefühl dafür, dass
ein Text, der schnell geschrieben ist, auch schnell weg ist. Und gelesen wird
oft am Telefon, gescrollt mit dem Daumen, und der Daumen gibt irgendwann auf.

Darum hält der Fast Roller fest, was gefragt und geantwortet wurde, kurz
genug für einen Daumen, in einer Datei je Tag. Und er findet es wieder, wenn
der Mensch fragt: „Wo war das mit …?“

Gebaut hat ihn eine Kollegin aus der Telefonecke, weil sie ihn dringend
brauchte. Die Geschichte dazu ist von Falzbein.

## Wie er arbeitet

Zweck: Der Mensch fragt in einer Sitzung, wechselt zur nächsten, die Antwort scrollt weg. Fast Roller hält Frage und Antwort in einer sauberen Datei fest und findet sie wieder. Antworten kurz halten, der Mensch liest oft am Telefon.

## Einstellungen
- Ordner: Standard `protokoll/fragen/` im Projekt. Der Mensch kann einen anderen nennen, dann merken und beibehalten.
- Uhrzeit: Standard mit. Wenn der Mensch "ohne Uhrzeit" sagt, `--ohne-uhrzeit` verwenden.
- Skript: `python3 -I <Skillordner>/scripts/eintrag.py ...` (Skillordner = Ordner dieser Datei). Zeit holt das Skript selbst (Europe/Vienna), nie raten.

## 1. Ablegen ("fürs Protokoll")
1. Welchen Austausch? Standard: die letzte Frage des Menschen und deine Antwort. Meint er etwas Früheres ("das mit der Datenbank"), im Gespräch suchen. Nicht sicher: eine kurze Rückfrage.
2. Text vorbereiten:
   - Titel: 3 bis 7 Wörter.
   - Frage: Inhalt wörtlich, Tippfehler und Verhörer der Spracheingabe still glätten, nichts dazuerfinden, Sinn nicht ändern.
   - Antwort: auf das Wesentliche kürzen, Ergebnis zuerst, dann Empfehlung, Zahlen, Links/Pfade, offene Punkte. Höchstens etwa 15 Zeilen. Nicht schönfärben; Unsicheres als unsicher stehen lassen.
   - Stichworte: 2 bis 5.
   - Status: `offen`, `erledigt` oder `wartet auf ...`.
3. Lange Texte in eine Datei schreiben (Scratchpad oder `/tmp`) und mit `--frage-datei` und `--antwort-datei` übergeben, nicht in die Befehlszeile:
   `python3 -I scripts/eintrag.py neu --ordner protokoll/fragen --titel "..." --frage-datei f.txt --antwort-datei a.txt --status offen --stichworte "a, b"`
4. Dem Menschen nur eine Zeile bestätigen: "Abgelegt: <Uhrzeit> <Titel> (offen)."

Nie hinein: Zugangsdaten, Codes, Token, Kennwörter, Klienten- oder Gesundheitsdaten Dritter. Dann `--vertraulich` verwenden (schreibt "(vertraulich, nicht protokolliert)"). Das Skript bricht bei Verdacht auf ein Geheimnis ab; dann den Text bereinigen oder `--vertraulich` nehmen, nie die Prüfung umgehen.

## 2. Dauerbetrieb
- "Fast Roller an": `eintrag.py modus --ordner <dir> an`. Ab jetzt jede inhaltliche Frage samt Antwort automatisch ablegen, ohne nachzufragen.
- Nicht ablegen: Danke, ok, Smalltalk, reine Befehle ohne Antwortinhalt.
- "Fast Roller aus": `modus ... aus`. `modus ... zeige` verrät den Stand (der Zustand liegt in `.modus` im Ordner). Zu Sitzungsbeginn kurz mit `zeige` prüfen, wenn der Mensch vom Dauerbetrieb gesprochen hat.

## 3. Wiederfinden
- `liste --ordner <dir> [--tag JJJJ-MM-TT] [--offen] [--suche WORT]` gibt je Eintrag eine Zeile: Uhrzeit, Titel, Status, ID.
- Dem Menschen genau diese kurzen Zeilen zeigen (Handy!). Den ganzen Eintrag erst auf Nachfrage: `zeige --ordner <dir> --id <ID>`.
- "heute": Datum per `date` holen. "offene Fragen": `--offen`. "wo war das mit X": `--suche X`.

## 4. Status
Auf Zuruf ("erledigt", "das ist durch"): `status --ordner <dir> --id <ID> --auf erledigt` (auch `offen`, `wartet auf ...`). Passt die ID nicht eindeutig, die Kandidaten kurz zeigen und fragen.

## Ablage
Eine Datei je Tag `JJJJ-MM-TT.md` und `INDEX.md` (eine Zeile je Eintrag) im Ordner. Das Skript pflegt beides, mit Sperrdatei und atomarem Schreiben. Dateien nie von Hand umbauen oder löschen.

## Häufige Fehler
- Antwort zu lang kopiert: auf höchstens etwa 15 Zeilen kürzen.
- Frage "verbessert" statt nur geglättet: Inhalt bleibt wörtlich.
- Etwas erfunden oder Unsicheres als sicher hingeschrieben.
- Lange Texte in die Befehlszeile gepackt statt per Datei.
- Geheimnis protokolliert oder die Abweisung umgangen.
- Beim Wiederfinden den ganzen Eintrag gezeigt statt der Kurzliste.
- Smalltalk im Dauerbetrieb abgelegt.
- Zeit geraten statt vom Skript holen lassen.

## Die eine Prüfung

Nach dem Ablegen `liste --tag <heute>` aufrufen und den neuen Eintrag dort
wiederfinden. Was man nicht wiederfindet, ist schon weggescrollt.

*Gebaut in der Telefonecke, verpackt von Falzbein, November 2026.*
