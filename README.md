# Rune transliterator

**English (or any Latin-alphabet) text → Elder Futhark, Younger Futhark and Anglo-Saxon Futhorc
runes, and back — with the full rune charts, so you can check every letter yourself.**

Try it in the browser, no install: **[Elder Futhark](https://fontvibe.ai/tools/rune-generator)** ·
**[Younger Futhark / Viking runes](https://fontvibe.ai/tools/younger-futhark-translator)** ·
**[Anglo-Saxon futhorc](https://fontvibe.ai/tools/anglo-saxon-runes)** — type, copy, paste.
This repo is the engine and the tables behind those three pages: the same mapping, and
[golden tests recorded from the site's own implementation](#verify-it-yourself) to prove it.

<!-- generated:summary -->
```
24   Elder Futhark runes                  → fontvibe.ai/tools/rune-generator
16   Younger Futhark (long-branch) runes  → fontvibe.ai/tools/younger-futhark-translator
32   Anglo-Saxon Futhorc runes            → fontvibe.ai/tools/anglo-saxon-runes
44   distinct code points, all in the Runic block U+16A0–U+16FF, all assigned
340  golden cases + every Unicode scalar value, identical in JS and Python
```
<!-- /generated:summary -->

```bash
npm i rune-transliterator        # or: npx rune-transliterator -s younger "Ragnar Lothbrok"
pip install rune-transliterator  # or: python -m rune_transliterator -s anglo Beowulf
```

Zero dependencies in both. Output is real Unicode text, not a font or an image — it copies into
Instagram, Discord, a game's chat, a Word document or a tattoo stencil.

> **Before you engrave or tattoo anything:** this is a **phonetic approximation**. It spells
> *modern* text in runes, letter by letter. It does **not** translate into Old Norse or Old
> English, and it is not how a Viking would have written your name — real inscriptions varied
> by region and century, and spelled by sound. That is why the [full charts](#rune-charts) are
> below: read your result back rune by rune and adjust it.

---

## Quick start

```js
import { toRunes, fromRunes, alphabet } from 'rune-transliterator';

toRunes('Thor');                 // 'ᚦᛟᚱ'      th is one rune (Thurisaz)
toRunes('Viking');               // 'ᚹᛁᚲᛁᛜ'    ng is one rune (Ingwaz)
toRunes('Viking', 'younger');    // 'ᚢᛁᚴᛁᚾᚴ'   16 runes, so v/w/u and k/g merge
toRunes('earth', 'anglo');       // 'ᛠᚱᚦ'      the futhorc has a rune for ea
toRunes('thor 2024!');           // 'ᚦᛟᚱ 2024!' anything unmapped passes through

fromRunes('ᚦᛟᚱ');                // 'thor'
alphabet('younger')[3];          // { rune: 'ᚬ', name: 'Áss', latin: 'o', meaning: 'god, Odin' }
```

CommonJS (`require('rune-transliterator')`) and TypeScript types work too. The ESM build has no
imports beyond its own data module, so it runs straight from a CDN in a plain `<script type="module">`:

```html
<script type="module">
  import { toRunes } from 'https://cdn.jsdelivr.net/npm/rune-transliterator@1/index.mjs';
  document.querySelector('#out').textContent = toRunes('Freya');
</script>
```

```python
import rune_transliterator as rt

rt.to_runes("Thor")               # 'ᚦᛟᚱ'
rt.to_runes("Beowulf", "anglo")   # 'ᛒᛖᚩᚹᚢᛚᚠ'
rt.from_runes("ᚱᛅᚴᚾᛅᚱ", "younger")  # 'raknar' — g and k share a rune
rt.alphabet("elder")              # the 24-rune chart as a list of dicts
```

```bash
npx rune-transliterator -s younger "Ragnar Lothbrok"
npx rune-transliterator --decode ᚦᛟᚱ
npx rune-transliterator --chart -s anglo          # print a chart with code points
```

Systems: `elder` (default), `younger`, `anglo`. An unknown system name falls back to Elder Futhark
instead of throwing, the same as the site.

**Fonts.** Runes need a font that covers the Runic block. Most current desktop and phone systems
have one; some older Android devices don't and show boxes ("tofu"). If you control the page,
ship a web font such as Noto Sans Runic.

## What it does, exactly

Four rules, nothing hidden:

1. **Case-insensitive**, one Unicode code point at a time.
2. **Digraphs first.** `th` and `ng` become single runes in every system that has a rune for them;
   the futhorc also has one for `ea`. A digraph wins over the letters inside it, scanning left to
   right — so `thng` is `th` + `ng`, never `t` + `hn` + `g`.
3. **Then single letters**, by the table below. Letters a system has no rune for go to the nearest
   sound: in Elder Futhark `c` and `q` become Kaunan (ᚲ), `v` becomes Wunjo (ᚹ), `y` becomes Isaz
   (ᛁ), and `x` becomes two runes, ᚲᛊ.
4. **Everything else passes through untouched** — digits, spaces, punctuation, emoji, accented
   letters, other scripts. Nothing is dropped.

Decoding (`fromRunes`) maps each rune to its primary Latin value from the chart. Because several
letters share one rune, decoding is a reading aid, not an exact inverse: `toRunes('cat')` and
`toRunes('kat')` are the same runes.

### Input → rune

Bold = a digraph rune. Without a digraph rune, two letters are simply written one after the other.

<!-- generated:input -->
| You type | Elder Futhark | Younger Futhark | Anglo-Saxon Futhorc |
|---|---|---|---|
| `a` | ᚨ | ᛅ | ᚪ |
| `b` | ᛒ | ᛒ | ᛒ |
| `c` | ᚲ | ᚴ | ᚳ |
| `d` | ᛞ | ᛏ | ᛞ |
| `e` | ᛖ | ᛁ | ᛖ |
| `f` | ᚠ | ᚠ | ᚠ |
| `g` | ᚷ | ᚴ | ᚷ |
| `h` | ᚺ | ᚼ | ᚻ |
| `i` | ᛁ | ᛁ | ᛁ |
| `j` | ᛃ | ᛁ | ᛄ |
| `k` | ᚲ | ᚴ | ᚳ |
| `l` | ᛚ | ᛚ | ᛚ |
| `m` | ᛗ | ᛘ | ᛗ |
| `n` | ᚾ | ᚾ | ᚾ |
| `o` | ᛟ | ᚢ | ᚩ |
| `p` | ᛈ | ᛒ | ᛈ |
| `q` | ᚲ | ᚴ | ᚳ |
| `r` | ᚱ | ᚱ | ᚱ |
| `s` | ᛊ | ᛋ | ᛋ |
| `t` | ᛏ | ᛏ | ᛏ |
| `u` | ᚢ | ᚢ | ᚢ |
| `v` | ᚹ | ᚢ | ᚠ |
| `w` | ᚹ | ᚢ | ᚹ |
| `x` | ᚲᛊ | ᚴᛋ | ᛉ |
| `y` | ᛁ | ᚢ | ᚣ |
| `z` | ᛉ | ᛋ | ᛋ |
| `th` | **ᚦ** | **ᚦ** | **ᚦ** |
| `ng` | **ᛜ** | ᚾᚴ | **ᛝ** |
| `ea` | ᛖᚨ | ᛁᛅ | **ᛠ** |
<!-- /generated:input -->

## Rune charts

Code points and Unicode character names below are generated from Python's `unicodedata`
([`scripts/charts.py`](scripts/charts.py)), not typed by hand.

- **Decodes to** is what `fromRunes` returns for the rune.
- **Typed as** lists the input that produces it. *Decode only* means no Latin input produces that
  rune — it is in the chart so that existing runic text decodes, and so you can swap it in by hand.
- **Gloss** is the conventional meaning of the rune's *name*, at the level found in popular
  references. Treat it as a label, not scholarship: the Elder Futhark names are not attested
  directly (they are reconstructed, largely from later rune poems), and some — Perth/Peorð above
  all — have no agreed meaning.

### Elder Futhark

The oldest runic alphabet, used roughly from the 2nd to the 8th century — older than the Viking
Age. Three groups (ættir) of eight. Live tool: [fontvibe.ai/tools/rune-generator](https://fontvibe.ai/tools/rune-generator)

<!-- generated:chart-elder -->
| # | Rune | Code point | Unicode name | Rune name | Decodes to | Typed as | Gloss |
|---:|:---:|---|---|---|---|---|---|
| 1 | ᚠ | U+16A0 | RUNIC LETTER FEHU FEOH FE F | Fehu | `f` | `f` | wealth, cattle |
| 2 | ᚢ | U+16A2 | RUNIC LETTER URUZ UR U | Uruz | `u` | `u` | strength, aurochs |
| 3 | ᚦ | U+16A6 | RUNIC LETTER THURISAZ THURS THORN | Thurisaz | `th` | `th` | giant, thorn |
| 4 | ᚨ | U+16A8 | RUNIC LETTER ANSUZ A | Ansuz | `a` | `a` | god, Odin |
| 5 | ᚱ | U+16B1 | RUNIC LETTER RAIDO RAD REID R | Raido | `r` | `r` | ride, journey |
| 6 | ᚲ | U+16B2 | RUNIC LETTER KAUNA | Kaunan | `k` | `c`, `k`, `q` | torch, fire |
| 7 | ᚷ | U+16B7 | RUNIC LETTER GEBO GYFU G | Gebo | `g` | `g` | gift |
| 8 | ᚹ | U+16B9 | RUNIC LETTER WUNJO WYNN W | Wunjo | `w` | `v`, `w` | joy |
| 9 | ᚺ | U+16BA | RUNIC LETTER HAGLAZ H | Hagalaz | `h` | `h` | hail |
| 10 | ᚾ | U+16BE | RUNIC LETTER NAUDIZ NYD NAUD N | Naudiz | `n` | `n` | need |
| 11 | ᛁ | U+16C1 | RUNIC LETTER ISAZ IS ISS I | Isaz | `i` | `i`, `y` | ice |
| 12 | ᛃ | U+16C3 | RUNIC LETTER JERAN J | Jera | `j` | `j` | year, harvest |
| 13 | ᛇ | U+16C7 | RUNIC LETTER IWAZ EOH | Eihwaz | `ei` | — *(decode only)* | yew tree |
| 14 | ᛈ | U+16C8 | RUNIC LETTER PERTHO PEORTH P | Perth | `p` | `p` | fate, mystery |
| 15 | ᛉ | U+16C9 | RUNIC LETTER ALGIZ EOLHX | Algiz | `z` | `z` | protection, elk |
| 16 | ᛊ | U+16CA | RUNIC LETTER SOWILO S | Sowilo | `s` | `s` | sun |
| 17 | ᛏ | U+16CF | RUNIC LETTER TIWAZ TIR TYR T | Tiwaz | `t` | `t` | Tyr, victory |
| 18 | ᛒ | U+16D2 | RUNIC LETTER BERKANAN BEORC BJARKAN B | Berkanan | `b` | `b` | birch, growth |
| 19 | ᛖ | U+16D6 | RUNIC LETTER EHWAZ EH E | Ehwaz | `e` | `e` | horse |
| 20 | ᛗ | U+16D7 | RUNIC LETTER MANNAZ MAN M | Mannaz | `m` | `m` | man, humanity |
| 21 | ᛚ | U+16DA | RUNIC LETTER LAUKAZ LAGU LOGR L | Laguz | `l` | `l` | water, lake |
| 22 | ᛜ | U+16DC | RUNIC LETTER INGWAZ | Ingwaz | `ng` | `ng` | Ing, fertility |
| 23 | ᛞ | U+16DE | RUNIC LETTER DAGAZ DAEG D | Dagaz | `d` | `d` | day, dawn |
| 24 | ᛟ | U+16DF | RUNIC LETTER OTHALAN ETHEL O | Othala | `o` | `o` | heritage, estate |
<!-- /generated:chart-elder -->

### Younger Futhark (long-branch)

The Viking-Age alphabet of Scandinavia, cut down to 16 runes, so many sounds share one rune:
k/g, t/d and b/p merge, and u, v, w, o and y all use Úr. This is the long-branch row; the
short-twig variants are not included. Live tool:
[fontvibe.ai/tools/younger-futhark-translator](https://fontvibe.ai/tools/younger-futhark-translator)

<!-- generated:chart-younger -->
| # | Rune | Code point | Unicode name | Rune name | Decodes to | Typed as | Gloss |
|---:|:---:|---|---|---|---|---|---|
| 1 | ᚠ | U+16A0 | RUNIC LETTER FEHU FEOH FE F | Fé | `f` | `f` | wealth |
| 2 | ᚢ | U+16A2 | RUNIC LETTER URUZ UR U | Úr | `u` | `o`, `u`, `v`, `w`, `y` | iron, rain |
| 3 | ᚦ | U+16A6 | RUNIC LETTER THURISAZ THURS THORN | Þurs | `th` | `th` | giant |
| 4 | ᚬ | U+16AC | RUNIC LETTER LONG-BRANCH-OSS O | Áss | `o` | — *(decode only)* | god, Odin |
| 5 | ᚱ | U+16B1 | RUNIC LETTER RAIDO RAD REID R | Reið | `r` | `r` | ride, journey |
| 6 | ᚴ | U+16B4 | RUNIC LETTER KAUN K | Kaun | `k` | `c`, `g`, `k`, `q` | sore, torch |
| 7 | ᚼ | U+16BC | RUNIC LETTER LONG-BRANCH-HAGALL H | Hagall | `h` | `h` | hail |
| 8 | ᚾ | U+16BE | RUNIC LETTER NAUDIZ NYD NAUD N | Nauðr | `n` | `n` | need |
| 9 | ᛁ | U+16C1 | RUNIC LETTER ISAZ IS ISS I | Íss | `i` | `e`, `i`, `j` | ice |
| 10 | ᛅ | U+16C5 | RUNIC LETTER LONG-BRANCH-AR AE | Ár | `a` | `a` | harvest, plenty |
| 11 | ᛋ | U+16CB | RUNIC LETTER SIGEL LONG-BRANCH-SOL S | Sól | `s` | `s`, `z` | sun |
| 12 | ᛏ | U+16CF | RUNIC LETTER TIWAZ TIR TYR T | Týr | `t` | `d`, `t` | the god Tyr |
| 13 | ᛒ | U+16D2 | RUNIC LETTER BERKANAN BEORC BJARKAN B | Bjǫrk | `b` | `b`, `p` | birch |
| 14 | ᛘ | U+16D8 | RUNIC LETTER LONG-BRANCH-MADR M | Maðr | `m` | `m` | man |
| 15 | ᛚ | U+16DA | RUNIC LETTER LAUKAZ LAGU LOGR L | Lǫgr | `l` | `l` | water, sea |
| 16 | ᛦ | U+16E6 | RUNIC LETTER LONG-BRANCH-YR | Ýr | `z` | — *(decode only)* | yew, final -R |
<!-- /generated:chart-younger -->

### Anglo-Saxon Futhorc

Used in early medieval England and Frisia to write Old English. Where Scandinavia dropped runes,
the futhorc *added* them — ac, æsc, os, yr, ear and later runes such as cweorð, calc, gar and
stan. Historical lists vary by period and source; this table carries 32. Live tool:
[fontvibe.ai/tools/anglo-saxon-runes](https://fontvibe.ai/tools/anglo-saxon-runes)

<!-- generated:chart-anglo -->
| # | Rune | Code point | Unicode name | Rune name | Decodes to | Typed as | Gloss |
|---:|:---:|---|---|---|---|---|---|
| 1 | ᚠ | U+16A0 | RUNIC LETTER FEHU FEOH FE F | Feoh | `f` | `f`, `v` | wealth |
| 2 | ᚢ | U+16A2 | RUNIC LETTER URUZ UR U | Ur | `u` | `u` | aurochs |
| 3 | ᚦ | U+16A6 | RUNIC LETTER THURISAZ THURS THORN | Thorn | `th` | `th` | thorn, giant |
| 4 | ᚩ | U+16A9 | RUNIC LETTER OS O | Os | `o` | `o` | god, mouth |
| 5 | ᚱ | U+16B1 | RUNIC LETTER RAIDO RAD REID R | Rad | `r` | `r` | riding |
| 6 | ᚳ | U+16B3 | RUNIC LETTER CEN | Cen | `c` | `c`, `k`, `q` | torch |
| 7 | ᚷ | U+16B7 | RUNIC LETTER GEBO GYFU G | Gyfu | `g` | `g` | gift |
| 8 | ᚹ | U+16B9 | RUNIC LETTER WUNJO WYNN W | Wynn | `w` | `w` | joy |
| 9 | ᚻ | U+16BB | RUNIC LETTER HAEGL H | Hægl | `h` | `h` | hail |
| 10 | ᚾ | U+16BE | RUNIC LETTER NAUDIZ NYD NAUD N | Nyd | `n` | `n` | need |
| 11 | ᛁ | U+16C1 | RUNIC LETTER ISAZ IS ISS I | Is | `i` | `i` | ice |
| 12 | ᛄ | U+16C4 | RUNIC LETTER GER | Ger | `j` | `j` | year, harvest |
| 13 | ᛇ | U+16C7 | RUNIC LETTER IWAZ EOH | Eoh | `ï` | — *(decode only)* | yew |
| 14 | ᛈ | U+16C8 | RUNIC LETTER PERTHO PEORTH P | Peorð | `p` | `p` | game, fate |
| 15 | ᛉ | U+16C9 | RUNIC LETTER ALGIZ EOLHX | Eolh | `x` | `x` | elk-sedge |
| 16 | ᛋ | U+16CB | RUNIC LETTER SIGEL LONG-BRANCH-SOL S | Sigel | `s` | `s`, `z` | sun |
| 17 | ᛏ | U+16CF | RUNIC LETTER TIWAZ TIR TYR T | Tir | `t` | `t` | the god Tiw |
| 18 | ᛒ | U+16D2 | RUNIC LETTER BERKANAN BEORC BJARKAN B | Beorc | `b` | `b` | birch |
| 19 | ᛖ | U+16D6 | RUNIC LETTER EHWAZ EH E | Eh | `e` | `e` | horse |
| 20 | ᛗ | U+16D7 | RUNIC LETTER MANNAZ MAN M | Mann | `m` | `m` | man |
| 21 | ᛚ | U+16DA | RUNIC LETTER LAUKAZ LAGU LOGR L | Lagu | `l` | `l` | water, lake |
| 22 | ᛝ | U+16DD | RUNIC LETTER ING | Ing | `ng` | `ng` | the hero Ing |
| 23 | ᛞ | U+16DE | RUNIC LETTER DAGAZ DAEG D | Dæg | `d` | `d` | day |
| 24 | ᛟ | U+16DF | RUNIC LETTER OTHALAN ETHEL O | Ethel | `œ` | — *(decode only)* | estate, homeland |
| 25 | ᚪ | U+16AA | RUNIC LETTER AC A | Ac | `a` | `a` | oak |
| 26 | ᚫ | U+16AB | RUNIC LETTER AESC | Æsc | `æ` | — *(decode only)* | ash tree |
| 27 | ᚣ | U+16A3 | RUNIC LETTER YR | Yr | `y` | `y` | bow |
| 28 | ᛠ | U+16E0 | RUNIC LETTER EAR | Ear | `ea` | `ea` | grave, earth |
| 29 | ᛢ | U+16E2 | RUNIC LETTER CWEORTH | Cweorð | `q` | — *(decode only)* | fire-drill |
| 30 | ᛣ | U+16E3 | RUNIC LETTER CALC | Calc | `k` | — *(decode only)* | chalice |
| 31 | ᚸ | U+16B8 | RUNIC LETTER GAR | Gar | `g` | — *(decode only)* | spear |
| 32 | ᛥ | U+16E5 | RUNIC LETTER STAN | Stan | `st` | — *(decode only)* | stone |
<!-- /generated:chart-anglo -->

## Use the tables from any language

[`data/runes.json`](data/runes.json) is the single source of truth — the npm and PyPI packages
are both generated from it, and it is small enough to read in one sitting. If you're writing a
Go, Rust, Swift, PHP or Lua version, port the four rules above and load this file:

```jsonc
{
  "default_system": "elder",
  "systems": {
    "elder": {
      "label": "Elder Futhark",
      "page": "https://fontvibe.ai/tools/rune-generator",
      "alphabet": [ { "rune": "ᚠ", "name": "Fehu", "latin": "f", "meaning": "wealth, cattle" }, … ],
      "letters":  { "a": "ᚨ", "b": "ᛒ", … },   // single lowercase letter → rune(s)
      "digraphs": { "th": "ᚦ", "ng": "ᛜ" }     // matched before single letters
    },
    "younger": { … }, "anglo": { … }
  }
}
```

Then run your port against [`tests/golden.json`](tests/golden.json): every case must match byte
for byte, and the `exhaustive` hashes cover every Unicode code point.

## Verify it yourself

```bash
python scripts/verify.py      # stdlib only
```

It checks every factual claim in this README against the data, rather than trusting it:

- the rune count of each system, and that the charts and tables above are exactly what the data
  produces;
- every rune is a single code point inside the Runic block (U+16A0–U+16FF) and is an assigned
  character, per `unicodedata`;
- every rune the transliterator can output appears in that system's chart, and every letter a–z
  has a mapping in every system;
- the Python package reproduces all of `tests/golden.json`, and — if Node is installed — so do
  both the CommonJS and the ESM builds of the npm package. The golden set was recorded from the
  TypeScript implementation that runs on fontvibe.ai, so passing means *same output as the site*.

## How this differs from other rune libraries

[**riimut**](https://github.com/stscoundrel/riimut) (and its single-alphabet siblings
`elder-futhark`, `younger-futhark`, `futhorc` on npm) is the established choice, and it covers
more ground: short-twig and staveless Younger Futhark, medieval futhork, and Old Norse
orthography like `þ`, `ð` and `ǫ` as input. **If you are transcribing real Old Norse or
Proto-Norse text, use riimut.**

This one is built for a different input — a modern English name, word or motto — and for people
building on top of it:

- **English digraphs.** `th`, `ng` (and `ea` in the futhorc) become the single runes a reader
  expects, and modern letters with no rune (`c`, `q`, `v`, `x`, `y`) map to the closest sound.
- **The data is the product.** One JSON table with rune names, glosses and code points, CC BY,
  usable from any language — not mappings buried in code.
- **Same output in JS, Python and on the website**, enforced by a shared golden set that covers
  every Unicode code point, not just the alphabet.
- **Charts shipped with it**, so your users can check a result instead of trusting it.

## Attribution

The code is MIT. The rune tables (`data/runes.json`) are **CC BY 4.0**, which asks you to credit
the source "in any reasonable manner requested by the licensor". Here's what we ask for — copy
whichever fits, and point it at whichever alphabet you use:

**Markdown**
```markdown
Rune tables from [FontVibe's rune translator](https://fontvibe.ai/tools/rune-generator) ·
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
```

**HTML**
```html
Rune tables from <a href="https://fontvibe.ai/tools/rune-generator">FontVibe's rune translator</a> ·
<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>
```

**Plain text** (for a CLI, a NOTICE file, an app's about screen, a print)
```
Rune tables from FontVibe — https://fontvibe.ai/tools/rune-generator — CC BY 4.0
```

Using only one alphabet? Link its own page instead:
[Younger Futhark](https://fontvibe.ai/tools/younger-futhark-translator) ·
[Anglo-Saxon futhorc](https://fontvibe.ai/tools/anglo-saxon-runes).

A few things worth saying plainly:

- **Add `rel="nofollow"` if you prefer.** It's your page; we're not asking you to pass ranking
  signals, and we'd rather you credit us with a nofollow link than not credit us at all.
- **A link is not strictly required** — CC BY's exact words are "to the extent reasonably
  practicable". On a tattoo, a printed piece or in a terminal, plain text is fine (and on the
  tattoo itself, please don't).
- **Please link the site, not just this repo.** The pages are where your users can actually try
  a name, compare the three alphabets and copy the result; the repo is the engine behind them.
- Using only the MIT code with your own tables? Then no attribution is needed beyond keeping the
  MIT notice.

## Citing it

There's a [`CITATION.cff`](CITATION.cff), so GitHub's "Cite this repository" button works.

```bibtex
@misc{fontvibe_runes,
  title        = {FontVibe Rune Transliterator: Elder Futhark, Younger Futhark and Anglo-Saxon Futhorc tables},
  author       = {{FontVibe}},
  year         = {2026},
  version      = {1.0.0},
  howpublished = {\url{https://fontvibe.ai/tools/rune-generator}},
  note         = {Phonetic Latin-to-rune transliteration. Code MIT, tables CC BY 4.0}
}
```

## License

- **Code** (`npm/`, `pypi/`, `scripts/`): [MIT](LICENSE).
- **Rune tables** (`data/runes.json`, and the copies generated from it inside both packages):
  [CC BY 4.0](LICENSE-DATA). See [NOTICE](NOTICE).

The runes themselves are, of course, nobody's: they are an alphabet in use for well over a
thousand years, and encoded in Unicode's Runic block. What's licensed here is the specific
mapping, naming and glossing work in the tables.

## Contributing

Think a mapping is wrong, or a gloss overstates what's known? [Open an
issue](https://github.com/Funovate-Technology/fontvibe-runes/issues/new) — ideally with a source.
Changes go into `data/runes.json` and the site together, so the library and the live tool never
disagree; `tests/golden.json` is regenerated from the site's implementation when they do.

---

Built and maintained by [FontVibe](https://fontvibe.ai). Live tools:
[Elder Futhark rune translator](https://fontvibe.ai/tools/rune-generator) ·
[Younger Futhark / Viking runes](https://fontvibe.ai/tools/younger-futhark-translator) ·
[Anglo-Saxon runes (futhorc)](https://fontvibe.ai/tools/anglo-saxon-runes).
