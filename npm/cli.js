#!/usr/bin/env node
'use strict';
const runes = require('./index.js');

const HELP = `Usage: rune-transliterator [options] <text...>

  -s, --system <id>   elder (default), younger, anglo
  -d, --decode        runes → Latin instead of Latin → runes
  -c, --chart         print the rune chart for the system
  -h, --help

Reads stdin when no text is given.
Phonetic approximation, not a translation into Old Norse or Old English.
Charts and live tool: https://fontvibe.ai/tools/rune-generator`;

const args = process.argv.slice(2);
let system = runes.DEFAULT_SYSTEM;
let decode = false;
let chart = false;
const words = [];
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === '-h' || a === '--help') { console.log(HELP); process.exit(0); }
  else if (a === '-d' || a === '--decode') decode = true;
  else if (a === '-c' || a === '--chart') chart = true;
  else if (a === '-s' || a === '--system') system = args[++i];
  else if (a.startsWith('--system=')) system = a.slice(9);
  else words.push(a);
}
if (!runes.SYSTEMS.includes(system)) {
  console.error(`unknown system "${system}" — use one of: ${runes.SYSTEMS.join(', ')}`);
  process.exit(2);
}

if (chart) {
  for (const e of runes.alphabet(system)) {
    const cp = 'U+' + e.rune.codePointAt(0).toString(16).toUpperCase();
    console.log(`${e.rune}  ${cp}  ${e.latin.padEnd(3)}  ${e.name.padEnd(9)}  ${e.meaning}`);
  }
  process.exit(0);
}

const convert = (t) => (decode ? runes.fromRunes(t, system) : runes.toRunes(t, system));
if (words.length) {
  console.log(convert(words.join(' ')));
} else if (!process.stdin.isTTY) {
  let buf = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (c) => { buf += c; });
  process.stdin.on('end', () => process.stdout.write(convert(buf)));
} else {
  console.log(HELP);
  process.exit(2);
}
