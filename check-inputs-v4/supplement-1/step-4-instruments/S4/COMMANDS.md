# Exact operator commands

These commands are inputs for a later separately authorized observation. None was used in observation mode during S4-P. Run from the laboratory root, with `S4_INPUTS` set to the absolute directory containing the committed S4 tree and `INPUTS_COMMIT` set to the commit containing `S4/PUBLISH.list`. `C1/actions/` is the unchanged previously committed action source. Verify `S4/input-files.sha256.tsv` from the records root before staging. On the laboratory host, use a task-local runner root with the same registered read-only bases, existing keys/client and shared slot locks. Do not select a different installation or change ordinary action commands.

Verify on the records host before staging; this reads files only:

```sh
python3 S4/fix-s4-p-3/verify-inputs.py
```

Laboratory-host preflight:

```sh
command -v python3
command -v dumpsolv
```

MicroOS decoding requires the existing host `dumpsolv`. Void's archive reader requires the guest's existing Python3 and libarchive.so.13; unavailability is a recorded query failure, not an instruction to install anything. Gentoo requires four free shared slots; the runner holds them atomically for the VM, with 16 GiB and eight vCPUs. The first-night Gentoo startup cause remains unknown.

Create exactly one fresh machine for each authorized system:

```sh
./lab.sh new d1b-alma alma
./lab.sh new d1b-void void
./lab.sh new d1b-gentoo gentoo
./lab.sh new d1b-microos microos
./lab.sh new d1b-talos talos
```

The operator may schedule these to respect available shared slots. A failed creation is recorded without retry. MicroOS and Talos have no assigned ordinary actions. AlmaLinux, Void and Gentoo receive the unchanged `C1/actions/` directory and run these exact entry points as the synthetic ordinary account inside their respective guests:

```sh
bash alma.sh
bash void.sh
bash gentoo.sh
```

The action directory must be the guest working directory so its unchanged helpers are available. The host may use the existing `lab.sh run NAME --timeout N` interface to stage and start them in a durable guest session, as the original operator did. Preserve statuses and separate stderr, wait for the entire fixed action list, and do not retry or replace a failed action. Script logs/status files used only for transport control are removed before collection, as in the committed rehearsal/operator workflow. A network action can interrupt the monitoring transport without ending its detached action session.

After those actions, the exact five collector commands are:

```sh
C1_INPUTS_COMMIT="$INPUTS_COMMIT" LAB_ROOT="$PWD" "$S4_INPUTS/fix-s4-p-3/collect.sh" --observe d1b-alma D1b/raw/alma
C1_INPUTS_COMMIT="$INPUTS_COMMIT" LAB_ROOT="$PWD" "$S4_INPUTS/fix-s4-p-3/collect.sh" --observe d1b-void D1b/raw/void
C1_INPUTS_COMMIT="$INPUTS_COMMIT" LAB_ROOT="$PWD" "$S4_INPUTS/fix-s4-p-3/collect.sh" --observe d1b-gentoo D1b/raw/gentoo
C1_INPUTS_COMMIT="$INPUTS_COMMIT" LAB_ROOT="$PWD" "$S4_INPUTS/fix-s4-p-3/collect.sh" --observe d1b-microos D1b/raw/microos
C1_INPUTS_COMMIT="$INPUTS_COMMIT" LAB_ROOT="$PWD" "$S4_INPUTS/fix-s4-p-3/collect.sh" --observe d1b-talos D1b/raw/talos
```

Each output directory must be absent. Preserve each actual exit status, duration and partial output; do not repair/repeat observation commands. The operator retains the observation inventories, unlike the S4-P rehearsal harnesses which delete their inventories unread. Stop/delete each disposable copy after its authorized work:

```sh
./lab.sh destroy d1b-alma
./lab.sh destroy d1b-void
./lab.sh destroy d1b-gentoo
./lab.sh destroy d1b-microos
./lab.sh destroy d1b-talos
```

If graceful termination fails, the existing runner's `kill NAME` then `destroy NAME` cleanup fallback is used and both statuses are recorded. This is cleanup, not a new observation.

The matching party subsequently follows `S4/MATCH.md`. It supplies only the two fixed first-night unknown tables to `collector/match.py`, with no earlier decisions. No decision or hypothesis outcome is assigned by these commands or by S4-P.

Instrument commit scope is the revised PUBLISH.list. S4_INPUTS still points to the S4 runtime directory containing collector/ and fix-s4-p-3/. The entry point is fix-s4-p-3/collect.sh. The active documents/tables are S4/COLLECT.md, S4/MATCH.md, S4/MISSING.tsv, S4/HANDOFF.md and S4/fix-s4-p-3/tables/missing-row-map.tsv. S4/fix-s4-p-3/RECORDS.list is published separately and withheld from deciding parties; use CLASSIFICATION-INPUTS.list for their document handoff.

Before classification handoff, create new neutral copies with the exact five commands in HANDOFF.md. Preserve D1b/raw as collected. Send D1b/handoff together with the document allowlist and unchanged matching output; withhold the originals, the handoff audit reports, `S4/MISSING.tsv`, the missing-row map and the match-scope check during the independent decisions. If the handoff copy of a machine fails, nothing is repaired and no observation is repeated; the objects of that machine are listed by id as not delivered, receive no decision in this step, and the machine gives “?”.
