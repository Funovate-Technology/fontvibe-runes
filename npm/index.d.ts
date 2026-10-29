export type RuneSystem = 'elder' | 'younger' | 'anglo';

export interface RuneEntry {
  /** The rune itself — one code point in the Runic block (U+16A0–U+16FF). */
  rune: string;
  /** Traditional rune name, e.g. "Fehu", "Áss", "Æsc". */
  name: string;
  /** Primary Latin value; what fromRunes() decodes this rune to. */
  latin: string;
  /** Conventional gloss of the rune name. Popular-reference level, not scholarship. */
  meaning: string;
}

export interface SystemTable {
  label: string;
  /** The FontVibe page that uses this table. */
  page: string;
  alphabet: RuneEntry[];
  /** Single lowercase letter → rune(s). */
  letters: Record<string, string>;
  /** Two-letter sequence → rune; matched before single letters. */
  digraphs: Record<string, string>;
}

export interface RuneData {
  name: string;
  version: string;
  license: string;
  attribution: string;
  default_system: RuneSystem;
  systems: Record<RuneSystem, SystemTable>;
}

/**
 * Latin → runes. Digraphs first (th, ng, and ea in the futhorc), then single
 * letters; case-insensitive. Unmapped characters pass through unchanged.
 * An unknown `system` falls back to Elder Futhark.
 */
export function toRunes(text: string | null | undefined, system?: RuneSystem | string): string;

/**
 * Runes → Latin, using each rune's primary value. Several letters share one
 * rune, so this is a reading aid rather than an exact inverse of toRunes.
 */
export function fromRunes(text: string | null | undefined, system?: RuneSystem | string): string;

/** The rune chart for one system, in futhark order. */
export function alphabet(system?: RuneSystem | string): RuneEntry[];

export const RUNE_ALPHABET: Record<RuneSystem, RuneEntry[]>;
export const SYSTEMS: readonly RuneSystem[];
export const DEFAULT_SYSTEM: RuneSystem;
/** The raw mapping tables (data/runes.json, CC BY 4.0). */
export const data: RuneData;

declare const _default: {
  toRunes: typeof toRunes;
  fromRunes: typeof fromRunes;
  alphabet: typeof alphabet;
  RUNE_ALPHABET: typeof RUNE_ALPHABET;
  SYSTEMS: typeof SYSTEMS;
  DEFAULT_SYSTEM: typeof DEFAULT_SYSTEM;
  data: typeof data;
};
export default _default;
