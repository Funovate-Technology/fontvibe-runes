'use strict';
/*!
 * rune-transliterator — English/Latin text to Elder Futhark, Younger Futhark
 * and Anglo-Saxon Futhorc runes, and back.
 * Code: MIT. Rune tables: CC BY 4.0 — https://fontvibe.ai/tools/rune-generator
 *
 * This is a phonetic approximation: it spells modern text in runes letter by
 * letter. It does not translate anything into Old Norse or Old English.
 */
const DATA = require('./data.js');

const SYSTEMS = Object.freeze(Object.keys(DATA.systems));
const DEFAULT_SYSTEM = DATA.default_system;
const hasOwn = (o, k) => Object.prototype.hasOwnProperty.call(o, k);

/* Unknown or misspelled system names fall back to Elder Futhark, never throw —
 * same as the site. Own-property check so names like "toString" can't resolve
 * to something off Object.prototype. */
function resolve(system) {
  const id = typeof system === 'string' && hasOwn(DATA.systems, system) ? system : DEFAULT_SYSTEM;
  return DATA.systems[id];
}

function asText(text, fn) {
  if (text == null) return '';
  if (typeof text !== 'string') throw new TypeError(fn + ': expected a string, got ' + typeof text);
  return text;
}

/**
 * Latin → runes. Longest match first (two-letter digraphs such as th / ng,
 * then single letters), case-insensitive, one Unicode code point at a time.
 * Anything without a mapping — digits, spaces, punctuation, emoji, other
 * scripts — passes through unchanged.
 */
function toRunes(text, system) {
  text = asText(text, 'toRunes');
  if (!text) return '';
  const def = resolve(system);
  const buf = Array.from(text);
  let out = '';
  let pos = 0;
  while (pos < buf.length) {
    const low = buf[pos].toLowerCase();
    if (pos + 1 < buf.length) {
      const di = low + buf[pos + 1].toLowerCase();
      if (hasOwn(def.digraphs, di)) { out += def.digraphs[di]; pos += 2; continue; }
    }
    out += hasOwn(def.letters, low) ? def.letters[low] : buf[pos];
    pos++;
  }
  return out;
}

/**
 * Runes → Latin, using each rune's primary transliteration from the chart.
 * Several letters share one rune (c/k/q, v/w …), so this is a reading aid,
 * not an exact inverse of toRunes. Non-runes pass through unchanged.
 */
function fromRunes(text, system) {
  text = asText(text, 'fromRunes');
  if (!text) return '';
  const def = resolve(system);
  const rev = Object.create(null);
  for (const e of def.alphabet) rev[e.rune] = e.latin;
  let out = '';
  for (const ch of text) out += ch in rev ? rev[ch] : ch;
  return out;
}

/** The rune chart for one system: [{rune, name, latin, meaning}], in futhark order. */
function alphabet(system) {
  return resolve(system).alphabet;
}

const RUNE_ALPHABET = {};
for (const id of SYSTEMS) RUNE_ALPHABET[id] = DATA.systems[id].alphabet;

module.exports = {
  toRunes,
  fromRunes,
  alphabet,
  RUNE_ALPHABET,
  SYSTEMS,
  DEFAULT_SYSTEM,
  data: DATA,
};
module.exports.default = module.exports;
