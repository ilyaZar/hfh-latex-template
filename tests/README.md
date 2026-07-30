# Visueller Vergleich mit einer Bachelorarbeit

Dieser Test vergleicht ausgewählte Passagen aus
`1127501_WB00-BAC-PB1-260630.pdf` mit der unveränderten Formatierung der
produktiven LaTeX-Vorlage. Die Passagen wurden in `main.tex` neu gesetzt.

Die Testdatei verändert die produktive `../main.tex` nicht. Zwischen den beiden
Seiten eines Vergleichsfalls gibt es keinen erzwungenen Seitenumbruch. Die
Seitengrenze entsteht daher aus dem Satz der Vorlage.

## Seitenzuordnung

| Fall | Inhalt                              | Original | Test |
|------|-------------------------------------|---------:|-----:|
| A    | Kapitelbeginn und Abschnitt 1.1     |      6-7 |  1-3 |
| B    | Reiner Fließtext                    |    18-19 |  4-5 |
| C    | Zwei Unterkapitel und Fließtext     |    20-21 |  6-8 |
| D    | Kapitel mit drei Gliederungsebenen  |    34-35 | 9-10 |

Die konkreten Paare für die manuelle Kontrolle sind:

- Original 6 und Test 1
- Original 7 und Test 2
- Fortsetzung von Original 7 und Test 3
- Original 18 und Test 4
- Original 19 und Test 5
- Original 20 und Test 6
- Original 21 und Test 7
- Fortsetzung von Original 21 und Test 8
- Original 34 und Test 9
- Original 35 und Test 10

## Wichtiger Befund zum PDF-Container

Die angehängte PDF besteht nicht durchgehend aus A4-Seiten:

- Seite 1: A4 mit 595 x 842 Punkt
- Seiten 2-55: US Letter mit 612 x 792 Punkt
- Seite 56: A4 mit 595 x 842 Punkt

PDF24 hat den ursprünglich erkennbaren A4-Inhalt der Seiten 2-55 mit dem
Faktor 0,9406 auf Letter verkleinert und horizontal zentriert. Das lässt sich
aus Schriftgrößen, Rändern und Koordinaten eindeutig zurückrechnen.

Deshalb gibt es zwei Arten von Vergleichsbildern:

- `compare-*`: tatsächliche Seitencontainer aus der gelieferten PDF
- `normalized-compare-*`: Letter-Verkleinerung rückgängig gemacht, links und
  rechts wieder im gleichen A4-Maßstab

In jedem Bild steht das Original links und die Test-PDF rechts.

## Messwerte

| Merkmal                 | Original roh | Original auf A4 | Test     |
|-------------------------|-------------:|----------------:|---------:|
| Seitenformat            | 612 x 792 pt | 595 x 842 pt    | A4       |
| Fließtext               | 11,26 pt     | 11,97 pt        | 11,96 pt |
| Hauptüberschrift        | 13,17 pt     | 14,00 pt        | 13,95 pt |
| Kopf-/Fußzeile          | 9,34 pt      | 9,93 pt         | 9,96 pt  |
| Linke Textkante         | 105,84 pt    | 84,70 pt        | 85,04 pt |
| Grundlinienabstand      | 19,44 pt     | 20,67 pt        | 20,70 pt |
| Zusätzlicher Absatzraum | ca. 5,7 pt   | ca. 6,1 pt      | ca. 6 pt |

Nach der A4-Normalisierung stimmen Seitenränder, Schriftgrößen,
Grundlinienabstand, Absatzabstand und Kopfzeilenposition sehr gut überein.

## Ergebnis mit der aktuellen Vorlage

Die Seiten sind nicht exakt identisch.

Der übernommene Text wurde unabhängig vom Umbruch normalisiert und verglichen.
Alle vier Originalpassagen stimmen vollständig mit der Testdatei überein. Bei
den Fällen A, C und D enthält die Testdatei nur wenige zusätzliche Wörter, um
den letzten begonnenen Absatz sauber zu beenden.

Von 252 sichtbaren Originalzeilen stimmen 90 Zeilen in einer
reihenfolgetreuen Zuordnung vollständig mit dem aktuellen Testsatz überein.
Die geringe Quote ist keine Bewertung der inhaltlichen Qualität. Sie zeigt,
dass Wort- und Seitenumbrüche nicht reproduziert werden.

Beispiele:

- Der Seitenabschluss von Originalseite 6 wird nahezu getroffen.
- Der Inhalt von Originalseite 18 reicht in der Test-PDF weiterhin nur über
  einen Teil von Testseite 4.
- Fall C benötigt in der Test-PDF drei statt zwei Seiten. Neben den
  Schriftmetriken wirken sich hier auch die Überschriftenabstände aus.

## Potenzielle Anpassungen

Die folgenden Änderungen wurden nur in temporären Experimenten getestet. Sie
sind nicht in die produktive Vorlage und nicht in die finale Test-PDF
übernommen worden.

### 1. Schriftmetriken

Im Original ist Times New Roman eingebettet. Die Vorlage verwendet
TeX Gyre Termes X über `newtxtext`. Größe und Erscheinungsbild sind sehr
ähnlich, die Zeichenbreiten sind aber nicht vollständig gleich.

Für pixelgenaue Word-Reproduktion wäre Times New Roman mit LuaLaTeX oder
XeLaTeX zu testen. Tabelle 1 nennt die konkrete Schrift jedoch nur als
Empfehlung. Ein Compilerwechsel ist deshalb derzeit nicht zu empfehlen.

### 2. Überschriftenabstände

Der sichtbare Abstand nach einer Abschnittsüberschrift beträgt im
normalisierten Original ungefähr 14 Punkt, im aktuellen Testsatz etwa
24 Punkt. Kleinere Werte für `afterskip` könnten das Word-Erscheinungsbild
annähern.

Tabelle 1 macht zu diesen Abständen keine Vorgabe. Eine Änderung sollte daher
erst gegen die offizielle Word-Formatvorlage und nicht nur gegen diese
Bachelorarbeit geprüft werden.

### 3. Fußzeilenposition

Die Bachelorarbeit richtet „Seite x von 55“ rechts aus. Die LaTeX-Vorlage
zentriert die Seitenangabe. Tabelle 1 schreibt keine Position vor. Dies ist
daher kein belastbarer Änderungsgrund.

## Nicht zu ändernde Punkte

Der Vergleich bestätigt folgende Einstellungen der LaTeX-Vorlage:

- A4-Hochformat
- linker Rand 3 cm und rechter Rand 4 cm
- 12-Punkt-Fließtext und 14-Punkt-Hauptüberschriften
- 10-Punkt-Kopf- und Fußzeilen
- ungefähr 6 Punkt Abstand zwischen Absätzen
- Name links und Matrikelnummer rechts in der Kopfzeile

## Übernommene Anpassungen

- `\setstretch{1.43}` bildet den 1,5-zeiligen Grundlinienabstand der
  Word-Vorlage mit etwa 20,7 Punkt nach.
- Der Verzicht auf `microtype` vermeidet die in Word nicht vorhandene
  Zeichenexpansion und optische Randausrichtung.

## Test ausführen

Aus dem Verzeichnis `tests/`:

```bash
latexmk -pdf -jobname=bachelor-layout-comparison main.tex
python3 compare_lines.py
```

Die finale PDF ist `bachelor-layout-comparison.pdf`.

## Screenshots

### Tatsächlicher PDF-Container

- [Original 6 / Test 1][raw-006-001]
- [Original 7 / Test 2][raw-007-002]
- [Original 7 / Test 3][raw-007-003]
- [Original 18 / Test 4][raw-018-004]
- [Original 19 / Test 5][raw-019-005]
- [Original 20 / Test 6][raw-020-006]
- [Original 21 / Test 7][raw-021-007]
- [Original 21 / Test 8][raw-021-008]
- [Original 34 / Test 9][raw-034-009]
- [Original 35 / Test 10][raw-035-010]

### Auf A4 normalisiertes Original

- [Original 6 / Test 1][norm-006-001]
- [Original 7 / Test 2][norm-007-002]
- [Original 7 / Test 3][norm-007-003]
- [Original 18 / Test 4][norm-018-004]
- [Original 19 / Test 5][norm-019-005]
- [Original 20 / Test 6][norm-020-006]
- [Original 21 / Test 7][norm-021-007]
- [Original 21 / Test 8][norm-021-008]
- [Original 34 / Test 9][norm-034-009]
- [Original 35 / Test 10][norm-035-010]

[raw-006-001]: screenshots/compare-original-006-test-001.png
[raw-007-002]: screenshots/compare-original-007-test-002.png
[raw-007-003]: screenshots/compare-original-007-test-003.png
[raw-018-004]: screenshots/compare-original-018-test-004.png
[raw-019-005]: screenshots/compare-original-019-test-005.png
[raw-020-006]: screenshots/compare-original-020-test-006.png
[raw-021-007]: screenshots/compare-original-021-test-007.png
[raw-021-008]: screenshots/compare-original-021-test-008.png
[raw-034-009]: screenshots/compare-original-034-test-009.png
[raw-035-010]: screenshots/compare-original-035-test-010.png
[norm-006-001]: screenshots/normalized-compare-original-006-test-001.png
[norm-007-002]: screenshots/normalized-compare-original-007-test-002.png
[norm-007-003]: screenshots/normalized-compare-original-007-test-003.png
[norm-018-004]: screenshots/normalized-compare-original-018-test-004.png
[norm-019-005]: screenshots/normalized-compare-original-019-test-005.png
[norm-020-006]: screenshots/normalized-compare-original-020-test-006.png
[norm-021-007]: screenshots/normalized-compare-original-021-test-007.png
[norm-021-008]: screenshots/normalized-compare-original-021-test-008.png
[norm-034-009]: screenshots/normalized-compare-original-034-test-009.png
[norm-035-010]: screenshots/normalized-compare-original-035-test-010.png
