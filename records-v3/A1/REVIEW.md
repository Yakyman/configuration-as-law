VERDICT: DISAGREE

# Review of A1/RESULT.md (wording trial of Section 5, first-cycle objects)

Review date: 2026-11-22 UTC. Inputs read: (not published: outside selected checks and direct evidence), `../TEXT.md` Sections 2–4, `../SENTENCES.md`, (not published: orchestration and working notes),
`RESULT.md`, `compare/STATS.md`, `adjudication/HOLES.md`, `adjudication/rows.tsv`,
`compare/joined.tsv`, plus the evidence files cited for the sampled claims. The headline `TRIAL: 2 confirmed holes`
and both hole cards hold. The disagreement concerns the established extent of hole 1 and the sample counts that rest on
it (findings 1–3).

1. **The hole-1 extent applies the single-program premise to sysctl and preset files but not to unit definitions.**
   Where: `RESULT.md`, "Established extent: 721 rows"; `review/hole-1-extent.tsv`. Evidence: 598 of the 721
   confirmed rows are unit definitions: 486 `system-unit`, 36 `user-unit` and 76 `unit-*` store objects. All 522
   `system-unit`/`user-unit` rows carry one of two templated qualifications ("File-backed X definition identified by
   its fragment path; systemd parses settings…"). No row is checked for a second program that applies the same
   file. The review uses that very check to exclude other files. `nixos-4d1b734b98` and four more rows are
   EXCLUDED-MULTIPLE-READERS because procps `sysctl --system` also applies sysctl.d files. Preset files are made
   FACTUAL-UNKNOWN because "Preset values are applied through systemctl preset" (`review/build-hole-1-extent.py`,
   line 144). Unit files have such a second applier too. systemctl(1), "Unit File Commands", `enable`: "This will
   create a set of symlinks, as encoded in the [Install] sections of the indicated unit files."
   (https://www.freedesktop.org/software/systemd/man/latest/systemctl.html). Minimal fix: check each unit-definition
   row against the review's own exclusion rule. Rows whose file systemctl also applies become
   EXCLUDED-MULTIPLE-READERS. Rows where a second applier is not established either way become FACTUAL-UNKNOWN.
   Then recompute the 721 and the per-kind counts. The hole itself does not depend on units: `nixos-195e0d56cd`
   logind.conf, `guix-f8cae21bbc` ntpd.conf and `freebsd-9a8da13e5c` newsyslog.conf remain.

2. **Unit rows are re-described as their unit files without stating that a reading was chosen.** Where:
   `RESULT.md`, "Stored native unit files and inventory rows explicitly backed by fragment files are included as
   configuration definitions". Evidence: the inventory objects of kind `system-unit` are units as the manager loaded
   them, for example `coreos-856c41bce5` "sys-kernel-tracing.mount loaded active mounted" and `coreos-101133305f`
   "initrd.target loaded inactive dead". These are the "services and timers" of Section 4.2. The text speaks of a
   service as an object with its own state: S2.1-3 "a service is enabled" and S2.4-4 "the service does not run and is
   not enabled". S2.2-7 exempts "settings", and no sentence calls a unit a setting. The review fits S2.2-7 to these
   rows only by taking the fragment file in place of the unit. Under (not published: outside selected checks and direct evidence), that choice belongs to the author.
   Minimal fix: count inventory-unit rows separately from file rows, and state that their membership depends on
   reading the unit as its fragment file. Alternatively, list them as uncertain candidates.

3. **The sample counts of CONFIRMED:H1 rest on findings 1–2.** Where: `RESULT.md`, "Agreed — … 10 candidates are
   CONFIRMED as hole 1" and "Resolved — … 2 CONFIRMED as hole 1". Evidence: in `review/agreed-audit.tsv`, 9 of
   the 10 CONFIRMED:H1 rows are unit definitions: 8 `system-unit` rows and `nixos-2353155ce2`
   unit-systemd-journal-flush.service. Only `freebsd-9a8da13e5c` newsyslog.conf is outside them. In the resolved sample,
   `coreos-4d2a7c7537` (`/etc/systemd` enablement links) is confirmed as "settings of one manager"
   (`resolved-audit.tsv`). By the systemctl(1) passage quoted in finding 1, those links are created by systemctl from
   [Install] sections and followed by the manager, so two programs apply them. Minimal fix: after fixing finding 1,
   recount both samples and report how many CONFIRMED:H1 rows remain once unit and enablement-link rows are settled.

4. **Templated evidence field in the hole-1 extent record.** Where: `review/hole-1-extent.tsv`, rows
   `nixos-4d1b734b98` and `coreos-29d771e7fa`. Evidence: the evidence column reads "A1/in/raw/nixos/system-closure.txt
   or A1/in/raw/coreos/packages.tsv" for rows of different machines. The underlying fact does hold for the NixOS row:
   `in/raw/nixos/system-closure.txt` contains a procps path. Minimal fix: name the one file and line that applies
   to each row.

5. **Saved loader sources have no stated origin.** Where: `RESULT.md`, hole 2, cites
   `(not published: adjudication scratch)` lines 1209–1272 and `(not published: adjudication scratch)`. Evidence: the
   cited lines do show the claimed order. The loader tries a compiled thunk, then the fallback cache, and then
   `scm_try_auto_compile` or `scm_primitive_load` of the source. But the result gives no upstream URL or version for
   either file, and the files sit in the adjudication's working folder. Minimal fix: add the upstream URL and release
   of both files next to the citation.

6. **Numbers: agreed.** Where: `RESULT.md`, "Numbers". Evidence: recomputed from `compare/joined.tsv` and
   `adjudication/rows.tsv`. The figures are 5,200 objects and 4,171 matching decisions (80.21 %). Cohen's kappa is
   0.48385. There are 1,084 adjudicated rows: 279 RESOLVED:MUST, 541 RESOLVED:NOT, 174 HOLE and 90 UNKNOWN. The 90
   UNKNOWN rows split into 66 stored, 15 package-owned-paths and 9 system-closure store objects. Adding 37 agreed
   UNKNOWN rows gives 127 (87 / 17 / 17 / 6). There are 820 resolved rows and 4,116 non-adjudicated agreed rows. The
   original card 1 splits 97 = 86 confirmed (68 standalone + 18 constituent) + 8 unknown + 3 excluded. The hole-1
   status counts (683 + 38 = 721) and the hole-2 counts (4 + 1 confirmed, 7 unknown, 7 fact-wrong) match their extent
   files. Input hashes in `review/counts.json` match the current files. Minimal fix: none.

7. **Samples: agreed.** Where: `RESULT.md`, "Seeded samples". Evidence: `random.Random(112221)` over the 820
   sorted resolved rows and `random.Random(112222)` over the 4,116 sorted agreed rows reproduce
   `review/resolved-sample.tsv` and `review/agreed-sample.tsv` exactly, in order. The audit columns give the reported counts:
   resolved 14 supported (20 "no" + 6 "outside" = 26 challenged), with 15 REFUTED (13 decided, 2 UNKNOWN),
   3 FACT-WRONG, 6 OUTSIDE and 2 CONFIRMED:H1; agreed 48 supported (46 MUST, 1 NOT, 1 UNKNOWN), 10 CONFIRMED:H1 and
   2 FACTUAL-UNKNOWN. Minimal fix: none, apart from finding 3.

8. **Hole 2 and the excluded instance `guix-2b6eee2e59`: agreed.** Where: `RESULT.md`, hole 2;
   `review/extent-evidence-limit.md`. Evidence: the saved `raw/narinfo/agiylfh65q5vxzmxb0351xl8ln2bdrvd.nar` is
   96 bytes and decodes to `nix-archive-1 ( type directory )`, an empty directory, matching `NarSize: 96` in the saved
   narinfo. S2.2-10 and S2.2-5 both apply literally to compiled code that has an automatic source fallback, and no
   sentence orders them. Minimal fix: none.

9. **Refuted and outside cards: agreed.** Where: `RESULT.md`, "Cards and instances not confirmed". Evidence:
   cards 2 and 3 are refuted by the conditions S2.2-4 and S2.2-5 themselves state ("the computer does and can do the
   same", "only more slowly"). Cards 6 and 7 are decided by S2.2-1 and S2.2-2, and S2.2-6 covers only past records.
   Card 5 is runtime state of the manager and kernel, which (not published: outside selected checks and direct evidence) lists under S2.5-1 as not a hole. The
   corrected fact for `guix-68f88fa3ed` is backed by the quoted GCC manual sentence for `-S`
   (`review/resolved-fact-challenges.md`). No rule beyond Sections 2–3 is used in these dispositions. Minimal fix: none.

10. **Scope and records: agreed.** Where: `A1/review/`. Evidence: no removal experiment, virtual machine or package
    action was run. Network use was limited to documentation, narinfo metadata, one 69-byte substitute stream and an
    APT source archive (`review/extent-evidence-limit.md`, `review/resolved-fact-challenges.md`). No review file references the c1
    or c2 folders. `bin/check_quotes.py A1/RESULT.md` reports 10 quotes checked, 0 not found. The result contains no
    proposal to change the text, no host names and no names of systems or vendors forbidden by (not published: outside selected checks and direct evidence). Minimal
    fix: none.
