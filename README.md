# 📅 DDR-Kalender

> Feiertage, Gedenk- und Kampftage der Deutschen Demokratischen Republik (1949–1990)  
> als fortlaufendes iCalendar-Abonnement

---

## Abonnieren

Die Kalenderdatei kann direkt in jede gängige Kalender-App als dauerhaftes Abonnement eingebunden werden:

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

Der Kalender enthält **1.820 Einträge** für die Jahre **2024–2075**. Jeder Termin enthält eine ausführliche Notiz und eine **automatische Erinnerung um 6:00 Uhr morgens**.

### Gesetzliche Feiertage
- Tag der Arbeit (1. Mai)
- Tag der Republik (7. Oktober) — Nationalfeiertag der DDR

### Politische Gedenk- und Kampftage
- Liebknecht & Luxemburg Gedenktag (Sonntag nearest 15. Januar)
- Jahrestag der Pariser Kommune (19. März)
- Gründungstag der SED (21. April)
- Geburtstag W. I. Lenin (22. April)
- Jahrestag der Befreiung vom Hitlerfaschismus (8. Mai)
- Tag des Sieges der UdSSR (9. Mai)
- Gedenktag Überfall auf die Sowjetunion (22. Juni)
- Tag der Internationalen Brigaden (18. Juli)
- Weltfriedenstag (1. September)
- OdF-Tag — Opfer des Faschismus (2. Sonntag im September)
- Jahrestag der Oktoberrevolution (7. November)
- KPD-Gründung (30. Dezember)
- Gründung der UdSSR (30. Dezember)

### Gesellschaftliche Feiertage
- Tag der FDJ (7. März)
- Internationaler Frauentag (8. März)
- Internationaler Kindertag (1. Juni)
- Tag des Lehrers (12. Juni)
- Pioniergeburtstag (13. Dezember)

### Militärische und Sicherheitsorgane
- Tag der NVA (1. März)
- Tag des MfS (8. Februar)
- Tag der Deutschen Volkspolizei (1. Juli)
- Tag der Grenztruppen der DDR (1. Dezember)

### Berufliche Ehrentage
- Tag der Werktätigen des Post- und Fernmeldewesens (2. Sonntag im Februar)
- Tag der Mitarbeiter des Handels (3. Sonntag im Februar)
- Tag des Metallarbeiters (2. Sonntag im April)
- Tag des Eisenbahners (2. Sonntag im Juni)
- Tag der Genossenschaftsbauern (3. Sonntag im Juni)
- Tag des Bauarbeiters (4. Sonntag im Juni)
- Tag des Bergmanns und Energiearbeiters (1. Sonntag im Juli)
- Tag des Chemiearbeiters (2. Sonntag im November)
- Tag des Metallurgen (3. Sonntag im November)
- Tag des Gesundheitswesens (11. Dezember)

### Historische Gedenktage
- Befreiung KZ Buchenwald (11. April)
- Tag der Internationalen Brigaden (18. Juli)

---

## Dateien

| Datei | Beschreibung |
|-------|-------------|
| `ddr-feiertage.ics` | Fertige Kalenderdatei zum Abonnieren |
| `generate_ddr_ical.py` | Python-Skript zur Generierung der Datei |
| `DDR-Feiertage-Uebersicht.pdf` | Gedruckte Übersicht aller Feiertage |

---

## Selbst generieren

Voraussetzung: Python 3

```bash
git clone https://github.com/amylasehai0z/ddr-kalender
cd ddr-kalender
python3 generate_ddr_ical.py
```

Der Jahresbereich lässt sich im Skript unter `YEARS = range(2024, 2076)` anpassen.

---

## Hintergrund

Die DDR pflegte einen eigenen sozialistischen Festkalender, der religiöse Feiertage weitgehend durch politische Gedenktage ersetzte oder ergänzte. Neben den gesetzlichen Feiertagen prägten Kampftage, Berufsehrentage und gesellschaftliche Festtraditionen wie die **Jugendweihe** das öffentliche Leben.

Dieser Kalender dokumentiert diesen Festkalender als lebendiges iCal-Abonnement — nutzbar in jeder modernen Kalender-App, mit Erinnerungen und ausführlichen historischen Notizen zu jedem Termin.

---

## Lizenz

Historische Daten sind gemeinfrei. Der Code steht unter der [MIT License](LICENSE).
