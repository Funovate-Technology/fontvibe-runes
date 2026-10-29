#!/usr/bin/env python3
"""Copy ../data/runes.json into the package before building.

data/runes.json at the repo root is the single source of truth for both the npm
and the PyPI package; the copy inside src/ is generated and never committed.
"""
import json
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
SRC = HERE.parent / "data" / "runes.json"
DST = HERE / "src" / "rune_transliterator" / "runes.json"

if not SRC.exists():
    sys.exit(f"[sync_data] missing {SRC} — run this from inside the repo")
data = json.loads(SRC.read_text(encoding="utf-8"))  # fail loudly on a broken table
for k, v in data["systems"].items():
    if not v["alphabet"]:
        sys.exit(f"[sync_data] system {k} has an empty alphabet — refusing")
shutil.copyfile(SRC, DST)
# golden.json too, so the tests still run from an unpacked sdist.
shutil.copyfile(HERE.parent / "tests" / "golden.json", HERE / "tests" / "golden.json")
print(f"[sync_data] ok — {', '.join(data['systems'])}")
