VERDICT: AGREED

Independent read-only review, 2026-11-19, of `E/E3.md` against the shared rules of the checks and PAPER.html §5, §9.
Scope: (1) outcomes vs FIXED failure conditions, (2) numbers vs data files, (3) no invented classification rule,
(4) a sample of 5 claims checked against cited evidence. No blocking defects found; the findings below are notes.

1. **Outcome `?` is consistent with the fixed conditions (check 1).** O7 is an open problem (§8). None of the
   fixed failure conditions in §9.2–9.6 covers old-version compatibility with new-version state. The closest one is in
   Check 4 (a *shared* derivative "made inaccessible while a program that needs it is present"), but it covers only
   shared derivatives, and E3 does not run Check 4. E3.md declines to call this a paper-level `0` ("This is not
   itself a paper-level `0`"), so no condition was reinterpreted. Fix: none. Optional: add one line saying that `?`
   here means "no fixed check applies to O7", not "the check ran short of data".

2. **Numbers match the data files (check 2).** `raw-E3/measurements.json`: Firefox SQLite file_count 16 (old) / 17
   (new, after refusal, recovery) / 16 (restored); user_version places 74→77, cookies 12→13, content-prefs 5→6, back to
   74/12/5 after restore; all integrity_ok true; "83 regular files, differences []" (Firefox) and "14, differences []"
   (Syncthing). Syncthing config version 35 (`st-old-inspection.json`, `st-initial-config.xml`) → 37 with a v35 backup
   (`st-new-inspection.json`). Fix: none.

3. **No invented classification rule (check 3).** The data/derivative status of the profile, the index and the fixture
   files is explicitly left open ("the content's data/derivative boundary is not settled here", "may also implicate
   O1/O2. No classification rule is invented"). The options table is marked "not adopted policy". Fix: none.

4. **Sample claim A: Firefox rollback refuses with exit 0. Confirmed.** events.jsonl l.25: 115.0esr argv, returncode 0,
   stderr "This profile was last used with a newer version of this application"; l.26: screenshot_exists false,
   0.019 s. The only occurrence of `ff-rollback-direct` in events.jsonl is that argv; there is no fixture-request for
   it. Fix: none.

5. **Sample claim B: Syncthing rollback refuses. Confirmed.** `st-rollback-latest.log`: "config file version (37) is
   newer than supported version (35)"; events l.72 returncode 1, l.73 works false, l.74 file_count 14. Fix: none.

6. **Sample claim C: old snapshot restores Firefox without the new marker. Confirmed.** events l.41–42: cookie and
   storage hold only `before=v115`; l.44 works true. Fix: none.

7. **Sample claim D: Syncthing old snapshot rescans to 2 / 47, sequence 2, errors 0. Confirmed.** events l.87
   (globalFiles 2, globalBytes 47, sequence 2, errors 0, idle); l.88–89 before.txt 24 B, after.txt 23 B. Fix: none.

8. **Sample claim E: inspection side effect, 50 → 70 files. Confirmed.** events l.12: file_count 50;
   `ff-old-state.tar.gz` has 70 regular files, including 10 zero-byte WAL files and 10 SHM files of 32768 bytes. The
   positive control (l.105–108: MOZ_ALLOW_DOWNGRADE null, rc 0, screenshot 23893 B) and the export manifest (56 lines)
   also match. Fix: none.

9. **Minor, not a contradiction: an unexplained count.** events l.45 records `ff-restored-inspection` file_count 68,
   but E3.md cites only the 70-file snapshot and the 16 SQLite DBs. That gap is unexplained. It does not affect any
   outcome. Fix: one clause in E3.md saying the restored profile's file count (68) differs from the snapshot's (70)
   after the 115 run.

10. **Cleanup claim is consistent.** The E3 VM was
    PID 169415 (`infrastructure-running.txt` l.6/8), and after cleanup its unit is inactive with MainPID 0, so no E3 VM was left running. Fix: none.
