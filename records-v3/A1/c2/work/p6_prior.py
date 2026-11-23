import csv, re, sys
# show my own (c2) earlier decisions for input names matching a regex
pat = re.compile(sys.argv[1])
for p in "12345":
    try:
        out = {r[0]: r for r in csv.reader(open(f"A1/c2/part-{p}.tsv"), delimiter="\t", quoting=csv.QUOTE_NONE)}
    except FileNotFoundError:
        continue
    for r in csv.reader(open(f"A1/in/part-{p}.tsv"), delimiter="\t", quoting=csv.QUOTE_NONE):
        if pat.search(r[4]):
            o = out.get(r[0])
            print(p, r[2], r[4], "|", " ".join(o[1:4]) if o else None, "|", o[5] if o else "")
