#!/usr/bin/env python3
"""Fast Roller: Fragen und Antworten in Tagesdateien ablegen (nur Standardbibliothek)."""
import argparse, os, re, sys, time
from datetime import datetime

WOCHENTAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
STATI = ("offen", "erledigt")
VERTRAULICH = "(vertraulich, nicht protokolliert)"
GEHEIM = [
    (re.compile(r"\b[0-9a-fA-F]{32,}\b"), "lange Hex-Folge"),
    (re.compile(r"(?<![\w/.-])(?=[A-Za-z0-9+/_=-]*\d)(?=[A-Za-z0-9+/_=-]*[A-Za-z])[A-Za-z0-9+/_=-]{40,}(?![\w/.-])"), "lange Zeichenfolge (Base64/Token)"),
    (re.compile(r"token\s*[=:]", re.I), "token="),
    (re.compile(r"passw|kennwort", re.I), "Passwort/Kennwort"),
    (re.compile(r"api[_-]?key|secret\s*[=:]", re.I), "API-Key/Secret"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY"), "privater Schluessel"),
]


def jetzt():
    t = os.environ.get("FAST_ROLLER_JETZT")  # nur fuer Tests: 2026-11-12T09:14
    if t:
        return datetime.fromisoformat(t)
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Vienna")).replace(tzinfo=None)
    except Exception:
        import subprocess
        out = subprocess.check_output(["date", "+%Y-%m-%dT%H:%M"], env={**os.environ, "TZ": "Europe/Vienna"})
        return datetime.fromisoformat(out.decode().strip())


def pruefe_geheimnis(*texte):
    for t in texte:
        for rx, name in GEHEIM:
            if rx.search(t or ""):
                sys.exit("ABBRUCH: Verdacht auf Geheimnis (%s). Nichts geschrieben. "
                         "Text ohne Geheimnis neu senden oder --vertraulich verwenden." % name)


class Sperre:
    def __init__(self, ordner):
        self.pfad = os.path.join(ordner, ".lock")

    def __enter__(self):
        ende = time.time() + 30
        while True:
            try:
                fd = os.open(self.pfad, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                return self
            except FileExistsError:
                try:
                    if time.time() - os.path.getmtime(self.pfad) > 20:
                        os.unlink(self.pfad)  # verwaiste Sperre
                        continue
                except OSError:
                    pass
                if time.time() > ende:
                    sys.exit("ABBRUCH: Sperre %s haengt." % self.pfad)
                time.sleep(0.05)

    def __exit__(self, *a):
        try:
            os.unlink(self.pfad)
        except OSError:
            pass


def schreibe(pfad, text):
    tmp = "%s.tmp.%d" % (pfad, os.getpid())
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, pfad)


def lies(pfad, standard=""):
    try:
        with open(pfad, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return standard


def eintraege(text):
    """Zerlegt eine Tagesdatei in Eintraege (dicts)."""
    res = []
    teile = re.split(r"(?m)^(?=## )", text)
    for t in teile:
        m = re.search(r'<a id="([^"]+)"></a>', t)
        if not t.startswith("## ") or not m:
            continue
        kopf = t.splitlines()[0][3:]
        mz = re.match(r"(\d\d:\d\d) — (.*)", kopf)
        st = re.search(r"(?m)^\*\*Status:\*\* (.*)$", t)
        res.append({"id": m.group(1), "zeit": mz.group(1) if mz else "", "titel": mz.group(2) if mz else kopf,
                    "status": st.group(1).strip() if st else "offen", "text": t.rstrip() + "\n"})
    return res


def tagesdateien(ordner):
    return sorted(f for f in os.listdir(ordner) if re.fullmatch(r"\d{4}-\d\d-\d\d\.md", f))


def index_zeile(tag, zeit, titel, status, eid):
    return "- %s | %s | %s | %s | [Eintrag](%s.md#%s) | %s" % (tag, zeit or "--:--", titel, status, tag, eid, eid)


def index_neu_schreiben(ordner):
    zeilen = ["# Index der Fragen und Antworten", ""]
    for f in tagesdateien(ordner):
        tag = f[:-3]
        for e in eintraege(lies(os.path.join(ordner, f))):
            zeilen.append(index_zeile(tag, e["zeit"], e["titel"], e["status"], e["id"]))
    schreibe(os.path.join(ordner, "INDEX.md"), "\n".join(zeilen) + "\n")


def text_arg(wert, datei, name):
    if datei:
        return lies(datei).strip()
    if wert == "-":
        return sys.stdin.read().strip()
    if wert is None:
        sys.exit("FEHLER: --%s oder --%s-datei fehlt." % (name, name))
    return wert.strip()


def cmd_neu(a):
    if a.vertraulich:
        frage = antwort = VERTRAULICH
    else:
        frage = text_arg(a.frage, a.frage_datei, "frage")
        antwort = text_arg(a.antwort, a.antwort_datei, "antwort")
        pruefe_geheimnis(a.titel, frage, antwort, a.stichworte)
    status = a.status
    if status not in STATI and not status.startswith("wartet auf"):
        sys.exit("FEHLER: Status muss offen, erledigt oder 'wartet auf ...' sein.")
    os.makedirs(a.ordner, exist_ok=True)
    t = jetzt()
    tag = t.strftime("%Y-%m-%d")
    zeit = None if a.ohne_uhrzeit else t.strftime("%H:%M")
    pfad = os.path.join(a.ordner, tag + ".md")
    with Sperre(a.ordner):
        text = lies(pfad)
        if not text:
            text = "# Fragen und Antworten – %s, %s\n" % (WOCHENTAGE[t.weekday()], t.strftime("%d.%m.%Y"))
        nr = len(eintraege(text)) + 1
        eid = "%s-%s-%02d" % (t.strftime("%Y%m%d"), t.strftime("%H%M"), nr)
        kopf = "## %s — %s" % (zeit, a.titel) if zeit else "## %s" % a.titel
        block = "\n%s\n<a id=\"%s\"></a>\n**Frage:** %s\n**Antwort:** %s\n**Status:** %s\n**Stichworte:** %s\n" % (
            kopf, eid, frage, antwort, status, a.stichworte or "")
        schreibe(pfad, text.rstrip("\n") + "\n" + block)
        idx = os.path.join(a.ordner, "INDEX.md")
        if os.path.exists(idx):
            alt = lies(idx).rstrip("\n") + "\n"
            schreibe(idx, alt + index_zeile(tag, zeit, a.titel, status, eid) + "\n")
        else:
            index_neu_schreiben(a.ordner)
    print("OK %s" % eid)


def alle(ordner):
    res = []
    if not os.path.isdir(ordner):
        return res
    for f in tagesdateien(ordner):
        for e in eintraege(lies(os.path.join(ordner, f))):
            e["tag"] = f[:-3]
            res.append(e)
    return res


def cmd_liste(a):
    treffer = []
    for e in alle(a.ordner):
        if a.tag and e["tag"] != a.tag:
            continue
        if a.offen and e["status"] == "erledigt":
            continue
        if a.suche and a.suche.lower() not in e["text"].lower():
            continue
        treffer.append(e)
    if not treffer:
        print("Nichts gefunden.")
    for e in treffer:
        vorn = "" if a.tag else e["tag"][5:] + " "
        print("%s%s %s [%s] (%s)" % (vorn, e["zeit"] or "--:--", e["titel"], e["status"], e["id"]))


def cmd_zeige(a):
    for e in alle(a.ordner):
        if e["id"] == a.id:
            print(e["text"])
            return
    sys.exit("FEHLER: ID %s nicht gefunden." % a.id)


def cmd_status(a):
    if a.auf not in STATI and not a.auf.startswith("wartet auf"):
        sys.exit("FEHLER: Status muss offen, erledigt oder 'wartet auf ...' sein.")
    tag = "%s-%s-%s" % (a.id[:4], a.id[4:6], a.id[6:8])
    pfad = os.path.join(a.ordner, tag + ".md")
    with Sperre(a.ordner):
        text = lies(pfad)
        teile = re.split(r"(?m)^(?=## )", text)
        gefunden = False
        for i, t in enumerate(teile):
            if '<a id="%s"></a>' % a.id in t:
                teile[i] = re.sub(r"(?m)^\*\*Status:\*\* .*$", lambda m: "**Status:** " + a.auf, t, count=1)
                gefunden = True
        if not gefunden:
            sys.exit("FEHLER: ID %s nicht gefunden." % a.id)
        schreibe(pfad, "".join(teile))
        index_neu_schreiben(a.ordner)
    print("OK %s -> %s" % (a.id, a.auf))


def cmd_modus(a):
    pfad = os.path.join(a.ordner, ".modus")
    if a.wert in ("an", "aus"):
        os.makedirs(a.ordner, exist_ok=True)
        with Sperre(a.ordner):
            schreibe(pfad, a.wert + "\n")
        print("Fast Roller " + a.wert)
    else:
        print("Fast Roller " + (lies(pfad, "aus").strip() or "aus"))


def main(argv=None):
    p = argparse.ArgumentParser(prog="eintrag.py")
    s = p.add_subparsers(dest="cmd", required=True)
    n = s.add_parser("neu")
    n.add_argument("--ordner", required=True)
    n.add_argument("--titel", required=True)
    n.add_argument("--frage")
    n.add_argument("--frage-datei")
    n.add_argument("--antwort")
    n.add_argument("--antwort-datei")
    n.add_argument("--status", default="offen")
    n.add_argument("--stichworte", default="")
    n.add_argument("--ohne-uhrzeit", action="store_true")
    n.add_argument("--vertraulich", action="store_true")
    n.set_defaults(f=cmd_neu)
    l = s.add_parser("liste")
    l.add_argument("--ordner", required=True)
    l.add_argument("--tag")
    l.add_argument("--offen", action="store_true")
    l.add_argument("--suche")
    l.set_defaults(f=cmd_liste)
    z = s.add_parser("zeige")
    z.add_argument("--ordner", required=True)
    z.add_argument("--id", required=True)
    z.set_defaults(f=cmd_zeige)
    st = s.add_parser("status")
    st.add_argument("--ordner", required=True)
    st.add_argument("--id", required=True)
    st.add_argument("--auf", required=True)
    st.set_defaults(f=cmd_status)
    m = s.add_parser("modus")
    m.add_argument("--ordner", required=True)
    m.add_argument("wert", choices=["an", "aus", "zeige"])
    m.set_defaults(f=cmd_modus)
    a = p.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
