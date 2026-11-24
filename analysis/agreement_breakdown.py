"""Agreement of two classifications in a joined table, by machine, and the make-up of the disagreements.

Usage: agreement_breakdown.py JOINED.tsv

The table must have the columns `machine`, `c1_decision` and `c2_decision`. The program only reads the file.
It prints, for the whole table and for each machine, the number of objects, the number of matching decisions,
their share and Cohen's kappa; then how many disagreements consist of one classification answering UNKNOWN
(a fact needed for the decision is missing) while the other gave a decision; then the agreement among the
objects for which both classifications gave a decision other than UNKNOWN.
"""
import csv
import sys
from collections import Counter, defaultdict

csv.field_size_limit(10 ** 9)


def kappa(pairs):
    total = sum(pairs.values())
    observed = sum(count for (a, b), count in pairs.items() if a == b) / total
    first, second = Counter(), Counter()
    for (a, b), count in pairs.items():
        first[a] += count
        second[b] += count
    expected = sum(first[k] * second[k] for k in set(first) | set(second)) / total ** 2
    return (observed - expected) / (1 - expected) if expected != 1 else float("nan")


def main(path):
    pairs = Counter()
    by_machine = defaultdict(Counter)
    with open(path, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t", quoting=csv.QUOTE_NONE):
            pair = (row["c1_decision"], row["c2_decision"])
            pairs[pair] += 1
            by_machine[row["machine"]][pair] += 1

    def line(name, table):
        objects = sum(table.values())
        same = sum(count for (a, b), count in table.items() if a == b)
        print(f"{name}: objects {objects}, matching {same} = {100 * same / objects:.2f} %, kappa {kappa(table):.5f}")

    line("all", pairs)
    for machine in sorted(by_machine):
        line(machine, by_machine[machine])

    objects = sum(pairs.values())
    same = sum(count for (a, b), count in pairs.items() if a == b)
    first_unknown = sum(count for (a, b), count in pairs.items() if a != b and a == "UNKNOWN")
    second_unknown = sum(count for (a, b), count in pairs.items() if a != b and b == "UNKNOWN")
    differing = objects - same
    print(f"disagreements: {differing}; first UNKNOWN while second decided: {first_unknown}; "
          f"second UNKNOWN while first decided: {second_unknown}; "
          f"both decided differently: {differing - first_unknown - second_unknown}")
    both = sum(count for (a, b), count in pairs.items() if a != "UNKNOWN" and b != "UNKNOWN")
    both_same = sum(count for (a, b), count in pairs.items() if a == b and a != "UNKNOWN")
    print(f"objects decided by both (neither UNKNOWN): {both}; matching: {both_same} = {100 * both_same / both:.2f} %")
    print("UNKNOWN in the first classification:", sum(c for (a, _), c in pairs.items() if a == "UNKNOWN"),
          "; in the second:", sum(c for (_, b), c in pairs.items() if b == "UNKNOWN"))


if __name__ == "__main__":
    main(sys.argv[1])
