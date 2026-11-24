# Private nft recorder native result

Development observation only; no numbered release, acceptance, or main-source mutation.
Completed 2026-11-24 around19:36UTC, within bounded private task.

| Observation | Native result |
|---|---|
| Ordinary add/delete | Exit1, authority message; declaration unchanged |
| Wrong family/table, port0, unknown handle999999 | Exit1, explicit unsupported/unknown error; declaration unchanged |
| `sudo nft add rule inet confos input tcp dport 32124 accept` | Exit0, one existing-format rule line, `RECORDED ba8a93cd0504ab884b931beefa8a4040c99038df7074e243cc6d164e81f67890; run confos apply` |
| Repeated add | Same declaration bytes/checksum |
| Before apply | Entire native JSON ruleset unchanged; port32124 absent |
| Direct `sudo /usr/sbin/nft add ...` | Exit1, Permission denied |
| Existing version/root tables/root JSON queries | Exit0; ordinary list retains root-required refusal |
| After apply | Exact APPLIED identity above; native handle3 expression tcp dport32124 accept |
| Ambiguous pending declaration with a second owner | Delete exit1 `ambiguous declaration rule ownership`; text unchanged, test then restores it |
| Abrupt termination/reboot | Same APPLIED identity and native rule present |
| `sudo nft delete rule inet confos input handle 3` | Exit0, requested line removed; native rule still present |
| Repeat delete before apply | Exit0, same declaration bytes; native rule still present |
| Apply removal, then termination/reboot | Exact APPLIED original fixture identity `6d3f50ae1a720dc5f8cb898577a94c1c14bf87f79bb7ca6efb35874efa36929f`; port32124 absent; original port32123 rule stays |

Root probe context explicitly `confos-session (enforce)` in applied/removal phases.
These are two post-success abrupt QEMU SIGTERM/restart observations, after native query assertions;
not the plan's three immediate cuts for each adding/changing/removing. No packet-delivery experiment.
The `drop` branch and additional refused syntaxes were not separately boot-tested.

Inputs/reproducible restrictions: NFT-RECORDING-DRAFT.md and nft-recording-private-build.py.
Original sealed41 nft-query SHA256 `037c8c1fe81688f5d65c30a720d94c1b9c31560d9f76607df991a688a2a2fdc6`.
Candidate SHA256 `ce46c183470ca81f20436f0c92850a741b9adddbbad3b6236cd8fff0c8b0d140`.
Private runtime SHA256 `1c0e62415aaf6e8eeca03b301c24f17745a1c2af6dded114a131d73eeba0ed21`.

Evidence: nft-recording-private.log, final-boot nft-recording-private.serial,
nft-recording-launch-failure.log (relative systemd launch path failed before work), metadata JSON,
and nft-recording-evidence.tar.gz SHA256 `d3f796825782197b47d823ede9dc1726f48212ce66eda270448240e01ee8f15e`.
Archive contains candidate runtime, fixture, scripts, logs, hashes. Probe was supplied as explicit stdin
material; observation-only status/context assertions were added between initial and applied phases.
No candidate code changed during the run. Serial file contains the final boot because harness reuses it;
main log preserves every tested command/output across boots.

Cleanup: unit confos-nft-recording-private-retry inactive, no qemu process referencing private disk,
private source/image/worktree removed after evidence archive. Worker build tree38G afterward.
Next: parent reviews candidate, broadens grammar if needed, integrates only after42 handoff, assigns
new version and runs canonical smoke/fresh-source/inventory plus case-party checks. Do not substitute
this private runtime into a published41 source archive.
