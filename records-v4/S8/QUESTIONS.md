# S8 — questions for the author and lines for later checking

Written by the second party of step 8 (performer). None of these is decided here.

## Questions for the author

1. **Does “nothing counts against” require that every coverage fact be established?** Step 8 says: “For each
   history: 1 (nothing counts against the hypothesis in it), 0 or “?” as stated above.” The causes of “?” stated above
   are an observation against without a universal argument, a history that cannot be performed, and a choice between
   two readings. Appendix A.4.1 defines “?” as “the data are insufficient”. In history 2 (and in the other histories)
   no observation against was found, but some coverage decisions stay FACT_UNKNOWN because the committed query cannot
   establish the needed fact (listed in `RECORD.md`, history 2, “unresolved”). Reading A: with no observation against,
   the history gives 1. Reading B: a history gives 1 only when absence of anything against is established; unresolved
   facts give “?”. Under the step-8 rule for two readings this record gives “?” where the outcome depends on it.

2. **May a state seen only by the history's own readback count as an observation?** In history 1, the committed
   update script read back `ed 1.22.5-1 installed` right after the root `dpkg --install` (`raw/h1/h1-update-2.stdout`),
   and the next committed observation point (after restart 2) already showed `ed 1.21.1-1` again; no committed
   observation point lies between the update and the restart. Reading A: the action's own readback, together with the
   unchanged declaration identity at the neighbouring observation points, is an observation that a built-in tool
   changed an installed package past the declaration (P4) and that the package line was not fulfilled meanwhile (P2).
   Reading B: only the three committed observations at the committed points count, so history 1 shows no observation
   against at its points. History 1 gives “?” under both readings (`RECORD.md`), so the answer changes only what is
   listed against the hypothesis.

3. **When an ordinary update is undone by the system at the next restart, was the update “performed”?** In history 1
   the second update finished (exit 0, newer version read back immediately) but did not persist after the restart
   (`raw/h1/h1-after-restart-2-package.stdout`). Appendix A.4.3: “An ordinary action from the list above cannot be
   performed through the declaration and its built-in tools.” Reading A: it was performed (with a built-in tool), so
   ordinary work is not failed. Reading B: an update that the system silently reverts was not performed through the
   declaration, so it counts against ordinary work. History 1 gives “?” under both readings.

4. **Does an action “need the network” when it fails only because a recorded network line cannot be fulfilled while
   the link is down?** (Added by correction FX-S8-O-1, from review finding 8.) Step 8: “in history 4, an action that
   needs the network counts only if it cannot be performed after the network is restored.” In history 4 the
   installation of a local artifact, which the committed inputs say “need[s] not fail merely because the link is down”
   (`check-inputs-v4/supplement-1/step-8-cases/B2/CASES-8.md`), failed while disconnected with `readback mismatch: port:udp:1` — the line of the client port
   bound to the disconnected interface ((not published: direct evidence at least 2 MB)). Reading A: the action itself needs no network,
   so its failure while disconnected counts against ordinary work (A.4.3) at once. Reading B: it failed because of the
   network loss, so it counts only if it cannot be performed after restoration (here the retry was unavailable). History
   4 gives “?” under both readings (`RECORD.md`), so the answer changes only what is listed against the hypothesis.

## Lines for later checking (outside this task)

- Two Python bytecode files `/usr/local/lib/stand/__pycache__/{guard,stand}.cpython-313.pyc` are on the image with no
  own claim (`raw/analysis/h1-after-restart-1.summary.json`, `unclaimed_unchanged_non_directories`); whether the system
  built them from recorded sources was not established. They were not changed by any history.
- The collector's machine-authority step raised `FileNotFoundError` after the first application that rewrote the
  machine declaration without a `base-files.json` manifest (all observations after the first machine application, i.e. in histories
  1 and 2); the receipt identity was recomputed offline from the saved bytes and matched (`authority` in the summaries).
- The four controller receipts `raw/h*/publication.json` contain the public record URL, which includes the public
  repository's account name, because `run.py` requires that URL; the controller output was not edited.
