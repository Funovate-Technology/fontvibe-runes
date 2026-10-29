#!/usr/bin/env node
// Golden tests: every case recorded from FontVibe's production implementation
// must come out byte-identical from both the CommonJS and the ESM build.
'use strict';
const assert = require('assert');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const golden = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'tests', 'golden.json'), 'utf8'));
const sha = (s) => crypto.createHash('sha256').update(Buffer.from(s, 'utf8')).digest('hex');

function everyScalar() {
  let s = '';
  for (let cp = 0; cp <= 0x10ffff; cp++) {
    if (cp >= 0xd800 && cp <= 0xdfff) continue;
    s += String.fromCodePoint(cp);
  }
  return s;
}

function run(label, lib) {
  let n = 0;
  for (const c of golden.cases) {
    const got = c.system === null ? lib[c.fn](c.input) : lib[c.fn](c.input, c.system);
    assert.strictEqual(got, c.output, `${label} ${c.fn}(${JSON.stringify(c.input)}, ${c.system})`);
    n++;
  }
  const all = everyScalar();
  assert.strictEqual(sha(all), golden.exhaustive.input_sha256, 'exhaustive input differs');
  for (const id of lib.SYSTEMS) {
    assert.strictEqual(sha(lib.toRunes(all, id)), golden.exhaustive[id].toRunes, `${label} exhaustive toRunes ${id}`);
    assert.strictEqual(sha(lib.fromRunes(all, id)), golden.exhaustive[id].fromRunes, `${label} exhaustive fromRunes ${id}`);
    n += 2;
  }

  // Contract checks beyond the golden set.
  assert.deepStrictEqual([...lib.SYSTEMS], ['elder', 'younger', 'anglo']);
  assert.strictEqual(lib.toRunes(undefined), '');
  assert.strictEqual(lib.toRunes(null, 'anglo'), '');
  assert.throws(() => lib.toRunes(42), TypeError);
  assert.strictEqual(lib.toRunes('thor', 'toString'), 'ᚦᛟᚱ'); // prototype names fall back too
  assert.strictEqual(lib.alphabet('younger').length, 16);
  assert.strictEqual(lib.RUNE_ALPHABET.anglo, lib.alphabet('anglo'));
  return n;
}

(async () => {
  const cjs = require('./index.js');
  const esm = await import('./index.mjs');
  const a = run('cjs', cjs);
  const b = run('esm', esm);
  assert.strictEqual(esm.default.toRunes('viking'), 'ᚹᛁᚲᛁᛜ');
  assert.strictEqual(cjs.default.toRunes('viking'), 'ᚹᛁᚲᛁᛜ');
  console.log(`ok — cjs ${a} checks, esm ${b} checks (${golden.cases.length} golden cases + exhaustive U+0000..U+10FFFF per system)`);
})().catch((e) => { console.error(e.message || e); process.exit(1); });
