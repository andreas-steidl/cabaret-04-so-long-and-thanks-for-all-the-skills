import os, subprocess, sys, tempfile, unittest

SKRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "eintrag.py")


def lauf(*args, jetzt="2026-11-12T09:14", stdin=None):
    env = {**os.environ, "FAST_ROLLER_JETZT": jetzt}
    return subprocess.run([sys.executable, "-I", SKRIPT, *args], capture_output=True, text=True, env=env, input=stdin)


class T(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.d = os.path.join(self._t.name, "fragen")

    def tearDown(self):
        self._t.cleanup()

    def neu(self, titel="Linux Distro", frage="Welche Distro?", antwort="Ubuntu.", **kw):
        extra = []
        for k, v in kw.items():
            extra += ["--" + k.replace("_", "-"), v]
        return lauf("neu", "--ordner", self.d, "--titel", titel, "--frage", frage, "--antwort", antwort, *extra)

    def lies(self, name):
        with open(os.path.join(self.d, name), encoding="utf-8") as f:
            return f.read()

    def test_anlegen_und_index(self):
        r = self.neu(stichworte="linux, distro")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("20261112-0914-01", r.stdout)
        t = self.lies("2026-11-12.md")
        self.assertIn("# Fragen und Antworten – Donnerstag, 12.11.2026", t)
        self.assertIn("## 09:14 — Linux Distro", t)
        self.assertIn("**Status:** offen", t)
        self.assertIn("**Stichworte:** linux, distro", t)
        i = self.lies("INDEX.md")
        self.assertIn("| 09:14 | Linux Distro | offen |", i)
        self.assertIn("2026-11-12.md#20261112-0914-01", i)

    def test_ohne_uhrzeit_und_dateien(self):
        fd = os.path.join(self._t.name, "f.txt")
        open(fd, "w").write("Lange Frage")
        r = lauf("neu", "--ordner", self.d, "--titel", "X", "--frage-datei", fd, "--antwort", "-", "--ohne-uhrzeit", stdin="Antwort per stdin")
        self.assertEqual(r.returncode, 0, r.stderr)
        t = self.lies("2026-11-12.md")
        self.assertIn("\n## X\n", t)
        self.assertIn("**Frage:** Lange Frage", t)
        self.assertIn("**Antwort:** Antwort per stdin", t)

    def test_liste_und_suche(self):
        self.neu(titel="Linux Distro")
        self.neu(titel="Steuer", frage="Wann USt?", antwort="Quartal.")
        r = lauf("liste", "--ordner", self.d, "--tag", "2026-11-12")
        self.assertEqual(len(r.stdout.strip().splitlines()), 2)
        r = lauf("liste", "--ordner", self.d, "--suche", "ubuntu")
        self.assertIn("Linux Distro", r.stdout)
        self.assertNotIn("Steuer", r.stdout)
        r = lauf("liste", "--ordner", self.d, "--suche", "gibtsnicht")
        self.assertIn("Nichts gefunden", r.stdout)

    def test_status(self):
        self.neu()
        r = lauf("status", "--ordner", self.d, "--id", "20261112-0914-01", "--auf", "erledigt")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("**Status:** erledigt", self.lies("2026-11-12.md"))
        self.assertIn("| erledigt |", self.lies("INDEX.md"))
        r = lauf("liste", "--ordner", self.d, "--offen")
        self.assertIn("Nichts gefunden", r.stdout)
        r = lauf("status", "--ordner", self.d, "--id", "20261112-0914-99", "--auf", "erledigt")
        self.assertNotEqual(r.returncode, 0)

    def test_modus(self):
        self.assertIn("aus", lauf("modus", "--ordner", self.d, "zeige").stdout)
        lauf("modus", "--ordner", self.d, "an")
        self.assertIn("an", lauf("modus", "--ordner", self.d, "zeige").stdout)
        lauf("modus", "--ordner", self.d, "aus")
        self.assertIn("aus", lauf("modus", "--ordner", self.d, "zeige").stdout)

    def test_geheimnis(self):
        for schlecht in ["token=abc", "mein Passwort ist x", "a" * 10 + "0123456789abcdef" * 3, "deadbeef" * 5]:
            r = self.neu(antwort=schlecht)
            self.assertNotEqual(r.returncode, 0, schlecht)
            self.assertIn("Geheimnis", r.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.d, "2026-11-12.md")))
        r = lauf("neu", "--ordner", self.d, "--titel", "Geheim", "--vertraulich")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("(vertraulich, nicht protokolliert)", self.lies("2026-11-12.md"))

    def test_gleichzeitig(self):
        os.makedirs(self.d)
        env = {**os.environ, "FAST_ROLLER_JETZT": "2026-11-12T09:14"}
        ps = [subprocess.Popen([sys.executable, "-I", SKRIPT, "neu", "--ordner", self.d, "--titel", "E%d" % i,
                                "--frage", "F%d" % i, "--antwort", "A%d" % i], env=env, stdout=subprocess.PIPE) for i in range(8)]
        for p in ps:
            p.communicate()
            self.assertEqual(p.returncode, 0)
        t = self.lies("2026-11-12.md")
        for i in range(8):
            self.assertIn("**Frage:** F%d\n" % i, t)
        ids = [l for l in self.lies("INDEX.md").splitlines() if l.startswith("- ")]
        self.assertEqual(len(ids), 8)
        self.assertEqual(len(set(l.split(" | ")[-1] for l in ids)), 8)


if __name__ == "__main__":
    unittest.main()
