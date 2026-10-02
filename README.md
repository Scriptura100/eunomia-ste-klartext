# Eunomia – Klartext nach 80 Prozent ASD-STE100

Ein Skill für Claude, der Texte im Stil „80 Prozent ASD-STE100“ (Simplified Technical English) schreibt und überarbeitet, für Deutsch und Englisch.

ASD-STE100 ist die kontrollierte Sprache der Luftfahrt-Wartung. „80 Prozent“ heißt: Die Regeln, die die Verständlichkeit tragen, gelten hart. Die Regeln, die vor allem Wartungshandbüchern dienen, gelten weich. Der Text soll eindeutig sein, aber nicht wie ein Flugzeughandbuch klingen.

## Beispiel

Eine Wartungsanweisung, deutsch, Stufe 80.

**Vorher**

> Nachdem die Abdeckung, welche mit vier Schrauben befestigt ist, entfernt wurde, sollte die Überprüfung des Filters auf eventuell vorhandene Verschmutzungen durchgeführt und dieser gegebenenfalls ersetzt werden.

**Nachher**

> 1. Lösen Sie die vier Schrauben der Abdeckung.
> 2. Entfernen Sie die Abdeckung.
> 3. Prüfen Sie den Filter auf Schmutz.
> 4. Wenn der Filter verschmutzt ist, ersetzen Sie ihn.

Gemessen mit `scripts/ste_check.py` (Stufe 80, Textart anweisend):

| | Vorher | Nachher |
|---|---:|---:|
| Sätze | 1 | 4 |
| Wörter je Satz (Durchschnitt) | 26 | 7,2 |
| Stufenquote (Ziel mindestens 95 %) | 0 % | 100 % |

Das Skript markiert im Ausgangssatz zwei harte Verstöße: 26 statt höchstens 20 Wörter und Passiv. Dazu kommen Hinweise auf Nominalstil („Überprüfung“, „Verschmutzungen“), vage Wörter („eventuell“, „gegebenenfalls“, „sollte“) und einen Schachtelsatz. Im Ergebnis stehen vier Schritte mit je einer Handlung, die Bedingung steht vorn und das Verb im Imperativ.

Das Beispiel besteht aus einem einzelnen Satz, die Quote ist deshalb grob. Bei längeren Texten liegt sie dazwischen.

## Was der Skill kann

- Kurze Sätze, ein Gedanke pro Satz, Aktiv, Befehlsform für Anweisungen, ein Begriff pro Sache, Warnungen zuerst
- Drei Strengestufen mit Stufenquote und STE-Nähe als Kennzahlen
- Glossarprüfung und Wortlisten für Deutsch und Englisch
- Geeignet für Anleitungen, Arbeitsanweisungen, Sicherheitshinweise, Checklisten und Prozessbeschreibungen

### Die drei Stufen

Standard ist Stufe 80. Wer nichts anderes verlangt, bekommt sie.

| Stufe | Wofür | Was gilt |
|---|---|---|
| **60** | Blog, E-Mail, Infotext, Präsentation | Die Regeln für Satzbau und Warnungen gelten hart, Sätze bis 25 beziehungsweise 30 Wörter. Die Regeln für Wortwahl sind nur Empfehlung. |
| **80** | Anleitung, SOP, Prozess, Fachtext | Alle harten Regeln, auch zur Wortwahl (ein Begriff pro Sache, kein Nominalstil). Die weichen Regeln sind gelockert. |
| **100** | Wartung, Sicherheit, Übersetzung, Luftfahrt | Volles STE100-Niveau: kein Passiv, keine vagen Wörter, verbindliche Wortliste, höchstens sechs Sätze pro Absatz. |

## Benutzung

Den Ordner als Skill einbinden, zum Beispiel für Claude Code nach `~/.claude/skills/eunomia-ste-klartext/` kopieren. Danach genügt ein Auftrag wie:

- „Schreibe diese Anleitung nach Eunomia um, Stufe 80.“
- „Prüfe diesen Text nach STE100 und nenne die Stufenquote.“
- „Überarbeite diese Sicherheitshinweise auf Stufe 100.“

Claude gibt den fertigen Text aus und darunter eine Zeile mit Stufe, Stufenquote und STE-Nähe. Auf Wunsch gibt er außerdem das Glossar und die wichtigsten Änderungen aus.

Das Prüfskript läuft auch allein:

```
python3 scripts/ste_check.py text.txt --lang de --typ anweisend --stufe 80
```

## Inhalt

| Datei | Zweck |
|---|---|
| `SKILL.md` | Die Skill-Anweisung für Claude |
| `references/regeln.md` | Die Regeln im Einzelnen |
| `references/wortliste-de.txt`, `references/wortliste-en.txt` | Wortlisten (eigene Zusammenstellung) |
| `references/glossar-vorlage.txt` | Vorlage für ein eigenes Glossar |
| `scripts/ste_check.py` | Prüfskript (Python 3, nur Standardbibliothek) |

## Grenzen

- **Eunomia ist nicht ASD-STE100.** Der Skill verwendet kein freigegebenes Wörterbuch mit rund 900 Wörtern, sondern erlaubt jedes gebräuchliche Wort und empfiehlt das einfachste. Die Wortlisten sind eine eigene Zusammenstellung, kein Auszug aus der Spezifikation.
- **Deutsch ist nicht Teil von ASD-STE100.** Die deutschen Regeln übertragen die Ziele auf deutsche Grammatik, etwa auf Nominalstil, Satzklammer und Komposita.
- **Das Prüfskript ist eine Heuristik, kein Parser.** Jede Markierung selbst bewerten. Fehlalarme sind möglich.
- **Nicht für Leichte Sprache gedacht.**

ASD-STE100 ist eine Spezifikation der ASD. Dieses Projekt ist nicht mit der ASD verbunden und nicht von ihr geprüft oder gebilligt.

## Hintergrund

Andrej Karpathy empfahl am 2. Oktober 2026 auf X, sich Antworten von Sprachmodellen in ASD-STE100 erklären zu lassen, weil die strengen Stilregeln oft lesbarer seien. Weil die Spezifikation sehr streng ist, bat er teils um „80% of the way to ASD-STE100“. Dieser Skill geht auf diesen Beitrag zurück. Er setzt die Abstufung als feste Stufen um (60, 80, 100) und macht sie mit einem Prüfskript messbar.

Quelle: [Andrej Karpathy auf X, 2. Oktober 2026](https://x.com/karpathy/status/2105819303471976479)

## Lizenz

MIT-Lizenz, siehe [LICENSE](LICENSE). © 2026 URWORTE | Nils Brauer
