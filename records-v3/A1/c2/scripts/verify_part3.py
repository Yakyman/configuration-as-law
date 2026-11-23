"""Verify A1/c2/part-3.tsv against A1/in/part-3.tsv and write part-3.done with counts per decision.
Usage: verify_part3.py <input> <output> <done-file>
"""
import collections
import sys

HEADER = "id\tdecision\tsentences\twhat_it_does\tbasis\treason"
ALLOWED = {"MUST", "NOT", "HOLE", "UNKNOWN", "MIXED"}

inp_lines = open(sys.argv[1], encoding="utf-8").read().splitlines()
out_lines = open(sys.argv[2], encoding="utf-8").read().splitlines()
in_ids = [l.split("\t", 1)[0] for l in inp_lines[1:] if l.strip()]
errors = []
if out_lines[0] != HEADER:
    errors.append("bad header")
out_ids, counts = [], collections.Counter()
for n, l in enumerate(out_lines[1:], 2):
    f = l.split("\t")
    if len(f) != 6:
        errors.append(f"line {n}: {len(f)} fields")
        continue
    out_ids.append(f[0])
    if f[1] not in ALLOWED:
        errors.append(f"line {n}: decision {f[1]!r}")
    if len(f[3].split()) > 15:
        errors.append(f"line {n}: what_it_does > 15 words")
    if len(f[5].split()) > 30:
        errors.append(f"line {n}: reason > 30 words")
    counts[f[1]] += 1
dups = [i for i, c in collections.Counter(out_ids).items() if c > 1]
if dups:
    errors.append(f"duplicate ids: {dups[:5]}")
if set(out_ids) != set(in_ids) or len(out_ids) != len(in_ids):
    errors.append(f"id sets differ: in={len(in_ids)} out={len(out_ids)} "
                  f"missing={sorted(set(in_ids) - set(out_ids))[:5]} extra={sorted(set(out_ids) - set(in_ids))[:5]}")
if errors:
    print("FAIL")
    print("\n".join(errors))
    sys.exit(1)
with open(sys.argv[3], "w", encoding="utf-8") as fh:
    for k in ["MUST", "NOT", "HOLE", "UNKNOWN", "MIXED"]:
        fh.write(f"{k}\t{counts[k]}\n")
    fh.write(f"total\t{sum(counts.values())}\n")
print("OK", dict(counts), "total", sum(counts.values()))
