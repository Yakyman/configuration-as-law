import csv, sys
# print my own part-5 decisions for given names (to keep readings consistent)
names = sys.argv[1:]
rows = list(csv.DictReader(open("A1/in/part-5.tsv"), delimiter="\t", quoting=csv.QUOTE_NONE))
out = {r["id"]: r for r in csv.DictReader(open("A1/c2/part-5.tsv"), delimiter="\t", quoting=csv.QUOTE_NONE)}
for n in names:
    for r in rows:
        if r["name"] == n:
            o = out.get(r["id"])
            if not o: print("nooutput", r["id"], n); continue
            print(r["machine"], n, "|", o["decision"], o["sentences"], "|", o["what_it_does"], "|", o["reason"])
