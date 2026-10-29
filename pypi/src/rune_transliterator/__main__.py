"""python -m rune_transliterator [-s elder|younger|anglo] [-d] [-c] TEXT..."""

from __future__ import annotations

import argparse
import sys

from . import DEFAULT_SYSTEM, SYSTEMS, alphabet, from_runes, to_runes


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="rune-transliterator",
        description="Latin text to runes and back. Phonetic approximation, not a "
        "translation. Charts and live tool: https://fontvibe.ai/tools/rune-generator",
    )
    p.add_argument("text", nargs="*", help="text to convert (reads stdin if omitted)")
    p.add_argument("-s", "--system", default=DEFAULT_SYSTEM, choices=SYSTEMS)
    p.add_argument("-d", "--decode", action="store_true", help="runes → Latin")
    p.add_argument("-c", "--chart", action="store_true", help="print the rune chart")
    a = p.parse_args(argv)

    if a.chart:
        for e in alphabet(a.system):
            print(f"{e['rune']}  U+{ord(e['rune']):04X}  {e['latin']:<3}  {e['name']:<9}  {e['meaning']}")
        return 0
    if a.text:
        src = " ".join(a.text)
    elif not sys.stdin.isatty():
        src = sys.stdin.read()
    else:
        p.print_help()
        return 2
    fn = from_runes if a.decode else to_runes
    out = fn(src, a.system)
    sys.stdout.write(out if not a.text else out + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
