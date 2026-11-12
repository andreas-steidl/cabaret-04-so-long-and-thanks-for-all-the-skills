# -*- coding: utf-8 -*-
"""Speichert eine Druckfassung der Kabarett-Plakate (gemeinsam für plakat*.py und plakate_en.py).

Die Leinwand trägt ringsum `off` Pixel Beschnitt. Daraus entstehen:
    <name>_beschnitt.png   ganze Leinwand (Endformat + 3 mm ringsum)
    <name>.png             Endformat (Leinwand ohne Beschnitt)
    <name>_vorschau.jpg    900 px breit, zum Ansehen
PNG mit 300 dpi (pHYs) und sRGB-Profil (iCCP), sonst ohne Metadaten: Das Bild wird über
den rohen Pixelpuffer neu aufgebaut, damit nichts aus der Quelle mitkommt.
"""
import os

from PIL import Image

SRGB_WINDOWS = os.path.join(os.environ.get("SystemRoot", "C:" + chr(92) + "Windows"),
                            "System32", "spool", "drivers", "color", "sRGB Color Space Profile.icm")


def srgb_profil():
    if os.path.exists(SRGB_WINDOWS):
        with open(SRGB_WINDOWS, "rb") as datei:
            return datei.read()
    from PIL import ImageCms
    return ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()


def speichern(leinwand, off, ziel, name):
    os.makedirs(ziel, exist_ok=True)
    rgb = leinwand.convert("RGB")
    rgb = Image.frombytes("RGB", rgb.size, rgb.tobytes())
    profil = srgb_profil()
    beschnitt = os.path.join(ziel, name + "_beschnitt.png")
    rgb.save(beschnitt, dpi=(300, 300), icc_profile=profil)
    end = rgb.crop((off, off, rgb.width - off, rgb.height - off))
    endformat = os.path.join(ziel, name + ".png")
    end.save(endformat, dpi=(300, 300), icc_profile=profil)
    vorschau = os.path.join(ziel, name + "_vorschau.jpg")
    end.resize((900, round(end.height * 900 / end.width)), Image.LANCZOS).save(vorschau, quality=88)
    print("ok", endformat, end.size, "|", beschnitt, rgb.size)
    return endformat, beschnitt, vorschau
