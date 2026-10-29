/*!
 * rune-transliterator — English/Latin text to Elder Futhark, Younger Futhark
 * and Anglo-Saxon Futhorc runes, and back.
 * Code: MIT. Rune tables: CC BY 4.0 — https://fontvibe.ai/tools/rune-generator
 *
 * Pure ESM with no imports beyond its own data module, so it also runs
 * directly in a browser from a CDN. Logic is identical to index.js;
 * test.js runs the golden set against both.
 */
import DATA from './data.mjs';

export const SYSTEMS = Object.freeze(Object.keys(DATA.systems));
export const DEFAULT_SYSTEM = DATA.default_system;
const hasOwn = (o, k) => Object.prototype.hasOwnProperty.call(o, k);

function resolve(system) {
  const id = typeof system === 'string' && hasOwn(DATA.systems, system) ? system : DEFAULT_SYSTEM;
  return DATA.systems[id];
}

function asText(text, fn) {
  if (text == null) return '';
  if (typeof text !== 'string') throw new TypeError(fn + ': expected a string, got ' + typeof text);
  return text;
}

export function toRunes(text, system) {
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

export function fromRunes(text, system) {
  text = asText(text, 'fromRunes');
  if (!text) return '';
  const def = resolve(system);
  const rev = Object.create(null);
  for (const e of def.alphabet) rev[e.rune] = e.latin;
  let out = '';
  for (const ch of text) out += ch in rev ? rev[ch] : ch;
  return out;
}

export function alphabet(system) {
  return resolve(system).alphabet;
}

export const RUNE_ALPHABET = {};
for (const id of SYSTEMS) RUNE_ALPHABET[id] = DATA.systems[id].alphabet;

export const data = DATA;

export default { toRunes, fromRunes, alphabet, RUNE_ALPHABET, SYSTEMS, DEFAULT_SYSTEM, data };
