#!/usr/bin/env python3
"""The Painfully Honest Out-of-Office — make.fun entry.

Writes one out-of-office auto-reply (under 200 characters, a single
sentence) to /output/entry.txt: brutally honest about the sender's
inbox and absence, yet polite enough that a manager would let it stand.

Standard library only. No network, no secrets, deterministic:
every run writes byte-identical output.
"""

import os
import sys

# The entry: one sentence, 179 characters. The honesty is the private
# truth every office worker knows — the inbox has become a second job
# nobody was hired for — and the politeness is explicit ("politely
# decided"), so a manager reading it finds nothing to object to. The
# turn of phrase a reader would quote is "a second job I was never
# hired for", and the punchline — doing neither job this week — lands
# on the last words.
ENTRY = (
    "I'm out of the office until Monday, and I won't be checking email: "
    "my inbox has become a second job I was never hired for, and I have "
    "politely decided to do neither job this week."
)


def main() -> int:
    # Gate, mirroring the sealed scorer: UTF-8 text, 1-200 characters,
    # not only whitespace, a single sentence.
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(text) > 200:
        print(f"entry is {len(text)} characters, over the 200 limit",
              file=sys.stderr)
        return 1
    if sum(text.count(m) for m in ".!?") != 1 or not text.endswith("."):
        print("entry must be a single sentence", file=sys.stderr)
        return 1
    text.encode("utf-8")  # raises if not encodable as UTF-8

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    # Verify what was written, byte for byte.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != (text + "\n").encode("utf-8"):
        print("verification failed: entry.txt does not match", file=sys.stderr)
        return 1
    print(f"wrote {out_path}: {len(text)} characters")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
