"""Validate the reviewed portions against the permitted inventories and assemble output."""
import collections
import csv
import json
from pathlib import Path
import re

csv.field_size_limit(100_000_000)
ROOT = Path(__file__).resolve().parents[3]
FIELDS = ["id", "source", "agreed_decision", "finding", "sentences", "reason"]
FINDINGS = ["FOLLOWS", "DOES-NOT-FOLLOW", "FACT-UNKNOWN"]


def table(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def metadata(value):
    while isinstance(value, str):
        value = json.loads(value)
    return value


reviewed = []
for portion in ["d1-first", "d1-second", "a3-first", "a3-second"]:
    rows = table(ROOT / "S2/a1/raw" / (portion + ".tsv"))
    assert len(rows) == 150
    assert list(rows[0]) == FIELDS
    reviewed.extend(rows)
by_id = {(row["source"], row["id"]): row for row in reviewed}
assert len(by_id) == 600

samples = []
inventories = {}
manifests = {}
for source in ["D1", "A3"]:
    rows = table(ROOT / "S2/sample" / ("sample-" + source + ".tsv"))
    assert len(rows) == 300
    for row in rows:
        row["source"] = source
        samples.append(row)
        machine, object_id = row["id"].split("-", 1)
        key = (source, machine)
        if key not in inventories:
            base = ROOT / source / "in/raw" / machine
            inventories[key] = {obj["id"]: obj for obj in table(base / "objects.tsv")}
            manifests[key] = table(base / "package-files.tsv")
        assert object_id in inventories[key]
assert set(by_id) == {(row["source"], row["id"]) for row in samples}

valid_sentences = set(re.findall(r"\*\*(S8\.[123]-\d+)\*\*", (ROOT / "SENTENCES.md").read_text()))
checks = collections.Counter()
runtime_exceptions = []
ordered = []
for sample in samples:
    source = sample["source"]
    machine, object_id = sample["id"].split("-", 1)
    key = (source, machine)
    original = inventories[key][object_id]
    members = metadata(original["members"])
    result = dict(by_id[(source, sample["id"])])
    assert result["agreed_decision"] == sample["decision"]
    assert result["finding"] in FINDINGS
    assert result["reason"] and len(result["reason"].split()) <= 30
    assert all("\n" not in value and "\t" not in value for value in result.values())
    citations = re.split("[,;]", result["sentences"])
    assert citations and set(citations) <= valid_sentences
    result["sentences"] = ",".join(citations)
    assert original["kind"] == sample["kind"].split(":", 1)[1]
    assert original["name"] in [sample["name"], sample["name"].replace("\\\\", "\\")]

    if original["kind"] == "package":
        decision = sample["decision"]
        checks["package " + decision] += 1
        if decision == "INSTALLED-OWN":
            assert members["reason"] == "explicit"
        elif decision == "INSTALLED-DERIVED":
            assert members["reason"] == "dependency"
        elif decision == "INSTALLED-PACKAGE":
            assert members["native_package_ids"]
        else:
            raise AssertionError(decision)

    if isinstance(members, dict) and "file" in members:
        base = ROOT / source / "in/raw" / machine
        children = table(base / members["file"])
        assert len(children) == members["count"] and members.get("complete") is True
        checks["complete immediate groups"] += 1
        if sample["decision"] == "RUNTIME":
            checks["runtime groups"] += 1
            if any(child["persistence"] != "runtime" for child in children):
                runtime_exceptions.append(sample["id"])
                assert sample["id"] in {
                    "developer-2fb915987929c6ab62914533",
                    "developer-b18fbe731b7c03811a1b2eea",
                }
                filesystem = {}
                with (base / "raw/0004-filesystem.out").open() as stream:
                    for line in stream:
                        entry = json.loads(line)
                        if "path" in entry:
                            filesystem[entry["path"]] = entry
                expected = "0x67596969" if "2fb915" in sample["id"] else "0x6e736673"
                assert all(filesystem[child["path"]]["filesystem"] == expected for child in children)
        if sample["decision"] == "PROGRAM-DERIVED":
            checks["bytecode groups with unchanged corresponding sources"] += 1
            unchanged = {item["path"] for item in manifests[key] if item["integrity"] == "unchanged"}
            for child in children:
                assert child["path"].endswith(".pyc")
                parent, filename = child["path"].split("/__pycache__/", 1)
                source_path = parent + "/" + filename.split(".cpython-", 1)[0] + ".py"
                assert source_path in unchanged
    ordered.append(result)

counts = collections.Counter(row["finding"] for row in ordered)
with (ROOT / "S2/a1/sample.tsv").open("w", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(ordered)
(ROOT / "S2/a1/DONE").write_text("".join(f"{finding}\t{counts[finding]}\n" for finding in FINDINGS))

assert table(ROOT / "S2/a1/sample.tsv") == ordered
assert sum(counts.values()) == 600
summary = {
    "rows": len(ordered),
    "unique_source_ids": len(by_id),
    "counts": {finding: counts[finding] for finding in FINDINGS},
    "cross_checks": dict(checks),
    "runtime_pseudofilesystem_exceptions_verified": runtime_exceptions,
    "max_reason_words": max(len(row["reason"].split()) for row in ordered),
}
(ROOT / "S2/a1/raw/validation.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
