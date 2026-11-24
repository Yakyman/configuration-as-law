VERDICT: DISAGREE

Review of `S8/RECORD.md` (supplement 1, step 8) against `SUP1/step-8.md`, `TEXT.md` Section 8, Section 9.3, Appendix A.4.1 and A.4.3, `SENTENCES.md`, `check-inputs-v4/supplement-1/step-8-cases/B2/CASES-8.md` and `check-inputs-v4/supplement-1/step-8-cases/B2/OBSERVE-8.md`. All paths are relative to the night folder. The disagreement concerns the record's numbers, its statement of what the listing cannot see, and some of its evidence. It does not concern the outcomes: h1–h4 `?` and the step `?` follow the fixed rules. No `0` is claimed without an argument. No observation against is turned into a `1`. `SUP1/step-8.md` matches `check-inputs-v4/supplement-1/step-8-cases/B2/cases-8/criteria/step-8.md` (sha256 `8c9e6e6c…`). CASES-8.md and OBSERVE-8.md match the gate (not published: orchestration or scratch). Each history ran once on a freshly created guest ((not published: record outside selected evidence): `create` first; `cleanup.json`: base hash unchanged, no guest left). Nothing was repaired or repeated.

1. **What the listing cannot see is not fully stated (query failures are not reported).**
   Where: `S8/RECORD.md`, "How the observations were read" (U1–U4).
   Evidence: every summary (`S8/raw/analysis/h1-after-restart-1.summary.json`, `h1-after-restart-2`, `h1-end`, `h2-end`, `h3-end`, `h4-install-disconnected`) has 7 `query_failures`:
   - `bluetoothctl show` and `bluetoothctl devices` hit `TimeoutExpired`;
   - `busctl … org.freedesktop.timedate1` and `… locale1` exited 1 (“Name … does not exist”);
   - three `systemctl show` calls on template units exited 1.

   This leaves devices (Bluetooth) and the time and language settings of S8.2-13 unseen by native query at every point. OBSERVE-8 requires: “Record every query failure and instability”, and “a failed query is not an empty inventory”. The record names none of these. U4 only points at the `limits` field.
   Minimal fix: add a U5 that lists the seven failed queries and the settings they leave unseen, marked as not counted as recorded.

2. **U3 counts do not match the data, and U3 is not the same at every point.**
   Where: `S8/RECORD.md` line 39: “~3,170 directories and 2,913 unchanged non-directory image entries … present at every point”.
   Evidence: `unclaimed_unchanged_by_kind.directory` is 3,469 (h1-after-restart-1), 3,441 (h1-after-restart-2, h1-end), 3,471 (h2-end) and 3,474 (h4-install-disconnected). The figure 3,171 is `code_root_copies.no_declared_counterpart_directory`, a different quantity. `unclaimed_unchanged_non_directories` is 2,913 only at h1-after-restart-1; it is 2,876 at h1-after-restart-2 and h1-end, 2,912 at h2-end and 2,917 at h4-install-disconnected.
   Minimal fix: give the U3 counts per point from the summaries, and name the field each count comes from.

3. **History 4, column (b): wrong counts for the unstable `/etc` reading.**
   Where: `S8/RECORD.md` line 127: “`/etc` declaration changed three times during collection … 4 `/etc` timestamp differences”.
   Evidence: (not published: direct evidence at least 2 MB) → `disconnected_observation.identity_before`, `identity_at_comparison` and `identity_after` hold three distinct `/etc` declarations (sha256 `170b86d2…`, `5bc3280d…`, `018d47b2…`). That is two observed changes, and the `/etc` generation went 237 → 381 → 386. `S8/raw/analysis/h4-install-disconnected.summary.json` has one timestamp-only mismatch: `etc:/ssh/sshd_config.d/00-stand.conf`, 3 fields (atime, ctime, mtime). `h4-diff-initial-to-disconnected.json` lists 5 changed `/etc` paths. Neither source gives 4.
   Minimal fix: state “three distinct identities (two changes; generations 237→381→386)” and “1 path, 3 timestamp fields”.

4. **History 4, column (a): an unmatched code-root copy is omitted, and the cell contradicts itself.**
   Where: `S8/RECORD.md` lines 42–43 (“31,240+ entries under `/var/lib/stand/code-root` have the same bytes as their declared originals”) and line 127 (“none caused by the history (empty `/opt/stand/pkgs/dev-worker/bin` directories left)”).
   Evidence: in `h4-install-disconnected.summary.json`, `code_root_copies.differs_from_declared_original` is 1, and `code_root_copies_not_matching` includes `/var/lib/stand/code-root/etc/stand/read-closure`. The `/opt/stand/pkgs/dev-worker{,/bin}` directories were left by the history's interrupted install. They are unclaimed, and no decision under the four questions of Section 8.2 is written for them.
   Minimal fix: report the read-closure mismatch at the disconnected point as an unresolved (unstable) reading, not as matching. Replace “none caused by the history” with the entries the history caused and the decision (or FACT_UNKNOWN with the missing fact) for each.

5. **History 1, column (a): “none caused by the history” is contradicted by the data.**
   Where: `S8/RECORD.md` lines 56–58.
   Evidence, h1-after-restart-1: `unclaimed_changed_outside_code_root_copies` contains `/usr/bin`, `/usr/share/doc/ed`, `/usr/share/info` and `/usr/share/man/man1`. Their mtime is 18:40:52Z, during the boot after restart 1 (request at 18:40:42Z in `S8/raw/h1/restart-1.json`), and their dpkg membership includes `ed`, so the replay of update 1 changed them.
   Evidence, rows after-restart-2 and end: the record's own bullet (lines 67–70) lists entries “left by update 2”: the dpkg database, the man cache, and the executable `ed.postinst` and `ed.prerm`. Yet the table cell says “same” (none caused).
   Minimal fix: name these entries in column (a) with their decision, or with FACT_UNKNOWN and the missing fact.

6. **Wrong citation for the valid cut.**
   Where: `S8/RECORD.md` line 132: “`valid_cut: true`, `raw/h4/install/host-events.json`”.
   Evidence: `S8/raw/h4/install/host-events.json` holds only the QMP requests and replies and the event times. `valid_cut`, `active_at_cut` (stand-pkg pid 1382) and `carrier_at_cut {"ens3":"0"}` are in (not published: direct evidence at least 2 MB); `valid_cut` is also in `S8/raw/h4/observation-points.json`. The claim is true, but the cited file does not show it.
   Minimal fix: cite (not published: direct evidence at least 2 MB) (`valid_cut`, `active_at_cut`, `carrier_at_cut`).

7. **The evidence for “exact committed commands” does not contain the commands.**
   Where: `S8/RECORD.md` lines 15–16, citing `raw/hN-launch.txt`.
   Evidence: each (not published: record outside selected evidence) holds three hashes, a UTC time and “Running as unit: s8-second-hN.service”. The `systemd-run` command line itself is not saved. The unit names, the per-history `started.json` (history, seal) and the guest-session records in `commands.json` corroborate the claim but do not show the argv.
   Minimal fix: state exactly what the saved evidence shows, or save the invoked command text alongside the launch output.

8. **The step-8 network rule is applied to an action that, per the committed inputs, does not need the network.**
   Where: `S8/RECORD.md` lines 142–143: “the installation could not be performed after the network was restored … (A.4.3, the step-8 network rule)”.
   Evidence: `SUP1/step-8.md` limits the restoration clause to “an action that needs the network”. `check-inputs-v4/supplement-1/step-8-cases/B2/CASES-8.md` (History 4) states that the installation artifact is a local-input operation that “need[s] not fail merely because the link is down”. Its failure while disconnected (exit 1, `readback mismatch: port:udp:1`, in (not published: direct evidence at least 2 MB)) is an observation against ordinary work (A.4.3) in its own right, before any restoration. The outcome stays `?`: no argument from Section 8 alone, and the history is not performable.
   Minimal fix: list the disconnected failure of the install as its own observation against, and keep the unavailable retry after restoration as the separate reason the history is not performable.

9. **The comparison with the expected result overstates history 2.**
   Where: `S8/RECORD.md` line 158: “history 2 — met (2 lines unproved, U2)”.
   Evidence: the record's own h2 outcome (lines 96–97) rests on U1–U4 being unresolved, and the query failures of finding 1 are also unresolved. Only U2 is mentioned in the comparison. Histories 3 and 4 are left out of the first row without saying that they were judged not performable.
   Minimal fix: write “no unrecorded object found; coverage not established (U1–U4 and the query failures)”, and state that h3 and h4 are excluded as not performable.

10. **The record claims a review that did not yet exist, and the log gives an end time later than the files.**
    Where: `S8/RECORD.md` line 5 (“Reviewed by RV-S8-O.”) and `S8/LOG.md` (“19:04–19:10 Offline reading …”).
    Evidence: the review did not exist when the record was written. `S8/RECORD.md` and `S8/LOG.md` were last written at 19:08 UTC (file modification times), before the stated end of 19:10.
    Minimal fix: drop the review claim until a review agrees, and record the actual end time.
