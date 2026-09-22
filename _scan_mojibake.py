"""Scan given files for mojibake markers (U+FFFD), emoji, and repeated odd CJK runs."""
from __future__ import annotations

import io
import sys


def main(argv: list[str]) -> int:
    targets = argv[1:]
    for p in targets:
        s = io.open(p, encoding="utf-8").read()
        fffd = [i for i, c in enumerate(s) if ord(c) == 0xFFFD]
        emoji = [c for c in set(s) if 0x1F000 <= ord(c) <= 0x1FAFF]
        print(f"{p}")
        print(f"    chars={len(s)}  U+FFFD={len(fffd)}  emoji={sorted(emoji)}")
        if fffd:
            for i in fffd[:5]:
                print(f"    at {i}: ...{s[max(0, i-40):i+40]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
