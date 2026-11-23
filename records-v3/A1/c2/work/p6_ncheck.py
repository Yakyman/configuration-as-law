import csv, json, re
# check: does evidence n= equal the number of entries (dirs included) in unowned-groups.json? (machine "debian", same inventory tool)
g = json.load(open("A1/in/raw/debian/unowned-groups.json"))
ok = bad = 0
for p in "12345":
    for r in csv.reader(open(f"A1/in/part-{p}.tsv"), delimiter="\t", quoting=csv.QUOTE_NONE):
        if r[2] != "debian" or r[3] != "stored":
            continue
        m = re.search(r"group=([^;]*); n=(\d+)", r[6])
        if not m or m.group(1) not in g:
            continue
        ents = g[m.group(1)]
        nd = sum(1 for e in ents if e["type"] == "d")
        if int(m.group(2)) == len(ents):
            ok += 1
        else:
            bad += 1
            print("diff", m.group(1), m.group(2), len(ents), nd)
print("equal", ok, "different", bad)
