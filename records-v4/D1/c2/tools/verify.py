import csv, re, collections, sys
csv.field_size_limit(10**9)
OK = {"INSTALLED-OWN","INSTALLED-PACKAGE","INSTALLED-DERIVED","PROGRAM-OWN","PROGRAM-DERIVED","SETTING-OWN","SETTING-DEFAULT","RECORD","MATERIAL","RUNTIME","ACTION","GAP-NONE","GAP-TWO","UNKNOWN","MIXED"}
sids = set(re.findall(r"\*\*(S8\.\d-\d+)\*\*", open("../../../SENTENCES.md").read()))
inp = [r["id"] for r in csv.DictReader(open("../../in/part-microos.tsv"), delimiter="\t")]
lines = open("../part-microos.tsv").read().split("\n")
assert lines[0] == "id\tdecision\tsentences\twhat_it_does\tbasis\treason", lines[0]
rows = [l.split("\t") for l in lines[1:] if l]
errs = []
for r in rows:
    if len(r) != 6: errs.append(("fields", r[0])); continue
    if r[1] not in OK: errs.append(("decision", r[0], r[1]))
    for s in r[2].split(","):
        if s not in sids: errs.append(("sentence", r[0], s))
    if len(r[3].split()) > 15: errs.append(("what>15", r[0]))
    if len(r[5].split()) > 30: errs.append(("reason>30", r[0]))
    if not re.match(r"^(evidence|none|(raw|doc):)", r[4]): errs.append(("basis", r[0], r[4]))
out = [r[0] for r in rows]
c = collections.Counter(out)
print("input", len(inp), "output", len(out), "unique", len(c), "dups", [k for k, v in c.items() if v > 1][:5])
print("same set", set(inp) == set(out), "missing", len(set(inp) - set(out)), "extra", len(set(out) - set(inp)))
print("errors", len(errs), errs[:10])
cnt = collections.Counter(r[1] for r in rows)
for k in sorted(OK): print(f"{k}\t{cnt.get(k, 0)}")
