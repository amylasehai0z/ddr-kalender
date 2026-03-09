from datetime import date, timedelta

def easter(year):
    a = year % 19
    b = year % 4
    c = year % 7
    k = year // 100
    p = (13 + 8*k) // 25
    q = k // 4
    m = (15 - p + k - q) % 30
    n = (4 + k - q) % 7
    d = (19*a + m) % 30
    e = (2*b + 4*c + 6*d + n) % 7
    if d == 29 and e == 6:
        return date(year, 4, 19)
    elif d == 28 and e == 6 and a > 10:
        return date(year, 4, 18)
    else:
        return date(year, 3, 22) + timedelta(days=d+e)

def nth_weekday(year, month, weekday, n):
    if n > 0:
        d = date(year, month, 1)
        count = 0
        while True:
            if d.weekday() == weekday:
                count += 1
                if count == n:
                    return d
            d += timedelta(days=1)
    else:
        if month == 12:
            last = date(year+1, 1, 1) - timedelta(days=1)
        else:
            last = date(year, month+1, 1) - timedelta(days=1)
        count = 0
        d = last
        while True:
            if d.weekday() == weekday:
                count -= 1
                if count == n:
                    return d
            d -= timedelta(days=1)

def nearest_sunday(year, month, day):
    d = date(year, month, day)
    wd = d.weekday()
    if wd == 6:
        return d
    elif wd <= 2:
        return d - timedelta(days=wd+1)
    else:
        return d + timedelta(days=6-wd)

def format_date(d):
    return d.strftime("%Y%m%d")

def make_uid(name, year):
    clean = name.lower().replace(" ", "-").replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss")
    clean = ''.join(c for c in clean if c.isalnum() or c == '-')
    return f"ddr-{clean}-{year}@ddr-kalender"

def add_event(lines, d, name, desc):
    uid = make_uid(name, d.year)
    lines.append("BEGIN:VEVENT")
    lines.append(f"UID:{uid}")
    lines.append("DTSTAMP:20240101T000000Z")
    lines.append(f"DTSTART;VALUE=DATE:{format_date(d)}")
    lines.append(f"DTEND;VALUE=DATE:{format_date(d + timedelta(days=1))}")
    lines.append(f"SUMMARY:{name}")
    lines.append(f"DESCRIPTION:{desc}")
    lines.append("CATEGORIES:DDR Feiertage")
    lines.append("TRANSP:TRANSPARENT")
    lines.append("BEGIN:VALARM")
    lines.append("ACTION:DISPLAY")
    lines.append(f"DESCRIPTION:{name}")
    lines.append("TRIGGER;VALUE=DATE-TIME:" + d.strftime("%Y%m%d") + "T060000")
    lines.append("END:VALARM")
    lines.append("END:VEVENT")

lines = []
lines.append("BEGIN:VCALENDAR")
lines.append("VERSION:2.0")
lines.append("PRODID:-//DDR Feiertage und Gedenktage//DE")
lines.append("CALSCALE:GREGORIAN")
lines.append("METHOD:PUBLISH")
lines.append("X-WR-CALNAME:DDR Gedenk- und Feiertage")
lines.append("X-WR-CALDESC:Offizielle Feiertage\\, Gedenk- und Kampftage der Deutschen Demokratischen Republik (DDR)")
lines.append("X-WR-TIMEZONE:Europe/Berlin")
lines.append("REFRESH-INTERVAL;VALUE=DURATION:P1W")
lines.append("X-PUBLISHED-TTL:P1W")

YEARS = range(2024, 2076)

for year in YEARS:

    # ── JANUAR ──────────────────────────────────────────────────────────────
    add_event(lines, nearest_sunday(year, 1, 15),
        "Liebknecht & Luxemburg Gedenktag 🌹",
        "Gedenktag für Karl Liebknecht und Rosa Luxemburg – am Sonntag\\, der dem 15. Januar am nächsten liegt. Beide wurden am 15. Januar 1919 ermordet. Jährliche Gedenkdemonstration in Berlin.")

    # ── FEBRUAR ─────────────────────────────────────────────────────────────
    add_event(lines, nth_weekday(year, 2, 6, 2),
        "Tag der Werktätigen des Post- und Fernmeldewesens 📮",
        "Ehrentag der Beschäftigten im Post- und Fernmeldewesen der DDR – zweiter Sonntag im Februar.")

    add_event(lines, date(year, 2, 8),
        "Tag des MfS 🔍",
        "Tag des Ministeriums für Staatssicherheit (MfS/Stasi) – gegründet am 8. Februar 1950. Inoffizieller Gedenktag innerhalb des Apparats.")

    add_event(lines, nth_weekday(year, 2, 6, 3),
        "Tag der Mitarbeiter des Handels 🛒",
        "Ehrentag der Beschäftigten im Einzelhandel und Handelswesen der DDR – dritter Sonntag im Februar.")

    # ── MÄRZ ────────────────────────────────────────────────────────────────
    add_event(lines, date(year, 3, 1),
        "Tag der NVA 🪖",
        "Tag der Nationalen Volksarmee der DDR – begangen am 1. März. Gegründet am 1. März 1956. Gefeiert mit Paraden und Appellen.")

    add_event(lines, date(year, 3, 7),
        "Tag der FDJ 🔵",
        "Jahrestag der Gründung der Freien Deutschen Jugend am 7. März 1946. Massenorganisation der DDR-Jugend. Gefeiert mit Appellen\\, Fackelzügen und kulturellen Veranstaltungen.")

    add_event(lines, date(year, 3, 8),
        "Internationaler Frauentag 👩",
        "Internationaler Frauentag – offizieller Gedenk- und Feiertag der DDR. Beschäftigte Frauen erhielten häufig einen bezahlten arbeitsfreien Tag. Mit Blumen\\, Veranstaltungen und Auszeichnungen begangen.")

    add_event(lines, date(year, 3, 19),
        "Jahrestag der Pariser Kommune 🏴",
        "Jahrestag der Pariser Kommune vom 18. März 1871 – erstes Experiment einer Arbeiterregierung in der Geschichte. In der DDR als revolutionäres Vorbild gewürdigt.")

    # ── APRIL ───────────────────────────────────────────────────────────────
    add_event(lines, date(year, 4, 11),
        "Befreiung KZ Buchenwald 🕯️",
        "Gedenktag zur Befreiung des Konzentrationslagers Buchenwald am 11. April 1945 durch US-amerikanische Truppen. Einer der zentralen Gedenkfeiern in der DDR – Buchenwald als nationales Mahnmal gepflegt.")

    add_event(lines, nth_weekday(year, 4, 6, 2),
        "Tag des Metallarbeiters ⚙️",
        "Ehrentag der Metallarbeiterinnen und Metallarbeiter der DDR – zweiter Sonntag im April. Gefeiert in Betrieben der metallerzeugenden und metallverarbeitenden Industrie.")

    add_event(lines, date(year, 4, 21),
        "Gründungstag der SED 🔴",
        "Jahrestag der Gründung der Sozialistischen Einheitspartei Deutschlands (SED) am 21./22. April 1946 durch Zwangsvereinigung von SPD und KPD in der Sowjetischen Besatzungszone.")

    add_event(lines, date(year, 4, 22),
        "Geburtstag W. I. Lenin ☭",
        f"Geburtstag Wladimir Iljitsch Lenins am 22. April 1870. Er wäre heute {year - 1870} Jahre alt. Begründer der Sowjetunion und theoretischer Vordenker des Marxismus-Leninismus. Gedenktag in Betrieben\\, Schulen und Parteiorganisationen.")

    # ── MAI ─────────────────────────────────────────────────────────────────
    add_event(lines, date(year, 5, 1),
        "Tag der Arbeit ✊",
        "Internationaler Kampf- und Feiertag der Werktätigen – 1. Mai. Größter politischer Feiertag im Frühling. Massenaufmärsche\\, Kundgebungen und Militärparaden in allen Städten der DDR.")

    add_event(lines, date(year, 5, 8),
        "Jahrestag der Befreiung 🕊️",
        "Jahrestag der Befreiung vom Hitlerfaschismus am 8. Mai 1945 – Tag der bedingungslosen Kapitulation der Wehrmacht. In der DDR als 'Tag der Befreiung' begangen\\, nicht als Niederlage\\, sondern als Befreiung durch die Sowjetunion.")

    add_event(lines, date(year, 5, 9),
        "Tag des Sieges 🎖️",
        "Tag des Sieges der Völker der UdSSR über den Hitlerfaschismus – 9. Mai 1945 (sowjetischer Kalender). In der DDR parallel zum 8. Mai als Ausdruck der engen Verbundenheit mit der Sowjetunion begangen.")

    # ── JUNI ────────────────────────────────────────────────────────────────
    add_event(lines, date(year, 6, 1),
        "Internationaler Kindertag 🎈",
        "Internationaler Kindertag – 1. Juni. Einer der beliebtesten Feiertage in der DDR. Kinder erhielten Geschenke\\, Schulen und Betriebe organisierten Feste und Ausflüge.")

    add_event(lines, date(year, 6, 12),
        "Tag des Lehrers 📚",
        "Tag des Lehrers – 12. Juni. Ehrentag für Lehrerinnen und Lehrer in der DDR. Schülerinnen und Schüler überreichten Blumen und Geschenke\\, Schulen veranstalteten Feierstunden.")

    add_event(lines, nth_weekday(year, 6, 6, 2),
        "Tag des Eisenbahners 🚂",
        "Tag des Eisenbahners und der Werktätigen des Verkehrswesens – zweiter Sonntag im Juni. Ehrentag der Beschäftigten der Deutschen Reichsbahn und des gesamten Verkehrswesens.")

    # Freitag vor Pfingsten = Ostersonntag + 48 Tage
    add_event(lines, easter(year) + timedelta(days=48),
        "Tag der Jugendbrigaden 👷",
        "Tag der Jugendbrigaden – Freitag vor Pfingsten (ab 1978). Ehrentag der sozialistischen Jugendbrigaden in Betrieben und Kombinaten der DDR. Auszeichnungen für herausragende Arbeitsleistungen junger Werktätiger.")

    add_event(lines, nth_weekday(year, 6, 5, 3),
        "Tag der Werktätigen der Wasserwirtschaft 💧",
        "Tag der Werktätigen der Wasserwirtschaft – dritter Sonnabend im Juni. Ehrentag der Beschäftigten in Wasserversorgung\\, Abwasserwirtschaft und Gewässerschutz der DDR.")

    add_event(lines, date(year, 6, 22),
        "Gedenktag: Überfall auf die Sowjetunion 🕯️",
        "Jahrestag des deutschen Überfalls auf die Sowjetunion am 22. Juni 1941 – Beginn des 'Großen Vaterländischen Krieges'. In der DDR als Mahntag gegen Krieg und Faschismus begangen.")

    add_event(lines, nth_weekday(year, 6, 6, 3),
        "Tag der Genossenschaftsbauern 🌾",
        "Tag der Genossenschaftsbauern und Arbeiter der sozialistischen Land- und Forstwirtschaft – dritter Sonntag im Juni. Ehrentag der Beschäftigten in den Landwirtschaftlichen Produktionsgenossenschaften (LPG).")

    add_event(lines, nth_weekday(year, 6, 6, 4),
        "Tag des Bauarbeiters 🏗️",
        "Tag des Bauarbeiters – vierter Sonntag im Juni. Ehrentag der Beschäftigten im Bauwesen der DDR. Mit Betriebsfeiern und Auszeichnungen begangen.")

    # ── JULI ────────────────────────────────────────────────────────────────
    add_event(lines, date(year, 7, 1),
        "Tag der Deutschen Volkspolizei 🚔",
        "Tag der Deutschen Volkspolizei – 1. Juli. Ehrentag der Volkspolizei der DDR. Begangen mit Appellen\\, Auszeichnungen und öffentlichen Veranstaltungen.")

    add_event(lines, nth_weekday(year, 7, 6, 1),
        "Tag des Bergmanns und Energiearbeiters ⛏️",
        "Tag des Bergmanns und des Energiearbeiters – erster Sonntag im Juli. Ehrentag der Beschäftigten im Bergbau und in der Energiewirtschaft. Besonders bedeutsam in den Braunkohlerevieren der DDR.")

    add_event(lines, date(year, 7, 18),
        "Tag der Internationalen Brigaden 🌍",
        "Tag der Internationalen Brigaden – 18. Juli. Gedenktag für die internationalen Freiwilligen\\, die im Spanischen Bürgerkrieg (1936–1939) gegen den Faschismus kämpften. In der DDR als antifaschistisches Symbol gewürdigt.")

    # ── SEPTEMBER ───────────────────────────────────────────────────────────
    add_event(lines, date(year, 8, 2),
        "Potsdamer Abkommen (1945) 📜",
        "Jahrestag der Unterzeichnung des Potsdamer Abkommens am 2. August 1945 durch UdSSR\\, USA und Großbritannien. Regelte die Nachkriegsordnung Deutschlands. In der DDR als Grundlage der Nachkriegspolitik gewürdigt.")

    add_event(lines, date(year, 8, 7),
        "Gründung der GST (1952) 🚀",
        "Jahrestag der Gründung der Gesellschaft für Sport und Technik (GST) am 7. August 1952. Paramilitärische Massenorganisation der DDR zur vormilitärischen Ausbildung von Jugendlichen.")

    add_event(lines, date(year, 9, 1),
        "Weltfriedenstag ☮️",
        "Weltfriedenstag – 1. September. Jahrestag des Beginns des Zweiten Weltkriegs (1939). In der DDR als internationaler Antikriegstag und Friedensappell begangen.")

    add_event(lines, date(year, 9, 8),
        "Weltalphabetisierungstag 📖",
        "Weltalphabetisierungstag – 8. September. Internationaler Gedenktag für Bildung und Bekämpfung des Analphabetismus. In der DDR im Kontext der sozialistischen Bildungspolitik begangen.")

    add_event(lines, nth_weekday(year, 9, 5, 3),
        "Tag der haus- und kommunalwirtschaftlichen Dienstleistungen 🏘️",
        "Tag der Werktätigen des Bereiches der haus- und kommunalwirtschaftlichen Dienstleistungen – dritter Sonnabend im September. Ehrentag der Beschäftigten in Hauswirtschaft\\, Wohnungswirtschaft und kommunalen Diensten.")

    add_event(lines, nth_weekday(year, 9, 6, 2),
        "OdF-Tag – Gedenktag Opfer des Faschismus 🕯️",
        "Internationaler Gedenktag für die Opfer des faschistischen Terrors und Kampftag gegen Faschismus und imperialistischen Krieg – zweiter Sonntag im September. Einer der bedeutendsten Gedenktage der DDR. Kranzniederlegungen\\, Gedenkfeiern an Mahnmalen.")

    # ── OKTOBER ─────────────────────────────────────────────────────────────
    add_event(lines, date(year, 10, 9),
        "Weltposttag 📬",
        "Weltposttag – 9. Oktober. Internationaler Gedenktag des Weltpostvereins. In der DDR im Zusammenhang mit dem Ehrentag der Post- und Fernmeldewerktätigen begangen.")

    add_event(lines, date(year, 10, 13),
        "Tag der Seeverkehrswirtschaft ⚓",
        "Tag der Seeverkehrswirtschaft – 13. Oktober. Ehrentag der Beschäftigten in der Seefahrt und Binnenschifffahrt der DDR. Bedeutsam für Rostock und die Ostseehäfen.")

    add_event(lines, date(year, 10, 16),
        "Welternährungstag 🌽",
        "Welternährungstag – 16. Oktober. Internationaler Gedenktag der FAO. In der DDR im Kontext sozialistischer Landwirtschaftspolitik und internationaler Solidarität begangen.")

    add_event(lines, nth_weekday(year, 10, 5, 3),
        "Tag der Leicht- und Lebensmittelindustrie 🏭",
        "Tag der Werktätigen der Leicht-\\, Lebensmittel- und Nahrungsgüterindustrie – dritter Sonnabend im Oktober. Ehrentag der Beschäftigten in der Konsumgüter- und Nahrungsmittelproduktion der DDR.")

    add_event(lines, date(year, 10, 24),
        "Tag der Vereinten Nationen 🌐",
        "Tag der Vereinten Nationen – 24. Oktober. Jahrestag des Inkrafttretens der UN-Charta (1945). Die DDR trat den Vereinten Nationen 1973 bei und nutzte den Tag für Bekenntnisse zu Frieden und internationaler Zusammenarbeit.")

    add_event(lines, date(year, 10, 7),
        "Tag der Republik 🇩🇩",
        "Nationalfeiertag der DDR – Jahrestag der Gründung der Deutschen Demokratischen Republik am 7. Oktober 1949. Bedeutendster Staatsfeiertag. Militärparaden\\, Fackelzüge der FDJ\\, Staatsakt in Berlin. Zu runden Jahrestagen besonders große Feierlichkeiten.")

    # ── NOVEMBER ────────────────────────────────────────────────────────────
    add_event(lines, date(year, 11, 7),
        "Jahrestag der Oktoberrevolution ☭",
        "Jahrestag der Großen Sozialistischen Oktoberrevolution vom 7. November 1917. Wichtigster ideologischer Feiertag der DDR nach dem Tag der Republik. Kundgebungen\\, Feierstunden in Betrieben\\, Schulen und Parteiorganisationen.")

    add_event(lines, date(year, 11, 10),
        "Gründung des WBDJ / Weltjugendtag 🌍",
        "Jahrestag der Gründung des Weltbundes der Demokratischen Jugend (WBDJ) am 10. November 1945 in London. Weltjugendtag – in der DDR als Zeichen internationaler Jugendbewegung und sozialistischer Solidarität begangen.")

    add_event(lines, date(year, 11, 17),
        "Internationaler Studententag 🎓",
        "Internationaler Studententag – 17. November. Gedenktag für die Opfer der nationalsozialistischen Repression gegen tschechische Studenten 1939. In der DDR als antifaschistischer Kampftag der Studentenbewegung begangen.")

    add_event(lines, date(year, 11, 17),
        "Tag der Militärjustizorgane ⚖️",
        "Tag der Militärjustizorgane der DDR – 17. November. Ehrentag der Beschäftigten in der Militärjustiz der Nationalen Volksarmee.")

    add_event(lines, date(year, 11, 29),
        "Solidaritätstag mit dem palästinensischen Volk 🫱",
        "Internationaler Tag der Solidarität mit dem palästinensischen Volk – 29. November. Von der UN-Generalversammlung 1977 ausgerufen. Die DDR unterhielt enge Beziehungen zur PLO und beging diesen Tag offiziell.")

    add_event(lines, nth_weekday(year, 11, 6, 2),
        "Tag des Chemiearbeiters 🧪",
        "Tag des Chemiearbeiters – zweiter Sonntag im November. Ehrentag der Beschäftigten in der chemischen Industrie der DDR\\, einem der wichtigsten Wirtschaftszweige.")

    add_event(lines, nth_weekday(year, 11, 6, 3),
        "Tag des Metallurgen 🔩",
        "Tag des Metallurgen – dritter Sonntag im November. Ehrentag der Beschäftigten in der Hüttenindustrie und Metallurgie der DDR.")

    # ── DEZEMBER ────────────────────────────────────────────────────────────
    add_event(lines, date(year, 12, 1),
        "Tag der Grenztruppen der DDR 🛡️",
        "Tag der Grenztruppen der DDR – 1. Dezember. Ehrentag der Grenzsoldaten\\, die die Staatsgrenze der DDR sicherten. Begangen mit Appellen und Auszeichnungen.")

    add_event(lines, date(year, 12, 11),
        "Tag des Gesundheitswesens 🏥",
        "Tag des Gesundheitswesens – 11. Dezember. Ehrentag der Beschäftigten im Gesundheits- und Sozialwesen der DDR. Auszeichnungen für herausragende Leistungen in der medizinischen Versorgung.")

    add_event(lines, date(year, 12, 13),
        "Pioniergeburtstag 🔴",
        "Jahrestag der Gründung der Pionierorganisation Ernst Thälmann am 13. Dezember 1948. Massenorganisation für Kinder und Jugendliche der DDR (6–14 Jahre). Gefeiert mit Appellen\\, kulturellen Veranstaltungen und Aufnahmezeremonien.")

    add_event(lines, date(year, 12, 30),
        "KPD-Gründung (1918) ✊",
        "Jahrestag der Gründung der Kommunistischen Partei Deutschlands (KPD) am 30. Dezember 1918 in Berlin. Mitgegründet von Rosa Luxemburg und Karl Liebknecht. Ideologischer Ursprungsfeiertag der SED.")

    add_event(lines, date(year, 12, 30),
        "Gründung der UdSSR (1922) ☭",
        "Jahrestag der Gründung der Union der Sozialistischen Sowjetrepubliken (UdSSR) am 30. Dezember 1922. In der DDR als Jubiläum des ersten sozialistischen Staates gewürdigt.")

    # ── NEUE EHRENTAGE ───────────────────────────────────────────────────────

    add_event(lines, date(year, 2, 11),
        "Tag der Zivilverteidigung 🪖",
        "Tag der Zivilverteidigung der DDR – 11. Februar. Ehrentag der Zivilschutzorgane und Bevölkerungsschutzeinrichtungen. Begangen mit Übungen und Auszeichnungen.")

    add_event(lines, date(year, 3, 21),
        "Internationaler Tag gegen Rassendiskriminierung ✊",
        "Internationaler Tag für die Beseitigung der Rassendiskriminierung – 21. März. Gedenkt dem Massaker von Sharpeville (1960). In der DDR als antiimperialistischer Kampftag und Zeichen der Solidarität mit den unterdrückten Völkern begangen.")

    add_event(lines, date(year, 3, 23),
        "Welttag der Meteorologie 🌤️",
        "Welttag der Meteorologie – 23. März. Internationaler Gedenktag der Weltorganisation für Meteorologie (WMO). In der DDR im Kontext des wissenschaftlich-technischen Fortschritts begangen.")

    add_event(lines, date(year, 3, 27),
        "Welttheatertag 🎭",
        "Welttheatertag – 27. März. Internationaler Gedenktag des Theaterlebens\\, ausgerufen vom Internationalen Theaterinstitut (ITI). In der DDR mit Aufführungen und Festveranstaltungen an Theatern begangen.")

    add_event(lines, date(year, 4, 7),
        "Weltgesundheitstag 🏥",
        "Weltgesundheitstag – 7. April. Jahrestag der Gründung der Weltgesundheitsorganisation (WHO\\, 1948). In der DDR mit Veranstaltungen zur sozialistischen Gesundheitspolitik und kostenloser Grundversorgung begangen.")

    add_event(lines, date(year, 4, 18),
        "Internationaler Denkmaltag 🏛️",
        "Internationaler Denkmaltag – 18. April. Tag des kulturellen Erbes\\, ausgerufen vom Internationalen Rat für Denkmalpflege (ICOMOS). In der DDR im Kontext der Denkmalpflege und des sozialistischen Kulturerbes begangen.")

    add_event(lines, date(year, 4, 24),
        "Internationaler Tag der Jugend gegen Kolonialismus 🌍",
        "Internationaler Tag der Jugend und Studenten gegen Kolonialismus und für friedliche Koexistenz – 24. April. In der DDR als antikolonialer Solidaritätstag begangen.")

    add_event(lines, date(year, 5, 8),
        "Weltrotkreuztag 🔴",
        "Weltrotkreuztag – 8. Mai. Geburtstag von Henri Dunant\\, dem Gründer des Roten Kreuzes (1828). In der DDR durch das Deutsche Rote Kreuz (DRK) mit Veranstaltungen und Spendenaktionen begangen.")

    add_event(lines, date(year, 5, 10),
        "Tag des freien Buches 📚",
        "Tag des freien Buches – 10. Mai. Gedenktag im Andenken an die Bücherverbrennung durch die Nationalsozialisten am 10. Mai 1933 in Deutschland. In der DDR als antifaschistischer Kulturtag begangen.")

    add_event(lines, date(year, 5, 17),
        "Weltfernmeldetag 📡",
        "Weltfernmeldetag – 17. Mai. Jahrestag der Gründung der Internationalen Fernmeldeunion (ITU\\, 1865). In der DDR im Zusammenhang mit dem Ehrentag der Post- und Fernmeldewerktätigen begangen.")

    add_event(lines, date(year, 5, 18),
        "Internationaler Museumstag 🏛️",
        "Internationaler Museumstag – 18. Mai. Ausgerufen vom Internationalen Museumsrat (ICOM). In der DDR mit kostenlosen Museumseintritten\\, Sonderführungen und kulturellen Veranstaltungen begangen.")

    add_event(lines, date(year, 6, 5),
        "Weltumwelttag 🌿",
        "Weltumwelttag – 5. Juni. Ausgerufen von den Vereinten Nationen seit 1972. In der DDR im Kontext des sozialistischen Umweltschutzes und der Naturpflege begangen.")

    add_event(lines, date(year, 10, 1),
        "Weltmusiktag 🎵",
        "Weltmusiktag – 1. Oktober. Internationaler Gedenktag der Musik\\, begangen in vielen sozialistischen Ländern. In der DDR mit Konzerten\\, Musikfestivals und kulturellen Veranstaltungen begangen.")

    # ── GEDENKTAGE: PERSONEN UND HISTORISCHE EREIGNISSE ─────────────────────

    add_event(lines, date(year, 1, 3),
        "Geburtstag Wilhelm Pieck (1876) 🕯️",
        f"Geburtstag Wilhelm Piecks am 3. Januar 1876. Er wäre heute {year - 1876} Jahre alt. Erster und einziger Staatspräsident der DDR (1949–1960)\\, Mitgründer der KPD und der SED. Nach ihm wurden viele Straßen\\, Betriebe und Einrichtungen in der DDR benannt.")

    add_event(lines, date(year, 1, 21),
        "Todestag W. I. Lenin (1924) 🕯️",
        "Todestag Wladimir Iljitsch Lenins am 21. Januar 1924. Begründer der Sowjetunion und des Marxismus-Leninismus. In der DDR mit Gedenkfeiern in Betrieben\\, Schulen und Parteiorganisationen begangen.")

    add_event(lines, date(year, 3, 5),
        "Geburtstag Rosa Luxemburg (1871) 🌹",
        f"Geburtstag Rosa Luxemburgs am 5. März 1871. Sie wäre heute {year - 1871} Jahre alt. Mitbegründerin der KPD\\, revolutionäre Sozialistin und Theoretikerin. Am 15. Januar 1919 ermordet. In der DDR als Märtyrerin der Arbeiterbewegung verehrt.")

    add_event(lines, date(year, 3, 11),
        "Geburtstag Otto Grotewohl (1894) 🕯️",
        f"Geburtstag Otto Grotewohls am 11. März 1894. Er wäre heute {year - 1894} Jahre alt. Erster Ministerpräsident der DDR (1949–1964)\\, führte die SPD in der Sowjetischen Besatzungszone in die Zwangsvereinigung mit der KPD zur SED (1946).")

    add_event(lines, date(year, 3, 14),
        "Todestag Karl Marx (1883) 🕯️",
        "Todestag Karl Marx' am 14. März 1883. Begründer des wissenschaftlichen Sozialismus gemeinsam mit Friedrich Engels. Autor des Kommunistischen Manifests (1848) und des Kapitals. Ideologisches Fundament der DDR.")

    add_event(lines, date(year, 4, 16),
        "Geburtstag Ernst Thälmann (1886) ✊",
        f"Geburtstag Ernst Thälmanns am 16. April 1886. Er wäre heute {year - 1886} Jahre alt. Vorsitzender der KPD (1925–1933)\\, inhaftiert von den Nationalsozialisten 1933\\, am 18. August 1944 im KZ Buchenwald ermordet. Zentrales Heldenbild der DDR – nach ihm wurde die Pionierorganisation benannt.")

    add_event(lines, date(year, 5, 5),
        "Geburtstag Karl Marx (1818) 🕯️",
        f"Geburtstag Karl Marx' am 5. Mai 1818 in Trier. Er wäre heute {year - 1818} Jahre alt. Philosoph\\, Ökonom und revolutionärer Theoretiker. Seine Schriften bildeten die ideologische Grundlage des Marxismus-Leninismus und damit der gesamten DDR-Staatsideologie.")

    add_event(lines, date(year, 6, 30),
        "Geburtstag Walter Ulbricht (1893) 🕯️",
        f"Geburtstag Walter Ulbrichts am 30. Juni 1893. Er wäre heute {year - 1893} Jahre alt. Erster Sekretär der SED (1950–1971) und Vorsitzender des Staatsrats (1960–1973). Maßgeblich für den Aufbau der DDR verantwortlich\\, ordnete den Mauerbau 1961 an. Gestorben am 1. August 1973.")

    add_event(lines, date(year, 8, 5),
        "Todestag Friedrich Engels (1895) 🕯️",
        "Todestag Friedrich Engels' am 5. August 1895. Mitbegründer des wissenschaftlichen Sozialismus gemeinsam mit Karl Marx. Finanzierte Marx' Arbeit und vollendete das Kapital nach dessen Tod. Ideologisches Fundament der DDR.")

    add_event(lines, date(year, 8, 13),
        "Geburtstag Karl Liebknecht (1871) 🕯️",
        f"Geburtstag Karl Liebknechts am 13. August 1871. Er wäre heute {year - 1871} Jahre alt. Mitbegründer der KPD\\, erklärte am 9. November 1918 die Freie Sozialistische Republik Deutschland. Am 15. Januar 1919 gemeinsam mit Rosa Luxemburg ermordet.")

    add_event(lines, date(year, 8, 13),
        "Jahrestag des Mauerbaus (1961) 🧱",
        "Jahrestag der Sicherung der Staatsgrenze der DDR am 13. August 1961 – in der DDR offiziell als notwendige Schutzmaßnahme gegen den 'Imperialismus' bezeichnet. Beginn des Baus der Berliner Mauer. In der DDR als Stabilisierung des sozialistischen Staates propagiert.")

    add_event(lines, date(year, 8, 18),
        "Ermordung Ernst Thälmanns (1944) 🕯️",
        "Jahrestag der Ermordung Ernst Thälmanns im KZ Buchenwald am 18. August 1944 auf Befehl Hitlers. Zentrales Märtyrerdatum der DDR-Gedenkkultur. Mit Gedenkfeiern\\, Kranzniederlegungen und Appellen der Pionierorganisation begangen.")

    add_event(lines, date(year, 11, 28),
        "Geburtstag Friedrich Engels (1820) 🕯️",
        f"Geburtstag Friedrich Engels' am 28. November 1820 in Barmen (heute Wuppertal). Er wäre heute {year - 1820} Jahre alt. Mitbegründer des Marxismus\\, enger Weggefährte von Karl Marx. Ideologisches Fundament der DDR-Staatsideologie.")

lines.append("END:VCALENDAR")

with open("/mnt/user-data/outputs/ddr-feiertage.ics", "w", encoding="utf-8") as f:
    f.write("\r\n".join(lines) + "\r\n")

print(f"Fertig! {len([l for l in lines if l == 'BEGIN:VEVENT'])} Einträge generiert.")
