#!/usr/bin/env python3
"""Render the generated sections of README.md from data/runes.json.

    python scripts/charts.py           # print what the sections should be
    python scripts/charts.py --write   # rewrite them in README.md

Every code point and Unicode character name comes from Python's unicodedata,
never typed by hand. Stdlib only.
"""
import json
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "runes.json").read_text(encoding="utf-8"))
GOLDEN = json.loads((ROOT / "tests" / "golden.json").read_text(encoding="utf-8"))
README = ROOT / "README.md"
BLOCK = (0x16A0, 0x16FF)
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def cp(ch):
    return f"U+{ord(ch):04X}"


def two_letter(table, s):
    """What toRunes() gives for a two-letter input (digraph, else letter by letter)."""
    if s in table["digraphs"]:
        return table["digraphs"][s]
    return "".join(table["letters"].get(c, c) for c in s)


def all_digraphs():
    seen = []
    for t in DATA["systems"].values():
        for k in t["digraphs"]:
            if k not in seen:
                seen.append(k)
    return seen


def distinct_runes():
    return sorted({e["rune"] for t in DATA["systems"].values() for e in t["alphabet"]})


def summary():
    s = DATA["systems"]
    rows = [(len(t["alphabet"]), f'{t["label"]} runes', t["page"].replace("https://", "")) for t in s.values()]
    d = distinct_runes()
    w = max(len(r[1]) for r in rows)
    lines = [f"{n:<4} {label:<{w}}  → {page}" for n, label, page in rows]
    lines.append(
        f"{len(d):<4} distinct code points, all in the Runic block U+{BLOCK[0]:04X}–U+{BLOCK[1]:04X}, all assigned"
    )
    lines.append(f"{len(GOLDEN['cases']):<4} golden cases + every Unicode scalar value, identical in JS and Python")
    return "```\n" + "\n".join(lines) + "\n```"


def input_table():
    ids = list(DATA["systems"])
    head = "| You type | " + " | ".join(DATA["systems"][i]["label"].split(" (")[0] for i in ids) + " |"
    sep = "|---|" + "---|" * len(ids)
    out = [head, sep]
    for key in list(LETTERS) + all_digraphs():
        cells = []
        for i in ids:
            t = DATA["systems"][i]
            r = two_letter(t, key) if len(key) == 2 else t["letters"][key]
            mark = "**" if len(key) == 2 and key in t["digraphs"] else ""
            cells.append(f"{mark}{r}{mark}")
        out.append(f"| `{key}` | " + " | ".join(cells) + " |")
    return "\n".join(out)


def chart(system):
    t = DATA["systems"][system]
    typed = {}
    for k, v in list(t["letters"].items()) + list(t["digraphs"].items()):
        if len(v) == 1:
            typed.setdefault(v, []).append(k)
    out = [
        "| # | Rune | Code point | Unicode name | Rune name | Decodes to | Typed as | Gloss |",
        "|---:|:---:|---|---|---|---|---|---|",
    ]
    for i, e in enumerate(t["alphabet"], 1):
        r = e["rune"]
        keys = ", ".join(f"`{k}`" for k in typed.get(r, [])) or "— *(decode only)*"
        out.append(
            f"| {i} | {r} | {cp(r)} | {unicodedata.name(r)} | {e['name']} | `{e['latin']}` | {keys} | {e['meaning']} |"
        )
    return "\n".join(out)


def sections():
    out = {"summary": summary(), "input": input_table()}
    for k in DATA["systems"]:
        out[f"chart-{k}"] = chart(k)
    return out


PAT = re.compile(r"(<!-- generated:([\w-]+) -->\n)(?:(.*?)\n)?(<!-- /generated:\2 -->)", re.S)


def render(text):
    secs = sections()
    found = set()

    def sub(m):
        found.add(m.group(2))
        return m.group(1) + secs[m.group(2)] + "\n" + m.group(4)

    new = PAT.sub(sub, text)
    missing = set(secs) - found
    return new, missing


if __name__ == "__main__":
    text = README.read_text(encoding="utf-8")
    new, missing = render(text)
    if missing:
        sys.exit(f"README.md has no marker for: {', '.join(sorted(missing))}")
    if "--write" in sys.argv:
        README.write_text(new, encoding="utf-8")
        print("README.md updated" if new != text else "README.md already up to date")
    else:
        for k, v in sections().items():
            print(f"--- {k}\n{v}\n")
