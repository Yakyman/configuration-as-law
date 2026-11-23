#!/usr/bin/env python3
"""Verify A1/c2/part-5.tsv against A1/in/part-5.tsv and write A1/c2/part-5.done."""
import collections, csv, sys

inp, out, done = sys.argv[1:4]
HEADER = ["id", "decision", "sentences", "what_it_does", "basis", "reason"]
ins = [r["id"] for r in csv.DictReader(open(inp, encoding="utf-8"), delimiter="\t")]
lines = open(out, encoding="utf-8").read().splitlines()
assert lines[0].split("\t") == HEADER, "bad header"
rows = [l.split("\t") for l in lines[1:]]
assert all(len(r) == 6 for r in rows), "bad field count"
outs = [r[0] for r in rows]
dup = [i for i, c in collections.Counter(outs).items() if c > 1]
assert not dup, ("duplicate ids", dup)
assert len(outs) == len(ins) and set(outs) == set(ins), ("id mismatch", set(ins) ^ set(outs))
dec = collections.Counter(r[1] for r in rows)
assert set(dec) <= {"MUST", "NOT", "HOLE", "UNKNOWN", "MIXED"}, dec
assert all(len(r[3].split()) <= 15 and len(r[5].split()) <= 30 for r in rows), "field too long"
with open(done, "w", encoding="utf-8") as f:
    f.write(f"rows\t{len(rows)}\n")
    for d in ["MUST", "NOT", "HOLE", "UNKNOWN", "MIXED"]:
        f.write(f"{d}\t{dec.get(d, 0)}\n")
print(open(done).read(), end="")
