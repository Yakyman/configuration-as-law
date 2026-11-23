import csv, sys, importlib.util
# list up to 10 rows per rule (spread over the rule's rows) with name and evidence, for the hand check
spec = importlib.util.spec_from_file_location("p6", "A1/c2/scripts/part6_decide.py")
p6 = importlib.util.module_from_spec(spec); spec.loader.exec_module(p6)
rows = list(csv.DictReader(open("A1/in/part-6.tsv"), delimiter="\t", quoting=csv.QUOTE_NONE))
by = {}
for r in rows:
    t, rec = p6.rule(r)
    if t:
        by.setdefault(t, []).append(r)
for t, rs in sorted(by.items()):
    step = max(1, len(rs) // 10)
    pick = rs[::step][:10]
    print(f"== {t} ({len(rs)})", ", ".join(r["id"] for r in pick))
    for r in pick:
        print("   ", r["id"], r["name"], "|", r["evidence"][:110])
