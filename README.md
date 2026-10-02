# Eunomia – Klartext nach 80 Prozent ASD-STE100

Ein Skill für Claude, der Texte im Stil „80 Prozent ASD-STE100“ (Simplified Technical English) schreibt und überarbeitet, für Deutsch und Englisch.

ASD-STE100 ist die kontrollierte Sprache der Luftfahrt-Wartung. „80 Prozent“ heißt: Die Regeln, die die Verständlichkeit tragen, gelten hart. Die Regeln, die vor allem Wartungshandbüchern dienen, gelten weich. Der Text soll eindeutig sein, aber nicht wie ein Flugzeughandbuch klingen.

## Was der Skill kann

- Strengestufen 60, 80 und 100 mit Konformitätsquote und STE-Nähe
- Kurze Sätze, ein Gedanke pro Satz, Aktiv, Befehlsform für Anweisungen, ein Begriff pro Sache, Warnungen zuerst
- Glossarprüfung und Wortlisten für Deutsch und Englisch
- Geeignet für Anleitungen, Arbeitsanweisungen, Sicherheitshinweise, Checklisten und Prozessbeschreibungen

Nicht gedacht ist er für Leichte Sprache.

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
