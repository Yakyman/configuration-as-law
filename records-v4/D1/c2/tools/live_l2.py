import csv, json, sys, os
csv.field_size_limit(10**9)
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../in/raw/microos")
for r in csv.DictReader(open(base + "/objects.tsv"), delimiter="\t"):
    if r["level"] != "2" or r["name"].startswith("/.snapshots/1/snapshot"): continue
    m = json.loads(r["members"])
    if r["kind"] == "stored-outside-packages":
        mem = list(csv.DictReader(open(base + "/" + m["file"]), delimiter="\t"))
        s = "; ".join(f'{x["path"].rsplit("/",1)[-1]}({x["type"][0]},{x["persistence"][:4]})' for x in mem[:12])
        print(r["id"][:8], "G", r["name"], m["count"], "|", s, "..." if len(mem) > 12 else "")
    else:
        md = m.get("metadata", m)
        print(r["id"][:8], r["kind"][:4], r["name"], md.get("size"), md.get("persistence"), "x" if md.get("executable") else "-", "sh" if md.get("shebang") else "", "st" if md.get("startup") else "")
