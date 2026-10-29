# rune-transliterator

English/Latin text → **Elder Futhark**, **Younger Futhark** and **Anglo-Saxon Futhorc** runes,
and back. Real Unicode output, full rune charts, no dependencies, typed.

Try it live first: **[fontvibe.ai/tools/rune-generator](https://fontvibe.ai/tools/rune-generator)** ·
[Younger Futhark](https://fontvibe.ai/tools/younger-futhark-translator) ·
[Anglo-Saxon runes](https://fontvibe.ai/tools/anglo-saxon-runes). This package is the same
engine and tables, verified against golden output recorded from the site.

```bash
pip install rune-transliterator
```

```python
import rune_transliterator as rt

rt.to_runes("Thor")                 # 'ᚦᛟᚱ'      th → one rune
rt.to_runes("Viking", "younger")    # 'ᚢᛁᚴᛁᚾᚴ'
rt.to_runes("earth", "anglo")       # 'ᛠᚱᚦ'
rt.from_runes("ᚦᛟᚱ")                # 'thor'
rt.alphabet("elder")[0]             # {'rune': 'ᚠ', 'name': 'Fehu', 'latin': 'f', 'meaning': 'wealth, cattle'}
rt.DATA                             # the raw tables
```

```bash
python -m rune_transliterator -s younger "Ragnar Lothbrok"
python -m rune_transliterator --decode ᚦᛟᚱ
python -m rune_transliterator --chart -s anglo
```

> **Phonetic approximation, not a translation.** It spells modern text in runes letter by letter;
> it does not produce Old Norse or Old English. Check results against the charts before engraving
> or tattooing anything.

Full rune charts with code points, the exact rules, and how to verify everything:
**[github.com/Funovate-Technology/fontvibe-runes](https://github.com/Funovate-Technology/fontvibe-runes)**

## Attribution

Code: MIT. Rune tables: CC BY 4.0. If you use the tables, please credit — and link the site, not
just the package:

```markdown
Rune tables from [FontVibe's rune translator](https://fontvibe.ai/tools/rune-generator) ·
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
```

`rel="nofollow"` is fine. Plain text is fine where a link isn't practical:
`Rune tables from FontVibe — https://fontvibe.ai/tools/rune-generator — CC BY 4.0`
