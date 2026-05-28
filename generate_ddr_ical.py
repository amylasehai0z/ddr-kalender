import re
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
    name = re.sub(r"\s*\(\d{4}\)", "", name).strip()
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
lines.append("X-WR-CALNAME:DDR Kalender")
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
        "Geburtstag Lenin ☭",
        f"Wladimir Iljitsch Lenin wurde am 22. April 1870 in Simbirsk (heute Uljanowsk) geboren und starb 1924 mit 53 Jahren. Er wäre heute {year - 1870} Jahre alt. Begründer der Sowjetunion und theoretischer Vordenker des Marxismus-Leninismus. Gedenktag in Betrieben\\, Schulen und Parteiorganisationen.")

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

    # Freitag vor Pfingsten = Ostersonntag + 47 Tage
    add_event(lines, easter(year) + timedelta(days=47),
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
        "Tag der Republik 🇩🇪",
        "Am 21. April 1950 wurde der Nationalfeiertag der Deutschen Demokratischen Republik am 7. Oktober zum bedeutendsten Staatsfeiertag der DDR erklärt. Seitdem wurde er jährlich in Berlin festlich mit einem Staatsakt und einer Militärparade begangen. In der ganzen Republik feierte das Volk mit staatlich organisierten Demonstrationen\\, Festveranstaltungen und Fackelzügen der FDJ den Tag der Republik. An diesem Tag wurden auch die Nationalpreise der DDR an verdiente Künstler\\, Wissenschaftler\\, Techniker und Aktivisten verliehen. Zu runden Jahrestagen gab besonders große Feierlichkeiten. Außerdem wurden alle fünf Jahre Sonderbriefmarken zum Staatsgeburtstag der DDR herausgegeben.")

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
        "Jahrestag der Gründung der Union der Sozialistischen Sowjetrepubliken (UdSSR) am 30. Dezember 1922. In der DDR als Jubiläum des ersten sozialistischen Staates gewürdigt. Die Sowjetunion war ein von der KPdSU zentralistisch regierter\\, föderativer Vielvölkerstaat\\, dessen Territorium sich über Osteuropa\\, den Kaukasus\\, Zentral- und über das gesamte Nordasien erstreckte. Zu den 15 Unionsrepubliken der UdSSR gehörten die Russische SFSR\\, die Ukrainische SSR\\, die Weißrussische SSR\\, die Usbekische SSR\\, die Kasachische SSR\\, die Georgische SSR\\, die Aserbaidschanische SSR\\, die Litauische SSR\\, die Moldauische SSR\\, die Lettische SSR\\, die Kirgisische SSR\\, die Tadschikische SSR\\, die Armenische SSR\\, die Turkmenische SSR und die Estnische SSR.")

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
        "Weltrotkreuztag 🏥 🔴",
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
        f"Wilhelm Pieck wurde am 3. Januar 1876 in Guben geboren und starb 1960 mit 84 Jahren. Er wäre heute {year - 1876} Jahre alt. Erster und einziger Staatspräsident der DDR (1949–1960)\\, Mitgründer der KPD und der SED. Nach ihm wurden viele Straßen\\, Betriebe und Einrichtungen in der DDR benannt.")

    add_event(lines, date(year, 1, 21),
        "Todestag Lenin (1924) 🕯️",
        "Wladimir Iljitsch Lenin\\, geboren im Jahre 1870\\, verstarb am 21. Januar 1924 in Gorki Leninskie. Er wurde 53 Jahre alt. Begründer der Sowjetunion und des Marxismus-Leninismus. In der DDR mit Gedenkfeiern in Betrieben\\, Schulen und Parteiorganisationen begangen.")

    add_event(lines, date(year, 3, 5),
        "Geburtstag Rosa Luxemburg (1871) 🌹",
        f"Rosa Luxemburg wurde am 5. März 1871 in Zamość (Russisches Kaiserreich\\, heute Polen) geboren und wurde 1919 mit 47 Jahren ermordet. Sie wäre heute {year - 1871} Jahre alt. Mitbegründerin der KPD\\, revolutionäre Sozialistin und Theoretikerin. Am 15. Januar 1919 ermordet. In der DDR als Märtyrerin der Arbeiterbewegung verehrt.")

    add_event(lines, date(year, 3, 11),
        "Geburtstag Otto Grotewohl (1894) 🕯️",
        f"Otto Grotewohl wurde am 11. März 1894 in Braunschweig geboren und starb 1964 mit 70 Jahren. Er wäre heute {year - 1894} Jahre alt. Erster Ministerpräsident der DDR (1949–1964)\\, führte die SPD in der Sowjetischen Besatzungszone in die Zwangsvereinigung mit der KPD zur SED (1946).")

    add_event(lines, date(year, 3, 14),
        "Todestag Karl Marx (1883) 🕯️",
        "Karl Marx\\, geboren im Jahre 1818\\, verstarb am 14. März 1883 in London. Er wurde 64 Jahre alt. Begründer des wissenschaftlichen Sozialismus gemeinsam mit Friedrich Engels. Autor des Kommunistischen Manifests (1848) und des Kapitals. Ideologisches Fundament der DDR.")

    add_event(lines, date(year, 4, 16),
        "Geburtstag Ernst Thälmann (1886) ✊",
        f"Ernst Thälmann wurde am 16. April 1886 in Hamburg geboren und wurde 1944 mit 57 Jahren ermordet. Er wäre heute {year - 1886} Jahre alt. Vorsitzender der KPD (1925–1933)\\, inhaftiert von den Nationalsozialisten 1933\\, am 18. August 1944 im KZ Buchenwald ermordet. Zentrales Heldenbild der DDR – nach ihm wurde die Pionierorganisation benannt.")

    add_event(lines, date(year, 5, 5),
        "Geburtstag Karl Marx (1818) 🕯️",
        f"Karl Marx wurde am 5. Mai 1818 in Trier geboren und starb 1883 mit 64 Jahren. Er wäre heute {year - 1818} Jahre alt. Philosoph\\, Ökonom und revolutionärer Theoretiker. Seine Schriften bildeten die ideologische Grundlage des Marxismus-Leninismus und damit der gesamten DDR-Staatsideologie.")

    add_event(lines, date(year, 6, 30),
        "Geburtstag Walter Ulbricht (1893) 🕯️",
        f"Walter Ulbricht wurde am 30. Juni 1893 in Leipzig geboren und starb 1973 mit 80 Jahren. Er wäre heute {year - 1893} Jahre alt. Erster Sekretär der SED (1950–1971) und Vorsitzender des Staatsrats (1960–1973). Maßgeblich für den Aufbau der DDR verantwortlich\\, ordnete den Mauerbau 1961 an. Gestorben am 1. August 1973.")

    add_event(lines, date(year, 8, 5),
        "Todestag Friedrich Engels (1895) 🕯️",
        "Friedrich Engels\\, geboren im Jahre 1820\\, verstarb am 5. August 1895 in London. Er wurde 74 Jahre alt. Mitbegründer des wissenschaftlichen Sozialismus gemeinsam mit Karl Marx. Finanzierte Marx' Arbeit und vollendete das Kapital nach dessen Tod. Ideologisches Fundament der DDR.")

    add_event(lines, date(year, 8, 13),
        "Geburtstag Karl Liebknecht (1871) 🕯️",
        f"Karl Liebknecht wurde am 13. August 1871 in Leipzig geboren und wurde 1919 mit 47 Jahren ermordet. Er wäre heute {year - 1871} Jahre alt. Mitbegründer der KPD\\, erklärte am 9. November 1918 die Freie Sozialistische Republik Deutschland. Am 15. Januar 1919 gemeinsam mit Rosa Luxemburg ermordet.")

    add_event(lines, date(year, 8, 13),
        "Jahrestag des Mauerbaus (1961) 🧱",
        "Jahrestag der Sicherung der Staatsgrenze der DDR am 13. August 1961 – in der DDR offiziell als notwendige Schutzmaßnahme gegen den 'Imperialismus' bezeichnet. Beginn des Baus der Berliner Mauer. In der DDR als Stabilisierung des sozialistischen Staates propagiert.")

    add_event(lines, date(year, 8, 18),
        "Ermordung Ernst Thälmanns (1944) 🕯️",
        "Ernst Thälmann\\, geboren im Jahre 1886\\, wurde am 18. August 1944 im KZ Buchenwald ermordet. Er wurde 57 Jahre alt. Auf Befehl Hitlers erschossen. Zentrales Märtyrerdatum der DDR-Gedenkkultur. Mit Gedenkfeiern\\, Kranzniederlegungen und Appellen der Pionierorganisation begangen.")

    add_event(lines, date(year, 11, 28),
        "Geburtstag Friedrich Engels (1820) 🕯️",
        f"Friedrich Engels wurde am 28. November 1820 in Barmen (heute Wuppertal) geboren und starb 1895 mit 74 Jahren. Er wäre heute {year - 1820} Jahre alt. Mitbegründer des Marxismus\\, enger Weggefährte von Karl Marx. Ideologisches Fundament der DDR-Staatsideologie.")

    add_event(lines, date(year, 9, 7),
        "Todestag Wilhelm Pieck (1960) 🕯️",
        "Wilhelm Pieck\\, geboren im Jahre 1876\\, verstarb am 7. September 1960 in Moskau. Er wurde 84 Jahre alt. Erster und einziger Staatspräsident der DDR (1949–1960)\\, Mitgründer der KPD und der SED. Nach seinem Tod wurde das Amt des Staatspräsidenten abgeschafft und durch den Staatsrat ersetzt.")

    add_event(lines, date(year, 9, 21),
        "Todestag Otto Grotewohl (1964) 🕯️",
        "Otto Grotewohl\\, geboren im Jahre 1894\\, verstarb am 21. September 1964 in Ost-Berlin. Er wurde 70 Jahre alt. Erster Ministerpräsident der DDR (1949–1964)\\, führte die SPD in der Sowjetischen Besatzungszone in die Zwangsvereinigung mit der KPD zur SED (1946).")

    add_event(lines, date(year, 8, 1),
        "Todestag Walter Ulbricht (1973) 🕯️",
        "Walter Ulbricht\\, geboren im Jahre 1893\\, verstarb am 1. August 1973 am Döllnsee in Brandenburg. Er wurde 80 Jahre alt. Erster Sekretär der SED (1950–1971) und Vorsitzender des Staatsrats (1960–1973). Maßgeblich für den Aufbau der DDR verantwortlich\\, ordnete den Mauerbau 1961 an.")

    add_event(lines, date(year, 8, 25),
        "Geburtstag Erich Honecker (1912) 🕯️",
        f"Erich Honecker wurde am 25. August 1912 in Neunkirchen (Saar) geboren und starb 1994 mit 81 Jahren. Er wäre heute {year - 1912} Jahre alt. Generalsekretär der SED und Vorsitzender des Staatsrats (1971–1989)\\, prägte die DDR in ihrer Spätphase. Verantwortlich für den Schießbefehl an der Grenze. Floh 1991 nach Chile\\, wo er 1994 verstarb.")

    add_event(lines, date(year, 5, 29),
        "Todestag Erich Honecker (1994) 🕯️",
        "Erich Honecker\\, geboren im Jahre 1912\\, verstarb am 29. Mai 1994 in Santiago de Chile. Er wurde 81 Jahre alt. Generalsekretär der SED und Vorsitzender des Staatsrats der DDR (1971–1989). Nach dem Mauerfall angeklagt\\, floh er 1991 in die chilenische Botschaft in Moskau und später nach Chile\\, wo er an Leberkrebs starb.")

    add_event(lines, date(year, 4, 17),
        "Geburtstag Margot Honecker (1927) 🕯️",
        f"Margot Honecker wurde am 17. April 1927 in Halle (Saale) geboren und starb 2016 mit 89 Jahren. Sie wäre heute {year - 1927} Jahre alt. Ministerin für Volksbildung der DDR (1963–1989)\\, eine der mächtigsten Frauen des Staates. Ehefrau von Erich Honecker. Verantwortlich für das sozialistische Bildungssystem der DDR. Floh nach dem Mauerfall nach Chile\\, wo sie 2016 verstarb.")

    add_event(lines, date(year, 5, 6),
        "Todestag Margot Honecker (2016) 🕯️",
        "Margot Honecker\\, geboren im Jahre 1927\\, verstarb am 6. Mai 2016 in Santiago de Chile. Sie wurde 89 Jahre alt. Ministerin für Volksbildung der DDR (1963–1989)\\, prägte das sozialistische Schul- und Erziehungswesen. Nach dem Mauerfall floh sie gemeinsam mit Erich Honecker nach Chile\\, wo sie bis zu ihrem Tod lebte.")

    add_event(lines, date(year, 3, 19),
        "Geburtstag Egon Krenz (1937) 🕯️",
        f"Egon Krenz wurde am 19. März 1937 in Kołobrzeg (damals Kolberg\\, heute Polen) geboren. Er ist heute {year - 1937} Jahre alt. Letzter Generalsekretär der SED und Vorsitzender des Staatsrats der DDR (Oktober–Dezember 1989). Langjähriger FDJ-Vorsitzender (1974–1983)\\, galt als designierter Nachfolger Honeckers. Öffnete am 9. November 1989 die Berliner Mauer. 1997 wegen Totschlags an Mauerflüchtlingen verurteilt.")

    add_event(lines, date(year, 12, 28),
        "Geburtstag Erich Mielke (1907) 🕯️",
        f"Erich Mielke wurde am 28. Dezember 1907 in Berlin geboren und starb 2000 mit 92 Jahren. Er wäre heute {year - 1907} Jahre alt. Minister für Staatssicherheit der DDR (1957–1989)\\, Chef der Stasi. Baute den DDR-Geheimdienst zu einem der effektivsten Überwachungsapparate der Welt aus. 1993 wegen Mordes an zwei Polizisten im Jahr 1931 verurteilt.")

    add_event(lines, date(year, 5, 21),
        "Todestag Erich Mielke (2000) 🕯️",
        "Erich Mielke\\, geboren im Jahre 1907\\, verstarb am 21. Mai 2000 in Berlin. Er wurde 92 Jahre alt. Minister für Staatssicherheit der DDR (1957–1989). Unter seiner Führung beschäftigte die Stasi über 90.000 hauptamtliche Mitarbeiter und rund 170.000 inoffizielle Informanten. Nach der Wende wegen Mordes verurteilt\\, wegen Verhandlungsunfähigkeit jedoch vorzeitig entlassen.")

    add_event(lines, date(year, 1, 15),
        "Ermordung Rosa Luxemburg (1919) 🌹",
        "Rosa Luxemburg\\, geboren im Jahre 1871\\, wurde am 15. Januar 1919 in Berlin ermordet. Sie wurde 47 Jahre alt. Mitbegründerin der KPD\\, revolutionäre Sozialistin und Theoretikerin. Nach dem Spartakusaufstand von Freikorpssoldaten verhaftet\\, misshandelt und erschossen. Ihre Leiche wurde in den Landwehrkanal geworfen. In der DDR als Märtyrerin der Arbeiterbewegung verehrt.")

    add_event(lines, date(year, 1, 15),
        "Ermordung Karl Liebknecht (1919) 🕯️",
        "Karl Liebknecht\\, geboren im Jahre 1871\\, wurde am 15. Januar 1919 in Berlin ermordet. Er wurde 47 Jahre alt. Mitbegründer der KPD\\, erklärte am 9. November 1918 die Freie Sozialistische Republik Deutschland. Nach dem Spartakusaufstand von Freikorpssoldaten verhaftet\\, misshandelt und erschossen. In der DDR als Märtyrer der Arbeiterbewegung verehrt.")

    add_event(lines, date(year, 3, 17),
        "Weltschifffahrtstag 🚢",
        "Weltschifffahrtstag – 17. März. Internationaler Gedenktag der Schifffahrt\\, ausgerufen von der Internationalen Seeschifffahrts-Organisation (IMO). In der DDR im Kontext der Seeverkehrswirtschaft und des Rostocker Hafens begangen.")

    add_event(lines, date(year, 4, 12),
        "Tag der Luft- und Raumfahrt 🚀",
        "Tag der Luft- und Raumfahrt – 12. April. Jahrestag des ersten bemannten Weltraumflugs durch Juri Gagarin am 12. April 1961. In der DDR mit Veranstaltungen in Schulen\\, Betrieben und Planetarien begangen. Besonders bedeutsam nach dem gemeinsamen Weltraumflug von Sigmund Jähn am 26. August 1978\\, dem ersten Deutschen im Weltall.")

    add_event(lines, date(year, 4, 12),
        "Tag der Jungen Techniker und Naturforscher 🔬",
        "Tag der Jungen Techniker und Naturforscher – 12. April. Ehrentag der Kinder und Jugendlichen\\, die sich in den Arbeitsgemeinschaften für Technik\\, Naturwissenschaft und Astronomie engagierten. Organisiert durch die Pionierorganisation Ernst Thälmann und die Gesellschaft für Sport und Technik (GST). Begleitet von Ausstellungen\\, Wettbewerben und Vorführungen.")

    add_event(lines, date(year, 4, 23),
        "Welttag des Buches 📖",
        "Welttag des Buches – 23. April. Internationaler Gedenktag für Literatur und das Lesen. In der DDR im Kontext der sozialistischen Bildungspolitik und des staatlichen Verlagswesens begangen. Die DDR hatte eine der höchsten Lesequoten der Welt.")

    add_event(lines, nth_weekday(year, 4, 6, -1),
        "Welttag der Partnerstädte 🤝",
        "Welttag der Partnerstädte – letzter Sonntag im April. Internationaler Gedenktag der Städtepartnerschaften\\, ausgerufen vom Weltverband der Partnerstädte (WFUCA). In der DDR wurden Partnerschaften vor allem mit sozialistischen Städten in der UdSSR\\, Polen\\, der Tschechoslowakei und anderen Bruderstaaten gepflegt.")

    add_event(lines, date(year, 6, 16),
        "Tag der Solidarität mit Südafrika ✊",
        "Tag der Solidarität mit dem Kampf des Volkes von Südafrika – 16. Juni. Gedenktag im Andenken an den Soweto-Aufstand vom 16. Juni 1976\\, bei dem südafrikanische Schüler gegen die Apartheidpolitik protestierten und von der Polizei erschossen wurden. In der DDR als antiimperialistischer Solidaritätstag begangen.")


    # ── Hannes Hegen ──────────────────────────────────────────────────────────
    add_event(lines, date(year, 5, 16),
        "Geburtstag Hannes Hegen 📖",
        f"Hannes Hegen (eigentl. Johannes Eduard Hegenbarth) wurde am 16. Mai 1925 in Böhmisch Kamnitz (heute Česká Kamenice\\, Tschechien) geboren und starb 2014 mit 89 Jahren. Er wäre heute {year - 1925} Jahre alt. Grafiker und Comiczeichner\\, Schöpfer der DDR-Comicreihe Mosaik mit den Digedags (1955–1975). Das Mosaik erschien im Verlag Junge Welt und war die meistgelesene Kinderzeitschrift der DDR. Sein Grab in Berlin-Karlshorst ist Ehrengrab des Landes Berlin.")

    add_event(lines, date(year, 11, 8),
        "Todestag Hannes Hegen 📖",
        "Hannes Hegen (eigentl. Johannes Eduard Hegenbarth)\\, geboren im Jahre 1925\\, verstarb am 8. November 2014 in Berlin. Er wurde 89 Jahre alt. Schöpfer der DDR-Comicreihe Mosaik mit den Digedags (1955–1975) und bedeutendster Comiczeichner der DDR.")


    # ── Willi Stoph (9.7.1914 – 13.4.1999) ────────────────────────────────────
    add_event(lines, date(year, 7, 9),
        "Geburtstag Willi Stoph 🏛️",
        f"Willi Stoph wurde am 9. Juli 1914 in Berlin-Schöneberg geboren und starb 1999 mit 84 Jahren. Er wäre heute {year - 1914} Jahre alt. Politiker der SED\\, Ministerratsvorsitzender der DDR 1964–1973 und 1976–1989\\, sowie Staatsratsvorsitzender 1973–1976. Einer der mächtigsten Männer der DDR über Jahrzehnte.")
    add_event(lines, date(year, 4, 13),
        "Todestag Willi Stoph 🏛️",
        "Willi Stoph\\, geboren 1914\\, verstarb am 13. April 1999 in Berlin. Er wurde 84 Jahre alt. Ministerratsvorsitzender und Staatsratsvorsitzender der DDR.")

    # ── Horst Sindermann (5.9.1915 – 20.4.1990) ────────────────────────────────
    add_event(lines, date(year, 9, 5),
        "Geburtstag Horst Sindermann 🏛️",
        f"Horst Sindermann wurde am 5. September 1915 in Dresden geboren und starb 1990 mit 74 Jahren. Er wäre heute {year - 1915} Jahre alt. Politiker der SED\\, Ministerratsvorsitzender der DDR 1973–1976 und langjähriger Präsident der Volkskammer 1976–1989.")
    add_event(lines, date(year, 4, 20),
        "Todestag Horst Sindermann 🏛️",
        "Horst Sindermann\\, geboren 1915\\, verstarb am 20. April 1990 in Ost-Berlin. Er wurde 74 Jahre alt. Ministerratsvorsitzender und Volkskammerpräsident der DDR.")

    # ── Kurt Hager (24.7.1912 – 18.9.1998) ─────────────────────────────────────
    add_event(lines, date(year, 7, 24),
        "Geburtstag Kurt Hager 📚",
        f"Kurt Hager wurde am 24. Juli 1912 in Bietigheim (Württemberg) geboren und starb 1998 mit 86 Jahren. Er wäre heute {year - 1912} Jahre alt. Chefideologe der SED\\, Mitglied des Politbüros\\, zuständig für Wissenschaft\\, Bildung und Kultur. Bekannt für sein Zitat von 1987: 'Wenn Ihr Nachbar seine Wohnung neu tapeziert\\, müssen Sie doch nicht auch Ihre Wohnung neu tapezieren.'")
    add_event(lines, date(year, 9, 18),
        "Todestag Kurt Hager 📚",
        "Kurt Hager\\, geboren 1912\\, verstarb am 18. September 1998 in Berlin. Er wurde 86 Jahre alt. Chefideologe der SED und langjähriges Politbüromitglied der DDR.")

    # ── Hanns Eisler (6.7.1898 – 6.9.1962) ─────────────────────────────────────
    add_event(lines, date(year, 7, 6),
        "Geburtstag Hanns Eisler 🎵",
        f"Hanns Eisler wurde am 6. Juli 1898 in Leipzig geboren und starb 1962 mit 64 Jahren. Er wäre heute {year - 1898} Jahre alt. Komponist und Schöpfer der DDR-Nationalhymne 'Auferstanden aus Ruinen' (1949\\, Text: Johannes R. Becher). Enger künstlerischer Weggefährte von Bertolt Brecht. Die Hochschule für Musik Berlin trägt seinen Namen.")
    add_event(lines, date(year, 9, 6),
        "Todestag Hanns Eisler 🎵",
        "Hanns Eisler\\, geboren 1898\\, verstarb am 6. September 1962 in Ost-Berlin. Er wurde 64 Jahre alt. Komponist der DDR-Nationalhymne 'Auferstanden aus Ruinen'.")

    # ── Bertolt Brecht (10.2.1898 – 14.8.1956) ─────────────────────────────────
    add_event(lines, date(year, 2, 10),
        "Geburtstag Bertolt Brecht ✍️",
        f"Bertolt Brecht wurde am 10. Februar 1898 in Augsburg geboren und starb 1956 mit 58 Jahren. Er wäre heute {year - 1898} Jahre alt. Bedeutendster deutschsprachiger Dramatiker des 20. Jahrhunderts\\, Begründer des epischen Theaters. Ab 1949 in Ost-Berlin tätig\\, gründete er das Berliner Ensemble. Werke: Die Dreigroschenoper\\, Mutter Courage und ihre Kinder\\, Der gute Mensch von Sezuan.")
    add_event(lines, date(year, 8, 14),
        "Todestag Bertolt Brecht ✍️",
        "Bertolt Brecht\\, geboren 1898\\, verstarb am 14. August 1956 in Ost-Berlin an einem Herzinfarkt. Er wurde 58 Jahre alt. Dramatiker\\, Lyriker und Gründer des Berliner Ensembles.")

    # ── Anna Seghers (19.11.1900 – 1.6.1983) ───────────────────────────────────
    add_event(lines, date(year, 11, 19),
        "Geburtstag Anna Seghers ✍️",
        f"Anna Seghers (eigentl. Netty Reiling) wurde am 19. November 1900 in Mainz geboren und starb 1983 mit 82 Jahren. Sie wäre heute {year - 1900} Jahre alt. Bedeutendste Schriftstellerin der DDR\\, Präsidentin des Schriftstellerverbandes 1952–1978. Bekannt für ihren Roman 'Das siebte Kreuz' (1942). Trägerin des Nationalpreises der DDR.")
    add_event(lines, date(year, 6, 1),
        "Todestag Anna Seghers ✍️",
        "Anna Seghers\\, geboren 1900\\, verstarb am 1. Juni 1983 in Ost-Berlin. Sie wurde 82 Jahre alt. Schriftstellerin und langjährige Präsidentin des Schriftstellerverbandes der DDR.")

    # ── Christa Wolf (18.3.1929 – 1.12.2011) ───────────────────────────────────
    add_event(lines, date(year, 3, 18),
        "Geburtstag Christa Wolf ✍️",
        f"Christa Wolf wurde am 18. März 1929 in Landsberg an der Warthe geboren und starb 2011 mit 82 Jahren. Sie wäre heute {year - 1929} Jahre alt. Bedeutendste Schriftstellerin der DDR ihrer Generation. Werke: Der geteilte Himmel\\, Nachdenken über Christa T.\\, Kassandra. Trägerin des Georg-Büchner-Preises 1980.")
    add_event(lines, date(year, 12, 1),
        "Todestag Christa Wolf ✍️",
        "Christa Wolf\\, geboren 1929\\, verstarb am 1. Dezember 2011 in Berlin. Sie wurde 82 Jahre alt. Schriftstellerin und wichtigste literarische Stimme der DDR.")

    # ── Marita Koch (18.2.1957) ─────────────────────────────────────────────────
    add_event(lines, date(year, 2, 18),
        "Geburtstag Marita Koch 🏃",
        f"Marita Koch wurde am 18. Februar 1957 in Wismar geboren. Sie ist heute {year - 1957} Jahre alt. DDR-Leichtathletin\\, Olympiasiegerin 1980 über 400 m in Moskau. Ihr Weltrekord von 47\\,60 Sekunden über 400 Meter (6. Oktober 1985) ist bis heute ungebrochen – der langlebigste Weltrekord der Leichtathletik. 15 Weltrekorde in olympischen Disziplinen. 2014 in die IAAF Hall of Fame aufgenommen.")

    # ── Manfred Krug (8.2.1937 – 21.10.2016) ───────────────────────────────────
    add_event(lines, date(year, 2, 8),
        "Geburtstag Manfred Krug 🎬",
        f"Manfred Krug wurde am 8. Februar 1937 in Duisburg geboren und starb 2016 mit 79 Jahren. Er wäre heute {year - 1937} Jahre alt. Schauspieler\\, Sänger und Schriftsteller\\, einer der bedeutendsten Künstler der DDR. Bekannt durch Filme wie 'Spur der Steine' (1966). 1977 Übersiedlung in die Bundesrepublik. Später in der BRD durch 'Tatort' und 'Liebling Kreuzberg' bekannt.")
    add_event(lines, date(year, 10, 21),
        "Todestag Manfred Krug 🎬",
        "Manfred Krug\\, geboren 1937\\, verstarb am 21. Oktober 2016 in Berlin. Er wurde 79 Jahre alt. Schauspieler und Sänger\\, einer der bedeutendsten Künstler der DDR.")

    # ── Gerhard Gundermann (21.2.1955 – 21.6.1998) ─────────────────────────────
    add_event(lines, date(year, 2, 21),
        "Geburtstag Gerhard Gundermann 🎸",
        f"Gerhard Gundermann wurde am 21. Februar 1955 in Weimar geboren und starb 1998 mit 43 Jahren. Er wäre heute {year - 1955} Jahre alt. Liedermacher\\, Rockmusiker und Baggerfahrer im Lausitzer Braunkohlerevier. Stimme der einfachen Arbeiter in der DDR. Bekannt für melancholische\\, authentische Lieder über Alltag\\, Arbeit und den Osten. Sein Leben wurde 2018 mit dem Film 'Gundermann' gewürdigt.")
    add_event(lines, date(year, 6, 21),
        "Todestag Gerhard Gundermann 🎸",
        "Gerhard Gundermann\\, geboren 1955\\, verstarb am 21. Juni 1998 in Spreetal (Lausitz). Er wurde nur 43 Jahre alt. Liedermacher und Baggerfahrer\\, Stimme der Arbeiter in der DDR.")


    # ══ TOP 30 DDR-SCHAUSPIELER ══════════════════════════════════════════════

    # Erwin Geschonneck (27.12.1906 – 12.3.2008)
    add_event(lines, date(year, 12, 27),
        "Geburtstag Erwin Geschonneck 🎬",
        f"Erwin Geschonneck wurde am 27. Dezember 1906 in Bartenstein (Ostpreußen) geboren und starb 2008 mit 101 Jahren. Er wäre heute {year - 1906} Jahre alt. Bedeutendster DEFA-Schauspieler\\, KZ-Überlebender (Sachsenhausen\\, Dachau). Bekannt durch 'Jakob der Lügner' (1974\\, Oscar-Nominierung)\\, 'Karbid und Sauerampfer' und 'Nackt unter Wölfen'. Über 100 Film- und Fernsehproduktionen.")
    add_event(lines, date(year, 3, 12),
        "Todestag Erwin Geschonneck 🎬",
        "Erwin Geschonneck\\, geboren 1906\\, verstarb am 12. März 2008 in Berlin. Er wurde 101 Jahre alt. Bedeutendster DEFA-Schauspieler und KZ-Überlebender.")

    # Armin Mueller-Stahl (17.12.1930)
    add_event(lines, date(year, 12, 17),
        "Geburtstag Armin Mueller-Stahl 🎬",
        f"Armin Mueller-Stahl wurde am 17. Dezember 1930 in Tilsit (Ostpreußen) geboren. Er ist heute {year - 1930} Jahre alt. Schauspieler und Maler\\, einer der bekanntesten DDR-Schauspieler. Bekannt durch 'Spur der Steine' (1966). 1980 Übersiedlung in die BRD\\, später internationale Karriere in Hollywood. Oscar-Nominierung für 'Shine' (1996).")

    # Rolf Hoppe (6.12.1930 – 14.11.2018)
    add_event(lines, date(year, 12, 6),
        "Geburtstag Rolf Hoppe 🎬",
        f"Rolf Hoppe wurde am 6. Dezember 1930 in Ellrich (Thüringen) geboren und starb 2018 mit 87 Jahren. Er wäre heute {year - 1930} Jahre alt. Schauspieler mit über 400 Film- und Fernsehrollen. Bekannt durch 'Drei Haselnüsse für Aschenbrödel' (1973) und 'Mephisto' (1981). Prägte Generationen von DDR-Kindern.")
    add_event(lines, date(year, 11, 14),
        "Todestag Rolf Hoppe 🎬",
        "Rolf Hoppe\\, geboren 1930\\, verstarb am 14. November 2018 in Dresden. Er wurde 87 Jahre alt. Schauspieler\\, bekannt durch 'Drei Haselnüsse für Aschenbrödel' und 'Mephisto'.")

    # Ulrich Mühe (20.6.1953 – 22.7.2007)
    add_event(lines, date(year, 6, 20),
        "Geburtstag Ulrich Mühe 🎬",
        f"Ulrich Mühe wurde am 20. Juni 1953 in Grimma (Sachsen) geboren und starb 2007 mit 54 Jahren. Er wäre heute {year - 1953} Jahre alt. Schauspieler\\, Star des Deutschen Theaters Berlin. Weltberühmt durch seine Rolle als Stasi-Hauptmann Wiesler in 'Das Leben der Anderen' (2006\\, Oscar-Gewinner). Sprach auf der Demonstration am Alexanderplatz am 4. November 1989.")
    add_event(lines, date(year, 7, 22),
        "Todestag Ulrich Mühe 🎬",
        "Ulrich Mühe\\, geboren 1953\\, verstarb am 22. Juli 2007 in Walbeck (Sachsen-Anhalt). Er wurde nur 54 Jahre alt. Schauspieler\\, bekannt durch 'Das Leben der Anderen'.")

    # Angelica Domröse (4.4.1941 – 15.5.2026)
    add_event(lines, date(year, 4, 4),
        "Geburtstag Angelica Domröse 🎬",
        f"Angelica Domröse wurde am 4. April 1941 in Berlin geboren und starb 2026 mit 85 Jahren. Sie wäre heute {year - 1941} Jahre alt. Bekannteste DDR-Schauspielerin\\, unsterblich als 'Paula' in 'Die Legende von Paul und Paula' (1973). Unterzeichnete 1976 die Biermann-Petition\\, siedelte 1980 in die BRD über. Verheiratet mit Hilmar Thate.")
    add_event(lines, date(year, 5, 15),
        "Todestag Angelica Domröse 🎬",
        "Angelica Domröse\\, geboren 1941\\, verstarb am 15. Mai 2026 in Berlin. Sie wurde 85 Jahre alt. Bekannteste DDR-Schauspielerin\\, unvergessen als Paula in 'Die Legende von Paul und Paula'.")

    # Winfried Glatzeder (26.4.1945)
    add_event(lines, date(year, 4, 26),
        "Geburtstag Winfried Glatzeder 🎬",
        f"Winfried Glatzeder wurde am 26. April 1945 in Zoppot (heute Polen) geboren. Er ist heute {year - 1945} Jahre alt. Schauspieler\\, bekannt als 'Paul' in 'Die Legende von Paul und Paula' (1973) – einer der meistgesehenen DDR-Filme. Spielte auch in 'Till Eulenspiegel' (1975). Siedelte 1982 in die BRD über.")

    # Hilmar Thate (17.4.1931 – 14.9.2016)
    add_event(lines, date(year, 4, 17),
        "Geburtstag Hilmar Thate 🎬",
        f"Hilmar Thate wurde am 17. April 1931 in Dölau bei Halle geboren und starb 2016 mit 85 Jahren. Er wäre heute {year - 1931} Jahre alt. Bedeutendster DDR-Theaterschauspieler\\, Berliner Ensemble. Bekannt durch 'Der geteilte Himmel' (1964) und 'Veronika Voss' (1982). Unterzeichnete die Biermann-Petition\\, siedelte 1980 mit Angelica Domröse in die BRD über.")
    add_event(lines, date(year, 9, 14),
        "Todestag Hilmar Thate 🎬",
        "Hilmar Thate\\, geboren 1931\\, verstarb am 14. September 2016 in Berlin. Er wurde 85 Jahre alt. Bedeutendster DDR-Theaterschauspieler und Mitglied des Berliner Ensembles.")

    # Gojko Mitic (13.6.1940)
    add_event(lines, date(year, 6, 13),
        "Geburtstag Gojko Mitić 🎬",
        f"Gojko Mitić wurde am 13. Juni 1940 in Strojkovce (Jugoslawien\\, heute Serbien) geboren. Er ist heute {year - 1940} Jahre alt. Serbisch-deutscher Schauspieler\\, 'Chefindianer der DDR'. Spielte in zahlreichen DEFA-Indianerfilmen Häuptlingsrollen (ab 1966). 'Die Söhne der großen Bärin' (1966) wurde von 29 Millionen Sowjetbürgern gesehen.")

    # Jutta Hoffmann (3.3.1941)
    add_event(lines, date(year, 3, 3),
        "Geburtstag Jutta Hoffmann 🎬",
        f"Jutta Hoffmann wurde am 3. März 1941 in Halle an der Saale geboren. Sie ist heute {year - 1941} Jahre alt. Bedeutende DDR-Schauspielerin\\, bekannt durch 'Solo Sunny' (1980) und zahlreiche DEFA-Produktionen. Galt als wichtige Charakterdarstellerin der DDR.")

    # Eberhard Esche (25.10.1933 – 15.5.2006)
    add_event(lines, date(year, 10, 25),
        "Geburtstag Eberhard Esche 🎬",
        f"Eberhard Esche wurde am 25. Oktober 1933 in Leipzig geboren und starb 2006 mit 72 Jahren. Er wäre heute {year - 1933} Jahre alt. DDR-Schauspieler\\, bekannt durch 'Spur der Steine' (1966) und 'Der geteilte Himmel' (1964). Mitglied des Berliner Ensembles.")
    add_event(lines, date(year, 5, 15),
        "Todestag Eberhard Esche 🎬",
        "Eberhard Esche\\, geboren 1933\\, verstarb am 15. Mai 2006 in Berlin. Er wurde 72 Jahre alt. DDR-Schauspieler und Mitglied des Berliner Ensembles.")

    # Ekkehard Schall (29.5.1930 – 3.9.2005)
    add_event(lines, date(year, 5, 29),
        "Geburtstag Ekkehard Schall 🎭",
        f"Ekkehard Schall wurde am 29. Mai 1930 in Magdeburg geboren und starb 2005 mit 75 Jahren. Er wäre heute {year - 1930} Jahre alt. Bedeutendster Brecht-Schauspieler der DDR\\, Mitglied des Berliner Ensembles ab 1952. Von Brecht persönlich engagiert. Verheiratet mit Brechts Tochter Barbara. Spielte den Arturo Ui über 500 Mal.")
    add_event(lines, date(year, 9, 3),
        "Todestag Ekkehard Schall 🎭",
        "Ekkehard Schall\\, geboren 1930\\, verstarb am 3. September 2005 in Berlin. Er wurde 75 Jahre alt. Bedeutendster Brecht-Schauspieler der DDR.")

    # Renate Blume (3.5.1944)
    add_event(lines, date(year, 5, 3),
        "Geburtstag Renate Blume 🎬",
        f"Renate Blume wurde am 3. Mai 1944 in Bad Wildungen geboren. Sie ist heute {year - 1944} Jahre alt. DDR-Schauspielerin\\, Publikumsliebling und Traumpaar mit Gojko Mitić. Bekannt durch 'Ulzana' (1974) und 'Der geteilte Himmel' (1964). War mit DEFA-Regisseur Frank Beyer verheiratet\\, später mit US-Sänger Dean Reed.")

    # Katrin Sass (23.10.1956)
    add_event(lines, date(year, 10, 23),
        "Geburtstag Katrin Sass 🎬",
        f"Katrin Sass wurde am 23. Oktober 1956 in Schwerin geboren. Sie ist heute {year - 1956} Jahre alt. DDR-Schauspielerin\\, Silberner Bär der Berlinale 1982. Weltweit bekannt durch 'Good Bye\\, Lenin!' (2003). Einer der bekanntesten DDR-Gesichter im wiedervereinigten Deutschland.")

    # Rolf Ludwig (15.6.1925 – 18.10.1999)
    add_event(lines, date(year, 6, 15),
        "Geburtstag Rolf Ludwig 🎬",
        f"Rolf Ludwig wurde am 15. Juni 1925 in Lauban (Schlesien) geboren und starb 1999 mit 74 Jahren. Er wäre heute {year - 1925} Jahre alt. Einer der populärsten DDR-Schauspieler\\, Volksschauspieler und Charakterdarsteller. Über vier Jahrzehnte prägend für Theater und Film in der DDR.")
    add_event(lines, date(year, 10, 18),
        "Todestag Rolf Ludwig 🎬",
        "Rolf Ludwig\\, geboren 1925\\, verstarb am 18. Oktober 1999 in Berlin. Er wurde 74 Jahre alt. Einer der populärsten Volksschauspieler der DDR.")

    # Jürgen Frohriep (21.3.1928 – 30.5.1993)
    add_event(lines, date(year, 3, 21),
        "Geburtstag Jürgen Frohriep 🎬",
        f"Jürgen Frohriep wurde am 21. März 1928 in Dresden geboren und starb 1993 mit 65 Jahren. Er wäre heute {year - 1928} Jahre alt. DDR-Fernsehikone\\, bekannt als 'Alter Fritz' und durch zahlreiche DEFA-Produktionen. Über Jahrzehnte eines der bekanntesten Gesichter im DDR-Fernsehen.")
    add_event(lines, date(year, 5, 30),
        "Todestag Jürgen Frohriep 🎬",
        "Jürgen Frohriep\\, geboren 1928\\, verstarb am 30. Mai 1993 in Berlin. Er wurde 65 Jahre alt. DDR-Fernsehikone und DEFA-Schauspieler.")

    # Michael Gwisdek (18.5.1942 – 28.8.2020)
    add_event(lines, date(year, 5, 18),
        "Geburtstag Michael Gwisdek 🎬",
        f"Michael Gwisdek wurde am 18. Mai 1942 in Berlin geboren und starb 2020 mit 78 Jahren. Er wäre heute {year - 1942} Jahre alt. DDR-Schauspieler und Regisseur. Bekannt durch 'Gritta vom Rattenschloss' und zahlreiche DEFA-Produktionen. Nach der Wende weiterhin erfolgreich.")
    add_event(lines, date(year, 8, 28),
        "Todestag Michael Gwisdek 🎬",
        "Michael Gwisdek\\, geboren 1942\\, verstarb am 28. August 2020 in Penzberg (Bayern). Er wurde 78 Jahre alt. DDR-Schauspieler und Regisseur.")

    # Renate Krößner (17.5.1945 – 26.5.2020)
    add_event(lines, date(year, 5, 17),
        "Geburtstag Renate Krößner 🎬",
        f"Renate Krößner wurde am 17. Mai 1945 in Fürstenwalde geboren und starb 2020 mit 75 Jahren. Sie wäre heute {year - 1945} Jahre alt. DDR-Schauspielerin\\, unvergessen als 'Solo Sunny' (1980). Silberner Bär der Berlinale 1980 für diese Rolle. Ihr Geburtstag wurde 2023 posthum mit einem Google Doodle geehrt.")
    add_event(lines, date(year, 5, 26),
        "Todestag Renate Krößner 🎬",
        "Renate Krößner\\, geboren 1945\\, verstarb am 26. Mai 2020. Sie wurde 75 Jahre alt. DDR-Schauspielerin\\, unvergessen als 'Solo Sunny'.")

    # Herbert Köfer (20.3.1921 – 1.9.2022)
    add_event(lines, date(year, 3, 20),
        "Geburtstag Herbert Köfer 🎬",
        f"Herbert Köfer wurde am 20. März 1921 in Berlin geboren und starb 2022 mit 101 Jahren. Er wäre heute {year - 1921} Jahre alt. Schauspieler und Entertainer\\, einer der bekanntesten Gesichter des DDR-Fernsehens. Präsentierte den 'Kessel Buntes' und zahlreiche Unterhaltungssendungen. Über 70 Jahre Bühnen- und Fernsehkarriere.")
    add_event(lines, date(year, 9, 1),
        "Todestag Herbert Köfer 🎬",
        "Herbert Köfer\\, geboren 1921\\, verstarb am 1. September 2022 in Berlin. Er wurde 101 Jahre alt. Schauspieler und Entertainer\\, das bekannteste Gesicht des DDR-Fernsehens.")

    # Kurt Böwe (2.7.1929 – 15.3.2000)
    add_event(lines, date(year, 7, 2),
        "Geburtstag Kurt Böwe 🎬",
        f"Kurt Böwe wurde am 2. Juli 1929 in Köslin (Pommern) geboren und starb 2000 mit 70 Jahren. Er wäre heute {year - 1929} Jahre alt. DDR-Schauspieler\\, Nationalpreisträger. Bekannt durch 'Einer trage des anderen Last' (1988) und 'Märkische Forschungen'. Hervorragender Charakterdarsteller.")
    add_event(lines, date(year, 3, 15),
        "Todestag Kurt Böwe 🎬",
        "Kurt Böwe\\, geboren 1929\\, verstarb am 15. März 2000. Er wurde 70 Jahre alt. DDR-Schauspieler und Nationalpreisträger.")

    # Rolf Herricht (27.7.1927 – 1.3.1981)
    add_event(lines, date(year, 7, 27),
        "Geburtstag Rolf Herricht 🎬",
        f"Rolf Herricht wurde am 27. Juli 1927 in Berlin geboren und starb 1981 mit 53 Jahren. Er wäre heute {year - 1927} Jahre alt. Beliebtester Komiker der DDR\\, Mitglied des legendären Komikerduos Herricht & Haase. Sein früher Tod mit 53 Jahren traf die DDR-Bevölkerung tief.")
    add_event(lines, date(year, 3, 1),
        "Todestag Rolf Herricht 🎬",
        "Rolf Herricht\\, geboren 1927\\, verstarb am 1. März 1981 in Berlin. Er wurde nur 53 Jahre alt. Beliebtester Komiker der DDR.")

    # Horst Drinda (1.5.1927 – 21.2.2005)
    add_event(lines, date(year, 5, 1),
        "Geburtstag Horst Drinda 🎬",
        f"Horst Drinda wurde am 1. Mai 1927 in Berlin geboren — ausgerechnet am Tag der Arbeit — und starb 2005 mit 77 Jahren. Er wäre heute {year - 1927} Jahre alt. Schauspieler und Regisseur\\, einer der meistbeschäftigten Darsteller des Deutschen Theaters Berlin in den 1950er Jahren. Beim DDR-Fernsehen wurde er vor allem bekannt als Kapitän Hans Karsten in der Kultserie 'Zur See' (1977). Daneben spielte er in der propagandistischen Serie 'Ich – Axel Cäsar Springer' (1967–1970) die Titelrolle. Mehrfacher Nationalpreisträger der DDR\\, zuletzt 1987 mit dem Nationalpreis I. Klasse für Kunst und Literatur.")
    add_event(lines, date(year, 2, 21),
        "Todestag Horst Drinda 🎬",
        "Horst Drinda (1927–2005) starb am 21. Februar 2005 in Berlin im Alter von 77 Jahren. Seit zwei Schlaganfällen im Mai 2003 war er gelähmt. Der Schauspieler und Regisseur gehörte jahrzehntelang zum Deutschen Theater Berlin und später zum Schauspielerensemble des DFF. Unvergessen als Kapitän Hans Karsten in 'Zur See' (1977) — der beliebtesten DDR-Fernsehserie. Sein Enkel ist die Schauspielerin Lea Drinda (* 2001).")

    # Peter Sodann (1.6.1936 – 5.4.2024)
    add_event(lines, date(year, 6, 1),
        "Geburtstag Peter Sodann 🎬",
        f"Peter Sodann wurde am 1. Juni 1936 in Meißen (Sachsen) geboren und starb 2024 mit 87 Jahren. Er wäre heute {year - 1936} Jahre alt. Schauspieler, Regisseur und Theaterleiter. Intendant des neuen theaters Halle (nt), das er 1981 aus einem alten Kinosaal aufbaute. Bundesweit bekannt durch die Rolle des Kommissars Bruno Ehrlicher im MDR-'Tatort' (1992–2007). 1961 wurde er verhaftet und zu zwei Jahren Haft verurteilt, weil sein Studentenkabarett als 'konterrevolutionär' eingestuft worden war. Kandidierte 2009 für das Bundespräsidentenamt. Ehrenbürger der Stadt Halle.")
    add_event(lines, date(year, 4, 5),
        "Todestag Peter Sodann 🎬",
        "Peter Sodann (1936–2024) starb am 5. April 2024 in Halle im Alter von 87 Jahren. Der Schauspieler und Theatermacher war als Kommissar Bruno Ehrlicher im MDR-'Tatort' (1992–2008) bundesweit bekannt. Als Intendant des Stadttheaters Halle prägte er das Kulturleben Sachsen-Anhalts. 2009 kandidierte er für das Bundespräsidentenamt.")

    # Helga Piur (24.5.1939 – lebt)
    add_event(lines, date(year, 5, 24),
        "Geburtstag Helga Piur 🎬",
        f"Helga Piur wurde am 24. Mai 1939 in Berlin geboren. Sie ist heute {year - 1939} Jahre alt. DDR-Schauspielerin\\, die durch ihre Rolle als Sprechstundenhilfe Victoria Happmeyer\\, genannt 'Häppchen'\\, in der Comedyserie 'Zahn um Zahn' (1985–1988\\, 21 Folgen) an der Seite von Alfred Struwe zur Publikumsliebsten wurde — 1986 und 1987 von den Zuschauern zum Fernsehliebling gewählt. In 678 Folgen der Hörspielserie 'Neumann\\, zweimal klingeln' (1967–1982) war sie als Brigitte Neumann zu hören. Als Synchronsprecherin lieh sie Brigitte Bardot ihre Stimme. Von 1999 bis 2019 spielte sie die Frau Holle in der MDR-Weihnachtssendung mit Frank Schöbel.")

    # Alfred Struwe (22.4.1927 – 12.2.1998)
    add_event(lines, date(year, 4, 22),
        "Geburtstag Alfred Struwe 🎬",
        f"Alfred Struwe wurde am 22. April 1927 in Marienburg (Westpreußen) geboren und starb 1998 mit 70 Jahren. Er wäre heute {year - 1927} Jahre alt. DDR-Schauspieler mit über 120 Film- und Fernsehproduktionen. Zum Publikumsliebling wurde er ab 1985 als kauziger Zahnarzt Dr. Alexander Wittkugel in der Comedyserie 'Zahn um Zahn' (1985–1988\\, 21 Folgen in drei Staffeln) — ursprünglich auf sieben Folgen geplant\\, wegen des Zuschauererfolgs deutlich verlängert. Mehrfach verkörperte er den Hitler-Attentäter Claus Schenk Graf von Stauffenberg. Als Synchronsprecher lieh er Philippe Noiret und Michel Serrault seine Stimme.")
    add_event(lines, date(year, 2, 12),
        "Todestag Alfred Struwe 🎬",
        "Alfred Struwe (1927–1998) starb am 12. Februar 1998 in Potsdam im Alter von 70 Jahren an einer Herzerkrankung. Er ist auf dem Südwestkirchhof Stahnsdorf begraben. DDR-weit unvergessen als Zahnarzt Dr. Wittkugel in 'Zahn um Zahn' (1985–1988) — einer der beliebtesten Comedyserien der DDR mit 21 Folgen. Seine Tochter Catharina Struwe ist ebenfalls Schauspielerin.")

    # Jürgen Zartmann (28.1.1941 – lebt)
    add_event(lines, date(year, 1, 28),
        "Geburtstag Jürgen Zartmann 🎬",
        f"Jürgen Zartmann wurde am 28. Januar 1941 in Darmstadt geboren und wuchs in Leipzig auf. Er ist heute {year - 1941} Jahre alt. DDR-Schauspieler und Synchronsprecher\\, der Ende der 1960er-Jahre beim Fernsehen der DDR entdeckt wurde. Bekannt durch die Krimiserie 'Polizeiruf 110' (1981–1991) als Oberleutnant Manfred Bergmann\\, die Abenteuerserie 'Archiv des Todes' (1980) und 'Front ohne Gnade' (1984). In der DDR-Lieblingsserie 'Zur See' (1977) spielte er den Bootsmann Reinhardt. Als Synchronsprecher lieh er Timothy Dalton und Jon Voight seine Stimme. Nach der Wende spielte er bis 2000 den Christoph von Anstetten in 'Verbotene Liebe'.")

    # Fred Delmare (24.4.1922 – 1.5.2009)
    add_event(lines, date(year, 4, 24),
        "Geburtstag Fred Delmare 🎬",
        f"Fred Delmare (bürgerlich Werner Vorndran) wurde am 24. April 1922 in Hüttensteinach (Thüringen) geboren und starb 2009 mit 87 Jahren. Er wäre heute {year - 1922} Jahre alt. Einer der beliebtesten DDR-Charakterdarsteller mit über 200 Film- und Fernsehproduktionen. Bekannt als Reifenhändler Saft in 'Die Legende von Paul und Paula' (1973)\\, als KZ-Häftling Rudi Pippig in 'Nackt unter Wölfen' (1963) und als Opa Friedrich Steinbach in 'In aller Freundschaft' (1999–2006\\, 240 Folgen). Träger des Vaterländischen Verdienstordens in Gold und des Kunstpreises der DDR.")
    add_event(lines, date(year, 5, 1),
        "Todestag Fred Delmare 🎬",
        "Fred Delmare (1922–2009) starb am 1. Mai 2009 in Leipzig — dem Tag der Arbeit — im Alter von 87 Jahren. Der Volksschauspieler der DDR wurde vor allem durch seine Nebenrollen geliebt: als Reifenhändler Saft in 'Die Legende von Paul und Paula' (1973)\\, in 'Nackt unter Wölfen' (1963) und zuletzt als Opa Friedrich Steinbach in 'In aller Freundschaft'. In fünf Jahrzehnten wirkte er in über 200 Produktionen mit.")

    # Günter Naumann (17.11.1925 – 6.11.2009)
    add_event(lines, date(year, 11, 17),
        "Geburtstag Günter Naumann 🎬",
        f"Günter Naumann wurde am 17. November 1925 in Chemnitz geboren und starb 2009 mit 83 Jahren. Er wäre heute {year - 1925} Jahre alt. DDR-Schauspieler und Charakterdarsteller\\, der am Berliner Ensemble begann und ab 1970 zum Fernsehen der DDR wechselte. Bekannt als Chief in der Kult-Serie 'Zur See' (1977) und als Kommissar Beck im 'Polizeiruf 110' (1988–1997). Spielte außerdem Robert Koch in 'Berühmte Ärzte der Charité' (1981) und wirkte in Frank Beyers Antikriegsfilm 'Fünf Patronenhülsen' (1960) mit. Nationalpreisträger der DDR 1982.")
    add_event(lines, date(year, 11, 6),
        "Todestag Günter Naumann 🎬",
        "Günter Naumann (1925–2009) starb am 6. November 2009 in Berlin-Köpenick im Alter von 83 Jahren an Nierenversagen. Der DDR-Charakterdarsteller war einer der meistbeschäftigten Schauspieler des Fernsehens der DDR. Als Kommissar Beck im 'Polizeiruf 110' ermittelte er von 1988 bis 1997 und verkörperte damit eine der bekanntesten Figuren der DDR-Krimireihe. Unvergessen auch als Chief in der Lieblingsserie 'Zur See' (1977).")

    # Hilmar Baumann (28.4.1931 – 7.7.2019)
    add_event(lines, date(year, 4, 28),
        "Geburtstag Hilmar Baumann 🎬",
        f"Hilmar Baumann wurde am 28. April 1931 in Berlin geboren und starb 2019 mit 88 Jahren. Er wäre heute {year - 1931} Jahre alt. DDR-Schauspieler\\, bekannt durch 'Die Abenteuer des Werner Holt' (1965) und zahlreiche DEFA-Produktionen.")
    add_event(lines, date(year, 7, 7),
        "Todestag Hilmar Baumann 🎬",
        "Hilmar Baumann\\, geboren 1931\\, verstarb am 7. Juli 2019. Er wurde 88 Jahre alt. DDR-Schauspieler und DEFA-Veteran.")

    # Willi Schwabe (25.2.1915 – 10.12.1992)
    add_event(lines, date(year, 2, 25),
        "Geburtstag Willi Schwabe 🎬",
        f"Willi Schwabe wurde am 25. Februar 1915 in Leipzig geboren und starb 1992 mit 77 Jahren. Er wäre heute {year - 1915} Jahre alt. Einer der beliebtesten Moderatoren und Schauspieler der DDR. Präsentierte jahrelang die Sendung 'Willi Schwabes Rumpelkammer' im DDR-Fernsehen. Volksschauspieler der DDR.")
    add_event(lines, date(year, 12, 10),
        "Todestag Willi Schwabe 🎬",
        "Willi Schwabe\\, geboren 1915\\, verstarb am 10. Dezember 1992. Er wurde 77 Jahre alt. Beliebter Moderator und Volksschauspieler der DDR.")

    # Günter Schubert (8.4.1938 – 2.1.2008)
    add_event(lines, date(year, 4, 8),
        "Geburtstag Günter Schubert 🎬",
        f"Günter Schubert wurde am 8. April 1938 in Weißwasser (Oberlausitz) geboren und starb 2008 mit 69 Jahren. Er wäre heute {year - 1938} Jahre alt. DDR-Schauspieler und Synchronsprecher\\, bekannt durch die Fernsehserie 'Zur See' (als Matrose Thomas Müller)\\, 'Treffpunkt Flughafen' und 'Bereitschaft Dr. Federau'. Ab 1970 Mitglied des DDR-Fernsehensembles.")
    add_event(lines, date(year, 1, 2),
        "Todestag Günter Schubert 🎬",
        "Günter Schubert\\, geboren 1938\\, verstarb am 2. Januar 2008 in Berlin. Er wurde 69 Jahre alt. DDR-Schauspieler\\, bekannt durch die Serie 'Zur See'.")

    # ══ TOP 30 DDR-SCHRIFTSTELLER ════════════════════════════════════════════

    # Johannes R. Becher (22.5.1891 – 11.10.1958)
    add_event(lines, date(year, 5, 22),
        "Geburtstag Johannes R. Becher ✍️",
        f"Johannes R. Becher wurde am 22. Mai 1891 in München geboren und starb 1958 mit 67 Jahren. Er wäre heute {year - 1891} Jahre alt. Schriftsteller\\, Kulturminister der DDR 1954–1958 und Verfasser des Textes der DDR-Nationalhymne 'Auferstanden aus Ruinen'. Expressionistischer Dichter und SED-Politiker.")
    add_event(lines, date(year, 10, 11),
        "Todestag Johannes R. Becher ✍️",
        "Johannes R. Becher\\, geboren 1891\\, verstarb am 11. Oktober 1958 in Ost-Berlin. Er wurde 67 Jahre alt. Kulturminister der DDR und Verfasser des Textes der Nationalhymne.")

    # Stefan Heym (10.4.1913 – 16.12.2001)
    add_event(lines, date(year, 4, 10),
        "Geburtstag Stefan Heym ✍️",
        f"Stefan Heym (eigentl. Helmut Flieg) wurde am 10. April 1913 in Chemnitz geboren und starb 2001 mit 88 Jahren. Er wäre heute {year - 1913} Jahre alt. Schriftsteller\\, emigrierte 1952 in die DDR. Bekannt für 'Fünf Tage im Juni'\\, 'Schwarzenberg'. Sprach 1989 auf der Alexanderplatz-Demonstration. 1994 Alterspräsident des Bundestags.")
    add_event(lines, date(year, 12, 16),
        "Todestag Stefan Heym ✍️",
        "Stefan Heym\\, geboren 1913\\, verstarb am 16. Dezember 2001 in En Bokek\\, Israel. Er wurde 88 Jahre alt. Bedeutendster DDR-Schriftsteller und Alterspräsident des Bundestags 1994.")

    # Heiner Müller (9.1.1929 – 30.12.1995)
    add_event(lines, date(year, 1, 9),
        "Geburtstag Heiner Müller ✍️",
        f"Heiner Müller wurde am 9. Januar 1929 in Eppendorf (Sachsen) geboren und starb 1995 mit 66 Jahren. Er wäre heute {year - 1929} Jahre alt. Bedeutendster DDR-Dramatiker\\, Nachfolger Brechts. Intendant des Berliner Ensembles. Bekannt für 'Die Hamletmaschine'\\, 'Der Lohndrücker'. Sprach 1989 auf der Alexanderplatz-Demonstration.")
    add_event(lines, date(year, 12, 30),
        "Todestag Heiner Müller ✍️",
        "Heiner Müller\\, geboren 1929\\, verstarb am 30. Dezember 1995 in Berlin. Er wurde 66 Jahre alt. Bedeutendster DDR-Dramatiker und Intendant des Berliner Ensembles.")

    # Wolf Biermann (15.11.1936)
    add_event(lines, date(year, 11, 15),
        "Geburtstag Wolf Biermann ✍️",
        f"Wolf Biermann wurde am 15. November 1936 in Hamburg geboren. Er ist heute {year - 1936} Jahre alt. Liedermacher und Lyriker\\, zog 1953 in die DDR. Sein Auftrittsverbot ab 1965 und die Ausbürgerung 1976 nach einem Konzert in Köln löste eine Protestwelle der DDR-Kulturschaffenden aus. Bekannt für 'Die Drahtharfe'\\, 'Ermutigung'.")

    # Jurek Becker (30.9.1937 – 14.3.1997)
    add_event(lines, date(year, 9, 30),
        "Geburtstag Jurek Becker ✍️",
        f"Jurek Becker wurde am 30. September 1937 in Łódź (Polen) geboren und starb 1997 mit 59 Jahren. Er wäre heute {year - 1937} Jahre alt. Schriftsteller und Drehbuchautor\\, KZ-Überlebender. Bekannt durch 'Jakob der Lügner' (1969\\, verfilmt 1974 – einziger DEFA-Film mit Oscar-Nominierung). Unterzeichnete die Biermann-Petition 1976.")
    add_event(lines, date(year, 3, 14),
        "Todestag Jurek Becker ✍️",
        "Jurek Becker\\, geboren 1937\\, verstarb am 14. März 1997 in Sieseby (Schleswig-Holstein). Er wurde 59 Jahre alt. Schriftsteller und Autor von 'Jakob der Lügner'.")

    # Franz Fühmann (15.1.1922 – 8.7.1984)
    add_event(lines, date(year, 1, 15),
        "Geburtstag Franz Fühmann ✍️",
        f"Franz Fühmann wurde am 15. Januar 1922 in Rochlitz an der Iser (Tschechoslowakei) geboren und starb 1984 mit 62 Jahren. Er wäre heute {year - 1922} Jahre alt. Bedeutender DDR-Schriftsteller\\, Erzähler und Kinderbuchautor. Geschwister-Scholl-Preis 1982. Wurde zunehmend kritisch gegenüber der DDR.")
    add_event(lines, date(year, 7, 8),
        "Todestag Franz Fühmann ✍️",
        "Franz Fühmann\\, geboren 1922\\, verstarb am 8. Juli 1984 in Ost-Berlin. Er wurde 62 Jahre alt. Bedeutender DDR-Schriftsteller und Kinderbuchautor.")

    # Günter de Bruyn (1.11.1926 – 4.10.2020)
    add_event(lines, date(year, 11, 1),
        "Geburtstag Günter de Bruyn ✍️",
        f"Günter de Bruyn wurde am 1. November 1926 in Berlin geboren und starb 2020 mit 93 Jahren. Er wäre heute {year - 1926} Jahre alt. DDR-Schriftsteller und Essayist\\, bekannt durch 'Buridans Esel' (1968) und 'Märkische Forschungen' (1978). Einer der wichtigsten Prosaautoren der DDR.")
    add_event(lines, date(year, 10, 4),
        "Todestag Günter de Bruyn ✍️",
        "Günter de Bruyn\\, geboren 1926\\, verstarb am 4. Oktober 2020. Er wurde 93 Jahre alt. DDR-Schriftsteller und Essayist.")

    # Günter Kunert (6.3.1929 – 21.9.2019)
    add_event(lines, date(year, 3, 6),
        "Geburtstag Günter Kunert ✍️",
        f"Günter Kunert wurde am 6. März 1929 in Berlin geboren und starb 2019 mit 90 Jahren. Er wäre heute {year - 1929} Jahre alt. Lyriker und Schriftsteller der DDR\\, bedeutendster DDR-Lyriker neben Brecht. Unterzeichnete die Biermann-Petition 1976\\, übersiedelte 1979 in die BRD.")
    add_event(lines, date(year, 9, 21),
        "Todestag Günter Kunert ✍️",
        "Günter Kunert\\, geboren 1929\\, verstarb am 21. September 2019 in Kaisborstel (Holstein). Er wurde 90 Jahre alt. Bedeutendster DDR-Lyriker neben Brecht.")

    # Volker Braun (7.5.1939)
    add_event(lines, date(year, 5, 7),
        "Geburtstag Volker Braun ✍️",
        f"Volker Braun wurde am 7. Mai 1939 in Dresden geboren. Er ist heute {year - 1939} Jahre alt. Schriftsteller und Dramatiker der DDR\\, bekannt für sein Stück 'Die Kipper' und den Roman 'Unvollendete Geschichte' (1975). Blieb nach der Wende in Deutschland und erhielt 2000 den Georg-Büchner-Preis.")

    # Bruno Apitz (28.4.1900 – 7.4.1979)
    add_event(lines, date(year, 4, 28),
        "Geburtstag Bruno Apitz ✍️",
        f"Bruno Apitz wurde am 28. April 1900 in Leipzig geboren und starb 1979 mit 78 Jahren. Er wäre heute {year - 1900} Jahre alt. DDR-Schriftsteller\\, KZ-Überlebender. Bekannt durch den Roman 'Nackt unter Wölfen' (1958) über das KZ Buchenwald – meistverkauftes Buch der DDR.")
    add_event(lines, date(year, 4, 7),
        "Todestag Bruno Apitz ✍️",
        "Bruno Apitz\\, geboren 1900\\, verstarb am 7. April 1979 in Ost-Berlin. Er wurde 78 Jahre alt. Autor von 'Nackt unter Wölfen'\\, dem meistverkauften Buch der DDR.")

    # Willi Bredel (2.5.1901 – 27.10.1964)
    add_event(lines, date(year, 5, 2),
        "Geburtstag Willi Bredel ✍️",
        f"Willi Bredel wurde am 2. Mai 1901 in Hamburg geboren und starb 1964 mit 63 Jahren. Er wäre heute {year - 1901} Jahre alt. Arbeiterschriftsteller und KPD-Mitglied\\, KZ-Überlebender (Fuhlsbüttel). Bekannt durch 'Maschinenfabrik N&K' (1930) und seine autobiografischen KZ-Berichte. Gründungsmitglied des Deutschen Schriftstellerverbandes der DDR.")
    add_event(lines, date(year, 10, 27),
        "Todestag Willi Bredel ✍️",
        "Willi Bredel\\, geboren 1901\\, verstarb am 27. Oktober 1964 in Ost-Berlin. Er wurde 63 Jahre alt. Arbeiterschriftsteller und KPD-Mitglied.")

    # Johannes Bobrowski (9.4.1917 – 2.9.1965)
    add_event(lines, date(year, 4, 9),
        "Geburtstag Johannes Bobrowski ✍️",
        f"Johannes Bobrowski wurde am 9. April 1917 in Tilsit (Ostpreußen) geboren und starb 1965 mit 48 Jahren. Er wäre heute {year - 1917} Jahre alt. Bedeutender DDR-Lyriker\\, bekannt für seine Gedichte über die Landschaft des Memelgebiets. Werke: 'Sarmatische Zeit'\\, 'Schattenland Ströme'. Erhielt 1962 den Preis der Gruppe 47.")
    add_event(lines, date(year, 9, 2),
        "Todestag Johannes Bobrowski ✍️",
        "Johannes Bobrowski\\, geboren 1917\\, verstarb am 2. September 1965 in Ost-Berlin. Er wurde nur 48 Jahre alt. Bedeutender DDR-Lyriker.")

    # Stephan Hermlin (13.4.1915 – 6.4.1997)
    add_event(lines, date(year, 4, 13),
        "Geburtstag Stephan Hermlin ✍️",
        f"Stephan Hermlin wurde am 13. April 1915 in Chemnitz geboren und starb 1997 mit 81 Jahren. Er wäre heute {year - 1915} Jahre alt. Schriftsteller und Lyriker der DDR\\, Vizepräsident der Akademie der Künste. Unterzeichnete die Biermann-Petition 1976. Organisierte 1981 einen bedeutenden Berliner Schriftstellerkongress gegen Atomkraft.")
    add_event(lines, date(year, 4, 6),
        "Todestag Stephan Hermlin ✍️",
        "Stephan Hermlin\\, geboren 1915\\, verstarb am 6. April 1997 in Berlin. Er wurde 81 Jahre alt. Schriftsteller\\, Lyriker und Vizepräsident der Akademie der Künste der DDR.")

    # Erwin Strittmatter (14.8.1912 – 31.1.1994)
    add_event(lines, date(year, 8, 14),
        "Geburtstag Erwin Strittmatter ✍️",
        f"Erwin Strittmatter wurde am 14. August 1912 in Spremberg (Niederlausitz) geboren und starb 1994 mit 81 Jahren. Er wäre heute {year - 1912} Jahre alt. Bedeutendster volksnaher Schriftsteller der DDR\\, sorbischer Herkunft. Bekannt durch 'Tinko' (1954)\\, 'Ole Bienkopp' (1963)\\, 'Der Wundertäter'. Vorsitzender des Schriftstellerverbandes.")
    add_event(lines, date(year, 1, 31),
        "Todestag Erwin Strittmatter ✍️",
        "Erwin Strittmatter\\, geboren 1912\\, verstarb am 31. Januar 1994 in Schulzenhof (Brandenburg). Er wurde 81 Jahre alt. Bedeutendster volksnaher Schriftsteller der DDR.")

    # Irmtraud Morgner (22.8.1933 – 6.5.1990)
    add_event(lines, date(year, 8, 22),
        "Geburtstag Irmtraud Morgner ✍️",
        f"Irmtraud Morgner wurde am 22. August 1933 in Chemnitz geboren und starb 1990 mit 56 Jahren. Sie wäre heute {year - 1933} Jahre alt. DDR-Schriftstellerin und Feministin\\, bekannt durch den Roman 'Leben und Abenteuer der Trobadora Beatriz' (1974) – das wichtigste feministische Buch der DDR.")
    add_event(lines, date(year, 5, 6),
        "Todestag Irmtraud Morgner ✍️",
        "Irmtraud Morgner\\, geboren 1933\\, verstarb am 6. Mai 1990 in Berlin. Sie wurde 56 Jahre alt. Bedeutendste feministische Schriftstellerin der DDR.")

    # Uwe Johnson (20.7.1934 – 23.2.1984)
    add_event(lines, date(year, 7, 20),
        "Geburtstag Uwe Johnson ✍️",
        f"Uwe Johnson wurde am 20. Juli 1934 in Cammin (Pommern) geboren und starb 1984 mit 49 Jahren. Er wäre heute {year - 1934} Jahre alt. Schriftsteller\\, zunächst in der DDR\\, dann in der BRD. Bekannt durch 'Mutmaßungen über Jakob' (1959) und die 'Jahrestage' (1970–1983). Georg-Büchner-Preis 1971.")
    add_event(lines, date(year, 2, 23),
        "Todestag Uwe Johnson ✍️",
        "Uwe Johnson\\, geboren 1934\\, verstarb am 23. Februar 1984 in Sheerness-on-Sea (England). Er wurde 49 Jahre alt. DDR-Schriftsteller\\, Autor der 'Jahrestage'.")

    # Christoph Hein (8.4.1944)
    add_event(lines, date(year, 4, 8),
        "Geburtstag Christoph Hein ✍️",
        f"Christoph Hein wurde am 8. April 1944 in Heinzendorf (Schlesien) geboren. Er ist heute {year - 1944} Jahre alt. Schriftsteller und Dramatiker der DDR\\, bekannt durch 'Der fremde Freund' (1982) und 'Drachenblut'. Sprach 1989 auf der Alexanderplatz-Demonstration. Einer der wenigen DDR-Autoren\\, die Glasnost offen unterstützten.")

    # Peter Hacks (21.3.1928 – 28.8.2003)
    add_event(lines, date(year, 3, 21),
        "Geburtstag Peter Hacks ✍️",
        f"Peter Hacks wurde am 21. März 1928 in Breslau geboren und starb 2003 mit 75 Jahren. Er wäre heute {year - 1928} Jahre alt. Dramatiker und Schriftsteller der DDR\\, bekannt für seine Dramen und Kinderbücher. Einer der wichtigsten Dramatiker nach Brecht. Nationalpreisträger.")
    add_event(lines, date(year, 8, 28),
        "Todestag Peter Hacks ✍️",
        "Peter Hacks\\, geboren 1928\\, verstarb am 28. August 2003 in Groß Machnow (Brandenburg). Er wurde 75 Jahre alt. Bedeutender DDR-Dramatiker und Kinderbuchautor.")

    # Ulrich Plenzdorf (26.10.1934 – 9.8.2007)
    add_event(lines, date(year, 10, 26),
        "Geburtstag Ulrich Plenzdorf ✍️",
        f"Ulrich Plenzdorf wurde am 26. Oktober 1934 in Berlin geboren und starb 2007 mit 72 Jahren. Er wäre heute {year - 1934} Jahre alt. Schriftsteller und Drehbuchautor der DDR\\, bekannt durch 'Die neuen Leiden des jungen W.' (1972) – das meistdiskutierte DDR-Buch der 1970er Jahre. Schrieb zahlreiche DEFA-Drehbücher.")
    add_event(lines, date(year, 8, 9),
        "Todestag Ulrich Plenzdorf ✍️",
        "Ulrich Plenzdorf\\, geboren 1934\\, verstarb am 9. August 2007 in Berlin. Er wurde 72 Jahre alt. DDR-Schriftsteller und Drehbuchautor\\, bekannt durch 'Die neuen Leiden des jungen W.'")

    # Sarah Kirsch (16.4.1935 – 5.5.2013)
    add_event(lines, date(year, 4, 16),
        "Geburtstag Sarah Kirsch ✍️",
        f"Sarah Kirsch wurde am 16. April 1935 in Limlingerode (Harz) geboren und starb 2013 mit 78 Jahren. Sie wäre heute {year - 1935} Jahre alt. Bedeutendste DDR-Lyrikerin\\, bekannt für ihre Naturgedichte. Unterzeichnete die Biermann-Petition 1976\\, siedelte 1977 in die BRD über. Büchner-Preis 1996.")
    add_event(lines, date(year, 5, 5),
        "Todestag Sarah Kirsch ✍️",
        "Sarah Kirsch\\, geboren 1935\\, verstarb am 5. Mai 2013 in Heide (Schleswig-Holstein). Sie wurde 78 Jahre alt. Bedeutendste DDR-Lyrikerin.")

    # Thomas Brasch (19.2.1945 – 3.11.2001)
    add_event(lines, date(year, 2, 19),
        "Geburtstag Thomas Brasch ✍️",
        f"Thomas Brasch wurde am 19. Februar 1945 in Westow (Yorkshire) geboren und starb 2001 mit 56 Jahren. Er wäre heute {year - 1945} Jahre alt. Schriftsteller\\, Lyriker und Dramatiker\\, Sohn eines DDR-Kulturoffiziers. Bekannt für seine Gedichte und das Stück 'Vor den Vätern sterben die Söhne' (1977). Siedelte 1976 aus der DDR aus.")
    add_event(lines, date(year, 11, 3),
        "Todestag Thomas Brasch ✍️",
        "Thomas Brasch\\, geboren 1945\\, verstarb am 3. November 2001 in Berlin. Er wurde 56 Jahre alt. DDR-Schriftsteller und Dramatiker.")

    # Reiner Kunze (16.8.1933)
    add_event(lines, date(year, 8, 16),
        "Geburtstag Reiner Kunze ✍️",
        f"Reiner Kunze wurde am 16. August 1933 in Oelsnitz (Erzgebirge) geboren. Er ist heute {year - 1933} Jahre alt. DDR-Lyriker und Schriftsteller\\, bekannt durch 'Die wunderbaren Jahre' (1976) – ein Buch über DDR-Jugendliche\\, das in der DDR verboten war. Siedelte 1977 in die BRD über. Büchner-Preis 1977.")

    # Jurij Brězan (9.6.1916 – 12.3.2006)
    add_event(lines, date(year, 6, 9),
        "Geburtstag Jurij Brězan ✍️",
        f"Jurij Brězan wurde am 9. Juni 1916 in Räckelwitz (Lausitz) geboren und starb 2006 mit 89 Jahren. Er wäre heute {year - 1916} Jahre alt. Sorbischer Schriftsteller\\, bedeutendster Autor in sorbischer und deutscher Sprache. Bekannt durch seinen 'Krabat'-Roman. Nationalpreisträger der DDR.")
    add_event(lines, date(year, 3, 12),
        "Todestag Jurij Brězan ✍️",
        "Jurij Brězan\\, geboren 1916\\, verstarb am 12. März 2006 in Bautzen. Er wurde 89 Jahre alt. Bedeutendster sorbischer Schriftsteller\\, Autor des Krabat-Romans.")

    # Dieter Noll (31.12.1927 – 6.2.2008)
    add_event(lines, date(year, 12, 31),
        "Geburtstag Dieter Noll ✍️",
        f"Dieter Noll wurde am 31. Dezember 1927 in Riesa (Sachsen) geboren. Er wäre heute {year - 1927} Jahre alt. Der DDR-Schriftsteller ist vor allem bekannt durch seinen zweibändigen Roman 'Die Abenteuer des Werner Holt' (Band 1: 1960\\, Band 2: 1963): Band 1 schildert die Entwicklung des Abiturienten Werner Holt vom Flakhelfer zum Kriegsgefangenen und seine wachsenden Zweifel am Nationalsozialismus\\, Band 2 zeigt seinen schwierigen Weg zum Sozialismus. Das Werk war Pflichtlektüre in DDR-Schulen und wurde über zwei Millionen Mal verkauft. 1964 verfilmte Joachim Kunert den ersten Band. Noll erhielt zweimal den Nationalpreis der DDR.")
    add_event(lines, date(year, 2, 6),
        "Todestag Dieter Noll ✍️",
        "Dieter Noll (1927–2008) starb am 6. Februar 2008 in Zeuthen bei Berlin im Alter von 80 Jahren. Sein Hauptwerk 'Die Abenteuer des Werner Holt' (1960/63) gilt als bedeutendster Antikriegsroman der DDR-Literatur: Der erste Band zeigt\\, wie der junge Werner Holt als Soldat im Zweiten Weltkrieg zunehmend an Hitlers Krieg zweifelt\\, der zweite Band begleitet ihn auf dem Weg zum überzeugten Sozialisten. Mehr als zwei Millionen Exemplare wurden verkauft.")

    # ── TOP 30 DDR-MUSIKER ────────────────────────────────────────────────────

    # Frank Schöbel (11.12.1942 – lebt)
    add_event(lines, date(year, 12, 11),
        "Geburtstag Frank Schöbel 🎵",
        f"Frank Schöbel wurde am 11. Dezember 1942 in Leipzig geboren. Er ist heute {year - 1942} Jahre alt. Der erfolgreichste Schlagersänger der DDR — Träger des Amiga-Platin-Awards für die meisten verkauften Platten im DDR-Label Amiga. Mit 'Wie ein Stern' (1971) hatte er einen gesamtdeutschen Hit\\, 1985 nahm er mit Aurora Lacasa das meistverkaufte Album der DDR-Geschichte auf: 'Weihnachten in Familie' (über 2 Millionen Exemplare bis 2019). In 'Heißer Sommer' (1968) spielte er die Hauptrolle. Zehnfacher Fernsehliebling.")

    # Chris Doerk (24.2.1942 – lebt)
    add_event(lines, date(year, 2, 24),
        "Geburtstag Chris Doerk 🎵",
        f"Chris Doerk wurde am 24. Februar 1942 in Königsberg (Ostpreußen) geboren. Sie ist heute {year - 1942} Jahre alt. Schlagersängerin und Schauspielerin der DDR\\, bekannt als Duett-Partnerin und Ehefrau (1966–1974) von Frank Schöbel. Gemeinsam gewannen sie zweimal den DDR-Schlagerwettbewerb. Spielte die weibliche Hauptrolle in 'Heißer Sommer' (1968). War die erste DDR-Künstlerin\\, die in den Niederlanden im Fernsehen auftreten durfte.")

    # Nina Hagen (11.3.1955 – lebt)
    add_event(lines, date(year, 3, 11),
        "Geburtstag Nina Hagen 🎸",
        f"Nina Hagen (bürgerlich Catharina Hagen) wurde am 11. März 1955 in Ost-Berlin geboren. Sie ist heute {year - 1955} Jahre alt. Als Teenager in der DDR sang sie mit der Band Automobil und wurde mit 'Du hast den Farbfilm vergessen' (1974) bekannt — ein subversiver Seitenhieb auf den grauen DDR-Alltag. 1976 verließ sie mit ihrer Mutter Eva-Maria Hagen nach der Ausbürgerung ihres Stiefvaters Wolf Biermann die DDR. In London und den USA wurde sie zur 'Godmother of Punk'.")

    # Veronika Fischer (28.7.1951 – lebt)
    add_event(lines, date(year, 7, 28),
        "Geburtstag Veronika Fischer 🎵",
        f"Veronika Fischer wurde am 28. Juli 1951 in Wölfis (Thüringen) geboren. Sie ist heute {year - 1951} Jahre alt. Eine der bekanntesten Rocksängerinnen der DDR\\, die in den 1970er Jahren mit der Stern-Combo Meißen und später mit eigener Band auftrat. 1975 verließ sie Panta Rhei\\, deren Kern anschließend die Band Karat gründete. Kunstpreisträger der DDR. Siedelte 1980 in die Bundesrepublik über.")

    # Tamara Danz (14.12.1952 – 22.7.1996)
    add_event(lines, date(year, 12, 14),
        "Geburtstag Tamara Danz 🎸",
        f"Tamara Danz wurde am 14. Dezember 1952 in Winne bei Breitungen (Thüringen) geboren und starb 1996 mit 43 Jahren. Sie wäre heute {year - 1952} Jahre alt. Frontfrau und Texterin der DDR-Rockband Silly — eine der charismatischsten Rocksängerinnen der DDR überhaupt. Mit 'Mont Klamott' (1983)\\, 'Bataillon d'Amour' (1985) und 'Verlorene Kinder' engagierte sich Silly auch politisch. Von den DDR-Behörden als politisch unzuverlässig eingestuft. Starb während der Produktion ihres letzten Albums 'Paradies' an Brustkrebs.")
    add_event(lines, date(year, 7, 22),
        "Todestag Tamara Danz 🎸",
        "Tamara Danz (1952–1996) starb am 22. Juli 1996 in Berlin im Alter von 43 Jahren an Brustkrebs. Die Frontfrau der Band Silly gilt als eine der größten Rocksängerinnen der DDR. Ihr letztes Album 'Paradies' erschien kurz vor ihrem Tod. Ihre Nachfolgerin bei Silly wurde 2006 die Schauspielerin Anna Loos.")

    # Herbert Dreilich / Karat (5.12.1942 – 12.12.2004)
    add_event(lines, date(year, 12, 5),
        "Geburtstag Herbert Dreilich 🎸",
        f"Herbert Dreilich wurde am 5. Dezember 1942 in Mauterndorf (Österreich) geboren und starb 2004 mit 62 Jahren. Er wäre heute {year - 1942} Jahre alt. Als Sänger und Gründungsmitglied der DDR-Rockband Karat (gegründet 1975) wurde er mit 'Über sieben Brücken musst du geh'n' berühmt — ein deutsch-deutscher Hit\\, den Peter Maffay im Westen coverte. 1982 trat Karat als einzige DDR-Band bei 'Wetten\\, dass..?' auf. Nationalpreisträger der DDR. Sein Sohn Claudius Dreilich ist seit 2005 Karat-Sänger.")
    add_event(lines, date(year, 12, 12),
        "Todestag Herbert Dreilich 🎸",
        "Herbert Dreilich (1942–2004) starb am 12. Dezember 2004 in Berlin an Leberkrebs im Alter von 62 Jahren. Der Karat-Sänger war das Gesicht einer der erfolgreichsten DDR-Rockbands\\, die auch in der Bundesrepublik Goldene Schallplatten erhielten. 'Über sieben Brücken musst du geh'n' gilt bis heute als Hymne der Wendezeit.")

    # Puhdys – Gründungstag 19.11.1969
    add_event(lines, date(year, 11, 19),
        "Gründungstag der Puhdys 🎸",
        f"Am 19. November 1969 gaben die Puhdys ihr erstes Konzert im Tivoli in Freiberg (Sachsen) — dieser Tag gilt als ihr offizieller Gründungstag. Die Berliner Rockband ist die erfolgreichste der DDR: bis zur Wende wurden weltweit fast 20 Millionen Alben verkauft\\, darunter die Filmmusik zu 'Die Legende von Paul und Paula' (1973) mit dem Hit 'Geh zu ihr'. Weitere Klassiker: 'Alt wie ein Baum'\\, 'Wenn ein Mensch lebt'. Sie durften als eine der wenigen DDR-Bands auch in der BRD auftreten. 2016 lösten sie sich auf.")

    # Dieter "Maschine" Birr (18.3.1944 – lebt)
    add_event(lines, date(year, 3, 18),
        "Geburtstag Dieter 'Maschine' Birr 🎸",
        f"Dieter 'Maschine' Birr wurde am 18. März 1944 in Köslin (Pommern) geboren. Er ist heute {year - 1944} Jahre alt. Sänger\\, Gitarrist und Kopf der Puhdys — der erfolgreichsten Rockband der DDR. Von 1969 bis zur Auflösung 2016 prägte er die Band mit über 250 selbst komponierten Titeln und mehr als 4.000 Konzerten. Sein Spitzname 'Maschine' wurde von Mitgründer Peter Meyer geprägt.")

    # Karat – Gründungstag 1975 (Bandjubiläum, kein exaktes Datum – nehmen den 1. Konzert-Nachweis)
    # Statt Banddatum nehmen wir den Geburtstag des zweiten Karat-Sängers Claudius Dreilich
    # Besser: City-Gründung 1972 und Hit "Am Fenster" 1977
    # City – Gründung 1972, Hit "Am Fenster" 1977
    add_event(lines, date(year, 6, 6),
        "Geburtstag Toni Krahl (City) 🎸",
        f"Toni Krahl wurde am 6. Juni 1948 in Ost-Berlin geboren. Er ist heute {year - 1948} Jahre alt. Sänger und Frontmann der Ost-Berliner Rockband City\\, die 1972 gegründet wurde. Mit 'Am Fenster' (1977) — einem der bekanntesten DDR-Rocksongs überhaupt — erreichte City schlagartig Bekanntheit in beiden deutschen Staaten. Der Song wurde zum Sinnbild einer ganzen Generation.")

    # Silly – Gründung 1978, vertreten durch Tamara Danz (bereits oben)

    # Reinhard Lakomy (19.1.1946 – 23.3.2013)
    add_event(lines, date(year, 1, 19),
        "Geburtstag Reinhard Lakomy 🎵",
        f"Reinhard Lakomy wurde am 19. Januar 1946 in Magdeburg geboren und starb 2013 mit 67 Jahren. Er wäre heute {year - 1946} Jahre alt. Komponist\\, Pianist\\, Sänger und Liedermacher der DDR mit einer einzigartigen Bandbreite von Jazz über Schlager und elektronische Musik bis hin zu Kinder-Hörspielen. Berühmt durch das Kinder-Hörspielmusical 'Der Traumzauberbaum' (mit Ehefrau Monika Ehrhardt). Gehörte neben den Puhdys zu den meistveröffentlichten DDR-Künstlern. 1976 protestierte er gegen die Ausbürgerung Wolf Biermanns.")
    add_event(lines, date(year, 3, 23),
        "Todestag Reinhard Lakomy 🎵",
        "Reinhard Lakomy (1946–2013) starb am 23. März 2013 in Berlin im Alter von 67 Jahren an Lungenkrebs — eine Behandlung lehnte er ab. Der vielseitige Musiker hinterließ ein riesiges Werk: von Schlagerhits wie 'Es war doch nicht das erste Mal' (1972) über elektronische Musik bis zum weltbekannten Kindermärchen 'Der Traumzauberbaum'. Er ist auf dem Friedhof Blankenburg in Berlin begraben.")

    # Ute Freudenberg (8.11.1956 – lebt)
    add_event(lines, date(year, 11, 8),
        "Geburtstag Ute Freudenberg 🎵",
        f"Ute Freudenberg wurde am 8. November 1956 in Weimar geboren. Sie ist heute {year - 1956} Jahre alt. Eine der beliebtesten Sängerinnen der DDR\\, die mit der Band Lift und später als Solistin bekannt wurde. Mit 'Jugendliebe' (1982) gelang ihr ein DDR-Megahit. Siedelte 1986 nach West-Berlin über. Nach der Wende setzte sie ihre Karriere gesamtdeutsch fort.")

    # Dagmar Frederic (15.4.1945 – lebt)
    add_event(lines, date(year, 4, 15),
        "Geburtstag Dagmar Frederic 🎵",
        f"Dagmar Frederic (bürgerlich Dagmar Elke Schulz) wurde am 15. April 1945 in Eberswalde geboren. Sie ist heute {year - 1945} Jahre alt. Sängerin\\, Tänzerin und Moderatorin — eine der populärsten Entertainerinnen der DDR. Durch Showmaster Heinz Quermann 1966 entdeckt\\, wurde sie mit Sendungen wie 'Ein Kessel Buntes' und 'Serenade bei Kerzenschein' zum TV-Star. Nationalpreisträger der DDR. Tritt auch mit 80 Jahren noch regelmäßig auf.")

    # Gunther Emmerlich (22.5.1944 – lebt)
    add_event(lines, date(year, 5, 22),
        "Geburtstag Gunther Emmerlich 🎵",
        f"Gunther Emmerlich wurde am 22. Mai 1944 in Zittau geboren. Er ist heute {year - 1944} Jahre alt. Bariton und Entertainer — eine der unverwechselbarsten Stimmen der DDR. Als Solist der Staatsoper Dresden und des Rundfunks der DDR verband er klassischen Gesang mit Unterhaltung. Durch zahlreiche TV-Auftritte\\, seine Zusammenarbeit mit Herbert Roth ('Bergvagabunden') und seine Kabarettnummern wurde er zum Publikumsliebling. Nach der Wende blieb er im Fernsehen präsent.")

    # Bettina Wegner (4.11.1947 – lebt)
    add_event(lines, date(year, 11, 4),
        "Geburtstag Bettina Wegner 🎵",
        f"Bettina Wegner wurde am 4. November 1947 in Berlin-Charlottenburg geboren. Sie ist heute {year - 1947} Jahre alt. Liedermacherin und wichtigste weibliche Stimme der DDR-Opposition. Ihr Lied 'Kinder' (1978) — 'Sind so kleine Hände...' — wurde zum Friedenslied und in der gesamten DDR heimlich verbreitet. Wegen ihrer systemkritischen Texte mehrfach mit Auftrittsverboten belegt. Siedelte 1983 in die Bundesrepublik über.")

    # Gundermann – bereits eingetragen (21.2.1955 – 21.6.1998)

    # Stephan Krawczyk (23.6.1955 – lebt)
    add_event(lines, date(year, 6, 23),
        "Geburtstag Stephan Krawczyk 🎵",
        f"Stephan Krawczyk wurde am 23. Juni 1955 in Weida (Thüringen) geboren. Er ist heute {year - 1955} Jahre alt. Liedermacher\\, Gitarrist und DDR-Oppositioneller. Durch systemkritische Texte mit Auftrittsverbot belegt\\, wurde er zum Symbol des Widerstands. Im Januar 1988 wurde er mit seiner Lebensgefährtin Freya Klier verhaftet und zur Ausreise gezwungen — ein Wendepunkt in der DDR-Oppositionsgeschichte. Nach der Wende weiter als Musiker und Autor tätig.")

    # Klaus Renft (19.7.1942 – 9.10.2006)
    add_event(lines, date(year, 7, 19),
        "Geburtstag Klaus Renft 🎸",
        f"Klaus Renft wurde am 19. Juli 1942 in Leipzig geboren und starb 2006 mit 64 Jahren. Er wäre heute {year - 1942} Jahre alt. Gründer der Klaus-Renft-Combo\\, einer der einflussreichsten DDR-Rockbands. 1958 erstmals gegründet\\, 1967 wieder zugelassen\\, wurde die Band 1975 endgültig verboten — wegen eines Liedes über eine missglückte DDR-Flucht und kritischer Texte über Bausoldaten. Einige Mitglieder wurden ausgebürgert. 1990 kurze Reunion\\, 2006 starb Renft in Leipzig.")
    add_event(lines, date(year, 10, 9),
        "Todestag Klaus Renft 🎸",
        "Klaus Renft (1942–2006) starb am 9. Oktober 2006 in Leipzig im Alter von 64 Jahren. Der Gründer der Klaus-Renft-Combo — eine der wichtigsten DDR-Rockbands — erlebte das Bandverbot 1975\\, die Ausbürgerung von Bandmitgliedern und nach der Wende noch eine kurze Reunion. Sein Geburtstag am 9. Oktober fällt auf den Jahrestag der Friedlichen Revolution in Leipzig.")

    # Karat – Gründung 1975 (kein exaktes Datum) → über Jubiläumskonzert
    # Stattdessen: City – Toni Krahl bereits oben. Ergänze noch einige weitere.

    # Karussell — gegründet 1975 aus Ex-Renft-Mitgliedern
    add_event(lines, date(year, 4, 15),
        "Geburtstag André Herzberg (Pankow) 🎸",
        f"André Herzberg wurde am 15. April 1957 in Ost-Berlin geboren. Er ist heute {year - 1957} Jahre alt. Sänger und Kopf der DDR-Rockband Pankow\\, die 1981 aus der ehemaligen Begleitband von Veronika Fischer hervorging. Mit der Rockoper 'Paule Panke' (1981) wurden sie sofort bekannt und galten als eine der wichtigsten kritischen Bands der DDR. Ihr Song 'Er will anders sein' (1986) wurde zur Hymne der jungen DDR-Generation. Pankow stand ständig unter Beobachtung der Stasi.")

    # Karussell-Sänger Jürgen Kerth
    # Nehmen stattdessen: Schlagersänger Fred Frohberg
    add_event(lines, date(year, 6, 3),
        "Geburtstag Fred Frohberg 🎵",
        f"Fred Frohberg wurde am 3. Juni 1927 in Leipzig geboren und lebte bis 2001. Er wäre heute {year - 1927} Jahre alt. Einer der beliebtesten Schlagersänger der frühen DDR\\, der mit samtweicher Tenorstimme zahlreiche Hits einsang. Seine Aufnahmen beim Label Amiga gehören zu den meistgespielten der DDR-Schlagergeschichte.")

    # Ute Freudenberg bereits oben. Ergänze: Monika Herz / Angelika Mann
    add_event(lines, date(year, 8, 7),
        "Geburtstag Angelika Mann 🎵",
        f"Angelika Mann wurde am 7. August 1952 in Karl-Marx-Stadt (heute Chemnitz) geboren. Sie ist heute {year - 1952} Jahre alt. Sängerin und langjährige Duett-Partnerin von Reinhard Lakomy. Gemeinsam produzierten sie zahlreiche Schlager und Lieder. Stellte 1984 einen Ausreiseantrag\\, der ihr berufliches Aus in der DDR bedeutete — ein typisches Schicksal kritischer Künstlerinnen.")

lines.append("END:VCALENDAR")

# ── ICS schreiben ─────────────────────────────────────────────────────────────
with open("ddr-feiertage.ics", "w", encoding="utf-8") as f:
    f.write("\r\n".join(lines) + "\r\n")

count = len([l for l in lines if l == "BEGIN:VEVENT"])
print(f"✓ ddr-feiertage.ics  — {count} Einträge")

# ── JSON für App generieren ───────────────────────────────────────────────────
import json

def categorize(title):
    t = title.lower()
    if any(x in t for x in ["geburtstag","todestag","ermordung rosa","ermordung karl","ermordung ernst"]):
        return "person"
    if any(x in t for x in ["tag der republik","tag der nva","tag der volkspolizei","tag der grenztruppen",
        "tag des mfs","tag der fdj","tag der arbeit","tag des sieges","jahrestag der befreiung",
        "jahrestag der oktoberrevolution","gründung der sed","gründung der kpd","gründung der udssr",
        "potsdamer","tag der zivilverteidigung","befreiung kz","mauerbau","liebknecht & luxemburg",
        "tag der jugendbrigaden","pariser kommune","jahrestag des mauerbaus","internationale brigaden",
        "gst (1952)"]):
        return "staat"
    if any(x in t for x in ["tag des metallarbeiters","tag des eisenbahners","tag des chemiearbeiters",
        "tag des metallurgen","tag des bergmanns","tag des bauarbeiters","tag des lehrers",
        "tag des gesundheit","pioniergeburtstag","tag der werktätigen","tag der mitarbeiter",
        "wasserwirtschaft","haus- und kommunal","seeverkehrs","post- und fernmelde",
        "tag der jungen techniker","tag der luft","tag der genossenschaft","tag der leicht"]):
        return "beruf"
    return "international"

# ICS-Zeilen zusammenführen (folded lines entfalten)
unfolded = []
for line in lines:
    if line.startswith(" ") or line.startswith("	"):
        if unfolded:
            unfolded[-1] += line[1:]
    else:
        unfolded.append(line)

# Events aus entfalteten ICS-Zeilen parsen
all_events = {}
current = {}
in_valarm = False
for line in unfolded:
    if line == "BEGIN:VEVENT":
        current = {}
        in_valarm = False
    elif line == "BEGIN:VALARM":
        in_valarm = True
    elif line == "END:VALARM":
        in_valarm = False
    elif line.startswith("DTSTART;VALUE=DATE:"):
        val = line.split(":")[1].strip()
        current["date"] = f"{val[4:6]}-{val[6:8]}"
        current["year"] = val[0:4]
    elif line.startswith("SUMMARY:"):
        current["title"] = line[8:].strip()
    elif line.startswith("DESCRIPTION:") and not in_valarm:
        # Nur VEVENT DESCRIPTION, VALARM-Description ignorieren (in_valarm-Flag)
        desc = line[12:].strip()
        desc = desc.replace("\\,", ",")
        current["desc"] = desc
    elif line == "END:VEVENT":
        if "date" in current and "title" in current and "desc" in current:
            yr = current.get("year", "")
            if yr not in all_events:
                all_events[yr] = []
            all_events[yr].append({
                "date":  current["date"],
                "title": current["title"],
                "desc":  current["desc"],
                "cat":   categorize(current.get("title", ""))
            })
        current = {}

# Nur App-relevante Jahre (2024-2035)
app_events = {yr: evs for yr, evs in all_events.items() if 2024 <= int(yr) <= 2035}

json_str = json.dumps(app_events, ensure_ascii=False, separators=(",",":"))
with open("ddr_events.json", "w", encoding="utf-8") as f:
    f.write(json_str)

total = sum(len(v) for v in app_events.values())
print(f"✓ ddr_events.json    — {len(app_events)} Jahre, {total} Einträge gesamt")
print(f"\nBeide Dateien bereit für GitHub:")
print(f"  → ddr-feiertage.ics")
print(f"  → ddr_events.json")
