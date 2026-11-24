# Offline audit transport correction

Recorded 2026-11-23 UTC. This changes the saved-evidence parser only; no guest, frozen recipe, test input or raw observation was changed.

## Observation and source

The initial partial audit rejected `boot ordering transport differs`. Compare the completed prior [boot-order output](../round-1/final-2/carried-suite/regressions/boot-order.jsonl) with the current [boot-order output](final-1/carried-suite/regressions/boot-order.jsonl). Each has one `BOOT-ORDER` JSON assertion followed by four named units, each with `Requires=`, `After=` and a blank separator. Every dependency token is identical, including multiplicity and quoted escaped unit spelling; only enumeration order within a property differs. The JSON timing values also differ, as expected for independent boots, and are not compared to old timings.

The frozen [driver](../../build/round3-driver.py), `boot_gate()` / `BOOT-ORDER` payload, calls `systemctl show UNIT -p After -p Requires`, prints that property listing, and asserts the presence of `stand-replay.service` for each named unit. A property lists dependency relations; its textual token order is not a sequence of execution steps. The parser must preserve relation membership rather than require the old enumeration order.

| Unit | Requires tokens | After tokens | Comparison |
|---|---:|---:|---|
| `getty@tty1.service` | 3 | 8 | Exact token multiplicities equal |
| `serial-getty@ttyS0.service` | 3 | 9 | Exact token multiplicities equal |
| `systemd-logind.service` | 4 | 14 | Exact token multiplicities equal |
| `systemd-user-sessions.service` | 3 | 10 | Exact token multiplicities equal |

Evidence SHA-256:

- Prior boot output: `9667fe34ef03be44867592c3ad6ed46078720ecde77eeef97b173035c62901e8`.
- Current boot output: `a3a35d387abe0ca7471a4f1c33819059a7eac87c82fdd87f58e7d4db13b4f8f4`.
- Frozen/current driver: `55f9d4eaad5bc9d1fbfe090493c428ee91be460a422d045bcaf480726368c710`; agrees with `final-1-source-sha256.json`.

## Narrow parser change

[audit.py](audit.py) now requires exactly 12 transport lines after the JSON assertion, the same four units in the same order, the exact `Requires=` / `After=` framing, and the four blank separators. It compares sorted token lists separately for each of the eight properties. Sorting preserves duplicate counts; no token is removed, decoded, renamed or accepted merely because another required token is present. Every property must still contain `stand-replay.service`. Missing or extra dependencies, units, properties or lines continue to invalidate the evidence. The JSON assertion schema and false verdict collection are unchanged.

A separate reviewed CLI-path correction resolves explicit `--final` and `--combined-declaration` arguments before path-relative reporting. Relative arguments previously turned a missing-file condition into an invalid-path error. It changes no evidence checks.

## Rechecks

The first incremental recheck after this correction exited `2` with zero invalid
sections and four incomplete sections, as independently recorded in
[the audit review](REVIEW-AUDIT.md). More completed evidence was then imported;
[the refreshed partial audit](audit-partial-carried.json) retained zero invalid
sections and waited only on combined/controller evidence. Neither stage accepted
missing evidence or changed any recorded observation.

The final command was
`python3 -B B2/raw/round-2/audit.py --output B2/raw/round-2/audit-final-1.json`.
The [complete audit](audit-final-1.json) exits `0`: all eight sections validate,
none is missing or invalid, and 19 false plus 13 not-tested/availability records
remain preserved. This is a saved-evidence consistency check; acceptance and
closure decisions belong to the [independent final review](REVIEW-FINAL.md).
