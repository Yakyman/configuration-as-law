"""Pick 10 rows per scripted rule (deterministic) and print them for hand checking.
Usage: sample_rules.py <input part-3.tsv> <output part-3.tsv>
"""
import csv
import random
import re
import sys

inp = {r["id"]: r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)}
out = {r["id"]: r for r in csv.DictReader(open(sys.argv[2], encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)}


def short(n):
    return re.sub(r"^/nix/store/[a-z0-9]{32}-", "", n)


RULES = {
    "R1-doc": lambda r: r["kind"] == "system-closure-store-object" and out[r["id"]]["what_it_does"].startswith("documentation"),
    "R2-unitfile": lambda r: r["kind"] == "system-closure-store-object" and short(r["name"]).startswith("unit-") and not short(r["name"]).startswith("unit-script-"),
    "R3-unitscript": lambda r: r["kind"] == "system-closure-store-object" and short(r["name"]).startswith("unit-script-"),
    "R4-restart-triggers": lambda r: r["kind"] == "system-closure-store-object" and short(r["name"]).startswith("X-Restart-Triggers-"),
    "R5-pam": lambda r: r["kind"] == "system-closure-store-object" and short(r["name"]).endswith(".pam"),
    "R6-program": lambda r: r["kind"] == "system-closure-store-object" and out[r["id"]]["what_it_does"].startswith("program or library package"),
    "R7-units": lambda r: r["kind"] in ("system-unit", "user-unit"),
    "R8-kernel-module": lambda r: r["kind"] == "kernel-module",
    "R9-process": lambda r: r["kind"] == "process",
    "R10-account": lambda r: r["kind"] == "account",
}
rng = random.Random(3)
for rule, f in RULES.items():
    ids = sorted(i for i, r in inp.items() if f(r))
    pick = sorted(rng.sample(ids, min(10, len(ids))))
    print("==", rule, "rows:", len(ids))
    for i in pick:
        o = out[i]
        print(" ", i, short(inp[i]["name"]), "|", o["decision"], o["sentences"], "|", o["what_it_does"])
