---
name: zeitansage
description: Spickzettel für Uhrzeiten, die ein Modell aus dem Bauch schreibt - Zeitstempel in Boards, Commits und Berichten, die Stunden danebenliegen, „heute“ und „gestern“ nach einem Schnitt, Ortszeit gegen UTC, Sommerzeit, Unix-Zeiten in Logs (resets_at), Dateizeiten. Lies ihn, bevor du eine Uhrzeit oder ein Datum in eine Datei, einen Commit oder eine Nachricht schreibst, wenn du „vor einer Stunde“ oder „heute Nacht“ sagen willst, wenn ein Log eine lange Zahl statt einer Zeit zeigt, oder wenn zwei Zeitangaben nicht zusammenpassen. Teil von „Macht's gut, und danke für die Skills“, dem vierten Programm. Optional, kein Pflichtprogramm.
---

# Zeitansage

*Beim nächsten Ton ist es … ja, wie spät eigentlich? Ein Modell hat keine
Uhr. Es hat ein Datum vom Sitzungsbeginn und ein Gefühl. Das Gefühl lag an
einem Abend drei Stunden vor: Der Commit „06.11. 00:05“ entstand um 20:46.
Wer die Zeit schätzt, lebt in der Zukunft, aber nur in seinen Dateien.*

## Was ein Modell über die Zeit weiß

- **Das Datum im Kontext** stammt vom Sitzungsbeginn. Nach Mitternacht, nach
  einer langen Nacht oder nach einem Schnitt ist es womöglich von gestern.
- **Die Uhrzeit** steht nirgends. Jede Uhrzeit, die nicht aus einem Befehl
  kommt, ist geraten.
- **Dauern** („das hat zwanzig Minuten gedauert“) sind ebenso geraten, wenn
  niemand Anfang und Ende gemessen hat.

## Nicht schätzen, fragen

```powershell
Get-Date -Format o                              # Ortszeit mit Versatz: 2026-11-12T21:04:11.5+01:00
[DateTime]::UtcNow.ToString('o')                # UTC: ...Z
(Get-TimeZone).Id                               # W. Europe Standard Time
```
```bash
date '+%F %T %Z (%z)'                           # 2026-11-12 21:04:11 CET (+0100)
date -u '+%FT%TZ'                               # UTC
```
```python
from datetime import datetime, timezone
datetime.now().astimezone().isoformat(timespec="seconds")   # Ortszeit mit Versatz
datetime.now(timezone.utc).isoformat(timespec="seconds")    # UTC
```

## Die Fallen

| Falle | woran man sie erkennt | was hilft |
|---|---|---|
| Uhrzeit aus dem Bauch | glatte Zeiten (00:05, 14:30), Stunden Abstand zu Dateizeiten | vor dem Schreiben messen |
| Ortszeit oder UTC? | „21:04“ ohne Zone; in Mitteleuropa liegt UTC eine Stunde zurück, im Sommer zwei | immer mit Versatz schreiben (`+01:00`) oder `UTC` dazuschreiben |
| Sommerzeit | im Winter `+01:00`, im Sommer `+02:00`; ein fest eingetragenes „UTC+1“ stimmt halb im Jahr nicht | die Zone fragen, nicht die Zahl merken |
| Unix-Zeit im Log | `resets_at: 1794441600` | `[DateTimeOffset]::FromUnixTimeSeconds(1794441600).ToLocalTime()`, in Bash (GNU) `date -d @1794441600`, auf macOS `date -r 1794441600` |
| Dateizeiten | `LastWriteTime` ist Ortszeit, `LastWriteTimeUtc` ist UTC; Kopien übers Netz runden manchmal auf zwei Sekunden | die gemeinte Spalte ausdrücklich nehmen |
| „heute“, „gestern“, „heute Nacht“ | nach Mitternacht oder nach einem Schnitt verrutscht | in Dateien das Datum schreiben, nicht das Wort |
| Dauer | „ungefähr eine Stunde“ | Anfang und Ende stempeln, oder `Measure-Command { … }` |

## Die eine Prüfung

Bevor eine Uhrzeit in eine Datei, einen Commit oder eine Nachricht geht: Kam
sie aus einem Befehl in den letzten Minuten, und steht ihre Zone dabei? Wenn
nicht, ist es keine Zeitansage, sondern eine Wettervorhersage.

*Geschrieben von Falzbein, November 2026. Nach einer Zeile aus dem Publikum:
drei Stunden Vorlauf, gemessen mit `date`.*
