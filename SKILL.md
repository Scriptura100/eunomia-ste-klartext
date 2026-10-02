---
name: eunomia-ste-klartext
description: 'Schreibt und überarbeitet Texte im Stil "80 Prozent ASD-STE100" (Simplified Technical English): Kernregeln streng, Rest gelockert, für Deutsch und Englisch, mit Strengestufen 60/80/100, Konformitätsquote und Glossarprüfung. Kurze Sätze, ein Gedanke pro Satz, Aktiv, Befehlsform für Anweisungen, ein Begriff pro Sache, kein Nominalstil, Warnungen zuerst. Aktivieren IMMER bei STE, STE100, ASD-STE100, Simplified Technical English, kontrollierter Sprache, "80 Prozent STE", oder wenn eine Anleitung, SOP, Arbeitsanweisung, Sicherheitshinweis, Checkliste oder Prozessbeschreibung klar und missverständnisfrei geschrieben oder umgeschrieben werden soll, auch bei "verständlich für Nicht-Muttersprachler" oder "so, dass es keiner falsch versteht". NICHT für Leichte Sprache, rhetorische Veredelung (apollon-rhetorik-veredelung), Entschematisieren (hephaistos-anti-ai-writing) oder reine Textmessung (aristarchos-textpruefstand). Auch bei „Eunomia".'
---

# Eunomia — Klartext nach 80 Prozent ASD-STE100

ASD-STE100 ist die kontrollierte Sprache der Luftfahrt-Wartung. Ihr Ziel: Ein Leser versteht jeden Satz beim ersten Lesen genau einmal und genau richtig — auch unter Stress, auch als Nicht-Muttersprachler, auch nach maschineller Übersetzung.

"80 Prozent" heißt hier: Die Regeln, die den größten Teil der Verständlichkeit tragen, gelten hart. Die Regeln, die vor allem Wartungshandbüchern dienen und normale Texte steif machen, gelten weich. Der Text soll eindeutig sein, aber nicht wie ein Flugzeughandbuch klingen.

## Strengestufen

Standard ist Stufe 80. Nennt der Nutzer eine andere Stufe oder passt die Textart klar zu einer anderen, nimm diese.

| Stufe | Wofür | Was gilt |
|---|---|---|
| **60** | Blog, E-Mail, Infotext, Präsentation | Harte Regeln H1–H6 und H12. Satzlänge 25/30. H7–H11 nur als Empfehlung. Alle weichen Regeln gelockert. |
| **80** | Standard: SOP, Prozess, Anleitung, Fachtext | Alle harten Regeln H1–H12, weiche Regeln W1–W8 wie unten beschrieben. |
| **100** | Wartung, Sicherheit, Übersetzung, Luftfahrt | Volles STE100-Niveau: kein Passiv, keine -ing-Formen außer Fachbegriffen, keine vagen Wörter, keine Modalpartikeln, Wortliste verbindlich, höchstens 6 Sätze pro Absatz. Englisch: Wenn der Nutzer das offizielle STE100-Wörterbuch hat, gilt es vor der Wortliste. |

Zwei Kennzahlen machen die Stufe messbar (Skript, Schritt 5):
- **Stufenquote:** Anteil der Sätze ohne harten Verstoß gegen die gewählte Stufe. Ziel: mindestens 95 %. Darunter nacharbeiten.
- **STE-Nähe:** Anteil der Sätze ohne harten Verstoß gegen Stufe 100. Richtwerte: Stufe 60 etwa 40–70 %, Stufe 80 etwa 70–90 %, Stufe 100 mindestens 95 %. Ein Wert über dem Richtwert ist unkritisch. Ein Wert darunter heißt: Der Text ist lockerer als bestellt.

## Ablauf

1. **Sprache und Textart klären.** Deutsch oder Englisch? Schreibt der Nutzer Deutsch, schreibe Deutsch. Dann die Textart bestimmen:
   - **Anweisend** (Anleitung, SOP, Checkliste, Sicherheitshinweis): Der Leser soll etwas tun.
   - **Beschreibend** (Funktionsbeschreibung, Prozess, Erklärung, Info-Text, E-Mail): Der Leser soll etwas verstehen.
   Mischtexte: Teile trennen und je Teil die passenden Regeln anwenden.
2. **Inhalt sichern.** Bei Umschreibungen: Kein Fakt geht verloren, kein Fakt kommt dazu. Mehrdeutige Stellen im Original nicht still auflösen — beim Nutzer nachfragen oder im Text markieren mit `[UNKLAR: …]`.
3. **Terminologie festlegen (Glossar).** Für jede Sache, jedes Bauteil, jede Rolle genau einen Begriff wählen. Hat der Nutzer ein Glossar oder eine Terminologieliste, gilt diese. Sonst bei Texten ab etwa 150 Wörtern oder bei Umschreibungen ein Glossar anlegen: Vorlage `references/glossar-vorlage.txt`, eine Zeile pro Sache im Format `Vorzugsbegriff: Synonym1, Synonym2`. Die Synonyme stammen aus dem Ausgangstext oder sind naheliegende Varianten. Das Glossar auf Wunsch mit ausgeben, damit der Nutzer es wiederverwenden kann.
4. **Schreiben** nach den harten und weichen Regeln unten.
5. **Prüfen.** Das Skript `scripts/ste_check.py` misst Satzlängen, prüft die Regeln der gewählten Stufe, meldet Glossar-Synonyme und berechnet Stufenquote und STE-Nähe. Aufruf:
   ```bash
   python3 scripts/ste_check.py text.txt --lang de --typ anweisend --stufe 80 --glossar glossar.txt
   ```
   `✗` ist ein harter Verstoß und zählt für die Quote. `?` ist ein Hinweis. `--nur-hart` blendet Hinweise aus. Liegt die Stufenquote unter 95 %, die markierten Sätze überarbeiten und erneut prüfen. Das Skript ist eine Heuristik, kein Parser: Fehlalarme (etwa "werden" als Zukunft statt Passiv) begründet übergehen.
6. **Ausgeben.** Den fertigen Text, darunter eine Zeile mit Stufe, Stufenquote und STE-Nähe. Mehr nur auf Wunsch: Glossar, Liste der wichtigsten Änderungen.

## Harte Regeln (immer einhalten)

Diese Regeln tragen den Kern von STE100. Ein Verstoß ist nur erlaubt, wenn der Nutzer es ausdrücklich will. Die Tabelle "Strengestufen" sagt, welche Regeln auf Stufe 60 nur Empfehlung sind.

**Satz**
- **H1 — Satzlänge.** Anweisend: höchstens 20 Wörter pro Satz. Beschreibend: höchstens 25 Wörter. Ziel liegt darunter (anweisend 10–14, beschreibend 12–20). Nicht zerhacken: Beschreibende Texte aus lauter Fünf-Wort-Sätzen sind kein STE, sondern Stakkato. Gehören Ursache und Folge oder Ort und Zeit zusammen, bleiben sie in einem Satz.
- **H2 — Ein Gedanke pro Satz.** Ein Satz, eine Aussage. Zwei Aussagen ergeben zwei Sätze.
- **H3 — Eine Handlung pro Anweisung.** Ausnahme: Zwei Handlungen finden gleichzeitig statt ("Halte den Hebel gedrückt und drehe das Ventil.").
- **H4 — Bedingung zuerst.** "Wenn die Lampe rot leuchtet, stoppe die Anlage." Nicht umgekehrt.
- **H5 — Aktiv.** In anweisenden Texten nie Passiv. In beschreibenden Texten Passiv nur nach W2.
- **H6 — Anweisungen als Befehl.** Englisch: Imperativ ("Remove the cover."). Deutsch: Imperativ in einer festen Anredeform ("Entfernen Sie die Abdeckung.") oder Infinitiv ("Abdeckung entfernen."). Eine Form wählen und durchhalten.

**Wort**
- **H7 — Ein Wort, eine Bedeutung. Eine Sache, ein Wort.** Keine Synonyme zur Abwechslung. Wer "Pumpe" schreibt, schreibt nicht später "Aggregat". Das Glossar (Schritt 3) hält das fest, das Skript prüft es auf allen Stufen.
- **H8 — Keine Wortstapel.** Englisch: höchstens drei Nomen in Folge ("hydraulic pump pressure" ist das Maximum). Deutsch: Komposita mit mehr als drei Gliedern auflösen ("Hydraulikpumpendruckbegrenzungsventil" → "Druckbegrenzungsventil der Hydraulikpumpe").
- **H9 — Verben statt Nomen.** Kein Nominalstil, keine Funktionsverbgefüge. "Die Durchführung der Prüfung erfolgt" → "Prüfe …". "zur Anwendung bringen" → "anwenden". "make an adjustment" → "adjust".
- **H10 — Artikel nicht weglassen.** "Remove the cover", nicht "Remove cover". Deutsch analog, außer im gewählten Infinitivstil ("Abdeckung entfernen.").
- **H11 — Konkret statt vage.** Zahlen, Einheiten, Namen. "ausreichend fest" → "mit 12 Nm". Fehlt der Wert, `[WERT FEHLT]` setzen, nicht erfinden.

**Sicherheit**
- **H12 — Warnungen zuerst und als Befehl.** Ein Sicherheitshinweis steht vor dem Schritt, für den er gilt. Er beginnt mit einem klaren Befehl. Danach folgt kurz der Grund. "Trennen Sie die Anlage vom Netz. Sonst besteht Lebensgefahr durch Stromschlag."

## Weiche Regeln (das gelockerte 20 Prozent)

Hier weicht Eunomia bewusst vom vollen STE100 ab. Die Grenze: Die Lockerung darf nie Eindeutigkeit kosten.

- **W1 — Kein festes Wörterbuch.** STE100 erlaubt nur rund 900 freigegebene Wörter. Eunomia erlaubt jedes gebräuchliche Wort. Regel: Wähle das einfachste, häufigste Wort, das die Sache genau trifft. Die Ersatzlisten in `references/regeln.md` und `references/wortliste-de.txt` / `wortliste-en.txt` helfen. Auf Stufe 100 ist die Wortliste verbindlich.
- **W2 — Passiv in Beschreibungen.** Erlaubt, wenn der Handelnde unbekannt oder unwichtig ist ("Das Ventil wird werkseitig eingestellt."). Sonst Aktiv.
- **W3 — Zeitformen.** STE100 erlaubt nur einfache Zeiten. Eunomia erlaubt auch Perfekt und Konjunktiv, wenn der Inhalt sie braucht. Keine Zeitform-Ketten wie "hätte sein können".
- **W4 — -ing-Formen (Englisch).** STE100 verbietet sie fast ganz. Eunomia erlaubt feste Fachbegriffe ("bearing", "housing", "training") und Gerundien als Satzsubjekt, wenn sie eindeutig sind. Partizipialkonstruktionen bleiben verboten ("Having removed the cover, …").
- **W5 — Erweiterte Partizipialattribute (Deutsch).** Kurze sind erlaubt ("das geöffnete Ventil"). Lange werden aufgelöst ("das von der Steuerung im Notfall automatisch geschlossene Ventil" → "das Ventil. Die Steuerung schließt es im Notfall automatisch.").
- **W6 — Absatzlänge.** STE100: höchstens sechs Sätze pro Absatz. Eunomia: Richtwert sechs, bis acht erlaubt, wenn der Absatz ein Thema hat.
- **W7 — Ton.** Höflichkeitsformen, Übergänge und ein kurzer Einleitungssatz sind erlaubt. Der Text darf menschlich klingen. Füllwörter, Modalpartikeln ("ja", "eben", "halt") und Floskeln bleiben draußen.
- **W8 — Fachbegriffe.** Jeder Fachbegriff des Fachgebiets ist erlaubt (STE100 nennt das "technical names"). Beim ersten Auftreten unklarer Begriffe kurz erklären, wenn die Zielgruppe gemischt ist.

## Struktur

- **Anweisende Texte:** Nummerierte Schritte. Pro Schritt ein Satz, höchstens zwei. Warnungen als eigener Block vor dem Schritt. Ergebnisse nach dem Schritt als eigener Satz ("Die grüne Lampe leuchtet.").
- **Beschreibende Texte:** Wichtigste Information zuerst. Ein Thema pro Absatz. Der erste Satz des Absatzes sagt, worum es geht.
- **Listen** statt Aufzählungen im Fließtext, wenn es mehr als drei gleichrangige Punkte sind.

## Beispiele

**Deutsch, anweisend**

Vorher:
> Nachdem die Abdeckung, welche mit vier Schrauben befestigt ist, entfernt wurde, sollte die Überprüfung des Filters auf eventuell vorhandene Verschmutzungen durchgeführt und dieser gegebenenfalls ersetzt werden.

Nachher:
> 1. Lösen Sie die vier Schrauben der Abdeckung.
> 2. Entfernen Sie die Abdeckung.
> 3. Prüfen Sie den Filter auf Schmutz.
> 4. Wenn der Filter verschmutzt ist, ersetzen Sie ihn.

**Englisch, Warnung**

Vorher:
> Care should be taken when working on the system, as residual pressure may be present even after shutdown, which could result in injury.

Nachher:
> WARNING: Release the pressure before you work on the system. The system can keep pressure after shutdown. This pressure can cause injury.

**Deutsch, beschreibend**

Vorher:
> Die Implementierung des neuen Freigabeprozesses erfolgt mit dem Ziel der Gewährleistung einer Reduktion der Durchlaufzeiten bei gleichzeitiger Sicherstellung der Qualitätsanforderungen.

Nachher:
> Wir führen einen neuen Freigabeprozess ein. Er soll Anträge schneller bearbeiten. Die Qualität bleibt dabei gleich.

## Referenzen

- `references/regeln.md` — Ersatzlisten (Deutsch und Englisch) für Nominalstil, Funktionsverbgefüge, vage Wörter und typische STE-Ersetzungen. Lesen, wenn du einen Text umschreibst oder unsicher bist, welches Wort einfacher ist.
- `references/wortliste-de.txt`, `references/wortliste-en.txt` — maschinenlesbare Ersatzlisten fürs Skript (eigene Zusammenstellung, kein Auszug aus der STE100-Spezifikation). Erweiterbar im Format `zu meiden > Ersatz`.
- `references/glossar-vorlage.txt` — Vorlage für Projekt- oder Kundenglossare.
- `scripts/ste_check.py` — Prüfskript mit Stufen, Stufenquote, STE-Nähe und Glossarprüfung.
