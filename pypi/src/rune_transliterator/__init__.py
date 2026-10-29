"""English/Latin text to Elder Futhark, Younger Futhark and Anglo-Saxon Futhorc runes.

    >>> import rune_transliterator as rt
    >>> rt.to_runes("Thor")
    'ᚦᛟᚱ'
    >>> rt.to_runes("viking", "younger")
    'ᚢᛁᚴᛁᚾᚴ'
    >>> rt.from_runes("ᚦᛟᚱ")
    'thor'

A phonetic approximation: modern spelling written in runes letter by letter,
not a translation into Old Norse or Old English.

Code: MIT. Rune tables: CC BY 4.0 — https://fontvibe.ai/tools/rune-generator
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

__version__ = "1.0.0"
__all__ = [
    "to_runes",
    "from_runes",
    "alphabet",
    "RUNE_ALPHABET",
    "SYSTEMS",
    "DEFAULT_SYSTEM",
    "DATA",
]

_DATA_FILE = Path(__file__).parent / "runes.json"
if not _DATA_FILE.exists():  # pragma: no cover - packaging error
    raise FileNotFoundError(
        f"rune-transliterator: {_DATA_FILE} is missing. The package was probably "
        "built without running scripts/sync_data.py; please open an issue at "
        "https://github.com/Funovate-Technology/fontvibe-runes/issues"
    )

with _DATA_FILE.open(encoding="utf-8") as _fh:
    DATA: Dict = json.load(_fh)

SYSTEMS = tuple(DATA["systems"])
DEFAULT_SYSTEM: str = DATA["default_system"]

RuneEntry = Dict[str, str]
RUNE_ALPHABET: Dict[str, List[RuneEntry]] = {k: v["alphabet"] for k, v in DATA["systems"].items()}
_REVERSE = {k: {e["rune"]: e["latin"] for e in v["alphabet"]} for k, v in DATA["systems"].items()}


def _resolve(system: Optional[str]) -> str:
    # Unknown names fall back to Elder Futhark rather than raising — same as the site.
    return system if isinstance(system, str) and system in DATA["systems"] else DEFAULT_SYSTEM


def _as_text(text: Optional[str], fn: str) -> str:
    if text is None:
        return ""
    if not isinstance(text, str):
        raise TypeError(f"{fn}: expected a string, got {type(text).__name__}")
    return text


def to_runes(text: Optional[str], system: Optional[str] = DEFAULT_SYSTEM) -> str:
    """Latin → runes.

    Digraphs first (``th``, ``ng``; plus ``ea`` in the futhorc), then single
    letters, case-insensitive, one code point at a time. Anything without a
    mapping — digits, spaces, punctuation, emoji, other scripts — passes
    through unchanged. An unknown ``system`` falls back to Elder Futhark.
    """
    text = _as_text(text, "to_runes")
    if not text:
        return ""
    table = DATA["systems"][_resolve(system)]
    letters, digraphs = table["letters"], table["digraphs"]
    out = []
    pos, n = 0, len(text)
    while pos < n:
        low = text[pos].lower()
        if pos + 1 < n:
            rune = digraphs.get(low + text[pos + 1].lower())
            if rune is not None:
                out.append(rune)
                pos += 2
                continue
        out.append(letters.get(low, text[pos]))
        pos += 1
    return "".join(out)


def from_runes(text: Optional[str], system: Optional[str] = DEFAULT_SYSTEM) -> str:
    """Runes → Latin, using each rune's primary value from the chart.

    Several letters share one rune (c/k/q, v/w, …), so this is a reading aid,
    not an exact inverse of :func:`to_runes`. Non-runes pass through unchanged.
    """
    text = _as_text(text, "from_runes")
    if not text:
        return ""
    rev = _REVERSE[_resolve(system)]
    return "".join(rev.get(ch, ch) for ch in text)


def alphabet(system: Optional[str] = DEFAULT_SYSTEM) -> List[RuneEntry]:
    """The rune chart for one system: ``[{rune, name, latin, meaning}]`` in futhark order."""
    return RUNE_ALPHABET[_resolve(system)]
