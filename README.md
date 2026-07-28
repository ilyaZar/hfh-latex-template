# HFH-LaTeX-Vorlage

Minimalistische LaTeX-Vorlage fuer wissenschaftliche Arbeiten an der
HFH Hamburger Fern-Hochschule, primaer auf Deutsch und optional auf Englisch.

**Autor und aktueller Maintainer:** Ilya Zarubin, 2026

[In Overleaf oeffnen](https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fgithub.com%2FilyaZar%2Fhfh-latex-template%2Farchive%2Frefs%2Fheads%2Fmain.zip&engine=pdflatex&main_document=main.tex)

> [!WARNING]
> Diese Vorlage ersetzt nicht die jeweils aktuellen offiziellen Regelungen.
> Sie erhebt keinen Anspruch auf Vollstaendigkeit, Fehlerfreiheit oder
> dauerhafte Uebereinstimmung mit allen studiengangsspezifischen
> HFH-Regelungen. Vor jeder Verwendung und insbesondere vor jeder Abgabe sind
> die aktuellen Vorgaben der HFH fuer Seminar-, Haus-, Bachelor- und
> Masterarbeiten zu pruefen. Bei Abweichungen gelten die offiziellen Vorgaben
> der HFH, des Pruefungsamts und der betreuenden beziehungsweise pruefenden
> Personen.

Die Vorlage wurde anhand der HFH-Formatvorgaben erstellt. Erklaerende Texte
aus den zugrundeliegenden Dokumenten wurden nicht uebernommen. Diese Dokumente
sind nicht Bestandteil der oeffentlichen Vorlage und werden nicht
weiterverteilt.

## Schnellstart

1. Den Metadatenblock am Anfang von `main.tex` bearbeiten.
2. `\MainLanguage` auf `ngerman` oder `english` setzen.
3. Fuer Bachelor- und Seminararbeiten `\IncludeAbstractfalse` setzen.
4. Optionale Verzeichnisse ueber die Schalter in `main.tex` konfigurieren.
5. Quellen in `references.bib` eintragen und im Text zitieren.
6. Mit `latexmk -pdf main.tex` oder in Overleaf mit pdfLaTeX kompilieren.

Einzelne englische Passagen erhalten mit Babel englische Silbentrennung:

```latex
\begin{otherlanguage}{english}
English text with English hyphenation.
\end{otherlanguage}
```

## Overleaf

Die Vorlage ist fuer ein Overleaf-Projekt mit folgenden Einstellungen
vorbereitet:

- Hauptdokument: `main.tex`
- Compiler: pdfLaTeX
- TeX Live: aktuelle von Overleaf angebotene Version
- Bibliografie: BibTeX ueber `natbib` und `plainnat`

Der Link **In Overleaf oeffnen** importiert den jeweils aktuellen Stand des
`main`-Branches als neues Overleaf-Projekt. Er funktioniert, sobald das
Repository als `ilyaZar/hfh-latex-template` oeffentlich erreichbar ist.

Eine Einreichung in die Overleaf Gallery ist vorgesehen. Overleaf akzeptiert
offizielle Hochschulvorlagen fuer Abschlussarbeiten, wenn die Beschreibung auf
die offizielle Hochschulseite mit den Gestaltungs- oder Einreichungsvorgaben
verweist. In der Gallery-Beschreibung sind deshalb die
[Modulhandbuecher der Technikstudiengaenge im HFH-WebCampus](https://campus.hamburger-fh.de/material/bug-material/fb-technik)
(Anmeldung erforderlich) sowie die oeffentlichen
[HFH-Hinweise zur Abschlussarbeit](https://www.hfh-fernstudium.de/blog/abschlussarbeit-so-nimmst-du-die-letzte-huerde-des-studiums)
anzugeben. Die oeffentliche HFH-Seite beschreibt auch das Pflichtmodul
`Wissenschaftliches Arbeiten (WSA)`.

## Offizielle Seiten

Die aktuellen Formatvorgaben stehen in den Appendizes der Modulhandbuecher der
Technikstudiengaenge. Die Modulhandbuecher werden im
[HFH-WebCampus](https://campus.hamburger-fh.de/material/bug-material/fb-technik)
bereitgestellt; der Zugriff erfordert ein HFH-Benutzerkonto. Eine oeffentliche
Uebersicht bietet die Seite zum
[Fachbereich Technik](https://www.hfh-fernstudium.de/fernhochschule-fachbereich-technik).

Bei anmeldepflichtigen Arbeiten stellt das Pruefungsamt nach der bestaetigten
Themenanmeldung ein offizielles Titelblatt bereit. Dieses ersetzt das
generische Titelblatt mit:

```latex
\MakeOfficialTitlePage{offizielles-titelblatt.pdf}
```

Die aktuelle Eigenstaendigkeitserklaerung ist unveraendert aus dem WebCampus
zu uebernehmen. Sie bildet die letzte Seite, erscheint nicht im
Inhaltsverzeichnis und traegt keine sichtbare Seitenzahl. Der Text in
`main.tex` ist nur ein Platzhalter.

## Verbindlich umgesetzte Angaben

- DIN A4 im Hochformat und einseitige Ausgabe
- Raender: links 3 cm, rechts 4 cm, oben und unten 2,5 cm
- Blocksatz mit 1,5-fachem Zeilenabstand
- Name und Matrikelnummer in einer 10-pt-Kopfzeile
- Titelblatt als mitgezaehlte Seite 1 ohne sichtbare Seitenzahl
- Fortlaufend nummerierte Fussnoten mit 10 pt und einzeiligem Text
- Fortlaufend nummerierte Tabellen und Abbildungen
- Beschriftungen und gesonderte Quellenzeilen fuer Tabellen und Abbildungen
- Alphabetisch sortiertes Quellenverzeichnis nur mit zitierten Quellen
- Einzeilige Quellenangaben mit Abstand zwischen den Eintraegen
- Eigenstaendigkeitserklaerung ohne Seitenzahl und Verzeichniseintrag

Der erforderliche Grossbuchstabe am Anfang und der Punkt am Ende jeder
Fussnote koennen nicht verlaesslich automatisiert werden. Auch korrekte
Quellenzeilen und Textverweise auf jede Tabelle und Abbildung bleiben in der
Verantwortung der Verfasserin beziehungsweise des Verfassers.

## Umgesetzte Empfehlungen

- Gut lesbare Times-kompatible Schrift in 12 pt
- Hauptueberschriften in fett 14 pt, tiefere Ebenen in fett 12 pt
- Sechs Punkt Abstand zwischen Absaetzen und automatische Silbentrennung
- Kopfzeile, Fusszeile, Fussnoten, Beschriftungen und Tabellen in 10 pt
- Einzeiliger Tabelleninhalt und gesonderte Quellenhinweise
- Kapitelbezogene Formelnummerierung
- Haengender Einzug von 0,5 cm im Quellenverzeichnis
- Dezimalgliederung mit standardmaessig drei nummerierten Ebenen

Bei umfangreichen Arbeiten kann eine vierte Ebene durch `secnumdepth` und
`tocdepth` mit dem Wert `3` aktiviert werden. Ein Gliederungspunkt darf nicht
nur einen einzigen Unterpunkt besitzen.

## Dokumentreihenfolge

1. Titelblatt
2. Abstract nur fuer Masterarbeiten, etwa eine bis maximal zwei Seiten
3. Inhaltsverzeichnis
4. Abbildungsverzeichnis
5. Tabellenverzeichnis
6. Abkuerzungsverzeichnis
7. Haupttext
8. Quellenverzeichnis
9. Optionale juristische und administrative Verzeichnisse
10. Optionales Verzeichnis der eingesetzten KI-Werkzeuge
11. Optionales Anlagenverzeichnis und Anlagen
12. Offizielle Eigenstaendigkeitserklaerung als unnummerierte letzte Seite

## Lizenz

Copyright (c) 2026 Ilya Zarubin. Die Vorlagendateien stehen unter der
LaTeX Project Public License, Version 1.3c oder spaeter. Einzelheiten stehen in
`LICENSE`. Die Lizenz gilt nicht fuer die nicht verteilte HFH-Word-Datei oder
fuer spaeter von Nutzerinnen und Nutzern eingefuegte offizielle HFH-Dokumente.

## Quellen und Dokumentation

- [HFH-WebCampus: Modulhandbuecher der Technikstudiengaenge](https://campus.hamburger-fh.de/material/bug-material/fb-technik)
- [HFH: Fachbereich Technik](https://www.hfh-fernstudium.de/fernhochschule-fachbereich-technik)
- [HFH-Wegweiser durchs Studium](https://www.hfh-fernstudium.de/fernstudium-studieren-wegweiser)
- [HFH-Hinweise zur Abschlussarbeit](https://www.hfh-fernstudium.de/blog/abschlussarbeit-so-nimmst-du-die-letzte-huerde-des-studiums)
- [Overleaf: Template Gallery](https://docs.overleaf.com/templates/submitting-to-the-overleaf-template-gallery)
- [Overleaf: Lizenzierung](https://docs.overleaf.com/templates/licensing-and-copyright)
- [Overleaf: Open-in-Overleaf-API](https://www.overleaf.com/devs)
