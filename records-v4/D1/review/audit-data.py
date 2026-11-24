"""Reproduce the review counts and whole-table candidate searches; no observations."""
import csv
import json
import re
from collections import Counter
from pathlib import Path

csv.field_size_limit(10_000_000)
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "D1/review"


def read(path):
    with path.open() as f:
        return list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))


def decode(value):
    value = value.replace('\\"', '"')
    for _ in range(3):
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('""', '"')
        try:
            return json.loads(value)
        except ValueError:
            pass
    raise ValueError(value)


joined = read(ROOT / "D1/compare/joined.tsv")
adjudicated = read(ROOT / "D1/adjudication/rows.tsv")
adj = {r["id"]: r for r in adjudicated}
unknown = []
scope = []
for row in joined:
    a = adj.get(row["id"], {})
    if a.get("verdict") == "UNKNOWN" or (
        not a and row["c1_decision"] == row["c2_decision"] == "UNKNOWN"
    ):
        unknown.append({
            "id": row["id"], "machine": row["machine"], "kind": row["kind"],
            "name": row["name"], "source": "adjudication" if a else "agreement",
            "missing_facts": a.get("note") or row["c1_reason"] + " | " + row["c2_reason"],
        })
    # Search every kind/name and all available member names, not only GAP rows.
    members = decode(row["members"]) if row["kind"].startswith("L2:") else {}
    paths = [(row["name"], "row")]
    if "file" in members:
        member_path = ROOT / "D1/in/raw" / row["machine"].removeprefix("d1-") / members["file"]
        paths += [(m["path"], m.get("type", "")) for m in read(member_path)]
    hits = {}
    for name, kind in paths:
        if row["machine"] == "d1-void" and (
            name == "/usr/lib/modules/6.12.11_1"
            or name.startswith("/usr/lib/modules/6.12.11_1/")
            or name in ("/boot/config-6.12.11_1", "/boot/vmlinuz-6.12.11_1")
        ):
            hits.setdefault("old-version-leftover", []).append(name)
        if kind != "symlink" and re.search(r"/boot/(?:initramfs-.*\.img|initrd-[^/]+)$", name):
            hits.setdefault("archive-of-code", []).append(name)
        if name.endswith("/extensions/{<REDACTED>}.xpi"):
            hits.setdefault("code-inside-program-package", []).append(name)
    for candidate, names in hits.items():
        scope.append({
            "candidate": candidate, "id": row["id"], "machine": row["machine"],
            "kind": row["kind"], "name": row["name"],
            "matching_members": " | ".join(sorted(set(names))),
            "adjudication_hole": a.get("hole", ""),
            "adjudication_verdict": a.get("verdict", "not adjudicated"),
        })


def write(name, rows):
    with (OUT / name).open("w") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


write("unknown-rows.tsv", unknown)
write("candidate-extent.tsv", scope)
additional_unknown = [
    {"id": r["id"], "machine": r["machine"], "kind": r["kind"], "name": r["name"],
     "missing_facts": "Original old-package provenance and unchanged receipt of retained members."}
    for r in scope if r["candidate"] == "old-version-leftover"
]
for row in joined:
    if row["id"] == "alma-caff428f8364f0a663721a85":
        additional_unknown.append({
            "id": row["id"], "machine": row["machine"], "kind": row["kind"], "name": row["name"],
            "missing_facts": "Compiled dconf values' contents/use: system, launch or access settings versus personal-program records.",
        })
write("additional-unknown-rows.tsv", additional_unknown)
summary = {
    "objects": len(joined),
    "matching": sum(r["c1_decision"] == r["c2_decision"] for r in joined),
    "adjudicated": len(adjudicated),
    "verdicts": dict(Counter(r["verdict"] for r in adjudicated)),
    "unknown_by_kind": dict(sorted(Counter(r["kind"] for r in unknown).items())),
    "unknown_by_machine": dict(Counter(r["machine"] for r in unknown)),
    "additional_unknown": len(additional_unknown),
    "identified_unknown_union": len({r["id"] for r in unknown + additional_unknown}),
    "candidate_counts": {
        c: dict(Counter(r["machine"] for r in scope if r["candidate"] == c))
        for c in sorted({r["candidate"] for r in scope})
    },
    "per_machine": {},
}
for machine in ("alma", "void", "gentoo", "microos", "talos"):
    rows = [r for r in joined if r["machine"] == "d1-" + machine]
    summary["per_machine"][machine] = {
        "objects": len(rows), "L1": sum(r["kind"].startswith("L1:") for r in rows),
        "L2": sum(r["kind"].startswith("L2:") for r in rows),
        "matching": sum(r["c1_decision"] == r["c2_decision"] for r in rows),
        "adjudicated": sum(r["id"] in adj for r in rows),
    }
(OUT / "counts.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
