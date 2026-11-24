"""How the adjudication decided the rows on which two classifications differ.

Usage: disagreement_adjudication.py FOLDER

FOLDER must contain compare/joined.tsv (columns id, machine, c1_decision, c2_decision) and
adjudication/rows.tsv (columns id, verdict, hole). The program only reads the files.

For every adjudicated row it determines the type of the pair of decisions:
  same             both classifications gave the same decision
  first-unknown    the first answered UNKNOWN, the second gave another decision
  second-unknown   the second answered UNKNOWN, the first gave another decision
  both-decided     both gave a decision other than UNKNOWN, and the decisions differ
and prints the verdicts of the adjudication (RESOLVED, GAP, UNKNOWN) for each type, then the rows with the
verdict GAP on which the classifications differ, by machine and by the kind of gap named by the adjudication.
"""
import csv
import sys
from collections import Counter

csv.field_size_limit(10 ** 9)
base = sys.argv[1].rstrip("/")

pairs = {}
with open(base + "/compare/joined.tsv", encoding="utf-8", newline="") as handle:
    for row in csv.DictReader(handle, delimiter="\t", quoting=csv.QUOTE_NONE):
        pairs[row["id"]] = (row["machine"], row["c1_decision"], row["c2_decision"])


def pair_type(first, second):
    if first == second:
        return "same"
    if first == "UNKNOWN":
        return "first-unknown"
    if second == "UNKNOWN":
        return "second-unknown"
    return "both-decided"


by_type = Counter()
gap_by_machine = Counter()
gap_by_kind = Counter()
gap_two = Counter()
with open(base + "/adjudication/rows.tsv", encoding="utf-8", newline="") as handle:
    for row in csv.DictReader(handle, delimiter="\t", quoting=csv.QUOTE_NONE):
        machine, first, second = pairs[row["id"]]
        kind = pair_type(first, second)
        verdict = row["verdict"].split(":")[0]
        by_type[(kind, verdict)] += 1
        if kind == "first-unknown" and second.startswith("GAP"):
            gap_two[verdict] += 1
        if verdict == "GAP" and kind != "same":
            gap_by_machine[(machine, kind)] += 1
            gap_by_kind[(row.get("hole", ""), kind)] += 1

print("adjudicated rows:", sum(by_type.values()))
for kind in ("same", "first-unknown", "second-unknown", "both-decided"):
    total = sum(count for (k, _), count in by_type.items() if k == kind)
    parts = ", ".join(f"{verdict} {count}" for (k, verdict), count in sorted(by_type.items()) if k == kind)
    print(f"{kind}: {total} ({parts})")
print("first-unknown rows where the second classification answered that the text decides both ways or not at all:",
      sum(gap_two.values()), dict(gap_two))
print("GAP rows on which the classifications differ, by machine and type:")
for (machine, kind), count in sorted(gap_by_machine.items()):
    print(f"  {machine} {kind}: {count}")
print("the same rows by the kind of gap named by the adjudication:")
for (hole, kind), count in sorted(gap_by_kind.items()):
    print(f"  kind {hole or '-'} {kind}: {count}")
