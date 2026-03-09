# 📅 DDR-Kalender

> Feiertage, Gedenk- und Kampftage der Deutschen Demokratischen Republik (1949–1990)  
> als fortlaufendes iCalendar-Abonnement

---

## Abonnieren

Die Kalenderdatei kann direkt in jede gängige Kalender-App als **dauerhaftes Abonnement** eingebunden werden:

```
https://amylasehai0z.github.io/ddr-kalender/ddr-feiertage.ics
```

| App | Anleitung |
|-----|-----------|
| **Google Calendar** | Einstellungen → Weitere Kalender → Per URL hinzufügen |
| **Apple Kalender** | Ablage → Neues Kalenderabonnement |
| **Outlook** | Kalender hinzufügen → Aus dem Internet abonnieren |

---

## Inhalt

Der Kalender enthält zur Zeit **988 Einträge** für die Jahre **2024–2075** und deckt folgende Kategorien ab:

### Gesetzliche Feiertage
- Tag der Arbeit (1. Mai)
- Tag der Republik (7. Oktober) — Nationalfeiertag der DDR

### Politische Gedenk- und Kampftage
- Gedenktag für Karl Liebknecht und Rosa Luxemburg (15. Januar)
- Tag der FDJ — Freie Deutsche Jugend (7. März)
- Internationaler Frauentag (8. März)
- Jahrestag der Pariser Kommune (19. März)
- Befreiung des KZ Buchenwald (11. April)
- Geburtstag W. I. Lenin (22. April)
- Internationaler Kindertag (1. Juni)
- Tag des Lehrers (12. Juni)
- Gedenktag Überfall auf die Sowjetunion (22. Juni)
- OdF-Tag — Opfer des Faschismus und Militarismus (2. Sonntag im September)
- Jahrestag der Oktoberrevolution (7. November)
- KPD-Gründung (1. Januar)

### Militärische und Berufliche Ehrentage
- Tag der Nationalen Volksarmee — NVA (23. Februar)
- Tag der Deutschen Volkspolizei (vorletzter Sonntag im März)
- Tag der Kampfgruppen der Arbeiterklasse (2. Sonntag im April)
- Tag des Eisenbahners (2. Sonntag im September)
- Tag des Bergmanns und Energiearbeiters (letzter Sonntag im August)

---

## Dateien

| Datei | Beschreibung |
|-------|-------------|
| `ddr-feiertage.ics` | Fertige Kalenderdatei zum Abonnieren |
| `generate_ddr_ical.py` | Python-Skript zur Generierung der Datei |
| `DDR-Feiertage.pdf` | Gedruckte Übersicht aller Feiertage |

---

## Selbst generieren

Voraussetzung: Python 3

```bash
git clone https://github.com/DEINNAME/ddr-kalender
cd ddr-kalender
python3 generate_ddr_ical.py
```

Der Jahresbereich lässt sich im Skript unter `YEARS = range(2024, 2076)` anpassen.

---

## Hintergrund

Die DDR pflegte einen eigenen sozialistischen Festkalender, der religiöse Feiertage weitgehend durch politische Gedenktage ersetzte oder ergänzte. Neben den gesetzlichen Feiertagen prägten Kampftage, Berufsehrentage und gesellschaftliche Festtradtionen wie die **Jugendweihe** das öffentliche Leben.

Dieser Kalender dokumentiert diesen Festkalender als lebendiges iCal-Abonnement — nutzbar in jeder modernen Kalender-App.

---

## Lizenz

Historische Daten sind gemeinfrei. Der Code steht unter der [MIT License](LICENSE).
