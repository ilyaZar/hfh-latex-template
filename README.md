# HFH-LaTeX-Vorlage

Minimalistische LaTeX-Vorlage für wissenschaftliche Arbeiten an der
HFH Hamburger Fern-Hochschule, primär auf Deutsch und optional auf Englisch.

**Autor und aktueller Maintainer:** Ilya Zarubin, 2026

[In Overleaf öffnen](https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fgithub.com%2FilyaZar%2Fhfh-latex-template%2Farchive%2Frefs%2Fheads%2Fmain.zip&engine=pdflatex&main_document=main.tex)

> [!WARNING]
> Diese Vorlage ersetzt nicht die jeweils aktuellen offiziellen Regelungen.
> Sie erhebt keinen Anspruch auf Vollständigkeit, Fehlerfreiheit oder
> dauerhafte Übereinstimmung mit allen studiengangsspezifischen
> HFH-Regelungen. Vor jeder Verwendung und insbesondere vor jeder Abgabe sind
> die aktuellen Vorgaben der HFH für Seminar-, Haus-, Bachelor- und
> Masterarbeiten zu prüfen. Bei Abweichungen gelten die offiziellen Vorgaben
> der HFH, des Prüfungsamts und der betreuenden beziehungsweise prüfenden
> Personen.

Die Vorlage wurde anhand der HFH-Formatvorgaben erstellt. Erklärende Texte
aus den zugrundeliegenden Dokumenten wurden nicht übernommen. Diese Dokumente
sind nicht Bestandteil der öffentlichen Vorlage und werden nicht
weiterverteilt.

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

## Overleaf

Die Vorlage ist für ein Overleaf-Projekt mit folgenden Einstellungen
vorbereitet:

- Hauptdokument: `main.tex`
- Compiler: pdfLaTeX
- TeX Live: aktuelle von Overleaf angebotene Version
- Bibliografie: BibTeX über `natbib` und `plainnat`

Der Link **In Overleaf öffnen** importiert den jeweils aktuellen Stand des
`main`-Branches als neues Overleaf-Projekt. Er funktioniert, sobald das
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
Themenanmeldung ein offizielles Titelblatt bereit. Dieses ersetzt das
generische Titelblatt mit:

```latex
\MakeOfficialTitlePage{offizielles-titelblatt.pdf}
```

Die aktuelle Eigenständigkeitserklärung ist unverändert aus dem WebCampus
zu übernehmen. Sie bildet die letzte Seite, erscheint nicht im
Inhaltsverzeichnis und trägt keine sichtbare Seitenzahl. Der Text in
`main.tex` ist nur ein Platzhalter.

## Verbindlich umgesetzte Angaben

- DIN A4 im Hochformat und einseitige Ausgabe
- Ränder: links 3 cm, rechts 4 cm, oben und unten 2,5 cm
- Blocksatz mit 1,5-fachem Zeilenabstand
- Name und Matrikelnummer in einer 10-pt-Kopfzeile
- Titelblatt als mitgezählte Seite 1 ohne sichtbare Seitenzahl
- Fortlaufend nummerierte Fußnoten mit 10 pt und einzeiligem Text
- Fortlaufend nummerierte Tabellen und Abbildungen
- Beschriftungen und gesonderte Quellenzeilen für Tabellen und Abbildungen
- Alphabetisch sortiertes Quellenverzeichnis nur mit zitierten Quellen
- Einzeilige Quellenangaben mit Abstand zwischen den Einträgen
- Eigenständigkeitserklärung ohne Seitenzahl und Verzeichniseintrag

Der erforderliche Großbuchstabe am Anfang und der Punkt am Ende jeder
Fußnote können nicht verlässlich automatisiert werden. Auch korrekte
Quellenzeilen und Textverweise auf jede Tabelle und Abbildung bleiben in der
Verantwortung der Verfasserin beziehungsweise des Verfassers.

## Umgesetzte Empfehlungen

- Gut lesbare Times-kompatible Schrift in 12 pt
- Hauptüberschriften in fett 14 pt, tiefere Ebenen in fett 12 pt
- Sechs Punkt Abstand zwischen Absätzen und automatische Silbentrennung
- Kopfzeile, Fußzeile, Fußnoten, Beschriftungen und Tabellen in 10 pt
- Einzeiliger Tabelleninhalt und gesonderte Quellenhinweise
- Kapitelbezogene Formelnummerierung
- Hängender Einzug von 0,5 cm im Quellenverzeichnis
- Dezimalgliederung mit standardmäßig drei nummerierten Ebenen

Bei umfangreichen Arbeiten kann eine vierte Ebene durch `secnumdepth` und
`tocdepth` mit dem Wert `3` aktiviert werden. Ein Gliederungspunkt darf nicht
nur einen einzigen Unterpunkt besitzen.

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

Copyright (c) 2026 Ilya Zarubin. Die Vorlagendateien stehen unter der
LaTeX Project Public License, Version 1.3c oder später. Einzelheiten stehen in
`LICENSE`. Die Lizenz gilt nicht für die nicht verteilte HFH-Word-Datei oder
für später von Nutzerinnen und Nutzern eingefügte offizielle HFH-Dokumente.

## Quellen und Dokumentation

- [HFH-WebCampus: Modulhandbücher der Technikstudiengänge](https://campus.hamburger-fh.de/material/bug-material/fb-technik)
- [HFH: Fachbereich Technik](https://www.hfh-fernstudium.de/fernhochschule-fachbereich-technik)
- [HFH-Wegweiser durchs Studium](https://www.hfh-fernstudium.de/fernstudium-studieren-wegweiser)
- [HFH-Hinweise zur Abschlussarbeit](https://www.hfh-fernstudium.de/blog/abschlussarbeit-so-nimmst-du-die-letzte-huerde-des-studiums)
