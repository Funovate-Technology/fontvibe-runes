# rune-transliterator

English/Latin text → **Elder Futhark**, **Younger Futhark** and **Anglo-Saxon Futhorc** runes,
and back. Real Unicode output, full rune charts, zero dependencies, ESM + CommonJS + TypeScript.

Try it live first: **[fontvibe.ai/tools/rune-generator](https://fontvibe.ai/tools/rune-generator)** ·
[Younger Futhark](https://fontvibe.ai/tools/younger-futhark-translator) ·
[Anglo-Saxon runes](https://fontvibe.ai/tools/anglo-saxon-runes). This package is the same
engine and tables, verified against golden output recorded from the site.

```bash
npm i rune-transliterator
```

```js
import { toRunes, fromRunes, alphabet } from 'rune-transliterator';

toRunes('Thor');               // 'ᚦᛟᚱ'      th → one rune
toRunes('Viking');             // 'ᚹᛁᚲᛁᛜ'    ng → one rune
toRunes('Viking', 'younger');  // 'ᚢᛁᚴᛁᚾᚴ'
toRunes('earth', 'anglo');     // 'ᛠᚱᚦ'
fromRunes('ᚦᛟᚱ');              // 'thor'
alphabet('elder');             // [{ rune: 'ᚠ', name: 'Fehu', latin: 'f', meaning: 'wealth, cattle' }, …]
```

In the browser, straight from a CDN:

```html
<script type="module">
  import { toRunes } from 'https://cdn.jsdelivr.net/npm/rune-transliterator@1/index.mjs';
</script>
```

CLI:

```bash
npx rune-transliterator -s younger "Ragnar Lothbrok"
npx rune-transliterator --decode ᚦᛟᚱ
npx rune-transliterator --chart -s anglo
```

The raw tables are exported too: `require('rune-transliterator/runes.json')`.

> **Phonetic approximation, not a translation.** It spells modern text in runes letter by letter;
> it does not produce Old Norse or Old English. Check results against the charts before engraving
> or tattooing anything.

Full rune charts with code points, the exact rules, and how to verify everything:
**[github.com/Funovate-Technology/fontvibe-runes](https://github.com/Funovate-Technology/fontvibe-runes)**

## Attribution

Code: MIT. Rune tables: CC BY 4.0. If you use the tables, please credit — and link the site, not
just the package:

```html
Rune tables from <a href="https://fontvibe.ai/tools/rune-generator">FontVibe's rune translator</a> ·
<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>
```

`rel="nofollow"` is fine. Plain text is fine where a link isn't practical:
`Rune tables from FontVibe — https://fontvibe.ai/tools/rune-generator — CC BY 4.0`
