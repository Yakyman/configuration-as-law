import os as _os; NIGHT_DIR = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../..")) + "/"  # night folder
"""Print N sampled rows (evenly spaced) of given input kinds with their c2 decision, for hand checks."""
import csv, sys, json
csv.field_size_limit(10**9)
N = NIGHT_DIR + "A3/"
inp = list(csv.DictReader(open(N + "in/part-server.tsv"), delimiter="\t"))
out = {r["id"]: r for r in csv.DictReader(open(N + "c2/part-server.tsv"), delimiter="\t", quoting=csv.QUOTE_NONE)}
kinds = sys.argv[1].split(","); n = int(sys.argv[2])
sel = [r for r in inp if r["kind"] in kinds]
step = max(1, len(sel) // n)
for r in sel[::step][:n]:
    o = out[r["id"]]
    print(r["id"], "|", r["kind"], "|", r["name"][:60], "|", r["members"][:150].replace("\n", " "))
    print("    ->", o["decision"], "|", o["what_it_does"], "|", o["reason"][:200])
