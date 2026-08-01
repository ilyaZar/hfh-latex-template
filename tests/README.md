# Vorlagenprüfungen

Die Prüfungen bauen die öffentliche Vorlage und eine synthetische
LaTeX-Fixture. Sie benötigen weder private Quelldokumente noch daraus
abgeleitete Texte, Bilder oder Metadaten.

## Ausführen

Im Repository:

```sh
bash tests/run.sh
```

Der Lauf:

- kompiliert die öffentliche Vorlage
- kompiliert eine achtseitige synthetische Testdatei
- prüft Fußnoten, Tabellen, Abbildungen und Quellenverzeichnisse
- prüft fortlaufende Nummerierung, Beschriftungen, Labels und Verweise
- vermisst A4-Format, Abstände, Einzüge und eingebettete Schriften
- lehnt redundante oder veraltete LaTeX-Pakete im Testlauf ab
- prüft die produktiven Formatdefinitionen in `hfh-formatierungen.sty`
- vermisst Einseitigkeit, Abstände und Textspalte des Inhaltsverzeichnisses
- prüft den Datenschutz und die Dateifreigabe des Overleaf-Archivs
- lehnt EXIF-, IPTC-, Photoshop- und XMP-Daten in Beispielbildern ab

Die gerenderte PDF und alle LaTeX-Hilfsdateien sind lokale Build-Artefakte und
werden nicht versioniert.

## Testseiten

| Seite | Prüfgegenstand                                           |
| ----: | -------------------------------------------------------- |
|     1 | Vier Überschriftenebenen und typische Übergänge          |
|     2 | Drei mehrzeilige Fußnoten                                |
|     3 | Fortlaufende Fußnotennummerierung über Kapitelgrenzen    |
|     4 | Tabelle und Abbildung mit Quelle, Label und Verweis       |
|     5 | Globale Nummerierung über Kapitelgrenzen                 |
|     6 | Nichtalphabetische Zitierreihenfolge                     |
|     7 | Automatisch alphabetisch sortiertes Quellenverzeichnis   |
|     8 | Manuell alphabetisches Rechtsprechungsverzeichnis        |

## GitHub Actions

Der Workflow `.github/workflows/compliance.yml` führt denselben Testlauf mit
TeX Live 2026 aus. `tests/`, `.github/`, private Quelldokumente und lokale
Build-Artefakte dürfen nicht in dem von GitHub erzeugten Overleaf-Archiv
erscheinen. Öffentliche Beispielbilder sind ausschließlich unter `images/`
zulässig.
