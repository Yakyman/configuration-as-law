"""Put the answers of the two parties next to each other, one row per object, without judging them.

usage: compare.py   (run from the night folder)
Reads W1/OBJECTS.tsv, W1/m1/objects.tsv, W1/m2/objects.tsv; writes W1/j/compare.tsv and prints the counts.
The columns `same_meaning` and the weights are NOT computed here: they are the third party's reading, in W1/RESULT.md.
"""
import collections
import csv
import sys

csv.field_size_limit(sys.maxsize)


def load(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))


def first_word(s):
    return s.strip().split(":")[0].split(",")[0].split(" ")[0].lower()


ob = load("W1/OBJECTS.tsv")
m1 = load("W1/m1/objects.tsv")
m2 = load("W1/m2/objects.tsv")
assert len(ob) == len(m1) == len(m2), (len(ob), len(m1), len(m2))
cols = ["gap", "id", "machine", "name", "m1_decided", "m2_decided", "m1_sentence", "m2_sentence",
        "m1_meaning", "m2_meaning", "m1_achievable", "m2_achievable"]
rows = []
for o, a, b in zip(ob, m1, m2):
    assert o["gap"] == a["gap"] == b["gap"] and o["id"] == a["id"] == b["id"], (o["id"], a["id"], b["id"])
    rows.append({
        "gap": o["gap"], "id": o["id"], "machine": o["machine"], "name": o["name"],
        "m1_decided": a["decided"], "m2_decided": b["decided"],
        "m1_sentence": a["sentence"], "m2_sentence": b["sentence"],
        "m1_meaning": a["meaning_answer"], "m2_meaning": b["meaning_answer"],
        "m1_achievable": first_word(a["achievable"]), "m2_achievable": first_word(b["achievable"]),
    })
with open("W1/j/compare.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, cols, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\")
    w.writeheader()
    w.writerows(rows)

by = collections.defaultdict(list)
for r in rows:
    by[r["gap"]].append(r)
print("rows", len(rows), "distinct objects", len({r["id"] for r in rows}))
for g, rs in by.items():
    print(g, "objects", len(rs),
          "| machines", dict(collections.Counter(r["machine"] for r in rs)),
          "| m1 decided", dict(collections.Counter(r["m1_decided"] for r in rs)),
          "| m2 decided", dict(collections.Counter(r["m2_decided"] for r in rs)),
          "| m1 achievable", dict(collections.Counter(r["m1_achievable"] for r in rs)),
          "| m2 achievable", dict(collections.Counter(r["m2_achievable"] for r in rs)))
    for r in rs:
        print("   ", r["machine"], r["name"][:60], "||", first_word(r["m1_meaning"]), "|", r["m1_meaning"][:28],
              "||", first_word(r["m2_meaning"]), "|", r["m2_meaning"][:28])
