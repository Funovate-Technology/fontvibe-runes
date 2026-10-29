#!/usr/bin/env node
// Builds data.js (CommonJS), data.mjs (ESM) and a copy of runes.json from ../data/runes.json.
// data/runes.json at the repo root is the single source of truth for both the
// npm and the PyPI package; these two files are generated and never committed.
'use strict';
const fs = require('fs');
const path = require('path');

const src = path.join(__dirname, '..', '..', 'data', 'runes.json');
if (!fs.existsSync(src)) {
  console.error('[sync-data] missing ' + src + ' — run this from inside the repo');
  process.exit(1);
}
const raw = fs.readFileSync(src, 'utf8');
const data = JSON.parse(raw); // fail loudly on a broken table
for (const id of Object.keys(data.systems)) {
  if (!data.systems[id].alphabet.length) {
    console.error('[sync-data] system ' + id + ' has an empty alphabet — refusing');
    process.exit(1);
  }
}
const body = JSON.stringify(data);
const banner = '// Generated from data/runes.json by scripts/sync-data.js — do not edit.\n' +
  '// Rune tables © FontVibe, CC BY 4.0 — https://fontvibe.ai/tools/rune-generator\n';
const out = path.join(__dirname, '..');
fs.writeFileSync(path.join(out, 'data.js'), banner + "'use strict';\nmodule.exports = " + body + ';\n');
fs.writeFileSync(path.join(out, 'data.mjs'), banner + 'export default ' + body + ';\n');
// The raw table too, for anyone who wants it without the code (require('rune-transliterator/runes.json')).
fs.copyFileSync(src, path.join(out, 'runes.json'));
console.log('[sync-data] ok — ' + Object.keys(data.systems).join(', '));
