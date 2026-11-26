# Part 1 portable freeze

2026-11-26 UTC. The portable cases, semantic declarations, payload sources and
checking programs are frozen locally by SHA256SUMS. Nothing has been published.
The files in PUBLICATION.txt are published before the first complete run.
The revised standalone set contains 56 hashed inputs plus SHA256SUMS and
PUBLICATION.txt (58 files). SELFTEST.md records the successful self-test in a
temporary copy containing exactly those publication files.

This is **not permission to start run 1**. There is no bound source-built release
or build/INTERFACE.md. Native command bindings, source/recipe locks and rendered
declarations must be added and frozen before any system observation. The
executable fixture checker never reports a fixture as a system run. No RUN-n.md
exists and no hypothesis success is asserted.

## Publication set

- README.md — entry point, self-test command and remaining native bindings.
- STATEMENT-LABELS.json — the 34 labels from records-confos/TABLE.md, with
  source checksum; catalogue validation needs no external file.
- PROGRAMS.md — base admission decisions, written first for the builder.
- PORT.md and port.json — 153 source case/step IDs, 19 search cases individually,
  with all generated check families retained. All 122 IDs in the stand's actual
  frozen casedefs are included; the stand's narrative count is not used to invent
  two extra case IDs. CASES-EXTRA has 21 final cases and 10 first-form radio steps.
- CASES.md, casedefs.py, plans.json — 86 portable cases with required variants,
  all 34 TABLE.md statement labels, including the eight previously untested ones.
- declarations/ — semantic test, opening, account, external-source, shared-owner,
  radio and update inputs, with payloads.lock.json. Unresolved bindings remain
  explicit errors; no dummy version, source hash or native syntax is substituted.
- payloads/ — small C programs, recorded/unrecorded shell inputs, harmless values
  and the staged build recipe. Source code under the MIT licence; see LICENSE-CODE
  at the top of the repository.
- adapter.py — stand interface plans, executable stand SSH/status/candidate
  primitives, fail-closed unbound operations, fixture transport and fixture readers.
- core.py, engine.py, cli.py; run, derive, inventory, compare — portable checking,
  per-check/per-case evidence, request extraction and suite variant enumeration.
- FORMATS.md, ASSUMPTIONS.md, QUESTIONS.md, local.env.example —
  schemas, assumptions and conservative unresolved readings.
- selftest/ (excluding LAST.txt), fixtures/, tools/, SELFTEST.md — reproducible
  checker fixtures and generators. 56 tests pass; see SELFTEST.md.
- SHA256SUMS, PUBLICATION.txt and this READY.md.

Exclude working correspondence, local.env, STATE.md, TASK.md, private evidence, machine-specific paths,
credentials, temporary work and caches. SELFTEST.md is the public test record;
selftest/LAST.txt is local wrapper output. No upload or commit is performed here.

## Required binding addendum before run 1

1. Read the builder’s REQUESTS.md, STATE.md and INTERFACE.md. Match
   the named release's immutable source identity. Resolve A01–A19 in ASSUMPTIONS.md.
2. Bind only adapter.py to build, boot, native syntax/package format, transport,
   disk/live inventory, real commands and exact query parsers. Keep all policy
   assertions in the case party's programs. Use four slot locks and confos.slice;
   each test VM at most 8 GiB/4 vCPU, all work within the common aggregate ceilings.
3. Freeze exact native commands for **every** variant, all rendered declarations,
   base and test package versions/source/recipe hashes, three true system update
   states, and independent derivation inputs. A generic variant label or unresolved
   operation is not execution evidence. Keep omitted capabilities as unobserved.
4. Run fixture tests against the native parsers, including planted-object and
   read-error cases, before any complete run. Record interface/binding/source
   hashes in the run metadata. Obtain separate review through the existing work
   process; the case party does not accept its own implementation.
5. This set and the binding addendum are published before the first complete
   run. The checking tools perform no publication. First complete run uses that exact frozen
   set and one named release, with every case/variant accounted for.

Part 2 produces RUN-n.md and entries in REQUESTS.md for every fail/unobserved,
then repeats complete runs after repairs, up to eight. Hardware connection and
pairing remain distinct required actions later on the laptop. A fixture result,
a skipped optional capability or a clean VM run never substitutes for them.
