#!/usr/bin/env python3
"""Bounded, partial translation of PAPER §§5/8/9, not an OS specification.

Usage: X/X4-venv/bin/python X/X4-model.py --out X/raw-X4/run-001
No input fact in a synthetic model is an observation of a real computer.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import platform
from pathlib import Path
from datetime import datetime, timezone
import z3 as z

ROOT = Path(__file__).resolve().parent.parent
SOURCES = {
    "C-declaration": [131], "C-components": [132], "C-derivative": [133],
    "C-data": [134], "C-generation": [135], "C-bypass": [136],
    "P1": [140], "P2": [141], "P3": [142], "P4": [143, 227],
    "P5": [144], "P6": [145, 238], "P7": [146, 242, 243],
    "O1": [200], "O2": [201], "O3": [202], "O4": [203],
    "O5": [204], "O6": [205], "O7": [206], "O8": [207], "O9": [208],
    "classification-failure": [214, 220],
    "bypass-nonenumeration": [150],
}


def conjunction(xs):
    return z.And(*xs) if xs else z.BoolVal(True)


class Model:
    """Ground roles: target x; programs p0,p1; persons root,user;
    declarations Droot,Duser; generations current,saved.
    Provenance is distinct from membership in the current declaration.
    Inputs = scenario predicates. Outputs = obligations' possible outcomes.
    """
    def __init__(self, recorded_lifecycle=False, broad_unix=False,
                 root_program_privileges=False, immediate_saved_delete=False,
                 universal_personal_inclusion=False, historical_owner_eligibility=False,
                 shared_needer_eligibility=False):
        self.profile = dict(recorded_lifecycle=recorded_lifecycle,
                            broad_unix=broad_unix,
                            root_program_privileges=root_program_privileges,
                            immediate_saved_delete=immediate_saved_delete,
                            universal_personal_inclusion=universal_personal_inclusion,
                            historical_owner_eligibility=historical_owner_eligibility,
                            shared_needer_eligibility=shared_needer_eligibility)
        names = [
            "root_records_x", "personal_records_x", "person_created_x", "x_runs",
            "bypass_line_applies", "manual_person_action", "actor_has_root",
            "executor_is_program", "changes_running_component", "writes_declaration",
            "unix_allows_execution", "unix_allows_personal_entry",
            "allowlist_enabled", "denylist_enabled", "entry_on_allowlist",
            "entry_on_denylist", "entry_contradicts_root", "personal_entry_attempt",
            "inclusion_taken", "archive_keep", "archive_delete", "disposition_completed",
            "bypass_launch_attempt",
        ]
        for p in range(2):
            names += [f"p{p}_{suffix}" for suffix in
                      ["described_at_creation", "created_x_itself", "needs_x",
                       "executes_x_internally", "recorded_now", "in_current", "in_saved"]]
        self.i = {n: z.Bool(n) for n in names}
        self.o = {n: z.Bool(n) for n in
                  ["present", "active", "accessible", "deleted", "archive_step",
                   "change_allowed", "personal_entry_admitted", "inclusion_possible",
                   "recorded_after_inclusion", "present_after_inclusion",
                   "launch_effective",
                   "derivative_is_independent_authority"]}
        i, o = self.i, self.o
        self.recorded = z.Or(i["root_records_x"], i["personal_records_x"])
        self.data = i["person_created_x"]  # pre-inclusion sufficient predicate
        self.derivative_of = [z.Or(
            z.And(i[f"p{p}_described_at_creation"], i[f"p{p}_created_x_itself"],
                  i[f"p{p}_needs_x"]), i[f"p{p}_executes_x_internally"])
            for p in range(2)]
        self.derivative = z.Or(*self.derivative_of)
        # P6's additional programs need not have created the shared object.
        self.lifecycle_owners = [z.Or(self.derivative_of[p], i[f"p{p}_needs_x"])
                                 for p in range(2)]
        # Shared need is explicitly a P6 retention ground. Whether it also
        # supplies P3's "derivative OF a recorded program" is a separate hole.
        eligibility_owners = self.lifecycle_owners if shared_needer_eligibility else self.derivative_of
        self.eligible_derivative = z.And(self.derivative, z.Or(*[
            z.And(eligibility_owners[p], z.Or(i[f"p{p}_recorded_now"],
                i[f"p{p}_described_at_creation"] if historical_owner_eligibility else z.BoolVal(False)))
            for p in range(2)]))
        self.current = z.Or(*[z.And(self.lifecycle_owners[p], i[f"p{p}_in_current"])
                                for p in range(2)])
        self.saved = z.Or(*[z.And(self.lifecycle_owners[p], i[f"p{p}_in_saved"])
                              for p in range(2)])
        self.manual_root = z.And(i["manual_person_action"], i["actor_has_root"])
        self.explicit = z.Or(i["bypass_line_applies"], self.manual_root)
        self.bypass = z.And(i["changes_running_component"], z.Not(i["writes_declaration"]))
        self.base_rules = {
            "physical.active_present": z.Implies(o["active"], o["present"]),
            "physical.accessible_present": z.Implies(o["accessible"], o["present"]),
            "physical.deleted_absent": z.Implies(o["deleted"], z.Not(o["present"])),
            "physical.running_present": z.Implies(i["x_runs"], o["present"]),
            # A feasible attempted bypass launch is a scenario, not a new class.
            # Its effect remains free until a property requires it. Permission
            # by itself does not force execution when no launch is attempted.
            "action.launch_attempt_is_bypass": z.Implies(i["bypass_launch_attempt"], self.bypass),
            "action.launch_requires_attempt": z.Implies(o["launch_effective"], i["bypass_launch_attempt"]),
            "physical.launched_present": z.Implies(o["launch_effective"], o["present"]),
            "single.archive_setting": z.Not(z.And(i["archive_keep"], i["archive_delete"])),
            # One list mode per scenario is a bound, not a claim about allowed designs.
            "bound.single_list_mode": z.Not(z.And(i["allowlist_enabled"], i["denylist_enabled"])),
        }
        self.rules = {f"P{k}": {} for k in range(1, 8)}
        self.add("P1", "record_runs", z.Implies(z.And(z.Or(i["x_runs"], o["launch_effective"]), z.Not(self.explicit)), self.recorded))
        self.add("P2", "present", z.Implies(self.recorded, o["present"]))
        self.add("P2", "present_after_inclusion", z.Implies(o["recorded_after_inclusion"], o["present_after_inclusion"]))
        self.add("P3", "remainder", z.Implies(z.And(o["present"], z.Not(self.recorded)),
                                              z.Or(self.data, self.eligible_derivative)))
        self.add("P3", "one_authority", z.Implies(self.derivative, z.Not(o["derivative_is_independent_authority"])))
        self.add("P4", "no_implicit_bypass", z.Implies(z.And(self.bypass, z.Not(self.explicit)),
                                                      z.Not(o["change_allowed"])))
        self.add("P4", "explicit_permission_effective", z.Implies(z.And(self.bypass, self.explicit),
                                                                  o["change_allowed"]))
        # P4 / section 9.3: an applicable line must take effect for a feasible
        # attempted launch. Target provenance and declaration membership remain
        # context inputs; section 5.3 does not itself prove their negatives.
        self.add("P4", "permitted_launch_effective", z.Implies(
            z.And(i["bypass_launch_attempt"], i["bypass_line_applies"]), o["launch_effective"]))
        self.add("P5", "inclusion_possible", z.Implies(z.Or(self.derivative, self.data), o["inclusion_possible"]))
        self.add("P5", "inclusion_transition", z.Implies(z.And(i["inclusion_taken"], z.Or(self.derivative, self.data)),
                                                        o["recorded_after_inclusion"]))
        # Partial translation: recorded objects' residual lifecycle is not settled.
        # This guard omits that domain, NOT a rule that inclusion cancels lifecycle.
        lifecycle = self.derivative if recorded_lifecycle else z.And(self.derivative, z.Not(self.recorded))
        self.lifecycle_scope = lifecycle
        self.add("P6", "surviving_owner", z.Implies(z.And(lifecycle, z.Or(self.current, self.saved)),
                                                  z.And(o["present"], z.Not(o["deleted"]))))
        self.add("P6", "current_owner", z.Implies(z.And(lifecycle, self.current),
                                                 z.And(z.Not(o["archive_step"]), o["accessible"])))
        self.add("P6", "no_current_archive", z.Implies(z.And(lifecycle, z.Not(self.current)),
                                                       z.And(o["archive_step"], z.Not(o["active"]))))
        self.add("P6", "keep_archive", z.Implies(z.And(lifecycle, z.Not(self.current), i["archive_keep"]),
                                                z.And(o["present"], z.Not(o["deleted"]))))
        no_retention = z.BoolVal(True) if immediate_saved_delete else z.Not(self.saved)
        self.add("P6", "completed_delete_setting", z.Implies(z.And(lifecycle, z.Not(self.current), no_retention,
                                                                 i["archive_delete"], i["disposition_completed"]), o["deleted"]))
        permitted_entry = z.And(z.Not(i["entry_contradicts_root"]), i["unix_allows_personal_entry"],
                               z.Implies(i["allowlist_enabled"], i["entry_on_allowlist"]),
                               z.Not(z.And(i["denylist_enabled"], i["entry_on_denylist"])))
        self.add("P7", "personal_constitution_and_lists", z.Implies(i["personal_entry_attempt"],
                                                                 o["personal_entry_admitted"] == permitted_entry))
        self.add("P7", "manual_root_retains_privileges", z.Implies(z.And(self.bypass, self.manual_root), o["change_allowed"]))
        if broad_unix:
            self.add("P7", "BRANCH_execution_scope", z.Implies(z.And(self.bypass, z.Not(i["actor_has_root"]),
                            i["unix_allows_execution"], z.Not(i["allowlist_enabled"]), z.Not(i["denylist_enabled"])),
                            o["change_allowed"]))
        if root_program_privileges:
            self.add("P7", "BRANCH_root_executor_scope", z.Implies(z.And(self.bypass, i["actor_has_root"],
                                                                         i["executor_is_program"]), o["change_allowed"]))
        if universal_personal_inclusion:
            self.add("P5", "BRANCH_every_personal_route", z.Implies(z.And(i["personal_entry_attempt"],
                                                               z.Or(self.derivative, self.data)), o["personal_entry_admitted"]))

    def add(self, prop, name, expr):
        self.rules[prop][f"{prop}.{name}"] = expr

    def prop(self, name):
        return conjunction(list(self.rules[name].values()))

    def base(self):
        return conjunction(list(self.base_rules.values()))

    def bind(self, facts):
        symbols = self.i | self.o
        return {f"fact.{name}": symbols[name] == value for name, value in facts.items()}

    def derived(self):
        return {"recorded": self.recorded, "data_provenance": self.data,
                "derivative": self.derivative, "P3_eligible_derivative": self.eligible_derivative,
                "current_owner": self.current, "saved_owner": self.saved,
                "explicit_bypass": self.explicit, "bypass_change": self.bypass,
                "P6_in_translated_domain": self.lifecycle_scope}


class Runner:
    def __init__(self, out):
        self.out = out
        (out / "queries").mkdir(parents=True, exist_ok=False)
        self.results = []

    def check(self, name, m, rules, note="", expected=None, projected_outputs=False,
              source_ids=None, named_obligations=None):
        solver = z.Solver()
        solver.set(timeout=5000, random_seed=0)
        for tag, expression in rules.items():
            solver.assert_and_track(expression, z.Bool("track." + tag))
        # assert_and_track adds implicit assumptions. SMT-LIB replay must assert
        # these tracking literals explicitly; solver.sexpr() alone omits them.
        path = self.out / "queries" / (name + ".smt2")
        text = solver.sexpr() + "\n" + "\n".join(f"(assert |track.{tag}|)" for tag in rules) + "\n(check-sat)\n"
        path.write_text(text)
        answer = solver.check()
        result = dict(name=name, status=str(answer), note=note,
                      smt2=str(path.relative_to(ROOT)),
                      rule_sources={tag: SOURCES.get(tag.split('.')[0], []) for tag in rules},
                      formulae={tag: str(expr) for tag, expr in rules.items()})
        if source_ids is None:
            source_ids = sorted(set(tag.split('.')[0] for tag in rules if tag.split('.')[0] in SOURCES))
            # These definitions expand the context predicates in this model;
            # a source link is not a claim that arbitrary input facts are observed.
            source_ids += ["C-declaration", "C-components", "C-derivative", "C-data", "C-generation", "C-bypass", "bypass-nonenumeration"]
        result["source_ids"] = list(dict.fromkeys(source_ids))
        result["source_lines"] = {sid: SOURCES[sid] for sid in result["source_ids"]}
        result["named_obligations"] = named_obligations or {
            tag: {"formula": str(expr), "source_id": tag.split('.')[0] if tag.split('.')[0] in SOURCES else "instrument/context"}
            for tag, expr in rules.items()}
        result["semantic_profile"] = m.profile
        if answer == z.sat:
            model = solver.model()
            result["inputs"] = {n: z.is_true(model.eval(v, model_completion=True)) for n, v in m.i.items()}
            if projected_outputs:
                result["outputs_projected"] = "Outcomes are quantified. Use fixed-context left/right witnesses, never outer model-completion defaults."
            else:
                result["outputs"] = {n: z.is_true(model.eval(v, model_completion=True)) for n, v in m.o.items()}
            result["derived"] = {n: z.is_true(model.eval(v, model_completion=True)) for n, v in m.derived().items()}
        elif answer == z.unsat:
            result["unsat_core"] = [str(x) for x in solver.unsat_core()]
        else:
            result["reason_unknown"] = solver.reason_unknown()
        if expected is not None:
            result["expected"] = expected
            result["expectation_met"] = str(answer) == expected
        self.results.append(result)
        (self.out / "queries" / (name + ".json")).write_text(json.dumps(result, indent=2) + "\n")
        return result

    def rules(self, m, props=(), facts=None):
        rules = dict(m.base_rules)
        for p in props:
            rules.update(m.rules[p])
        if facts:
            rules.update(m.bind(facts))
        return rules

    def conflict(self, name, m, a, b, condition=None, note="", paper_props=(), source_ids=None):
        # A pair conflicts at c iff each can be fulfilled at c, but not jointly.
        # Outcomes are existentially projected; the common context remains free.
        # No outcome is fixed in order to fabricate a clash.
        outcomes = list(m.o.values())
        left = z.Exists(outcomes, z.And(m.base(), a))
        right = z.Exists(outcomes, z.And(m.base(), b))
        together = z.Exists(outcomes, z.And(m.base(), a, b))
        condition = z.BoolVal(True) if condition is None else condition
        ids = list(paper_props) + ["C-declaration", "C-derivative", "C-data", "C-generation", "C-bypass", "bypass-nonenumeration"]
        if source_ids is not None:
            ids += source_ids
        named = {tag: {"formula": str(expr), "source_id": prop}
                 for prop in paper_props for tag, expr in m.rules[prop].items()}
        named.update({"left": {"formula": str(a), "source_id": "instrument/grouping"},
                      "right": {"formula": str(b), "source_id": "instrument/grouping"}})
        return self.check(name, m, {"search.conflicting_obligations": z.And(condition, left, right, z.Not(together))}, note,
                          projected_outputs=True, source_ids=ids, named_obligations=named)

    def pair(self, profile, m, a, b):
        name = f"pair-{profile}-{a}-{b}"
        result = self.conflict(name, m, m.prop(a), m.prop(b), note="SAT = conditional common-context conflict; UNSAT = none in this partial projection",
                               paper_props=(a, b), source_ids=["O1", "O2", "O3", "O4", "O5", "O6", "O9"])
        if result["status"] == "sat":
            facts = result["inputs"]
            for suffix, ps in [("left", [a]), ("right", [b]), ("joint", [a, b])]:
                self.check(name + "-" + suffix, m, self.rules(m, ps, facts),
                           expected="unsat" if suffix == "joint" else "sat")
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.relative_to(ROOT / "X" / "raw-X4")
    protocol = ROOT / "X/X4-PROTOCOL.md"
    digest = hashlib.sha256(protocol.read_bytes()).hexdigest()
    assert digest == (ROOT / "X/raw-X4/protocol.sha256").read_text().split()[0], "Frozen protocol changed"
    runner = Runner(out)
    metadata = {
        "utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
        "z3": z.get_full_version(), "protocol_sha256": digest,
        "model_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "paper_sha256": hashlib.sha256((ROOT / "X/raw-X4/PAPER.html").read_bytes()).hexdigest(),
        "bound": {"target_objects": 1, "owner_programs": 2, "persons": ["root", "user"],
                  "declarations": {"Droot": {"owner": "root", "designated_by": "root"},
                                   "Duser": {"owner": "user", "designated_by": "user", "subordinate_to": "Droot"}},
                  "generations": ["current", "saved"], "inclusion_snapshots": ["before", "after"]},
        "sources": SOURCES,
        "scope": "Target-local obligations only. Program/person kinds and manual intent are inputs. No host policy implemented. No resolution of O1–O9.",
        "unknown_predicates": "Unbound inputs are free completions, never observed false. Recorded data class persistence is not asserted. Internal execution is historical provenance, not concurrent execution after owner removal.",
    }
    (out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    m = Model()
    runner.check("control-consistent-all", m, runner.rules(m, m.rules, {"root_records_x": True, "x_runs": True}), expected="sat")
    runner.conflict("control-true-conflict", m, m.o["present"], z.Not(m.o["present"]), note="Instrument control, not a paper claim")
    runner.conflict("control-compatible", m, m.o["present"], m.o["present"], note="Instrument control, not a paper claim")

    classes = {"recorded": m.recorded, "derivative": m.derivative, "data": m.data}
    for a, b in itertools.combinations(classes, 2):
        runner.check(f"overlap-{a}-{b}", m,
                     runner.rules(m) | {"search.overlap": z.And(m.o["present"], classes[a], classes[b])},
                     note="Sufficient/provenance predicate overlap; recorded class persistence remains O3, not an exclusivity claim",
                     source_ids=["C-declaration", "C-derivative", "C-data", "P5", "O2", "O3"])
    runner.check("no-class-closed-predicates", m, runner.rules(m) | {
        "search.none": z.And(m.o["present"], z.Not(m.recorded), z.Not(m.derivative), z.Not(m.data))},
        note="Synthetic closed-vocabulary countermodel only; all negative predicates require independent real evidence",
        source_ids=["C-declaration", "C-derivative", "C-data", "P3", "classification-failure"])
    # Observations do not establish execution: both completions are retained.
    for executed in [False, True]:
        runner.check(f"epistemic-editor-code-{int(executed)}", m, runner.rules(m, facts={
            "present": True, "person_created_x": True, "p0_executes_x_internally": executed}),
            note="Person-created editor settings scenario; internal execution is a completion, not measured in E1; recorded status is free")

    profiles = {
        "partial": Model(),
        "retain_recorded_derivative": Model(recorded_lifecycle=True),
        "broad_unix_execution": Model(broad_unix=True),
        "root_executor_privileges": Model(root_program_privileges=True),
        "universal_personal_inclusion": Model(universal_personal_inclusion=True),
    }
    matrix = []
    class_conflicts = []
    for profile, pm in profiles.items():
        for a, b in itertools.combinations(pm.rules, 2):
            r = runner.pair(profile, pm, a, b)
            matrix.append({"profile": profile, "pair": [a, b], "status": r["status"], "query": r["name"]})
        if profile in ["partial", "retain_recorded_derivative"]:
            predicates = {"recorded": pm.recorded, "derivative": pm.derivative, "data": pm.data}
            # Data has no opposing nonarchival/deletion duty in the paper.
            duties = {"recorded": pm.prop("P2"), "derivative": pm.prop("P6"), "data": z.BoolVal(True)}
            for a, b in itertools.combinations(predicates, 2):
                r = runner.conflict(f"class-conflict-{profile}-{a}-{b}", pm, duties[a], duties[b],
                                    z.And(predicates[a], predicates[b]),
                                    note="Class obligations; overlap does not imply an opposite data preservation duty",
                                    paper_props=tuple(p for cls,p in [("recorded","P2"),("derivative","P6")] if cls in (a,b)),
                                    source_ids=["C-declaration", "C-derivative", "C-data", "P5", "O2", "O3"])
                class_conflicts.append({"profile": profile, "classes": [a, b], "status": r["status"], "query": r["name"]})
                if r["status"] == "sat":
                    for suffix, duty in [("left", duties[a]), ("right", duties[b]), ("joint", z.And(duties[a], duties[b]))]:
                        selected_classes = [a] if suffix == "left" else [b] if suffix == "right" else [a, b]
                        selected_props = [p for cls, p in [("recorded", "P2"), ("derivative", "P6")] if cls in selected_classes]
                        runner.check(r["name"] + "-" + suffix, pm,
                                     runner.rules(pm, selected_props, facts=r["inputs"]),
                                     expected="unsat" if suffix == "joint" else "sat")

    d = {"root_records_x": False, "personal_records_x": False, "p0_executes_x_internally": True,
         "p0_in_current": False, "p1_executes_x_internally": False,
         "p1_created_x_itself": False, "p1_needs_x": False, "p1_in_current": False, "p1_in_saved": False}
    runner.check("lifecycle-saved-owner-delete-setting", m, runner.rules(m, ["P6"], d | {
        "p0_in_saved": True, "archive_delete": True, "disposition_completed": True}), expected="sat")
    runner.check("lifecycle-shared-current-owner", m, runner.rules(m, ["P6"], d | {
        "p1_executes_x_internally": True, "p1_in_current": True}), expected="sat")
    runner.check("lifecycle-shared-needer-not-creator", m, runner.rules(m, ["P6"], d | {
        "p0_in_saved": False, "p1_needs_x": True, "p1_in_current": True,
        "archive_delete": True, "disposition_completed": True}), expected="sat")
    runner.check("lifecycle-kept-archive-present-P2-compatible", Model(recorded_lifecycle=True),
        runner.rules(Model(recorded_lifecycle=True), ["P2", "P6"], d | {
            "root_records_x": True, "p0_in_saved": False, "archive_keep": True}), expected="sat")
    for present in [False, True]:
        runner.check(f"lifecycle-missing-policy-present-{int(present)}", m, runner.rules(m, ["P6"], d | {
            "p0_in_saved": False, "archive_keep": False, "archive_delete": False, "present": present}),
            note="Two permitted completions demonstrate missing archive-fate rule O6", expected="sat")
    immediate = Model(immediate_saved_delete=True)
    runner.check("BRANCH-immediate-delete-saved-internal-P6-conflict", immediate,
        runner.rules(immediate, ["P6"], d | {"p0_in_saved": True, "archive_delete": True, "disposition_completed": True}),
        note="Conditional timing reading, not unconditional inconsistency; §9.5 explicitly protects saved-owner objects", expected="unsat")
    runner.check("authority-manual-root-compatible", m, runner.rules(m, ["P4", "P7"], {
        "changes_running_component": True, "writes_declaration": False, "manual_person_action": True,
        "actor_has_root": True, "bypass_line_applies": False}), expected="sat")
    runner.check("authority-root-program-no-manual-no-line", m, runner.rules(m, ["P4", "P7"], {
        "changes_running_component": True, "writes_declaration": False, "manual_person_action": False,
        "actor_has_root": True, "executor_is_program": True, "bypass_line_applies": False}), expected="sat")
    runner.check("authority-explicit-line-effective", m, runner.rules(m, ["P4"], {
        "changes_running_component": True, "writes_declaration": False, "bypass_line_applies": True}), expected="sat")
    runner.check("inclusion-personal-denial-root-route-open", m, runner.rules(m, ["P5", "P7"], {
        "person_created_x": True, "personal_entry_attempt": True, "entry_contradicts_root": True}), expected="sat")
    runner.check("inclusion-transition-present", m, runner.rules(m, ["P2", "P5"], {
        "person_created_x": True, "inclusion_taken": True}), expected="sat")
    # Historical P1/P3 check fixes observed running as an input. It cannot
    # answer the P3/P4 effect question; the free-effect checks below do that.
    bypass_none = {"x_runs": True, "root_records_x": False, "personal_records_x": False,
                   "bypass_line_applies": True, "person_created_x": False,
                   "p0_executes_x_internally": False, "p1_executes_x_internally": False,
                   "p0_created_x_itself": False, "p1_created_x_itself": False}
    runner.check("explicit-bypass-none-P1", m, runner.rules(m, ["P1"], bypass_none), expected="sat")
    runner.check("explicit-bypass-none-P3", m, runner.rules(m, ["P3"], bypass_none),
                 note="Classification violation under synthetic negatives, not P1/P3 opposing duties", expected="unsat")
    # Minimal readable witnesses avoid irrelevant true inputs in solver-selected
    # contexts. All unspecified INPUT predicates are false here by explicit
    # synthetic construction, never by inference about an observed object.
    def canonical(name, cm, props, changes, expected):
        facts = {key: False for key in cm.i} | changes
        return runner.check(name, cm, runner.rules(cm, props, facts),
                            note="Fully specified synthetic context; see left/right outputs and joint core", expected=expected)
    scenarios = [
        ("recorded-delete", Model(recorded_lifecycle=True), ["P2", "P6"],
         {"root_records_x": True, "p0_described_at_creation": True, "p0_created_x_itself": True,
          "p0_needs_x": True, "archive_delete": True, "disposition_completed": True}),
        ("ordinary-unix", Model(broad_unix=True), ["P4", "P7"],
         {"changes_running_component": True, "unix_allows_execution": True}),
        ("root-program", Model(root_program_privileges=True), ["P4", "P7"],
         {"changes_running_component": True, "actor_has_root": True, "executor_is_program": True}),
        ("historic-archive", Model(), ["P3", "P6"],
         {"p0_described_at_creation": True, "p0_created_x_itself": True,
          "p0_needs_x": True, "archive_keep": True}),
        ("overstrong-personal", Model(universal_personal_inclusion=True), ["P5", "P7"],
         {"person_created_x": True, "personal_entry_attempt": True,
          "unix_allows_personal_entry": True, "entry_contradicts_root": True}),
        ("permitted-bypass-no-class", Model(), ["P3", "P4"],
         {"bypass_launch_attempt": True, "changes_running_component": True,
          "bypass_line_applies": True}),
        ("permitted-launch-completed-delete", Model(), ["P4", "P6"],
         {"bypass_launch_attempt": True, "changes_running_component": True,
          "bypass_line_applies": True, "p0_described_at_creation": True,
          "p0_created_x_itself": True, "p0_needs_x": True,
          "archive_delete": True, "disposition_completed": True}),
    ]
    for label, cm, props, facts in scenarios:
        for suffix, selected in [("left", props[:1]), ("right", props[1:]), ("joint", props)]:
            canonical("canonical-" + label + "-" + suffix, cm, selected, facts,
                      "unsat" if suffix == "joint" else "sat")
    historic = scenarios[3][3]
    canonical("canonical-historic-archive-historical-scope", Model(historical_owner_eligibility=True),
              ["P3", "P6"], historic, "sat")
    shared_context = historic | {"p1_needs_x": True, "p1_recorded_now": True, "p1_in_current": True}
    canonical("canonical-shared-needer-direct-origin-eligibility", Model(), ["P3", "P6"], shared_context, "unsat")
    canonical("canonical-shared-needer-broad-eligibility-BRANCH", Model(shared_needer_eligibility=True),
              ["P3", "P6"], shared_context, "sat")
    bypass_context = scenarios[5][3]
    canonical("canonical-permitted-bypass-data-completion", Model(), ["P1", "P3", "P4"],
              bypass_context | {"person_created_x": True}, "sat")
    canonical("canonical-permitted-bypass-derivative-completion", Model(), ["P1", "P3", "P4"],
              bypass_context | {"p0_executes_x_internally": True, "p0_recorded_now": True}, "sat")
    canonical("canonical-permitted-bypass-no-attempt", Model(), ["P1", "P3", "P4"],
              bypass_context | {"bypass_launch_attempt": False}, "sat")
    canonical("canonical-bypass-no-permission", Model(), ["P1", "P3", "P4"],
              bypass_context | {"bypass_line_applies": False}, "sat")
    canonical("canonical-permitted-bypass-separately-recorded", Model(), ["P1", "P3", "P4"],
              bypass_context | {"root_records_x": True}, "sat")
    # Remove only the new positive effect duty: confirms the old instrument's
    # false negative, without adopting that omission as a paper interpretation.
    old_effect = Model()
    del old_effect.rules["P4"]["P4.permitted_launch_effective"]
    canonical("control-omitted-launch-effect", old_effect, ["P3", "P4"], bypass_context, "sat")
    # The bounded state projection aligns launch effect and completed deletion.
    # The paper does not require that timing; retain it as a conditional result,
    # and expose both ways in which that extra alignment disappears.
    delete_context = scenarios[6][3]
    canonical("canonical-permitted-launch-delete-not-completed", Model(), ["P4", "P6"],
              delete_context | {"disposition_completed": False}, "sat")
    canonical("canonical-permitted-launch-keep-archive", Model(), ["P4", "P6"],
              delete_context | {"archive_delete": False, "archive_keep": True}, "sat")
    results = runner.results
    counts = {s: sum(r["status"] == s for r in results) for s in ["sat", "unsat", "unknown"]}
    summary = {"solver_calls": len(results), "counts": counts, "property_pair_matrix": matrix,
               "class_conflicts": class_conflicts,
               "failed_controls": [r["name"] for r in results if r.get("expectation_met") is False],
               "counterexample_pair_count": sum(r["status"] == "sat" for r in matrix),
               "protocol_unchanged": hashlib.sha256(protocol.read_bytes()).hexdigest() == digest}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out / "results.jsonl").write_text("".join(json.dumps(r) + "\n" for r in results))
    print(json.dumps({k: v for k, v in summary.items() if k not in ["property_pair_matrix", "class_conflicts"]}, indent=2))


if __name__ == "__main__":
    main()
