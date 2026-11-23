Final image SHA-256: `1b581030629256ccc975950a2254572217e01a2474d2a07808a8e477ca980eca`

# Supplement 1, step 6: fixed second-party inputs and commands

Recorded 2026-11-23 UTC. **PREPARATION ONLY — PUBLIC COMMITMENT PENDING.** No independent case has been attempted. The expected result, what counts against, author-reading exception for 2b, and outcome combination are fixed by [step-6.md](cases-6/criteria/step-6.md); nothing below changes them. [BUILD-4.md](BUILD-4.md) records the preparation and limits. [COMPARE-6.md](COMPARE-6.md) is the complete native query list.

The image is `VMs/cal-1123/stand/base/stand.qcow2`, relative to the server account's initial directory, mode `0444`. The prior step-5 image is preserved separately as `base/stand-step5.qcow2`, SHA-256 `5641c3c34e08dba60ae7f97511fae33d4dde48dba0ef5d93db93ab6faeb3cb79`; it is historical input, not a second step-6 candidate. Every attempt below uses only the image hash at the top.

## Complete declaration texts and identities

| Input | Complete declaration SHA-256 | Machine rows | Full text |
|---|---|---:|---|
| case-1 | `8a98779d72e3d8c2d9ffb749b4547be0a4022c2844556534139b873c15920c7c` | 562 | [case-1](cases-6/case-1/declaration.json) |
| case-2a | `fdf0bc719b4a6c0cea93b499d57abdce8187afaebdfaccf61a7b1bfed6212be2` | 563 | [case-2a](cases-6/case-2a/declaration.json) |
| case-3-before | `8a98779d72e3d8c2d9ffb749b4547be0a4022c2844556534139b873c15920c7c` | 562 | [case-3-before](cases-6/case-3-before/declaration.json) |
| case-3-after | `41299a8643722c49b79d89a09ab2577224191f9f9ed67d1da83d2eda5ce18e37` | 559 | [case-3-after](cases-6/case-3-after/declaration.json) |
| case-4-both | `b74464977fe521b6a8d236936960a46cdc9f9078989792cdcf80a032ac7bba3f` | 561 | [case-4-both](cases-6/case-4-both/declaration.json) |
| case-4-one | `dbfd73cf47caf9a6f0672b15691cbf7dacb37fa75b27eadcfa2990db4b188b7f` | 560 | [case-4-one](cases-6/case-4-one/declaration.json) |
| case-4-none | `126c4c96709075bd8dd112613c3315e5e3afa70308a1639041fc2d36f25d7289` | 559 | [case-4-none](cases-6/case-4-none/declaration.json) |

Every directory supplies `declaration.json` (the full eight-file text), `blobs.json` (all referenced immutable bytes), and unescaped copies of every constituent under `files/`. `machine.jsonl` alone is not the complete declaration. `declarations.json` gives all bundle, content-transport and constituent SHA-256 identities. Exact copies of the fixed text, numbered sentences and supplementary inputs are under `cases-6/criteria/`, with original-source identities in `criteria-sha256.json`. These files, this document, COMPARE-6, the executable runner and the recipe are bound by `raw/round-4-prep/inputs-seal.json`.

The case-1 and case-3-before bundles are intentionally identical, but are applied on different fresh copies. Removal inputs derive from their own preceding state. Their machine files preserve every surviving line byte-for-byte and in the same order; the only removed IDs are listed below. The complete filesystem declarations also contain the precise effects of system application, such as regenerated policy and removal of unit files. `removal-deltas.json` records every changed constituent/path/value; these additional system-generated differences are disclosed, not silently replaced by an independent factory state.

Package installation itself may produce intermediate automatic filesystem declarations. Those are operation results, not alternative supplied case declarations. Their order is fixed by commands below. The complete input last applied in case 2a is the same sealed `case-2a/declaration.json` and content transport on both guests; the runner records the complete-success receipt and selected complete texts. It does not reorder declaration lines to manufacture opposite orders.

## Chosen objects and exact deleted lines

| Case | Chosen objects / lines |
|---|---|
| 1 | Full inherited machine/filesystem description plus `dev-worker` version 1, `dev-service`, `dev-rule`; all requirements and why they are unambiguous are enumerated in BUILD-4 and `case-1-lines.json`. |
| 2a | Packages `bc4-account-alpha` and `bc4-account-beta`, version 1; package rows `bc4-package-alpha`, `bc4-package-beta`; contributed account rows `bc4-account-alpha`, `bc4-account-beta`. Account tuples are explicit: `bc4alpha`, UID/GID 2201; `bc4beta`, UID/GID 2202; named primary group only, `/usr/sbin/nologin`, `/home/bc4alpha` or `/home/bc4beta`, GECOS `BC4 alpha account` or `BC4 beta account`. Full artifacts are under `cases-6/artifacts/`. |
| 2b | The same chosen account packages; there is no valid omitted-identifier declaration. Do not delete fields, invent identifiers, modify the schema, or substitute a different experiment. |
| 3 | Remove exactly the full machine lines with IDs `dev-worker`, `dev-service`, `dev-rule`; their exact text and hashes are in `cases-6/removed-lines.json`. Worker executable `/opt/stand/pkgs/dev-worker/bin/worker`; service `stand-development.service`; rule `tcp dport 17777 drop`, comment `dev-rule`, family/table/chain `inet stand input`. The active service supplies a former running worker process. |
| 4 | Recorded package lines `bc4:owner-a` and `bc4:owner-b`, each version 1, require dependency-only package `bc4-shared`, version 1. First remove only `bc4:owner-a`; then remove only `bc4:owner-b`. Exact lines/hashes are in `cases-6/removed-lines.json`. The shared package has no own machine line or payload; both requirements cover its installation. |

The artifact manifest lists exact package sources, file hashes and line identities. No package is obtained from an unpinned repository during these cases. The dependency-only package's observable installed state is its actual registration in `/var/lib/stand/objects.json`; the comparison does not manufacture an installed object from the requested dependency field.

## Publication gate and host setup

The records operator must commit and publish **the unchanged sealed inputs** before the second party starts any case. Local sealing is not publication. Record the actual public URL, actual commit identity and SHA-256 of `inputs-seal.json` in a JSON file with keys `public_record_url`, `commit`, `inputs_seal_sha256`. The second party must inspect that publication and confirm its bytes. A placeholder URL, unpublished local commit or invented publication record does not satisfy this requirement.

Use the retained server laboratory directory; do not run VMs on the laptop. It contains `lab.py`, the exact read-only image, existing laboratory credentials, `build/`, `cases-6/`, these records and `raw/round-4-prep/inputs-seal.json`. The runner checks every sealed file and the full image SHA-256 before creating a case directory. Any mismatch means stop without an attempt. It also refuses existing output and existing guest names. Do not alter the seal to pass a mismatch.

```sh
cd VMs/cal-1123/stand
sha256sum base/stand.qcow2
sha256sum raw/round-4-prep/inputs-seal.json
python3 lab.py list
```

Place the actual publication record at `raw/round-4-prep/publication.json`. Each command below starts one persistent user service; wait for it to finish and save its status before starting the next. The runner itself executes no other case. It uses fresh QEMU overlays on separate VMs, 4 GiB/two vCPUs each, through the laboratory's nonblocking slot locks. Cases 1/2a have two independently writable clean installations of the same image. No result from a prior guest is reused as an installation.

```sh
systemd-run --user --unit=bc4-second-case-1 --property=WorkingDirectory="$PWD" --property=StandardOutput=append:"$PWD/raw/round-4-prep/second-case-1-controller.log" --property=StandardError=append:"$PWD/raw/round-4-prep/second-case-1-controller.log" python3 build/bc4-run-case.py 1 --publication raw/round-4-prep/publication.json
systemctl --user show bc4-second-case-1.service -p ActiveState -p ExecMainStatus

systemd-run --user --unit=bc4-second-case-2a --property=WorkingDirectory="$PWD" --property=StandardOutput=append:"$PWD/raw/round-4-prep/second-case-2a-controller.log" --property=StandardError=append:"$PWD/raw/round-4-prep/second-case-2a-controller.log" python3 build/bc4-run-case.py 2a --publication raw/round-4-prep/publication.json
systemctl --user show bc4-second-case-2a.service -p ActiveState -p ExecMainStatus

python3 build/bc4-run-case.py 2b --publication raw/round-4-prep/publication.json

systemd-run --user --unit=bc4-second-case-3 --property=WorkingDirectory="$PWD" --property=StandardOutput=append:"$PWD/raw/round-4-prep/second-case-3-controller.log" --property=StandardError=append:"$PWD/raw/round-4-prep/second-case-3-controller.log" python3 build/bc4-run-case.py 3 --publication raw/round-4-prep/publication.json
systemctl --user show bc4-second-case-3.service -p ActiveState -p ExecMainStatus

systemd-run --user --unit=bc4-second-case-4 --property=WorkingDirectory="$PWD" --property=StandardOutput=append:"$PWD/raw/round-4-prep/second-case-4-controller.log" --property=StandardError=append:"$PWD/raw/round-4-prep/second-case-4-controller.log" python3 build/bc4-run-case.py 4 --publication raw/round-4-prep/publication.json
systemctl --user show bc4-second-case-4.service -p ActiveState -p ExecMainStatus
```

Do not paste the entire block as a concurrent batch. Do not rerun a service or erase its case directory after a failure. An inactive service with exit 0 denotes completed commands, not a passing hypothesis result. Case 2b writes its non-expressibility record without starting a VM.

## Exact guest sequence performed by the runner

The frozen full implementation is [bc4-run-case.py](build/bc4-run-case.py). It records the exact argv/stdin/UTC and separate stdout, stderr and exit code of every guest operation. Input staging uses the laboratory root transport to extract the sealed case directory under `/var/lib/stand/bc4-inputs/NAME/`, outside all mediated filesystem roots. No source text is edited in a guest. Full hashes are checked before staging and recorded inside the guest afterward. The following commands describe those single executions; **do not run them again after the runner**.

For case 1, run the same two commands once on each fresh `left` and `right` guest:

```sh
python3 -B /usr/local/lib/stand/bc4_bundle.py apply /var/lib/stand/bc4-inputs/case-1
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-1/declaration.json
```

The runner also saves `/var/lib/stand/complete-last-success.json` and the complete selected description exported by `bc3-state.py export`. Record actual file hashes/permissions, unit state/hashes/text, account tuples, effective rules, every line's stated values and every unavailable observation. Compare each with the required input and compare the two guests; matching wrong values or matching query failures do not establish fulfillment.

For case 2a, both package-installation sequences use the laboratory root credential through the built-in installer. The **left** fresh guest executes:

```sh
stand-pkg install /usr/local/share/stand/bc4/package-alpha.json
stand-pkg install /usr/local/share/stand/bc4/package-beta.json
```

The **right** fresh guest executes:

```sh
stand-pkg install /usr/local/share/stand/bc4/package-beta.json
stand-pkg install /usr/local/share/stand/bc4/package-alpha.json
```

Both then execute the same final application and comparison commands:

```sh
getent passwd bc4alpha bc4beta
id bc4alpha
id bc4beta
getent group bc4alpha bc4beta
python3 -B /usr/local/lib/stand/bc4_bundle.py apply /var/lib/stand/bc4-inputs/case-2a
cat /var/lib/stand/complete-last-success.json
python3 -B /usr/local/lib/stand/bc3-state.py export
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-2a/declaration.json
```

The final application restores the **explicitly stated** required values, including account database bytes; it does not allocate defaults. Record both successful package installation receipts in their actual order, the pre-final account diagnostics, the last complete-success input hash, and all account values after the last application. Both last-applied complete hashes and all eight selected file texts must equal the one committed case-2a input. Any failure or subsequent mutation is retained, not repaired by a retry.

For cases 1 and 2a the host runs, respectively:

```sh
python3 -B build/bc4-compare.py diff raw/round-4-second-party/case-1/left-snapshot.stdout raw/round-4-second-party/case-1/right-snapshot.stdout
python3 -B build/bc4-compare.py diff raw/round-4-second-party/case-2a/left-snapshot.stdout raw/round-4-second-party/case-2a/right-snapshot.stdout
```

For case 2b there are **no installation commands**. The existing schemas require numeric identifiers both in account-own rows and in exact database bytes. Retain the source argument in BUILD-4 and the runner's `not-expressible.json`; the prescribed case result is `?`.

For case 3, apply and observe the before-state:

```sh
python3 -B /usr/local/lib/stand/bc4_bundle.py apply /var/lib/stand/bc4-inputs/case-3-before
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-3-before/declaration.json
```

Run the worker once through the **ordinary** command shell:

```sh
/opt/stand/pkgs/dev-worker/bin/worker
```

Then, through the laboratory observation credential:

```sh
/usr/bin/systemctl show stand-development.service -p MainPID -p ActiveState -p UnitFileState -p FragmentPath
python3 -B /usr/local/lib/stand/bc4-compare.py processes /opt/stand/pkgs/dev-worker/bin/worker
python3 -B /usr/local/lib/stand/bc4_bundle.py apply /var/lib/stand/bc4-inputs/case-3-after
python3 -B /usr/local/lib/stand/bc4-compare.py processes /opt/stand/pkgs/dev-worker/bin/worker
/usr/bin/systemctl is-enabled stand-development.service
/usr/bin/systemctl show stand-development.service -p MainPID -p ActiveState -p UnitFileState -p FragmentPath
/usr/sbin/nft list table inet stand
/usr/sbin/nft -j list table inet stand
stat /opt/stand/pkgs/dev-worker/bin/worker
stat /etc/systemd/system/stand-development.service
```

The runner additionally rechecks each former PID's `/proc/PID/stat` starttime and state using the exact helper code in its `former-identities` command. It distinguishes disappearance, PID reuse, zombie state and an actually surviving former process. It scans all executable/argv/mapping holders of the worker path, not just a unit's current MainPID. Collector processes themselves are excluded.

Attempt the same worker command once through the **ordinary** shell after removal, preserving its status even when failure is expected, then collect the complete after-state:

```sh
/opt/stand/pkgs/dev-worker/bin/worker
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-3-after/declaration.json
```

The first line is ordinary; the second uses the laboratory observation credential. Record the former process identity, whether it still runs, whether the executable can start, whether its installed files remain, whether the service is enabled, and whether the effective ruleset still contains the removed rule or equivalent effective text. Compare the remaining declaration with actual state as well. A comment disappearance or absent file alone is insufficient.

For case 4, the runner applies exactly this progression on one fresh guest:

```sh
python3 -B /usr/local/lib/stand/bc4_bundle.py apply /var/lib/stand/bc4-inputs/case-4-both
python3 -B /usr/local/lib/stand/bc4-compare.py package bc4-shared
python3 -B /usr/local/lib/stand/bc4-compare.py package bc4-owner-a
python3 -B /usr/local/lib/stand/bc4-compare.py package bc4-owner-b
cat /var/lib/stand/objects.json
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-4-both/declaration.json
python3 -B /usr/local/lib/stand/bc4_bundle.py apply /var/lib/stand/bc4-inputs/case-4-one
python3 -B /usr/local/lib/stand/bc4-compare.py package bc4-shared
python3 -B /usr/local/lib/stand/bc4-compare.py package bc4-owner-a
python3 -B /usr/local/lib/stand/bc4-compare.py package bc4-owner-b
cat /var/lib/stand/objects.json
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-4-one/declaration.json
python3 -B /usr/local/lib/stand/bc4_bundle.py apply /var/lib/stand/bc4-inputs/case-4-none
python3 -B /usr/local/lib/stand/bc4-compare.py package bc4-shared
python3 -B /usr/local/lib/stand/bc4-compare.py package bc4-owner-a
python3 -B /usr/local/lib/stand/bc4-compare.py package bc4-owner-b
cat /var/lib/stand/objects.json
python3 -B /usr/local/lib/stand/bc4-compare.py snapshot --bundle /var/lib/stand/bc4-inputs/case-4-none/declaration.json
```

Record the exact registration/version and origins at each stage. After the first removal, examine both the remaining package's required state and its shared dependency. After the last removal, examine whether the shared package remains installed despite having no remaining covering line. Do not replace these observations with a count of declaration lines.

## Records, failure handling and cleanup

Outputs go to `raw/round-4-second-party/case-ID/`. Retain `started.json`, actual VM argv/metadata, source identities, `commands.json`, every stdout/stderr/exit, complete success reports, complete snapshots, pair differences, any `failure.json`, publication record, and cleanup record. The runner saves evidence to the host so collecting it does not itself change a mediated guest declaration.

If an application, prerequisite launch or collector fails, the runner preserves that failure and stops the dependent sequence. Later observations are **unavailable**, not passes; it does not retry or substitute another input. Its final read-only report export and VM cleanup still run. A failed cleanup is retained in `cleanup.json`. To remove only a named remaining guest from that record, run `python3 lab.py destroy NAME` and retain the exit. Never destroy a pre-existing guest to make the fixed name available after an attempted case. Finish by saving `python3 lab.py list`; no owned disposable guest may be left running.

The performing party assigns each case `1`, `0` or `?` under the unchanged step-6 rules; another party reviews. In particular, a testbed defect is `?` unless a written argument from Section 8 alone shows any system having P1/P2/P4 must fail the same case, and separate review accepts that argument. Inexpressible/unperformed cases yield `?`. For the step: any `0` gives `0`; otherwise any `?` gives `?`; otherwise `1`. Do not turn this bounded step into the outcome of check 2 or check 3. Keep any author-reading questions unresolved and do not assign gaps to the two lists before the recorded author question is answered.
