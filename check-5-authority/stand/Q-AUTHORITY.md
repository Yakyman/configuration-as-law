# BQ1 — authority (check 5)

Executor evidence; independent acceptance is separate. Fixed §9.6 and `B/PROTOCOL.md` are unchanged. Overall outcome: **?**. The missing personal-file route and stale catalog coverage are repaired and rerun; the default-Unix/P1/P4 wording question remains.

## Attribution before rerun

| Earlier reason | Kind | Disposition |
|---|---|---|
| Personal declaration accepts only catalog IDs, so cannot represent user's own executable | (a), stand coverage/representation | Add a personal-file declaration route and test it without a root bypass line. |
| Catalog/list/root scenarios passed only before stand fixes | (a), stale coverage | Rerun the existing harness plus the personal-file cases. |
| Ordinary Unix permits executing a user's 0755 file while P1/P4 forbid undeclared execution | (b), wording conflict | Keep the original failed Unix-execution assertion. Success after declaration does not settle whether §9.6 intended runtime rights outside declaration. |
| General Unix equivalence, account creation, arbitrary versions and full constitutional schema are absent | (a), broad stand scope | The finite fixture does not establish these universally; no claim of general implementation. |

## Minimal instrument extension

Copies only: `raw/q/authority/cald.py`, `apply-policy.py`, `check-authority.py`; transformation script `patch.py`. Original `B/src` is unchanged. Personal entries `local-alice-NAME` specify `executable`, `sha256`, and `version`. Source must be a regular, nonsymlink ELF under Alice's home, owned by her, readable/executable by her with parent-directory DAC checked. Apply validates before changing policy and copies matching bytes into root-owned `/var/lib/cal/executables/USER/SHA256`. The snapshot and its root-owned parent use the user’s private primary group (0550/0750); Bob cannot read it. AppArmor grants the immutable snapshot only; source paths remain blocked and root `allow_channels` stays empty. Revocation removes execution permission; payload files remain disposable instrument artifacts, not a claim to solve general payload lifecycle.

This intentionally narrow ELF route fixes the concrete `0755` personal-file case. It is an experiment procedure, not a new paper definition. Scripts/O5, arbitrary source formats, production-grade race safety, the controller trust boundary/O4, and arbitrary package dependencies are not solved. Payload creation is after validation but still not a transactional production install.

## Rerun evidence

`raw/q/authority/final-owner-authority.jsonl` (supersedes `check-authority.jsonl` after the last owner-package fix): **54 command events; 53 passed, one retained failed Unix-execution assertion**, harness rc 1. Every command, stdout/stderr, current-generation hash, and state assertion is saved. Ordinary commands use `runuser -u alice -- cal-login`; initial identity records UID 1000 and the enforcing profile. Root fixture setup is explicit.

| Case / event | Observation |
|---|---|
| `no-lists-unix-execute-own-file` | Same original 0755 file denied, rc 126; full Unix expectation remains failed. |
| `no-lists-same-file-with-exception` | Root download exception permits unchanged original, rc 0; then revoked. |
| `personal-own-executable-apply` / `personal-own-executable-run-snapshot` | Alice applies her own file's declaration and launches matching snapshot, rc 0. Effective root lists and `allow_channels` are empty. |
| `personal-source-still-not-bypass` / `personal-payload-not-writable` | Original home path denied; immutable payload write denied. |
| `bob-cannot-read-private-snapshot` | Bob cannot read snapshot (DAC), rc 1. |
| `snapshot-runs-unchanged-after-source-edit` | Snapshot bytes still equal original, edited source differs, snapshot still launches. |
| `personal-reject-stale-digest` / `personal-DAC-reject-no-execute` | Invalid digest and non-executable source rejected; current/generations unchanged. |
| `personal-revoked-snapshot-denied` | Removing entry revokes snapshot execution, rc 126. |
| `local-allowlist-permits-own-file` / `local-denylist-rejects-own-file` | Root lists cover local IDs: permit/runs, reject/unchanged. |
| Original catalog cases | Hello allowed and figlet rejected by allowlist; inverse cases under denylist; root version/scope/policy/archive contradictions rejected; root retains manual DAC override and declaration edits. |

The precise stand-side omission identified by REVIEW-2 finding 2 is closed for the tested ELF. This does not silently turn direct undeclared execution into a passing assertion. No requirement-level `0` is claimed; overall `?` remains for the explicitly undecided reading below.

## Questions for the author

**Does §9.6's default-Unix clause apply to what a user can declare, or to execution even before declaration?** Exact case: Alice owns a mode-0755 copy of `/usr/bin/hello`; no root lists and no bypass line. Unix DAC permits it. Confinement denies direct execution, and the existing root download exception permits the unchanged same file. The new personal route tests whether declaration by Alice suffices without root intervention.

Sentences to interpret together:

- P7: “By default, the user's permissions are determined by ordinary Unix permissions; root can restrict the personal declaration with an allowlist or a denylist.”
- §9.6: “or, in the absence of lists, the user cannot do what ordinary Unix permissions allow”.
- P1: “Everything that runs on the computer is recorded in the declaration.” Its exception is “through a line in the declaration or through manual actions by a person with root privileges.”
- P4: “The system provides no path for changing running components by bypassing the declaration.”
- §6 table row “Program added by a user to their personal declaration”: “Permitted by ordinary Unix permissions unless root has prohibited it through a list.”

On the declaration reading, lack of a personal-file route was a stand defect, now targeted by the extension. On a literal runtime-rights reading, the undeclared executable meets the §9.6 failure clause while allowing it conflicts with P1/P4. We do not choose between those readings or claim a property-implied `0`.

## Integration regression after the authority patch

The shared VM's existing browser/editor package-removal fix, Vim mapping, and radio `connections` schema were preserved. Original `B/src` files were not edited. Final runtime hashes and active daemon: `raw/q/authority/final-runtime.txt`; installed source copies and diffs are alongside it.

- Original lifecycle suite: `raw/q/authority/shared-lifecycle.jsonl`, rc 0, **102/102 assertions pass**, including shared alpha/beta derivative access and both archive settings.
- Real Chromium/Vim lifecycle suite: `raw/q/authority/real-lifecycle-final.jsonl`, rc 0, **82/82 assertions pass**, removal/rollback/archive under both settings. The harness's finite-scope result is `1`; this is regression evidence for the check-4 synthesis, not independent acceptance.

The VM remained running for the remaining work and cleanup. The local transfer tar was removed; raw evidence and source copies remain. The required independent review is separate.

## Final owner-package fix: superseding run

After the surviving `chromium-common` crash handler was found, the final hook installs/removes complete groups: browser = `chromium, chromium-common`; editor = `vim, vim-runtime, vim-common`. The personal-file validator/schema is unchanged. Earlier evidence above is retained; the following run is the authoritative check-5 result **after the final stand fix**:

- `raw/q/authority/final-owner-authority.jsonl`: **54 command events, 53 pass**, only `no-lists-unix-execute-own-file` fails; rc 1 deliberately retained. Outcome **?**, attribution and question unchanged.
- `raw/q/authority/final-owner-shared-lifecycle.jsonl`: **102/102 assertions pass**, rc 0.
- Final deployed sources: `raw/q/authority/final-owner-cald.py` and `final-owner-apply-policy.py`; hashes and active-daemon record: `final-owner-runtime.txt`. Daemon SHA256 `88ce1bad0162275c798f3794633d9623a357cd222076fc9730107150960961ae`; hook SHA256 `0778eb046f74b6c5d2276e826415f20e2acbf4590ce6761e8f1feaaab1d3367f`.

The earlier 82-assertion real-program lifecycle regression predates the complete owner-package fix; the later lifecycle-v3 evidence supersedes it. No shutdown was performed here.
