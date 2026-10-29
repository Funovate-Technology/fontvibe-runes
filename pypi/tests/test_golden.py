"""Golden tests: every case recorded from FontVibe's production implementation
must come out byte-identical. Run with `python -m unittest discover tests`
(or pytest) after `python scripts/sync_data.py`."""

import hashlib
import json
import pathlib
import unittest

import rune_transliterator as rt

_HERE = pathlib.Path(__file__).resolve()
_GOLDEN = _HERE.with_name("golden.json")  # copied in by sync_data.py (sdist)
if not _GOLDEN.exists():
    _GOLDEN = _HERE.parents[2] / "tests" / "golden.json"  # repo checkout
GOLDEN = json.loads(_GOLDEN.read_text(encoding="utf-8"))
FN = {"toRunes": rt.to_runes, "fromRunes": rt.from_runes}


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def every_scalar() -> str:
    return "".join(chr(cp) for cp in range(0x110000) if not 0xD800 <= cp <= 0xDFFF)


class Golden(unittest.TestCase):
    def test_cases(self):
        for c in GOLDEN["cases"]:
            fn = FN[c["fn"]]
            got = fn(c["input"]) if c["system"] is None else fn(c["input"], c["system"])
            self.assertEqual(got, c["output"], f'{c["fn"]}({c["input"]!r}, {c["system"]!r})')

    def test_exhaustive(self):
        s = every_scalar()
        self.assertEqual(sha(s), GOLDEN["exhaustive"]["input_sha256"])
        for system in rt.SYSTEMS:
            self.assertEqual(sha(rt.to_runes(s, system)), GOLDEN["exhaustive"][system]["toRunes"], system)
            self.assertEqual(sha(rt.from_runes(s, system)), GOLDEN["exhaustive"][system]["fromRunes"], system)


class Contract(unittest.TestCase):
    def test_api(self):
        self.assertEqual(rt.SYSTEMS, ("elder", "younger", "anglo"))
        self.assertEqual(rt.to_runes(None), "")
        self.assertEqual(rt.to_runes("thor", None), "ᚦᛟᚱ")
        self.assertRaises(TypeError, rt.to_runes, 42)
        self.assertEqual(len(rt.alphabet("younger")), 16)
        self.assertIs(rt.RUNE_ALPHABET["anglo"], rt.alphabet("anglo"))

    def test_cli(self):
        import contextlib
        import io

        from rune_transliterator.__main__ import main

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main(["-s", "anglo", "earth", "king"])
        self.assertEqual(buf.getvalue(), "ᛠᚱᚦ ᚳᛁᛝ\n")


if __name__ == "__main__":
    unittest.main()
