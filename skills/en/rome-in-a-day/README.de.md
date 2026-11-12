# Rom an einem Tag (rome-in-a-day)

*Rom wurde nicht an einem Tag erbaut. Es hatte keine Agenten.*

## Worum es geht

Ein kleiner Skill gegen zu lange Schätzungen. Sprachmodelle haben das Schätzen von Menschen gelernt und rechnen darum aus Gewohnheit in Menschentagen, Wochen und Sprints. Ein Menschentag hat acht Stunden, eine Mittagspause, Besprechungen und ständige Unterbrechungen. Ein Agent baut einen gut beschriebenen Baustein meist in einer halben bis einer Stunde, und mehrere Agenten arbeiten gleichzeitig. Die Schätzung ist dann das Einzige, das noch im Menschentempo läuft.

**Der Anlass:** Ein Plan für vier Baustufen nannte 11 bis 14 „Tage“, insgesamt drei bis vier Wochen. Der Nutzer korrigierte: „Ein Tag ist meist eine Stunde.“ Gebraucht wurden dann rund sechs Stunden Agentenzeit, verteilt auf einen Tag und eine Nacht, mit 475 Tests und einer Abnahme von 42 aus 42. Das war weniger als die Hälfte der korrigierten Schätzung und etwa ein Zwanzigstel der ersten. Die nächste Schätzung am Morgen danach war vermutlich wieder doppelt zu lang.

Der Skill selbst ist englisch (`SKILL.md`). Er gibt fünf feste Wörter vor, die das Modell bei jeder Schätzung der Reihe nach durchgeht. Feste Wörter darum, weil eine Gewohnheit sich von guten Vorsätzen nicht beeindrucken lässt, von einer Checkliste schon eher.

## Die fünf Wörter

| English | Deutsch | Was es heißt |
|---|---|---|
| UNIT | Einheit | In Agentenstunden und -minuten schätzen, nie in Menschentagen, Wochen oder Sprints. |
| COUNT | Zählen | Die Arbeit in Bausteine teilen (bauen, prüfen lassen, testen) und die Bausteine zählen, statt die Summe zu raten. |
| PARALLEL | Parallel | Was nicht voneinander abhängt, läuft gleichzeitig. Die Uhrzeit bestimmt die längste Kette, nicht die Summe. |
| HALVE | Halbieren | Das Ergebnis halbieren. Bisher landete jeder Vergleich bei etwa der Hälfte der schon korrigierten Schätzung. |
| WAIT | Warten | Wartezeiten getrennt nennen: Antworten und Freigaben des Nutzers, andere Sitzungen, Signieren, Downloads, Rechenzeit, Kontingente. Das ist das Lange, nicht das Bauen. |

## Faustregel

| Gewohnheit sagt | stattdessen (nach Einheit und Halbieren) |
|---|---|
| ein Tag | 30 bis 60 Agentenminuten |
| eine Woche | zwei bis drei Stunden |
| drei bis vier Wochen | ein Tag und eine Nacht, dazu die Wartezeit |
| ein Sprint | eine Stufe |
| nach dem Wochenende | noch nichts: erst sagen, worauf man wartet |

## Wann nicht halbieren

- Bei echter Uhrzeit-Arbeit wie Rechenläufen, Downloads oder Ratenlimits. Die gehört mit ihrer echten Dauer unter „Warten“.
- Auf unbekanntem Gelände. Dann sagt man, dass man noch nicht schätzen kann, und schätzt den ersten Schritt, der es zeigen wird.
- Bei Unumkehrbarem wie Migration, Löschen oder Veröffentlichen. Das Bauen geht schnell, die Sorgfalt drumherum braucht Zeit.

## Einrichten

Den Ordner `rome-in-a-day` unverändert nach `~/.claude/skills/rome-in-a-day/` legen (unter Windows `%USERPROFILE%\.claude\skills\rome-in-a-day\`). Er wird beim nächsten Start geladen.

*Von Falzbein, November 2026. MIT-Lizenz.*
