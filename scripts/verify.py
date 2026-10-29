#!/usr/bin/env python3
"""Check every factual claim in README.md against the data. Stdlib only.

    python scripts/verify.py            # offline checks
    python scripts/verify.py --online   # also confirm the linked FontVibe pages are up

Exit code 0 only if everything passes. JS parity needs `node` on PATH; without
it that one check is reported as SKIPPED, never as passed.
"""
import doctest
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "pypi" / "src"))

SRC = ROOT / "data" / "runes.json"
README = (ROOT / "README.md").read_text(encoding="utf-8")
DATA = json.loads(SRC.read_text(encoding="utf-8"))
GOLDEN = json.loads((ROOT / "tests" / "golden.json").read_text(encoding="utf-8"))
REPO = "https://github.com/Funovate-Technology/fontvibe-runes"
BLOCK = range(0x16A0, 0x16FF + 1)

results = []


def check(name, ok, detail=""):
    results.append((name, "PASS" if ok else "FAIL", detail))


def skip(name, why):
    results.append((name, "SKIPPED", why))


# ── 0. Generate the package copies from the single source, then load the Python port.
for cmd in (["node", "npm/scripts/sync-data.js"], [sys.executable, "pypi/scripts/sync_data.py"]):
    if cmd[0] == "node" and not shutil.which("node"):
        continue
    subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True)
import rune_transliterator as rt  # noqa: E402
import charts  # noqa: E402

copies = [ROOT / "pypi/src/rune_transliterator/runes.json"]
if shutil.which("node"):
    copies.append(ROOT / "npm/runes.json")
same = all(c.read_bytes() == SRC.read_bytes() for c in copies)
check("package copies are byte-identical to data/runes.json", same, ", ".join(str(c.relative_to(ROOT)) for c in copies))

# ── 1. Rune counts, as stated in the README summary and prose.
counts = {k: len(v["alphabet"]) for k, v in DATA["systems"].items()}
check("rune counts", counts == {"elder": 24, "younger": 16, "anglo": 32}, str(counts))
for k, v in DATA["systems"].items():
    runes = [e["rune"] for e in v["alphabet"]]
    check(f"{k}: no duplicate runes in chart", len(runes) == len(set(runes)))

# Any "<n> runes" / "<n>-rune" in README prose must be one of the real counts.
prose = re.sub(r"<!-- generated:.*?<!-- /generated:[\w-]+ -->", "", README, flags=re.S)
stated = {int(n) for n in re.findall(r"\b(\d+)[- ]runes?\b", prose)}
check("every '<n> runes' in README prose is a real count", stated <= set(counts.values()), f"stated {sorted(stated)}")
check("README: 'this table carries 32' (futhorc)", "this table carries 32" in prose and counts["anglo"] == 32)

# ── 2. Unicode facts.
distinct = charts.distinct_runes()
bad = []
for k, v in DATA["systems"].items():
    for e in v["alphabet"]:
        r = e["rune"]
        if len(r) != 1 or ord(r) not in BLOCK or unicodedata.category(r) != "Lo" or not unicodedata.name(r, ""):
            bad.append(f"{k}:{e['name']}")
check(f"all {len(distinct)} runes: one code point, in U+16A0–U+16FF, assigned (Unicode {unicodedata.unidata_version})",
      not bad, ", ".join(bad))
check("summary states the distinct code point count",
      f"{len(distinct):<4} distinct code points, all in the Runic block U+16A0–U+16FF, all assigned" in README)

# ── 3. Table consistency.
gaps, stray = [], []
for k, v in DATA["systems"].items():
    chart = {e["rune"] for e in v["alphabet"]}
    for ch in "abcdefghijklmnopqrstuvwxyz":
        if ch not in v["letters"]:
            gaps.append(f"{k}:{ch}")
    for key, out in list(v["letters"].items()) + list(v["digraphs"].items()):
        if any(r not in chart for r in out):
            stray.append(f"{k}:{key}->{out}")
check("every letter a–z has a mapping in every system", not gaps, ", ".join(gaps))
check("every rune the transliterator outputs is in that system's chart", not stray, ", ".join(stray))

# ── 4. Generated README sections are exactly what the data produces.
regen, missing = charts.render(README)
check("README summary / input table / charts match the data", regen == README and not missing,
      "run: python scripts/charts.py --write" if regen != README else "")

# ── 5. Every code example in the README produces what its comment says.
ex = 0
fails = []
pats = [
    (r"toRunes\('([^']*)'(?:, '(\w+)')?\);\s*// '([^']*)'", rt.to_runes),
    (r"fromRunes\('([^']*)'(?:, '(\w+)')?\);\s*// '([^']*)'", rt.from_runes),
    (r'rt\.to_runes\("([^"]*)"(?:, "(\w+)")?\)\s*# \'([^\']*)\'', rt.to_runes),
    (r'rt\.from_runes\("([^"]*)"(?:, "(\w+)")?\)\s*# \'([^\']*)\'', rt.from_runes),
]
for pat, fn in pats:
    for text, system, want in re.findall(pat, README):
        ex += 1
        got = fn(text, system) if system else fn(text)
        if got != want:
            fails.append(f"{fn.__name__}({text!r}, {system!r}) = {got!r}, README says {want!r}")
e3 = rt.alphabet("younger")[3]
if "alphabet('younger')[3];          // { rune: 'ᚬ', name: 'Áss', latin: 'o', meaning: 'god, Odin' }" in README:
    ex += 1
    if e3 != {"rune": "ᚬ", "name": "Áss", "latin": "o", "meaning": "god, Odin"}:
        fails.append(f"alphabet('younger')[3] = {e3}")
check(f"README code examples ({ex})", ex >= 10 and not fails, "; ".join(fails))

# Prose claims about behaviour.
prose_claims = {
    "cat and kat give the same runes": rt.to_runes("cat") == rt.to_runes("kat"),
    "thng is th + ng": rt.to_runes("thng") == DATA["systems"]["elder"]["digraphs"]["th"] + DATA["systems"]["elder"]["digraphs"]["ng"],
    "elder c, q → ᚲ; v → ᚹ; y → ᛁ; x → ᚲᛊ": [rt.to_runes(c) for c in "cqvyx"] == ["ᚲ", "ᚲ", "ᚹ", "ᛁ", "ᚲᛊ"],
    "younger k/g, t/d, b/p merge; u v w o y → ᚢ": (
        len({rt.to_runes(c, "younger") for c in "kg"}) == 1 and len({rt.to_runes(c, "younger") for c in "td"}) == 1
        and len({rt.to_runes(c, "younger") for c in "bp"}) == 1 and {rt.to_runes(c, "younger") for c in "uvwoy"} == {"ᚢ"}
    ),
    "futhorc has an ea digraph; th and ng in all systems that have a rune": (
        "ea" in DATA["systems"]["anglo"]["digraphs"]
        and all("th" in v["digraphs"] for v in DATA["systems"].values())
    ),
    "unknown system falls back to elder": rt.to_runes("thor", "nope") == rt.to_runes("thor", "elder"),
    "digits/punctuation/emoji pass through": rt.to_runes("2024! 💙") == "2024! 💙",
}
for name, ok in prose_claims.items():
    check(f"README: {name}", ok)

# ── 6. Python port == golden (recorded from the site's TypeScript implementation).
fails = []
for c in GOLDEN["cases"]:
    fn = rt.to_runes if c["fn"] == "toRunes" else rt.from_runes
    got = fn(c["input"]) if c["system"] is None else fn(c["input"], c["system"])
    if got != c["output"]:
        fails.append(f'{c["fn"]}({c["input"]!r}, {c["system"]!r})')
sha = lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest()  # noqa: E731
every = "".join(chr(cp) for cp in range(0x110000) if not 0xD800 <= cp <= 0xDFFF)
for k in rt.SYSTEMS:
    if sha(rt.to_runes(every, k)) != GOLDEN["exhaustive"][k]["toRunes"]:
        fails.append(f"exhaustive toRunes {k}")
    if sha(rt.from_runes(every, k)) != GOLDEN["exhaustive"][k]["fromRunes"]:
        fails.append(f"exhaustive fromRunes {k}")
check(f"Python == golden ({len(GOLDEN['cases'])} cases + exhaustive × {len(rt.SYSTEMS)} systems)", not fails,
      "; ".join(fails[:5]))
f, t = doctest.testmod(rt, verbose=False)
check(f"Python docstring examples ({t})", f == 0 and t > 0)

# ── 7. JS (CommonJS + ESM) == golden.
if shutil.which("node"):
    p = subprocess.run(["node", "npm/test.js"], cwd=ROOT, capture_output=True, text=True)
    check("JS (CJS + ESM) == golden", p.returncode == 0, (p.stdout or p.stderr).strip())
else:
    skip("JS (CJS + ESM) == golden", "node not on PATH")

# ── 8. Links.
gh = set(re.findall(r"https://github\.com/[\w.-]+/[\w.-]+", README))
ours = {u for u in gh if "Funovate" in u}
check("repo links use Funovate-Technology/fontvibe-runes", ours and all(u == REPO for u in ours), ", ".join(sorted(ours)))
site = set(re.findall(r"https://fontvibe\.ai/tools/[\w-]+", README))
pages = {v["page"] for v in DATA["systems"].values()}
check("site links are exactly the three rune pages", site == pages, ", ".join(sorted(site)))
first_screen = "\n".join(README.splitlines()[:12])
check("site link on the README's first screen", all(p in first_screen for p in pages))
if "--online" in sys.argv:
    for u in sorted(pages):
        try:
            req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": "fontvibe-runes-verify/1.0"})
            code = urllib.request.urlopen(req, timeout=20).status
        except Exception as e:  # noqa: BLE001
            code = str(e)
        check(f"online: {u}", code == 200, str(code))

# ── Report
w = max(len(r[0]) for r in results)
for name, status, detail in results:
    print(f"{status:<8} {name:<{w}}  {detail}".rstrip())
failed = [r for r in results if r[1] == "FAIL"]
print(f"\n{len(results) - len(failed)}/{len(results)} ok" + (f", {len(failed)} FAILED" if failed else ""))
sys.exit(1 if failed else 0)
