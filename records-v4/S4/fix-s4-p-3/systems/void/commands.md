# Rehearsal commands

2026-11-23 UTC. The isolated server runner contains a copy of the existing
laboratory `lab.sh`, read-only links to the committed Void base and laboratory
keys/install resources, its own (not published: pre-observation input or preparation record), and the shared twelve slot locks.
The runner starts one durable virtual-machine unit with one slot (4 GiB,
2 vCPU; 4608 MiB unit memory limit). No source base is written.

The controller is launched from the isolated runner with:

```sh
systemd-run --user --quiet --collect --unit=fx-s4-p-3-void-rehearsal \
  --property=MemoryMax=1G --property=RuntimeMaxSec=6500 python3 run.py
```

`run.py` preserves the concrete argument arrays and scripts for:

```sh
./lab.sh new fx-s4-p-3-void void
./lab.sh run fx-s4-p-3-void --timeout 5400
./lab.sh run fx-s4-p-3-void --root --timeout 300
./lab.sh destroy fx-s4-p-3-void
```

The first run stages and executes byte-identical `check-inputs-v4/actions` files and saves
only action exit statuses and stderr. The privileged runs execute the five
`probes/*.py` query sources with `python3` on the guest. Those emit numerical
diagnostics only. Guest data is inspected in memory to reduce those diagnostics;
no rehearsal inventory is delivered or retained and no object receives a decision.
After copying diagnostics out, the isolated server runner is deleted.

Only the changed fact-specific collection routes are rerun. The existing
unchanged full collector is not replayed. Prior full collector evidence remains
`S4/rehearsal/void/round3/status.tsv` (exit 0). The new terminal-status basis is
the fact-specific attempts, not a claim that the old full run acquired these facts.
