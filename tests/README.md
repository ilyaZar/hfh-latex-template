# Tabelle-1-Compliance-Tests

Diese Tests prüfen ausschließlich synthetische LaTeX-Beispiele. Sie benötigen
weder private Quelldokumente noch daraus abgeleitete Texte, Bilder oder
Metadaten.

## Ausführen

Im Verzeichnis `tests/`:

```bash
python3 run_table1_compliance.py
```

Der Lauf:

- kompiliert eine achtseitige synthetische Testdatei
- prüft Fußnoten, Tabellen, Abbildungen und Quellenverzeichnisse
- prüft fortlaufende Nummerierung, Beschriftungen, Labels und Verweise
- prüft offensichtliche Inhaltsverstöße mit positiven und negativen Fällen
- vermisst A4-Format, Abstände, Einzüge und eingebettete Schriften
- lehnt redundante oder veraltete LaTeX-Pakete im Testlauf ab

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

Der statische Prüfer erkennt nur offensichtliche Verstöße. Inhaltliche
Richtigkeit und stark verschachtelte eigene Makros bleiben manuell zu prüfen.
