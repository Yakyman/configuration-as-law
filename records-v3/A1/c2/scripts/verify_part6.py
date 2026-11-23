#!/usr/bin/env python3
"""Verify A1/c2/part-6.tsv against A1/in/part-6.tsv and write A1/c2/part-6.done."""
import collections, csv, sys

HEAD = ["id", "decision", "sentences", "what_it_does", "basis", "reason"]
inp = [r["id"] for r in csv.DictReader(open("A1/in/part-6.tsv", encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)]
lines = open("A1/c2/part-6.tsv", encoding="utf-8").read().splitlines()
assert lines[0].split("\t") == HEAD, lines[0]
rows = [l.split("\t") for l in lines[1:]]
assert all(len(r) == 6 for r in rows), [r[0] for r in rows if len(r) != 6]
out = [r[0] for r in rows]
dup = [k for k, v in collections.Counter(out).items() if v > 1]
assert not dup, dup
assert len(out) == len(inp) and set(out) == set(inp), (len(out), len(inp), set(inp) ^ set(out))
bad = [r[0] for r in rows if r[1] not in {"MUST", "NOT", "HOLE", "UNKNOWN", "MIXED"}]
assert not bad, bad
assert all(len(r[3].split()) <= 15 and len(r[5].split()) <= 30 for r in rows)
c = collections.Counter(r[1] for r in rows)
with open("A1/c2/part-6.done", "w", encoding="utf-8") as f:
    for k in ["MUST", "NOT", "HOLE", "UNKNOWN", "MIXED"]:
        f.write(f"{k}\t{c.get(k, 0)}\n")
    f.write(f"TOTAL\t{len(rows)}\n")
print("OK", len(rows), dict(c))
