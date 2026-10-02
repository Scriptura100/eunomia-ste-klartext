# Eunomia – Klartext nach 80 Prozent ASD-STE100

Ein Skill für Claude, der Texte im Stil „80 Prozent ASD-STE100“ (Simplified Technical English) schreibt und überarbeitet, für Deutsch und Englisch.

ASD-STE100 ist die kontrollierte Sprache der Luftfahrt-Wartung. „80 Prozent“ heißt: Die Regeln, die die Verständlichkeit tragen, gelten hart. Die Regeln, die vor allem Wartungshandbüchern dienen, gelten weich. Der Text soll eindeutig sein, aber nicht wie ein Flugzeughandbuch klingen.

## Hintergrund

Andrej Karpathy empfahl am 2. Oktober 2026 auf X, sich Antworten von Sprachmodellen in ASD-STE100 erklären zu lassen. Er beschreibt die Spezifikation als kontrollierte Sprache, die ursprünglich für die Dokumentation von Luftfahrt-Wartung entstand. Ihre strengen Regeln für einen klaren Schreibstil findet er oft lesbarer. Weil die Spezifikation sehr streng ist, bat er teils um „80% of the way to ASD-STE100“. Dieser Skill geht auf diesen Beitrag zurück. Er setzt die Abstufung als feste Stufen um (60, 80, 100) und macht sie mit einem Prüfskript messbar.

Quelle: [Andrej Karpathy auf X, 2. Oktober 2026](https://x.com/karpathy/status/2105819303471976479)

## Was der Skill kann

- Strengestufen 60, 80 und 100 mit Konformitätsquote und STE-Nähe
- Kurze Sätze, ein Gedanke pro Satz, Aktiv, Befehlsform für Anweisungen, ein Begriff pro Sache, Warnungen zuerst
- Glossarprüfung und Wortlisten für Deutsch und Englisch
- Geeignet für Anleitungen, Arbeitsanweisungen, Sicherheitshinweise, Checklisten und Prozessbeschreibungen

Nicht gedacht ist er für Leichte Sprache.

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

## Inhalt

| Datei | Zweck |
|---|---|
| `SKILL.md` | Die Skill-Anweisung für Claude |
| `references/regeln.md` | Die Regeln im Einzelnen |
| `references/wortliste-de.txt`, `references/wortliste-en.txt` | Wortlisten |
| `references/glossar-vorlage.txt` | Vorlage für ein eigenes Glossar |
| `scripts/ste_check.py` | Prüfskript (Python 3, nur Standardbibliothek) |

## Benutzung

Den Ordner als Skill einbinden, zum Beispiel für Claude Code nach `~/.claude/skills/eunomia-ste-klartext/` kopieren. Das Prüfskript läuft auch allein:

```
python3 scripts/ste_check.py text.txt --lang de --typ anweisend --stufe 80
```

Das Skript ist eine Heuristik, kein Parser. Jede Markierung selbst bewerten.

## Lizenz

MIT-Lizenz, siehe [LICENSE](LICENSE). © 2026 URWORTE | Nils Brauer
