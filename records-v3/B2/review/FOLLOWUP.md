# B2 follow-up static review

Recorded 2026-11-22 UTC. Scope: static inspection of `../build/stand.py`, `capture.py`, `noexec.py`, `install-noexec.sh`, `build.py`, `selftest.py`, and `powercut.py`. No VM, probe, or formal test was run. Python AST parsing and shell syntax parsing passed. The review accepts the stated partial boundary: native file launch protection is not a closure of interpreter inputs, direct backend paths, complete transaction rollback, or base updates.

## Blocking findings

1. **Replay is ordered after SSH, leaving a post-boot interval before runtime declaration state is restored.**

   - Source: `B2/build/install-noexec.sh:22-33` gives `stand-replay.service` `After=... ssh.service ...`, whereas the no-exec service correctly says `Before=ssh.service` at `:10-20`.
   - Effect: on a fresh boot, SSH can accept a session before replay recreates runtime state such as the owned firewall table, managed services, and the selected declaration's other active effects. That interval conflicts with the power-cut requirement, which checks state after a new boot against the last reported-success declaration.
   - Fix: remove `ssh.service` from the replay unit's `After=` list and add `Before=ssh.service`; retain `After=` only for services whose state replay must consume. Verify the ordering with the service manager's dependency view and with a post-cut boot record before treating it as a power-cut pass.

2. **The power-cut runner does not check that the booted declaration is the declaration whose success marker triggered the cut.**

   - Source: `B2/build/powercut.py:13-18` reads but does not retain the declaration identifier from `SUCCESS`. After restart, `:25-26` runs only `stand-verify`.
   - Effect: verification can pass for an older declaration selected during recovery. That does not show that the state equals the declaration reported successful before the cut.
   - Fix: parse the identifier after `SUCCESS`, then after boot read the selected declaration identifier and require exact equality before `stand-verify`. Save both identifiers and every verify row in the evidence record for each add/change/remove phase.

## Material claim and test limits

3. **The supplied self-test does not perform the two-clean-installation comparison.**

   - Source: `B2/build/selftest.py:26-31` writes local snapshots only. It creates neither a second clean VM nor an invocation of `stand-compare` with two independently collected snapshots.
   - Effect: the repaired snapshot dispatch can be exercised, but these operations alone cannot evidence reproducibility. Do not label Check 3 tested or successful from the current self-test logs.
   - Fix: add a separate integration step that creates two independent clean instances, applies byte-identical declaration inputs, snapshots both, and invokes `stand-compare` on the resulting pair. This can remain outside the guest self-test if it is recorded in the build/test procedure.

4. **The user-service inventory is global-only and must not be described as a complete per-account inventory.**

   - Source: `B2/build/capture.py:64-69` queries `systemctl --global list-unit-files --state=enabled` and assumes the unit file lies below `/usr/lib/systemd/user`. It does not inspect enabled or running units for each recorded account, nor user-unit files from other valid locations.
   - Effect: the added rows improve the factory baseline but do not establish that all user services and timers are declared. This is a finite scope limit, separate from the accepted general P4 gap.
   - Fix: either construct and verify the fresh image has no per-account user-manager state before capture, then state that bounded fact, or inventory each supported account's user manager and its relevant unit search paths.

## Disposition

Do not use the power-cut runner as evidence for P2, Removal, or power-cut recovery until findings 1-2 are fixed and observed. The listener parser uses the separate TCP/UDP `ss` layouts; preserve a raw final-instance output to substantiate that layout. The no-exec mechanism's stated interpreter and direct-backend limitations are accurately partial and should remain reported as NOT CLOSED rather than treated as implementation defects.
