#!/usr/bin/env python3
"""Count ERROR lines in a log file and rank the most frequent error messages.

Usage:
    python3 count_errors.py <logfile> [--top N]

A line is an error when its level token (the 3rd field in a
`<date> <time> <LEVEL> <message>` line, falling back to the first level-like
token) is ERROR/ERR/E. Stdlib only.
"""
import argparse
from collections import Counter

LEVELS = {"ERROR", "ERR", "E"}


def find_level_idx(toks):
    if len(toks) >= 3 and toks[2].upper() in LEVELS:
        return 2
    for i, t in enumerate(toks):
        if t.upper() in LEVELS:
            return i
    return None


def main():
    ap = argparse.ArgumentParser(description="Count ERROR lines and rank top messages.")
    ap.add_argument("logfile", help="path to the log file")
    ap.add_argument("--top", type=int, default=5, help="how many top messages to report (default 5)")
    args = ap.parse_args()

    counts = Counter()
    total = 0
    with open(args.logfile, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            toks = raw.split()
            if not toks:
                continue
            idx = find_level_idx(toks)
            if idx is None:
                continue
            total += 1
            msg = " ".join(toks[idx + 1:]) if idx + 1 < len(toks) else "(no message)"
            counts[msg] += 1

    print("TOTAL_ERRORS =", total)
    print("SUM_BY_MESSAGE =", sum(counts.values()), "(sanity: must equal TOTAL_ERRORS)")
    print("TOP_MESSAGES:")
    for m, c in counts.most_common(args.top):
        print(f"  {c}  {m}")
    print("DISTINCT_MESSAGES =", len(counts))


if __name__ == "__main__":
    main()
