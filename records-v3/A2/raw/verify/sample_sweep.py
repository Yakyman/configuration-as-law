"""Seeded sample of 30 SWEEP.tsv rows with decision MUST or NOT (verification of A2).

usage: python3 -I sample_sweep.py SWEEP.tsv
Line numbers are file lines (header is line 1).
"""
import csv
import random
import sys

SEED = 20261122
csv.field_size_limit(sys.maxsize)
with open(sys.argv[1], encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))
pool = [(i + 2, r) for i, r in enumerate(rows) if r["decision"] in ("MUST", "NOT")]
print(f"seed={SEED} rows={len(rows)} pool(MUST|NOT)={len(pool)}")
random.seed(SEED)
for line, r in sorted(random.sample(pool, 30), key=lambda x: x[0]):
    print("\t".join([f"L{line}", r["type"], r["system"], r["decision"], r["sentence IDs"], r["reason"],
                     r["source evidence"], r["source URL"]]))
