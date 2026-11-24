import csv, collections, sys
part = sys.argv[1]
W = {"INSTALLED-OWN","INSTALLED-PACKAGE","INSTALLED-DERIVED","PROGRAM-OWN","PROGRAM-DERIVED","SETTING-OWN",
     "SETTING-DEFAULT","RECORD","MATERIAL","RUNTIME","ACTION","GAP-NONE","GAP-TWO","UNKNOWN","MIXED"}
inp = list(csv.DictReader(open(f"D1/in/part-{part}.tsv"), delimiter="\t"))
outp = f"D1/c2/part-{part}.tsv"
out = list(csv.DictReader(open(outp), delimiter="\t"))
assert open(outp).readline().rstrip("\n") == "id\tdecision\tsentences\twhat_it_does\tbasis\treason"
ii = [r["id"] for r in inp]; oo = [r["id"] for r in out]
assert len(ii) == len(oo) and sorted(ii) == sorted(oo) and len(set(oo)) == len(oo)
assert all(r["decision"] in W for r in out)
c = collections.Counter(r["decision"] for r in out)
with open(f"D1/c2/part-{part}.done", "w") as f:
    f.write(f"input rows: {len(ii)}\noutput rows: {len(oo)}\n")
    for w in sorted(W): f.write(f"{w}\t{c.get(w,0)}\n")
    if not ii: f.write("note: input is header-only (inventory not run, see D1/in/raw/gentoo/NOT-RUN.md)\n")
print("OK", len(ii), len(oo), dict(c))
