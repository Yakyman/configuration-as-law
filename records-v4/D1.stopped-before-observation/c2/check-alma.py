import csv
from collections import Counter

W = {"INSTALLED-OWN", "INSTALLED-PACKAGE", "INSTALLED-DERIVED", "PROGRAM-OWN", "PROGRAM-DERIVED",
     "SETTING-OWN", "SETTING-DEFAULT", "RECORD", "MATERIAL", "RUNTIME", "ACTION", "GAP-NONE",
     "GAP-TWO", "UNKNOWN", "MIXED"}
d = "D1/"
inp = list(csv.DictReader(open(d + "in/part-alma.tsv", encoding="utf-8"), delimiter="\t"))
out = list(csv.DictReader(open(d + "c2/part-alma.tsv", encoding="utf-8"), delimiter="\t"))
hdr = open(d + "c2/part-alma.tsv", encoding="utf-8").readline().rstrip("\n")
assert hdr == "id\tdecision\tsentences\twhat_it_does\tbasis\treason", hdr
ii = [r["id"] for r in inp]
oi = [r["id"] for r in out]
assert sorted(ii) == sorted(oi), "id sets differ"
assert len(oi) == len(set(oi)), "duplicate ids"
bad = [r["id"] for r in out if r["decision"] not in W]
assert not bad, bad
c = Counter(r["decision"] for r in out)
with open(d + "c2/part-alma.done", "w", encoding="utf-8") as f:
    f.write(f"rows: {len(out)} (input rows: {len(inp)})\n")
    for w in sorted(W):
        f.write(f"{w}\t{c.get(w, 0)}\n")
print("OK", len(inp), len(out))
