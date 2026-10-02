#!/usr/bin/env python3
"""Eunomia-Prüfskript: Stufen 60/80/100, Konformitätsquote, STE-Nähe, Glossar.

Aufruf:
    python3 ste_check.py text.txt --lang de --typ anweisend --stufe 80
    python3 ste_check.py text.txt --lang de --glossar glossar.txt
    echo "Text" | python3 ste_check.py - --lang en --stufe 100

Kennzahlen:
    Stufenquote  Anteil der Sätze ohne harten Verstoß gegen die gewählte Stufe.
                 Ziel: mindestens 95 %.
    STE-Nähe     Anteil der Sätze ohne harten Verstoß gegen Stufe 100.
                 Richtwert: Stufe 60 ≈ 40–70 %, Stufe 80 ≈ 70–90 %, Stufe 100 ≥ 95 %.

Heuristik, kein Parser. Jede Markierung selbst bewerten.
"""
import argparse
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))

# Satzlängen-Grenzen je Stufe: (anweisend, beschreibend)
LAENGE = {60: (25, 30), 80: (20, 25), 100: (20, 25)}
# Absatzlänge (Sätze) je Stufe, None = keine Prüfung
ABSATZ = {60: None, 80: 8, 100: 6}

# Schwere je Prüfung und Stufe: "hart" zählt für die Quote, "hinweis" nicht, None = aus
SCHWERE = {
    "laenge":        {60: "hart", 80: "hart", 100: "hart"},
    "passiv_anw":    {60: "hart", 80: "hart", 100: "hart"},
    "passiv_beschr": {60: None, 80: "hinweis", 100: "hart"},
    "fvg":           {60: "hinweis", 80: "hart", 100: "hart"},
    "kompositum":    {60: "hinweis", 80: "hart", 100: "hart"},
    "partizip_start":{60: "hart", 80: "hart", 100: "hart"},
    "ing":           {60: None, 80: "hinweis", 100: "hart"},
    "wortliste":     {60: None, 80: "hinweis", 100: "hart"},
    "vage":          {60: "hinweis", 80: "hinweis", 100: "hart"},
    "nominal":       {60: None, 80: "hinweis", 100: "hinweis"},
    "partikel":      {60: "hinweis", 80: "hinweis", 100: "hart"},
    "schachtel":     {60: "hinweis", 80: "hinweis", 100: "hart"},
    "synonym":       {60: "hart", 80: "hart", 100: "hart"},
}

DE_NOMINAL = re.compile(r"\b\w+(ung|heit|keit|ion|tät)(en)?\b", re.I)
DE_FVG = re.compile(
    r"\b(erfolgt|erfolgen|vornehmen|vorgenommen|zur Anwendung|zum Einsatz|"
    r"Berücksichtigung finden|in Kenntnis|Sorge tragen|im Rahmen|hinsichtlich|"
    r"bezüglich|mittels|zwecks|aufgrund der Tatsache)\b", re.I)
DE_PASSIV = re.compile(
    r"\b(wird|werden|wurde|wurden|worden)\b.{0,60}?\b(ge\w+t|ge\w+en|\w+iert)\b"
    r"|\b(\w+t|\w+en)\s+(wird|werden|wurde|wurden|worden)\b", re.I)
DE_VAGE = re.compile(r"\b(ggf\.?|gegebenenfalls|eventuell|ausreichend|entsprechend|zeitnah|diverse|etwaige|sollte|sollten)\b", re.I)
DE_PARTIKEL = re.compile(r"\b(ja|eben|halt|wohl|doch)\b", re.I)

EN_ING = re.compile(r"\b\w{3,}ing\b", re.I)
EN_ING_OK = {"bearing", "housing", "training", "during", "something", "nothing", "anything",
             "everything", "string", "spring", "ring", "thing", "bring", "king", "wing",
             "ceiling", "fitting", "wiring", "tubing", "coupling", "warning", "lighting", "landing"}
EN_PASSIV = re.compile(r"\b(is|are|was|were|be|been|being)\s+(\w+ly\s+)?\w+(ed|en)\b", re.I)
EN_VAGE = re.compile(r"\b(should|may|might|sufficient|appropriate|as required|if necessary)\b", re.I)
EN_PARTIZIP_START = re.compile(r"^(Having|Being|After \w+ing)\b")


def lade_wortliste(pfad):
    paare = []
    if not os.path.exists(pfad):
        return paare
    for zeile in open(pfad, encoding="utf-8"):
        zeile = zeile.strip()
        if not zeile or zeile.startswith("#") or ">" not in zeile:
            continue
        falsch, richtig = [t.strip() for t in zeile.split(">", 1)]
        paare.append((re.compile(r"\b" + re.escape(falsch) + r"\b", re.I), falsch, richtig))
    return paare


def lade_glossar(pfad):
    """Zeilenformat:  Vorzugsbegriff: Synonym1, Synonym2"""
    eintraege = []
    for zeile in open(pfad, encoding="utf-8"):
        zeile = zeile.strip()
        if not zeile or zeile.startswith("#") or ":" not in zeile:
            continue
        vorzug, rest = zeile.split(":", 1)
        for syn in [s.strip() for s in rest.split(",") if s.strip()]:
            eintraege.append((re.compile(r"\b" + re.escape(syn) + r"\w{0,3}\b", re.I), syn, vorzug.strip()))
    return eintraege


def absaetze(text):
    return [a for a in re.split(r"\n\s*\n", text.strip()) if a.strip()]


def saetze(absatz):
    t = re.sub(r"\s+", " ", absatz.strip())
    for abk in ["z. B.", "z.B.", "d. h.", "d.h.", "ggf.", "bzw.", "usw.", "e.g.", "i.e.", "etc.", "Nr.", "ca.", "Dr.", "Abb."]:
        t = t.replace(abk, abk.replace(".", "§"))
    t = re.sub(r"\b(\d{1,2})\.(?=\s)", r"\1§", t)
    # Listenpunkte "1." am Satzanfang schützen
    teile = re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ0-9\"„])", t)
    return [x.replace("§", ".").strip() for x in teile if x.strip()]


def woerter(s):
    return re.findall(r"[\wÄÖÜäöüß\-]+", s)


def befunde_satz(s, lang, typ, wortliste, glossar):
    """Liefert Liste (pruef_id, text) — unabhängig von der Stufe."""
    b = []
    n = len(woerter(s))
    b.append(("laenge", n))
    if lang == "de":
        if DE_PASSIV.search(s):
            b.append(("passiv_anw" if typ == "anweisend" else "passiv_beschr", "Passiv"))
        f = sorted({m.group(0) for m in DE_FVG.finditer(s)})
        if f:
            b.append(("fvg", "Funktionsverbgefüge/Amtsdeutsch: " + ", ".join(f)))
        k = [w for w in woerter(s) if len(w) >= 20 and "-" not in w]
        if k:
            b.append(("kompositum", "langes Kompositum: " + ", ".join(k)))
        nom = [m.group(0) for m in DE_NOMINAL.finditer(s)]
        if len(nom) >= 3:
            b.append(("nominal", "Nominalstil? " + ", ".join(nom)))
        v = sorted({m.group(0) for m in DE_VAGE.finditer(s)})
        if v:
            b.append(("vage", "vage: " + ", ".join(v)))
        p = sorted({m.group(0) for m in DE_PARTIKEL.finditer(s)})
        if p:
            b.append(("partikel", "Modalpartikel? " + ", ".join(p)))
        if s.count(",") >= 3:
            b.append(("schachtel", "viele Kommas — Schachtelsatz?"))
        treffer = [f"{f} → {r}" for rx, f, r in wortliste if rx.search(s)]
        if treffer:
            b.append(("wortliste", "Wortliste: " + "; ".join(treffer)))
    else:
        if EN_PASSIV.search(s):
            b.append(("passiv_anw" if typ == "anweisend" else "passiv_beschr", "passive"))
        if EN_PARTIZIP_START.search(s):
            b.append(("partizip_start", "participle opener"))
        ing = sorted({m.group(0) for m in EN_ING.finditer(s) if m.group(0).lower() not in EN_ING_OK})
        if ing:
            b.append(("ing", "-ing: " + ", ".join(ing)))
        v = sorted({m.group(0) for m in EN_VAGE.finditer(s)})
        if v:
            b.append(("vage", "vague: " + ", ".join(v)))
        treffer = [f"{f} → {r}" for rx, f, r in wortliste if rx.search(s)]
        if treffer:
            b.append(("wortliste", "word list: " + "; ".join(treffer)))
        if s.count(",") >= 3:
            b.append(("schachtel", "many commas — split?"))
    syn = [f"{m.group(0)} → {vorzug}" for rx, _, vorzug in glossar for m in rx.finditer(s)]
    if syn:
        b.append(("synonym", "Glossar: " + "; ".join(syn)))
    return b


def bewerte(befunde, stufe, typ):
    """Teilt Befunde nach Schwere für eine Stufe auf."""
    limit = LAENGE[stufe][0 if typ == "anweisend" else 1]
    hart, hinweis = [], []
    for pid, info in befunde:
        if pid == "laenge":
            if info > limit:
                hart.append(f"LÄNGE {info} > {limit}")
            continue
        sch = SCHWERE[pid][stufe]
        if sch == "hart":
            hart.append(info)
        elif sch == "hinweis":
            hinweis.append(info)
    return hart, hinweis


def pruefe(text, lang, typ, stufe, glossar, nur_hart):
    wortliste = lade_wortliste(os.path.join(HIER, "..", "references", f"wortliste-{lang}.txt"))
    alle = []
    absatz_warn = []
    for ai, a in enumerate(absaetze(text), 1):
        ss = saetze(a)
        grenze = ABSATZ[stufe]
        if grenze and len(ss) > grenze:
            absatz_warn.append(f"Absatz {ai}: {len(ss)} Sätze > {grenze}")
        alle.extend(ss)

    n = len(alle)
    if n == 0:
        print("Kein Text.")
        return 1
    laengen = [len(woerter(s)) for s in alle]
    ok_stufe = ok_ste = 0
    zeilen = []
    for i, s in enumerate(alle, 1):
        bf = befunde_satz(s, lang, typ, wortliste, glossar)
        hart, hinweis = bewerte(bf, stufe, typ)
        hart100, _ = bewerte(bf, 100, typ)
        ok_stufe += not hart
        ok_ste += not hart100
        if hart or (hinweis and not nur_hart):
            zeilen.append((i, laengen[i - 1], s, hart, hinweis))

    schnitt = sum(laengen) / n
    q_stufe = 100 * ok_stufe / n
    q_ste = 100 * ok_ste / n
    print(f"Stufe {stufe} | {lang} | {typ}")
    print(f"Sätze: {n} | Ø {schnitt:.1f} Wörter | max {max(laengen)}")
    print(f"Stufenquote: {q_stufe:.0f} % (Ziel ≥ 95 %)  {'OK' if q_stufe >= 95 else 'NACHARBEITEN'}")
    soll = {60: (40, 70), 80: (70, 90), 100: (95, 100)}[stufe]
    lage = "im Rahmen" if soll[0] <= q_ste <= soll[1] else ("strenger als nötig (unkritisch)" if q_ste > soll[1] else "lockerer als Stufe — nachschärfen")
    print(f"STE-Nähe:    {q_ste:.0f} % (Richtwert Stufe {stufe}: {soll[0]}–{soll[1]} %) → {lage}")
    if typ == "beschreibend" and schnitt < 10:
        print("HINWEIS: Ø unter 10 Wörtern — Text wirkt zerhackt. Sätze verbinden (Ziel 12–20).")
    for w in absatz_warn:
        print("ABSATZ: " + w)
    print()
    for i, ln, s, hart, hinweis in zeilen:
        print(f"[{i}] ({ln} W) {s}")
        for h in hart:
            print(f"    ✗ {h}")
        if not nur_hart:
            for h in hinweis:
                print(f"    ? {h}")
        print()
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("datei", help="Textdatei oder - für stdin")
    ap.add_argument("--lang", choices=["de", "en"], default="de")
    ap.add_argument("--typ", choices=["anweisend", "beschreibend"], default="beschreibend")
    ap.add_argument("--stufe", type=int, choices=[60, 80, 100], default=80)
    ap.add_argument("--glossar", help="Glossardatei (Vorzugsbegriff: Synonym1, Synonym2)")
    ap.add_argument("--nur-hart", action="store_true", help="Nur harte Verstöße zeigen")
    a = ap.parse_args()
    text = sys.stdin.read() if a.datei == "-" else open(a.datei, encoding="utf-8").read()
    glossar = lade_glossar(a.glossar) if a.glossar else []
    sys.exit(pruefe(text, a.lang, a.typ, a.stufe, glossar, a.nur_hart))


if __name__ == "__main__":
    main()
