# HFH-LaTeX-Vorlage

Minimalistische LaTeX-Vorlage für wissenschaftliche Arbeiten an der HFH
Hamburger Fern-Hochschule, primär auf Deutsch und optional auf Englisch.

**Autor und aktueller Maintainer:** Ilya Zarubin, 2026

[In Overleaf öffnen](https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fgithub.com%2FilyaZar%2Fhfh-latex-template%2Farchive%2Frefs%2Fheads%2Fmain.zip&engine=pdflatex&main_document=main.tex)

> [!WARNING] Diese Vorlage ersetzt nicht die jeweils aktuellen offiziellen
> Regelungen. Sie erhebt keinen Anspruch auf Vollständigkeit, Fehlerfreiheit
> oder dauerhafte Übereinstimmung mit allen studiengangsspezifischen
> HFH-Regelungen. Vor jeder Verwendung und insbesondere vor jeder Abgabe sind
> die aktuellen Vorgaben der HFH für Seminar-, Haus-, Bachelor- und
> Masterarbeiten zu prüfen. Bei Abweichungen gelten die offiziellen Vorgaben der
> HFH, des Prüfungsamts und der betreuenden beziehungsweise prüfenden Personen.

Die Vorlage wurde anhand der HFH-Formatvorgaben erstellt. Allgemeine Anleitungen
und Beispiele aus der offiziellen Word-Vorlage sind enthalten; Word-spezifische
Bedienhinweise wurden sachlogisch für LaTeX und Overleaf angepasst. Die
Quelldokumente selbst sind nicht Bestandteil der öffentlichen Vorlage und werden
nicht weiterverteilt.

## Schnellstart

1. Den Metadatenblock am Anfang von `main.tex` bearbeiten.
2. `\MainLanguage` auf `ngerman` oder `english` setzen.
3. Für Bachelor- und Seminararbeiten `\IncludeAbstractfalse` setzen.
4. Optionale Verzeichnisse über die Schalter in `main.tex` konfigurieren.
5. Quellen in `references.bib` eintragen und im Text zitieren.
6. Mit `latexmk -pdf main.tex` oder in Overleaf mit pdfLaTeX kompilieren.

Einzelne englische Passagen erhalten mit Babel englische Silbentrennung:

```latex
\begin{otherlanguage}{english}
English text with English hyphenation.
\end{otherlanguage}
```

## Dateistruktur

- `main.tex` enthält Dokumentklasse, Metadaten, Schalter und die geordnete Liste
  aller Dokumentteile.
- `hfh-formatierungen.sty` lädt die benötigten Pakete und enthält sämtliche
  zentralen Formatdefinitionen und Vorlagenbefehle.
- `docs/00-frontmatter.tex` enthält Titelblatt, Abstract und die vorderen
  Verzeichnisse.
- `docs/01-verwendungshinweis.tex` erläutert die Verwendung der Vorlage.
- `docs/02-formale-aspekte.tex` enthält Tabelle 1 und die Formatbeispiele.
- `docs/03-aufbau-wissenschaftlicher-arbeiten.tex` beschreibt den Aufbau.
- `docs/04-verzeichnisse.tex` enthält Quellenverzeichnisse, KI-Verzeichnis und
  Anlagen.
- `docs/05-eigenstaendigkeitserklaerung.tex` enthält den Platzhalter für die
  abschließende Erklärung.
- `references.bib` enthält die Literaturdaten.

`main.tex` bindet alle Dokumentteile mit `\include` ein. Dadurch beginnt jeder
Teil auf einer neuen Seite, erhält eine eigene Hilfsdatei und kann bei Bedarf
mit `\includeonly` ausgewählt werden. Soll ein eigener Teil ohne automatischen
Seitenumbruch unmittelbar im laufenden Text fortgesetzt werden, kann dafür
alternativ `\input` verwendet werden.

## Overleaf

Die Vorlage ist für ein Overleaf-Projekt mit folgenden Einstellungen
vorbereitet:

- Hauptdokument: `main.tex`
- Compiler: pdfLaTeX
- TeX Live: aktuelle von Overleaf angebotene Version
- Bibliografie: BibTeX über `natbib` und `plainnat`

Der Link **In Overleaf öffnen** importiert das über `.gitattributes`
freigegebene Archiv des jeweils aktuellen `main`-Branches als neues
Overleaf-Projekt. Es enthält nur die produktiven Dateien `main.tex`,
`hfh-formatierungen.sty`, `references.bib`, `README.md`, `LICENSE`, die Kapitel
unter `docs/` und die öffentlichen Dateien unter `images/`. Entwicklungsdateien,
CI und Tests werden nicht importiert. Der Link funktioniert, sobald das
Repository als `ilyaZar/hfh-latex-template` öffentlich erreichbar ist.

Eine Einreichung in die Overleaf Gallery ist vorgesehen. Overleaf akzeptiert
offizielle Hochschulvorlagen für Abschlussarbeiten, wenn die Beschreibung auf
die offizielle Hochschulseite mit den Gestaltungs- oder Einreichungsvorgaben
verweist. In der Gallery-Beschreibung sind deshalb die
[Modulhandbücher der Technikstudiengänge im HFH-WebCampus](https://campus.hamburger-fh.de/material/bug-material/fb-technik)
(Anmeldung erforderlich) sowie die öffentlichen
[HFH-Hinweise zur Abschlussarbeit](https://www.hfh-fernstudium.de/blog/abschlussarbeit-so-nimmst-du-die-letzte-huerde-des-studiums)
anzugeben. Die öffentliche HFH-Seite beschreibt auch das Pflichtmodul
`Wissenschaftliches Arbeiten (WSA)`.

## Offizielle Seiten

Die aktuellen Formatvorgaben stehen in den Anhängen der Modulhandbücher der
Technikstudiengänge. Die Modulhandbücher werden im
[HFH-WebCampus](https://campus.hamburger-fh.de/material/bug-material/fb-technik)
bereitgestellt; der Zugriff erfordert ein HFH-Benutzerkonto. Eine öffentliche
Übersicht bietet die Seite zum
[Fachbereich Technik](https://www.hfh-fernstudium.de/fernhochschule-fachbereich-technik).

Bei anmeldepflichtigen Arbeiten stellt das Prüfungsamt nach der bestätigten
Themenanmeldung ein offizielles Titelblatt bereit. Dieses ersetzt das generische
Titelblatt mit:

```latex
\MakeOfficialTitlePage{offizielles-titelblatt.pdf}
```

Die aktuelle Eigenständigkeitserklärung ist unverändert aus dem WebCampus zu
übernehmen. Sie bildet die letzte Seite, erscheint nicht im Inhaltsverzeichnis
und trägt keine sichtbare Seitenzahl. Der Text in `main.tex` ist nur ein
Platzhalter.

## Prüfmatrix zu Tabelle 1

Die folgenden Tabellen geben Tabelle 1 der Word-Vorlage in unveränderter
Reihenfolge und Formulierung wieder. Nur die Spalten `ID` und `Status` wurden
ergänzt. Die Aufteilung nach Hauptpunkten dient der Lesbarkeit.

`V` bedeutet „zwingend einzuhaltende Vorgabe“, `E` bedeutet „Empfehlung“. Der
Status `auto` bezeichnet eine technisch gesetzte Vorgabe. `prüfen` bezeichnet
eine Inhaltsregel: `hfh-formatierungen.sty` und die Dateien unter `docs/`
stellen Befehl, Umgebung und Muster bereit, die Verfasserin oder der Verfasser
muss die konkrete Verwendung aber prüfen.

### A - Seitenformat

| ID  | Hauptpunkte  | Unterpunkte                          | V / E | Status |
| --- | ------------ | ------------------------------------ | ----- | ------ |
| A.1 | Seitenformat | DIN A4, Hochformat                   | V     | auto   |
| A.2 |              | einseitig bedruckt                   | V     | auto   |
| A.3 |              | Ränder: L 3 cm, R: 4 cm, O/U: 2,5 cm | V     | auto   |

### B - Absatzformat

| ID  | Hauptpunkte  | Unterpunkte                                                             | V / E | Status |
| --- | ------------ | ----------------------------------------------------------------------- | ----- | ------ |
| B.1 | Absatzformat | Zeilenabstand 1,5-zeilig                                                | V     | auto   |
| B.2 |              | Blocksatz                                                               | V     | auto   |
| B.3 |              | Abstand zwischen den Absätzen 6 Punkt (neuer Absatz bei neuem Gedanken) | E     | auto   |
| B.4 |              | automatische Silbentrennung                                             | E     | auto   |

### C - Zeichenformat

| ID  | Hauptpunkte   | Unterpunkte                                                                                                                 | V / E | Status |
| --- | ------------- | --------------------------------------------------------------------------------------------------------------------------- | ----- | ------ |
| C.1 | Zeichenformat | gut lesbare Schriftart und Schriftgröße (Empfehlungen: Times New Roman in 12 Punkt, Arial in 11 Punkt, Univers in 11 Punkt) | E     | auto   |
| C.2 |               | Schriftgröße Hauptüberschriften/1. Gliederungsebene 14 - 16 Punkt, Fettdruck (im Textteil, nicht im Inhaltsverzeichnis)     | E     | auto   |
| C.3 |               | Schriftgröße Überschriften ab 2. Gliederungsebene 12 Punkt, Fettdruck                                                       | E     | auto   |

### D - Kopf- / Fußzeilen

| ID  | Hauptpunkte       | Unterpunkte                                      | V / E | Status |
| --- | ----------------- | ------------------------------------------------ | ----- | ------ |
| D.1 | Kopf- / Fußzeilen | Schriftgröße 2 Punkt kleiner als Standardschrift | E     | auto   |
| D.2 |                   | Name/Matrikelnummer im Kopfzeile                 | V     | auto   |

### E - Fußnoten

| ID  | Hauptpunkte | Unterpunkte                                                                                              | V / E | Status |
| --- | ----------- | -------------------------------------------------------------------------------------------------------- | ----- | ------ |
| E.1 | Fußnoten    | Fußnotenzeichen: Schriftgröße 9–10 Punkt hochgestellt                                                    | E     | auto   |
| E.2 |             | Schriftgröße Fußnotentext 2 Punkt kleiner als Standardschrift                                            | V     | auto   |
| E.3 |             | Zeilenabstand innerhalb der Fußnote 1-zeilig                                                             | V     | auto   |
| E.4 |             | Zeilenabstand zwischen den einzelnen Fußnoten 1,5-zeilig (bzw. ca. 4 Punkt Abstand zur nächsten Fußnote) | V     | auto   |
| E.5 |             | fortlaufende Fußnotennummerierung                                                                        | V     | auto   |
| E.6 |             | Fußnote beginnt grundsätzlich mit Großbuchstaben                                                         | V     | prüfen |
| E.7 |             | Punkt am Ende der Fußnote                                                                                | V     | prüfen |

### F - Tabellen

| ID  | Hauptpunkte | Unterpunkte                                                                          | V / E | Status |
| --- | ----------- | ------------------------------------------------------------------------------------ | ----- | ------ |
| F.1 | Tabellen    | Eindeutige Beschriftung, fortlaufende Nummerierung und Quellenangabe                 | V     | prüfen |
| F.2 |             | Schriftgröße von Tabellennummer/-bezeichnung ca. 2 Punkt kleiner als Standardschrift | E     | auto   |
| F.3 |             | Abstand zwischen Bezeichnung und Tabelle ca. 6 Punkt                                 | E     | auto   |
| F.4 |             | Bezug / Verweis im laufenden Text                                                    | V     | prüfen |
| F.5 |             | Zeilenabstand innerhalb einer Tabelle 1-zeilig                                       | E     | auto   |
| F.6 |             | Schriftgröße in der Tabelle i. d. R. 2 Punkt kleiner als Standardschrift             | E     | auto   |
| F.7 |             | Text in Kopfzeile / Randspalte der Tabelle ggf. fett                                 | E     | prüfen |

### G - Abbildungen

| ID  | Hauptpunkte | Unterpunkte                                                                            | V / E | Status |
| --- | ----------- | -------------------------------------------------------------------------------------- | ----- | ------ |
| G.1 | Abbildungen | Eindeutige Beschriftung, fortlaufende Nummerierung und Quellenangabe                   | V     | prüfen |
| G.2 |             | Schriftgröße von Abbildungsnummer/-bezeichnung ca. 2 Punkt kleiner als Standardschrift | E     | auto   |
| G.3 |             | Abstand zwischen Abbildung und Bezeichnung ca. 6 Punkt                                 | E     | auto   |
| G.4 |             | Abstand zwischen Bezeichnung und nachfolgendem Text ca. 12 Punkt                       | E     | auto   |
| G.5 |             | Bezug/Verweis im laufenden Text                                                        | V     | prüfen |
| G.6 |             | Zeilenabstand bei Text innerhalb einer Abbildung 1-zeilig                              | E     | auto   |
| G.7 |             | Schriftgröße in der Abbildung i. d. R. 2 Punkt kleiner als Standardschrift             | E     | auto   |

### H - Formeln

| ID  | Hauptpunkte | Unterpunkte                                                          | V / E | Status |
| --- | ----------- | -------------------------------------------------------------------- | ----- | ------ |
| H.1 | Formeln     | Erstellung mit Formeleditor und mit kapitelorientierter Nummerierung | E     | auto   |

### I - Quellenverzeichnisse

| ID  | Hauptpunkte                                                          | Unterpunkte                                                                                                      | V / E | Status |
| --- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ----- | ------ |
| I.1 | Quellenverzeichnis, Verzeichnis der Gesetze, Rechtsverordnungen etc. | Zeilenabstand innerhalb der Quellenangabe 1-zeilig                                                               | V     | auto   |
| I.2 |                                                                      | Zeilenabstand zwischen den einzelnen Quellen 1,5-zeilig (alternativ: 6 Punkt Abstand zur nächsten Quellenangabe) | V     | auto   |
| I.3 |                                                                      | Sondereinzug: hängend bei 0,5 cm                                                                                 | E     | auto   |
| I.4 |                                                                      | Quellen nach Autor/Herausgeber alphabetisch aufsteigend sortiert                                                 | V     | prüfen |

### LaTeX-Nachweise

Die IDs stehen als Kommentare unmittelbar an den zuständigen Befehlen in
`main.tex`, `hfh-formatierungen.sty` und den Dateien unter `docs/`. Die
wichtigsten Zuordnungen sind:

- A.1-A.3: Klassenoptionen `a4paper`, `oneside` und Paket `geometry`
- B.1-B.4: Klassenstandard Blocksatz, `setspace`, `\parskip` und `babel`
- C.1-C.3: 12-pt-Klasse, `newtx` und KOMA-Schriftdefinitionen
- D.1-D.2: `scrlayer-scrpage`, 10-pt-Schrift, `\ihead` und `\ohead`
- E.1-E.5: `\HFHFootnoteMark`, `\deffootnote`, `\footnotesep` und
  `\counterwithout`
- E.6-E.7: kommentierte Musterfußnote als obligatorische Inhaltsprüfung
- F.1-F.7: `caption`, `hfhtable`, `\source`, `\ref` und fett gesetzte
  Musterkopfzeile
- G.1-G.7: `caption`, `hfhfigure`, `\source`, `\ref`, `\intextsep` und
  `\textfloatsep`
- H.1: `\numberwithin{equation}{chapter}` und die Umgebung `equation`
- I.1-I.4: `\singlespacing`, `\bibsep`, `\bibhang`, `plainnat`,
  `hfhsourceentries` und `\hfhsourceentry`

Die vier Punkte mit reinem Textbezug können nicht verlässlich automatisiert
werden: E.6, E.7, F.4 und G.5. Für F.1, F.7, G.1 und I.4 stellt die Vorlage
Befehle und Muster bereit; Vollständigkeit und korrekte Inhalte bleiben
prüfpflichtig.

## Weitere Anforderungen der Word-Vorlage

Die Word-Vorlage enthält außerhalb von Tabelle 1 weitere Struktur- und
Inhaltsvorgaben. Auch diese sind geprüft:

- J.1 - Bei themenvereinbarungspflichtigen Arbeiten ist das offizielle
  Titelblatt des Prüfungsamts zu verwenden. `\MakeOfficialTitlePage` bindet
  dieses ein. Das generische Titelblatt bleibt für andere Arbeiten verfügbar.
- J.2 - Das Titelblatt zählt als Seite 1, zeigt aber keine Seitenzahl.
  `\MakeThesisTitle` und `\MakeOfficialTitlePage` setzen die Zählung
  entsprechend.
- J.3 - Der Abstract ist nur für Masterarbeiten vorgesehen und umfasst etwa
  eine, höchstens zwei Seiten. `\IncludeAbstracttrue` beziehungsweise
  `\IncludeAbstractfalse` und der sichtbare Erläuterungstext bilden dies ab.
- J.4 - Inhalts-, Abbildungs- und Tabellenverzeichnis werden automatisch
  erzeugt. Quellenzeilen von Abbildungen und Tabellen erscheinen durch den
  getrennten Befehl `\source` nicht in den Verzeichnissen.
- J.5 - Das Abkürzungsverzeichnis ist alphabetisch zu sortieren; nicht
  allgemeinsprachliche Abkürzungen sind bei der ersten Verwendung
  auszuschreiben. Muster und Erläuterungstext machen beide Inhaltsprüfungen
  sichtbar.
- J.6 - Die Dezimalgliederung soll regelmäßig drei, bei umfangreichen Arbeiten
  höchstens vier Ebenen umfassen. Ein Gliederungspunkt darf nicht nur einen
  Unterpunkt besitzen. `secnumdepth`, `tocdepth` und der Mustertext bilden die
  Regeln ab.
- J.7 - Das Quellenverzeichnis enthält ausschließlich zitierte Quellen. BibTeX
  erzeugt es aus den tatsächlich zitierten Einträgen in `references.bib`.
- J.8 - Rechtsprechungs- sowie Verwaltungs- und Parlamentariaverzeichnisse
  werden nur bei Bedarf aktiviert. Die Vorlagenhinweise nennen die
  erforderlichen Fundstellen; `hfhsourceentries` setzt deren Format.
- J.9 - Der Einsatz von KI-Werkzeugen ist bei tatsächlicher Nutzung
  nachvollziehbar zu dokumentieren. Der optionale Schalter und die Mustertabelle
  stellen die geforderten Felder bereit.
- J.10 - Mehrere Anlagen erhalten ein Anlagenverzeichnis mit Nummer, Bezeichnung
  und Seite. Anlagen müssen für das Verständnis notwendig sein und dürfen eine
  Seitenbegrenzung nicht umgehen. Schalter, Verzeichnis und Vorlagenhinweis
  bilden dies ab.
- J.11 - Die aktuelle Eigenständigkeitserklärung aus dem WebCampus wird
  unverändert als letzte Seite eingefügt, nicht im Inhaltsverzeichnis
  aufgeführt, nicht sichtbar nummeriert, datiert und unterschrieben. Der
  Platzhalter und der kommentierte `\includepdf`-Befehl bilden den Ablauf ab.

## Dokumentreihenfolge

1. Titelblatt
2. Abstract nur für Masterarbeiten, etwa eine bis maximal zwei Seiten
3. Inhaltsverzeichnis
4. Abbildungsverzeichnis
5. Tabellenverzeichnis
6. Abkürzungsverzeichnis
7. Haupttext
8. Quellenverzeichnis
9. Optionale juristische und administrative Verzeichnisse
10. Optionales Verzeichnis der eingesetzten KI-Werkzeuge
11. Optionales Anlagenverzeichnis und Anlagen
12. Offizielle Eigenständigkeitserklärung als unnummerierte letzte Seite

## Lizenz

Copyright (c) 2026 Ilya Zarubin. Die Vorlagendateien stehen unter der LaTeX
Project Public License, Version 1.3c oder später. Einzelheiten stehen in
`LICENSE`. Die Lizenz gilt nicht für die nicht verteilte HFH-Word-Datei, das
HFH-Logo, das Bild `images/arbeitsplatz.jpg` oder für später von Nutzerinnen und
Nutzern eingefügte offizielle HFH-Dokumente. Das Arbeitsplatzbild stammt laut
eingebetteter Quellenangabe der offiziellen Vorlage von ioannis kounadeas,
Fotolia, Bild 4598956. Die Bilddateien wurden ausschließlich aus der offiziellen
HFH-Vorlage übernommen; ihre jeweiligen Rechte bleiben unberührt.

## Quellen und Dokumentation

- [HFH-WebCampus: Modulhandbücher der Technikstudiengänge](https://campus.hamburger-fh.de/material/bug-material/fb-technik)
- [HFH: Fachbereich Technik](https://www.hfh-fernstudium.de/fernhochschule-fachbereich-technik)
- [HFH-Wegweiser durchs Studium](https://www.hfh-fernstudium.de/fernstudium-studieren-wegweiser)
- [HFH-Hinweise zur Abschlussarbeit](https://www.hfh-fernstudium.de/blog/abschlussarbeit-so-nimmst-du-die-letzte-huerde-des-studiums)
