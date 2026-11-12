# CLAUDE.md – 04-machsgut

Vierte Spielzeit des Kabaretts von Falzbein und Andy: **„Macht's gut, und danke für die Skills“** /
**„So Long, and Thanks for All the Skills“**. Thema: Zeit und Gedächtnis.
**Stand: in Arbeit.** Zwei Nummern liegen schon da (fast-roller de/en, rome-in-a-day en mit
deutschem README), die übrigen sind vorbereitet. Noch kein Plakat, keine Seite.
Host: **https://solong.special.at/** (noch nicht angelegt; später Inhalt von `web/`, flach
hochgeladen: `index.html` als Sprachwähler, `de/index.html`, `en/index.html`).

## Nummern (laut `../SPIELPLAN.md`)

| Nr. | Name | worum | Stand |
|---|---|---|---|
| 21 | zeitansage | Uhrzeiten nie schätzen, immer messen; UTC und Ortszeit benennen | vorbereitet |
| 22 | brief-an-den-boten | Übergaben vor dem Schnitt, die ohne Leser wirken | vorbereitet |
| 23 | goldfisch | Wachen, die nach einer Lücke alles für neu halten | vorbereitet |
| 24 | durch-den-schnitt | sich selbst durch eine Kompaktierung bringen | vorbereitet |
| 25 | rome-in-a-day | Schätzen in Agentenstunden: UNIT, COUNT, PARALLEL, HALVE, WAIT | fertig, `skills/en/rome-in-a-day/` |
| 26 | fast-roller (Don't Forget Me) | Fragen und Antworten über Sitzungswechsel hinweg festhalten | fertig, `skills/de/` und `skills/en/` |
| Extra | grau-in-grau | Sitzungen, die die Umgebung ihrer Eltern erben | Entwurf (`../03-katastrophen/doku/entwurf_grau-in-grau_SKILL.md`) |

## Ordner
- `doku/VIERTE_SPIELZEIT.md` – Kopie der Sammelmappe aus `../zwischenraum/doku/` (dort wird weiter gesammelt).
- `skills/de/fast-roller/`, `skills/en/fast-roller/` – SKILL.md, `scripts/eintrag.py`, `tests/test_eintrag.py`, `beispiel/`, `PRUEFSUMMEN.sha256`. Skript und Tests unverändert aus der Quelle; Ausgaben des Skripts sind deutsch, in beiden Fassungen.
- `skills/en/rome-in-a-day/` – SKILL.md englisch, `README.de.md` deutsch, unverändert aus der Baustelle.
- `web/`, `plakat/` – leer (`.gitkeep`), bis das Programm steht.

## Bauen
- **Skills:** `skills/de/<name>/` und `skills/en/<name>/`, Ordnername in beiden Sprachen gleich.
- **Tests von fast-roller:** `python -I -B -m unittest discover -s tests` im Skillordner (unittest, kein pytest nötig).
- **Prüfsummen:** nach jeder Änderung in einem Skillordner `PRUEFSUMMEN.sha256` neu schreiben (`<sha256>  ./<pfad>`, LF, ohne die Datei selbst).
- **Zips:** wie in den anderen Spielzeiten, `<name>.zip` / `<name>-en.zip`.
- **Plakat und Seite:** nach dem Muster von `../03-katastrophen`.

## Querverweise
Erste Spielzeit `../01-grauen` (horrors.special.at), zweite `../02-panik` (dontpanic.special.at),
dritte `../03-katastrophen` (lostintranslation.special.at), Bühne und Gesamtskill `../zwischenraum`
(zwischenraum.special.at). Quelle von fast-roller: `\\nas\Public\dev\linde\fuer-falzbein\fast-roller\`
(nur lesen). Quelle von rome-in-a-day: `\\nas\Public\dev\skill-suite-des-grauens\rome-in-a-day\` (nur lesen).

## Regeln
- Sprachen: siehe ..\WIE_MACH_ICH_SPRACHEN.md
- Texte UTF-8 (ohne BOM), keine Steuerzeichen.
- Jede Seite und jeder Skill auf Deutsch **und** Englisch.
- Keine Religion, keine Politik in Namen und Texten.
- Namen von Menschen und Sitzungen in Skill-Texten nur als Rollen („der Mensch“, „eine andere Sitzung“).
- Vor dem Veröffentlichen schaut der Legal-Agent drüber (KI-Kennzeichnung, Lizenzzeile, Plakate).
- Signatur und Manifest kommen gesammelt am Schluss, nicht je Änderung.
- Nach jedem Schreiben im Ergebnis nachsehen: Datei öffnen, Zip auflisten, Pfad wiederfinden.
