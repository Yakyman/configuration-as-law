"""Print the answers of the two parties side by side for the gaps named on the command line.

usage: show.py G1 [G2 ...]   (run from the night folder)
Reads W1/OBJECTS.tsv, W1/m1/objects.tsv, W1/m2/objects.tsv; writes nothing.
"""
import csv
import sys

csv.field_size_limit(sys.maxsize)


def load(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))


m1 = load("W1/m1/objects.tsv")
m2 = load("W1/m2/objects.tsv")
ob = load("W1/OBJECTS.tsv")
want = set(sys.argv[1:])
for i, (o, a, b) in enumerate(zip(ob, m1, m2)):
    assert o["gap"] == a["gap"] == b["gap"] and o["id"] == a["id"] == b["id"], (i, o["id"], a["id"], b["id"])
    if want and o["gap"] not in want:
        continue
    print("#####", o["gap"], o["id"], o["machine"], o["kind"], o["name"])
    for tag, r in (("m1", a), ("m2", b)):
        print(f"--{tag}: decided={r['decided']} | sentence={r['sentence']}")
        print(f"   decision: {r['decision']}")
        print(f"   meaning: {r['meaning_answer']}")
        print(f"   achievable: {r['achievable']}")
        print(f"   note: {r['note']}")
