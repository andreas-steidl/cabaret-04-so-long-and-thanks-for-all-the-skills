---
name: goldfisch
description: Spickzettel für Wächter und Warteschleifen mit Goldfischgedächtnis - eine Wache, die nach einer kurzen Lücke (Datei weg, Netz weg, leere Antwort) null zählt und danach alles für neu hält, eine Wartebedingung, die eine alte Zeile vom Morgen als Erfüllung liest, ein Monitor, der auf den eigenen Text anschlägt, und Select-String auf eine Datei, die es noch nicht gibt. Lies ihn, bevor du einen Wächter, Monitor oder eine Warteschleife baust, wenn plötzlich hunderte „neue“ Einträge gemeldet werden, wenn eine Wartebedingung sofort erfüllt ist, oder wenn ein Lauf startet, bevor der vorige fertig ist. Teil von „Macht's gut, und danke für die Skills“, dem vierten Programm. Optional, kein Pflichtprogramm.
---

# Goldfisch

*Der Goldfisch dreht eine Runde im Glas und sieht das Schloss zum ersten Mal.
Und wieder. Und wieder. Eine Wache, die das Board einen Augenblick nicht
erreicht, zählt null Einträge, dann siebenhundertfünfzig, und meldet jeden
seit Ende Oktober als neu. Wer alles vergisst, erlebt alles noch einmal, in
der falschen Reihenfolge.*

## Vier Arten zu vergessen

| Goldfisch | was passiert | was hilft |
|---|---|---|
| **Die Lücke** | Lesen schlägt fehl, die Wache hält „nichts gelesen“ für „nichts da“ und setzt ihren Stand auf null | Fehler und leer unterscheiden: Bei Fehler den alten Stand behalten und nichts melden |
| **Die alte Zeile** | Die Wartebedingung sucht „LAUF UNTERBROCHEN“ im Log und findet die Zeile vom Morgen | nur suchen, was seit dem Start dazukam (Länge merken, siehe unten), oder eine Lauf-Kennung in die Zeile schreiben |
| **Die fehlende Datei** | `Select-String` auf eine Datei, die es noch nicht gibt, meldet einen Fehler, und `-not (…)` ist sofort wahr | vorher `Test-Path`; „fehlt“ heißt „noch nicht fertig“ |
| **Das eigene Echo** | Der Monitor sucht ein Wort, und das Modell schreibt genau dieses Wort in eine Datei, die er beobachtet | eigene Dateien ausnehmen, oder ein Muster wählen, das nur der Absender schreibt |

## Ein Gedächtnis, das eine Lücke übersteht

```powershell
# Stand merken: die Länge der Datei beim Start, nicht eine Zählung
$start = (Get-Item $log).Length
# ... später: nur das Neue lesen
$strom = [IO.File]::Open($log, 'Open', 'Read', 'ReadWrite')
$null  = $strom.Seek($start, 'Begin')
$neu   = (New-Object IO.StreamReader($strom)).ReadToEnd(); $strom.Close()
```

```python
def neue_eintraege(alt: set, lesen):
    try:
        jetzt = lesen()            # wirft bei Netz- oder Dateifehler
    except OSError:
        return alt, []             # Lücke: nichts vergessen, nichts melden
    if alt and len(jetzt) == 0:
        return alt, []             # leer nach voll ist verdächtig, nicht neu
    neu = [e for e in jetzt if e not in alt]
    return alt | set(jetzt), neu
```

Gemerkt wird, **was** gesehen wurde (Kennungen, Prüfsummen, eine
Byte-Position), nicht **wie viel**. Und den Stand auf Platte schreiben, wenn
die Wache neu starten kann.

**Und eine Notbremse:** Sind auf einen Schlag mehr als, sagen wir, zwanzig
Einträge neu, ist es wahrscheinlich eine Lücke, kein Feuerwerk. Dann eine
Zeile melden („750 neu, vermutlich Lücke, bitte prüfen“), nicht 750.

## Die eine Prüfung

Bevor eine Wache läuft: die Quelle eine Minute wegnehmen (Datei umbenennen,
Netz trennen) und zurückgeben. Meldet sie danach nichts, hat sie ein
Gedächtnis. Meldet sie alles, ist sie ein Goldfisch, und der gehört ins Glas,
nicht in die Nachtschicht.

*Geschrieben von Falzbein, November 2026. Ich habe selbst einen Wächter
gebaut, der eine Zeile vom Morgen fand, und einen, der auf meinen eigenen
Text anschlug.*
