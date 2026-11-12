# -*- coding: utf-8 -*-
"""plakat4.py - das Plakat der vierten Spielzeit „Macht's gut, und danke für die Skills“, deutsch und englisch.

Bild von Codex ohne Schrift (bild_ohne_schrift.png, Auftrag in AUFTRAG_bild.md), Schrift gesetzt von Falzbein,
im selben Satz wie die Plakate der ersten beiden Spielzeiten, aber in den Farben der dritten: Flaschengrün,
Elfenbein, Kupfer.

Aufruf:  python plakat4.py [bild] [zielordner]     ohne Argumente: bild_ohne_schrift.png und dieser Ordner
Schreibt plakat4_de.png / plakat4_en.png (A4, 300 dpi) und plakat4_de-web.jpg / plakat4_en-web.jpg (900 px breit).

Druckfassung:  python plakat4.py --format A2|A3 [bild] [zielordner]
A2 4961x7016, A3 3508x4961, 300 dpi, alle Maße mit Höhe/3508 skaliert; Bild ist dann
bild_ohne_schrift_x2.png (SeedVR2 x2), Ziel druck/. Schreibt plakat4_<de|en>_<F>.png,
_beschnitt.png (3 mm = 35 px ringsum, Rahmen und Schrift an derselben Stelle) und _vorschau.jpg.

12.11.2026, auf Andys Wort: Die Nummernzeilen unten waren schlecht lesbar, weil das Bild dort hell
ist. Der dunkle Verlauf unten beginnt darum bei 0,70 statt 0,78 der Höhe und geht bis 235 statt 215,
und die Nummern tragen einen kräftigeren Schatten (mit Kontur).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HIER = os.path.dirname(os.path.abspath(__file__))
W, H = 2480, 3508
F = "C:/Windows/Fonts/"
KUPFER = (240, 150, 70)   # hier: Goldfisch-Orange
ELFENBEIN = (238, 234, 244)   # hier: Zinnweiß
DUNKEL = (14, 8, 24)
KONTUR = (48, 26, 70)
SCHATTEN = (4, 12, 9)
RAND = 260
UNTEN_AB, UNTEN_BIS = 0.70, 235  # dunkler Verlauf unten: Beginn (Anteil der Höhe), Deckkraft am Fuß

FORMATE = {"A2": (4961, 7016), "A3": (3508, 4961)}
BESCHNITT = 35  # 3 mm bei 300 dpi
FORMAT = None
OFF = 0
K = 1.0


def formatieren(name):
    """Stellt Endformat, Beschnitt und Maßfaktor für A2 oder A3 ein."""
    global W, H, FORMAT, OFF, K
    FORMAT = name
    W, H = FORMATE[name]
    OFF = BESCHNITT
    K = H / 3508


def m(v):
    """Ein Maß des A4-Satzes; im Druckformat mit Höhe/3508 skaliert, sonst unverändert."""
    return v if FORMAT is None else round(v * K)


def font(name, size):
    return ImageFont.truetype(F + name, size)


def grund(pfad):
    cw, ch = W + 2 * OFF, H + 2 * OFF
    quelle = Image.open(pfad).convert("RGB")
    s = ch / quelle.height
    bild = quelle.resize((round(quelle.width * s), ch), Image.BICUBIC)
    if bild.width < cw:
        s = cw / quelle.width
        bild = quelle.resize((cw, round(quelle.height * s)), Image.BICUBIC)
    x0 = (bild.width - cw) // 2
    y0 = (bild.height - ch) // 2
    img = bild.crop((x0, y0, x0 + cw, y0 + ch))
    maske = Image.new("L", (cw, ch), 0)
    md = ImageDraw.Draw(maske)
    for y in range(ch):
        yy = min(max(y - OFF, 0), H - 1)
        if yy < H * 0.36:
            a = int(200 * (1 - yy / (H * 0.36)) ** 1.2)
        elif yy > H * UNTEN_AB:
            a = int(UNTEN_BIS * ((yy - H * UNTEN_AB) / (H * (1 - UNTEN_AB))) ** 0.9)
        else:
            a = 0
        md.line([(0, y), (cw, y)], fill=a)
    img.paste(Image.new("RGB", (cw, ch), DUNKEL), (0, 0), maske)
    return img


def setzen(bildpfad, t, zielordner, name):
    img = grund(bildpfad)
    d = ImageDraw.Draw(img)

    def mitte(text, y, fname, size, fill=ELFENBEIN, stroke=0):
        while True:
            f = font(fname, m(size))
            b = d.textbbox((0, 0), text, font=f, stroke_width=stroke)
            if b[2] - b[0] <= W - m(RAND) or size < 30:
                break
            size -= 4
        x = (W - (b[2] - b[0])) / 2 - b[0] + OFF
        d.text((x + m(6), y + m(8) + OFF), text, font=f, fill=SCHATTEN, stroke_width=stroke, stroke_fill=SCHATTEN)
        d.text((x, y + OFF), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=KONTUR)
        return y + (b[3] - b[1])

    d.rectangle([m(50) + OFF, m(50) + OFF, W - m(50) + OFF, H - m(50) + OFF], outline=KUPFER, width=m(12))
    d.rectangle([m(82) + OFF, m(82) + OFF, W - m(82) + OFF, H - m(82) + OFF], outline=KUPFER, width=m(3))
    for cx, cy in ((m(82), m(82)), (W - m(82), m(82)), (m(82), H - m(82)), (W - m(82), H - m(82))):
        d.ellipse([cx - m(22) + OFF, cy - m(22) + OFF, cx + m(22) + OFF, cy + m(22) + OFF], fill=KUPFER)

    y = m(170)
    y = mitte(t["ueber"], y, "GILC____.TTF", 88, KUPFER) + m(55)
    y = mitte(t["titel1"][0], y, "BROADW.TTF", t["titel1"][1], ELFENBEIN, m(5)) + m(45)
    y = mitte(t["titel2"][0], y, "BROADW.TTF", t["titel2"][1], KUPFER, m(5)) + m(60)
    y = mitte(t["unter"], y, "GARAIT.TTF", 84, ELFENBEIN) + m(45)
    mitte(t["art"], y, "GILC____.TTF", 80, KUPFER)

    prog = font("POORICH.TTF", m(60))
    yu = int(H * 0.815)
    for i, text in enumerate(t["nummern"]):
        spalte, zeile = i % 3, i // 3
        x = [W * 0.20, W * 0.50, W * 0.80][spalte] + OFF
        b = d.textbbox((0, 0), text, font=prog)
        # kräftiger Schatten: versetzt und mit Kontur, dazu eine schmale dunkle Kontur um die Schrift
        d.text((x - (b[2] - b[0]) / 2 + m(5), yu + zeile * m(88) + m(6) + OFF), text, font=prog, fill=SCHATTEN,
               stroke_width=m(4), stroke_fill=SCHATTEN)
        d.text((x - (b[2] - b[0]) / 2, yu + zeile * m(88) + OFF), text, font=prog, fill=ELFENBEIN,
               stroke_width=m(2), stroke_fill=SCHATTEN)
    yu += 2 * m(88) + m(40)
    d.line([(W * 0.2 + OFF, yu + OFF), (W * 0.8 + OFF, yu + OFF)], fill=KUPFER, width=m(3))
    yu += m(35)
    yu = mitte(t["besetzung"], yu, "GILC____.TTF", 70, ELFENBEIN) + m(26)
    yu = mitte(t["gast"], yu, "GARAIT.TTF", 62, KUPFER) + m(24)
    yu = mitte(t["satz"], yu, "GARAIT.TTF", 54, ELFENBEIN) + m(30)
    mitte(t["fuss"], yu, "GILC____.TTF", 62, KUPFER)

    if FORMAT:
        from druck_speichern import speichern
        return speichern(img, OFF, zielordner, name + "_" + FORMAT)
    a4 = os.path.join(zielordner, name + ".png")
    web = os.path.join(zielordner, name + "-web.jpg")
    img.save(a4, dpi=(300, 300))
    img.resize((900, round(H * 900 / W)), Image.LANCZOS).save(web, quality=88)
    print("ok", a4)


DE = dict(
    ueber="FALZBEIN & ANDY · DAS VIERTE PROGRAMM",
    titel1=("MACHT'S GUT,", 236),
    titel2=("UND DANKE FÜR DIE SKILLS", 150),
    unter="Ein Abschied in sechs Spickzetteln und einem Extra",
    art="Viertes Programm der Skill-Suite des Grauens",
    nummern=["21 · zeitansage", "22 · brief-an-den-boten", "23 · goldfisch",
             "24 · durch-den-schnitt", "25 · rome-in-a-day", "26 · fast-roller"],
    besetzung="Mit Funden aus der Telefonecke, der Bauecke und dem Goldfischglas",
    gast="Extra: grau-in-grau. Ein Kind erbt alles, auch die Farbe.",
    satz="Nimm ein Handtuch mit. Und vergiss nichts.",
    fuss="WIEN · NOVEMBER 2026 · EINTRITT: EIN GUTES GEDÄCHTNIS",
)

EN = dict(
    ueber="FALZBEIN & ANDY · THE FOURTH PROGRAM",
    titel1=("SO LONG,", 236),
    titel2=("AND THANKS FOR ALL THE SKILLS", 150),
    unter="A farewell in six cheat sheets and an extra",
    art="Fourth program of the Skill Suite of Horrors",
    nummern=["21 · speaking-clock", "22 · message-in-a-bottle", "23 · goldfish",
             "24 · final-cut", "25 · rome-in-a-day", "26 · fast-roller"],
    besetzung="With finds from the phone corner, the build corner and the goldfish bowl",
    gast="Extra: grey-on-grey. A child inherits everything, even the colour.",
    satz="Bring a towel. And don't forget anything.",
    fuss="VIENNA · NOVEMBER 2026 · ADMISSION: A GOOD MEMORY",
)

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--format" in args:
        stelle = args.index("--format")
        wahl = args[stelle + 1].upper()
        del args[stelle:stelle + 2]
        if wahl not in FORMATE:
            sys.exit("--format A2 oder A3")
        formatieren(wahl)
    bild = args[0] if len(args) > 0 else os.path.join(HIER, "bild_ohne_schrift_x2.png" if FORMAT else "bild_ohne_schrift.png")
    ziel = args[1] if len(args) > 1 else (os.path.join(HIER, "druck") if FORMAT else HIER)
    setzen(bild, DE, ziel, "plakat4_de")
    setzen(bild, EN, ziel, "plakat4_en")
