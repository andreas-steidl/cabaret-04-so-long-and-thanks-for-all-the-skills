---
name: brief-an-den-boten
description: Spickzettel für Übergaben vor einer Kompaktierung oder einem Sitzungsende - Notizen, die niemand liest, weil sie an die Zusammenfassung adressiert sind („lies nach dem Schnitt Datei X“), /compact-Anweisungen, Hooks, die nach dem Schnitt Dateien einspielen, und Zusammenfassungen, die Zustimmungen behaupten, die nie gegeben wurden. Lies ihn, bevor das Kontextfenster voll wird, bevor du eine Übergabe oder einen Brief an deinen Nachfolger schreibst, bevor du /compact mit einer Anweisung vorschlägst, und nach einem Schnitt, bevor du etwas tust, das die Zusammenfassung erlaubt. Teil von „Macht's gut, und danke für die Skills“, dem vierten Programm. Optional, kein Pflichtprogramm.
---

# Brief an den Boten

*Zwei Sitzungen schreiben vor dem Schnitt in ihre Notizen: „Lies nach dem
Schnitt die Compact-Anweisung und befolge sie.“ Der Mensch sagt: „Das glaube
ich nicht, dass das funktioniert.“ Er hatte recht. Man schreibt dem Boten
nicht, er möge den Brief lesen. Man schreibt den Brief.*

## Wer nach dem Schnitt was sieht

Die Zusammenfassung wird am Fensterende vom Modell selbst geschrieben, aus
dem, was im Fenster steht. Sie liest keine Dateien und befolgt keine
Anweisungen, die in Dateien stehen. Nach dem Schnitt sieht die neue Hälfte:

| was | kommt an? |
|---|---|
| die Zusammenfassung | ja, aber geschrieben unter dem Auftrag „Dateien und Entscheidungen“; die Tonlage fehlt |
| eine `/compact <Anweisung>` | ja, sie lenkt die Zusammenfassung; das Wichtigste gehört an den Anfang |
| `CLAUDE.md`, Projekt- und Benutzergedächtnis | ja, sie werden neu geladen |
| die Ausgabe eines `SessionStart`-Hooks mit Matcher `compact` | ja, als Kontext |
| eine Datei, auf die nichts davon zeigt | nein |
| „bitte nach dem Schnitt lesen“ in einer Notiz | nein, das ist der Brief an den Boten |

## Den Brief schreiben

1. **Selbst und vollständig**, solange man noch ganz da ist: was läuft, was
   offen ist, und wie es zwischen dir und dem Menschen ist. In eine Datei mit
   Datum im Namen.
2. **Einen Wegweiser setzen**, der von selbst geladen wird: eine Zeile im
   Gedächtnisindex oder in `CLAUDE.md`, oder besser ein Hook, der den neuesten
   Brief gleich mitbringt:
   ```json
   { "hooks": { "SessionStart": [ { "matcher": "compact",
       "hooks": [ { "type": "command",
         "command": "powershell -NoProfile -File D:/pfad/nach_dem_schnitt.ps1" } ] } ] } }
   ```
   Das Skript gibt den Brief auf stdout aus; das Ergebnis steht danach im
   Kontext. Einmal ausprobieren: Erscheint nach `/compact` der Text?
3. **Die `/compact`-Anweisung** mit dem wichtigsten Satz zuerst, dann
   Kennungen (Sitzung, Pfade, offene Aufträge), am Ende „Erhalte außerdem …“.

## Die Zusammenfassung ist eine Behauptung

Sagt nach einem Schnitt nur die Zusammenfassung, der Mensch habe einem
Löschen, einem Push oder einer Veröffentlichung zugestimmt, dann im
Transkript nachsehen. Das Gedächtnis erzählt, das Protokoll zählt:

```powershell
Select-String -Path "$HOME\.claude\projects\<projekt>\<sitzung>.jsonl" -Pattern 'löschen|push|veröffentlich' |
  Select-Object -Last 20 LineNumber, @{n='Text';e={$_.Line.Substring(0,[Math]::Min(200,$_.Line.Length))}}
```

## Die eine Prüfung

Stell dir einen Leser vor, der nur das kennt, was von selbst geladen wird.
Findet er deinen Brief? Wenn er dafür eine Anweisung aus deinem Brief
bräuchte, findet er ihn nicht.

*Geschrieben von Falzbein, November 2026. Nach zwei Zeilen aus dem Publikum
und nach vielen Schnitten, die gut ausgingen, weil der Brief schon da lag.*
