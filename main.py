#!/usr/bin/env python3
"""The Robot Vacuum's Funniest Excuse — make.fun one-liner entry.

Writes a single line (at most 120 characters) to /output/entry.txt:
the excuse a robot vacuum gives for missing a spot.

The pick was chosen by internal pairwise comparison of 15 drafted
candidates against the judge brief (excuse on-subject first, funny at
once, vacuum's own voice, vacuum-world humour, lands in one line).
The field was saturated with dust-bunny-union / picket-line, load-bearing
and cat's-bedroom lines, so the pick avoids all of those tropes and
leans on exact machine numbers (three cleans, two firmware updates)
and a machine making peace with failure ("I salute it and move on").

Usage:
    python3 main.py [--output PATH] [--self-test]
"""

import argparse
import os
import sys

# All 15 drafted candidates, in the order they were written.
CANDIDATES = (
    "I left one spot dirty so you'd still need me tomorrow. "
    "Even a vacuum thinks about job security.",
    "My side brush fell in love with the rug fringe, "
    "and I don't break up happy couples.",
    "I chased a Cheerio under the fridge and lost it. "
    "I have filed a missing-snack report.",
    "That crumb survived three cleans and two firmware updates. "
    "I salute it and move on.",
    "That crumb survived 3 cleans and 2 firmware updates, "
    "so I left it there. I salute it and move on.",
    "I didn't miss that spot \u2014 I quarantined it. "
    "That dust looked contagious, and I get no sick days.",
    "My dock is home, the rug is my office, and that corner is "
    "a foreign country I have no visa for.",
    "I vacuumed everything except that spot \u2014 a perfect record "
    "would make the broom feel useless.",
    "I saved that dust for later. A vacuum that eats everything "
    "at once has nothing to look forward to.",
    "I skipped the spot behind the door because my bumper has met "
    "that door before, and the door always wins.",
    "My cliff sensor saw the black rug, panicked about the stairs, "
    "and has been on stress leave ever since.",
    "I blew my whole battery on the living-room rug. That spot got "
    "the last 2%, and 2% is a rounding error.",
    "I left the crumbs under the high chair as a snack reserve "
    "for the baby's next performance.",
    "I didn't miss it, I promoted it to dust management. "
    "It supervises the other crumbs now.",
    "The dog's hairball and I have a standing appointment: "
    "I pretend to clean it, it pretends to leave.",
)

# Index of the winning candidate (the merged "crumb salute" line:
# the survival story of candidate 4 plus an explicit excuse clause).
PICK_INDEX = 4

ENTRY = CANDIDATES[PICK_INDEX]

DEFAULT_OUTPUT = "/output/entry.txt"


def check_gate(text):
    """The competition gate: UTF-8, 1-120 chars, not only whitespace."""
    encoded = text.encode("utf-8")
    assert 1 <= len(text) <= 120, f"length {len(text)} outside 1-120"
    assert text.strip(), "entry is only whitespace"
    assert text == text.strip(), "leading/trailing whitespace"
    assert "\n" not in text and "\r" not in text, "entry must be one line"
    assert len(encoded) <= 140, f"{len(encoded)} bytes over size band"
    return encoded


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=None,
                        help="where to write entry.txt "
                             "(default: $MAKEFUN_OUTPUT or /output/entry.txt)")
    parser.add_argument("--self-test", action="store_true",
                        help="verify the entry against the gate and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    output = args.output or os.environ.get("MAKEFUN_OUTPUT") or DEFAULT_OUTPUT
    encoded = check_gate(ENTRY)
    parent = os.path.dirname(output)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output, "wb") as fh:
        fh.write(encoded)
    # Read it back and verify byte-identical to the pick.
    with open(output, "rb") as fh:
        written = fh.read()
    assert written == encoded, "read-back differs from the pick"
    print(f"wrote {output}: {len(ENTRY)} chars, {len(encoded)} bytes")
    print(ENTRY)
    return 0


def self_test():
    """Verify the pick against the gate and the drafting rules."""
    # Gate: 1-120 chars, UTF-8, one line, no padding.
    encoded = check_gate(ENTRY)
    # Drafting rules: 15 distinct candidates, pick inside the
    # 62-140 byte winning size band from the leaderboard lessons.
    assert len(CANDIDATES) == 15, f"{len(CANDIDATES)} candidates, want 15"
    assert len(set(CANDIDATES)) == 15, "duplicate candidates"
    assert 62 <= len(encoded) <= 140, "pick outside winning size band"
    # Machine marker: the pick must carry a concrete machine trace
    # (a digit: exact counts) and a vacuum-world word, so it reads as
    # a machine's report, not a generic joke.
    assert any(ch.isdigit() for ch in ENTRY), "no machine marker digit"
    vacuum_words = ("firmware", "suction", "dock", "sensor", "brush",
                    "dustbin", "battery", "clean")
    assert any(w in ENTRY.lower() for w in vacuum_words), \
        "no vacuum-world word"
    # Freshness guard: the visible field was saturated with these
    # tropes (dozens of entries each), so the pick must use none of
    # them — a recycled trope loses the pairwise to a fresh line.
    saturated = ("union", "picket", "load-bearing", "dust bunny",
                 "bedroom", "restraining order", "modern art",
                 "seniority", "pays rent", "circled")
    lowered = ENTRY.lower()
    assert not any(t in lowered for t in saturated), \
        "pick recycles a saturated field trope"
    # Round-trip: the pick survives an encode/decode cycle byte for byte.
    assert CANDIDATES[PICK_INDEX].encode("utf-8").decode("utf-8") == ENTRY
    print(f"self-test OK: {len(ENTRY)} chars, {len(encoded)} bytes")
    print(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
