import os as _os; NIGHT_DIR = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../..")) + "/"  # night folder
"""Validate an output TSV: header, ids equal input, decisions valid, word limits, no empty fields."""
import csv
import sys

csv.field_size_limit(10**9)
NIGHT = NIGHT_DIR + ""
out = sys.argv[1] if len(sys.argv) > 1 else NIGHT + "A3/c2/part-server.tsv"
WORDS = {"INSTALLED-OWN", "INSTALLED-PACKAGE", "INSTALLED-DERIVED", "PROGRAM-OWN", "PROGRAM-DERIVED", "SETTING-OWN",
         "SETTING-DEFAULT", "RECORD", "MATERIAL", "RUNTIME", "ACTION", "GAP-NONE", "GAP-TWO", "UNKNOWN", "MIXED"}
lines = open(out, encoding="utf-8").read().split("\n")
assert lines[-1] == "", "file must end with newline"
lines = lines[:-1]
assert lines[0] == "id\tdecision\tsentences\twhat_it_does\tbasis\treason", lines[0]
ids, bad = [], 0
for ln in lines[1:]:
    f = ln.split("\t")
    if len(f) != 6:
        print("FIELDS", len(f), ln[:80]); bad += 1; continue
    ids.append(f[0])
    if f[1] not in WORDS:
        print("DECISION", f[0], f[1]); bad += 1
    if any(x.strip() == "" for x in f):
        print("EMPTY", f[0]); bad += 1
    if len(f[3].split()) > 15:
        print("WHAT>15", f[0], len(f[3].split()), f[3]); bad += 1
    if len(f[5].split()) > 30:
        print("REASON>30", f[0], len(f[5].split()), f[5][:120]); bad += 1
inp = [r["id"] for r in csv.DictReader(open(NIGHT + "A3/in/part-server.tsv"), delimiter="\t")]
print("rows", len(ids), "unique", len(set(ids)), "input", len(inp), "same set", set(ids) == set(inp),
      "dups", len(ids) - len(set(ids)), "problems", bad)
