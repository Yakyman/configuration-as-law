# Agreed-row sample review

Seed: `112222`. Algorithm: `random.Random(112222).sample(sorted(eligible_ids), 60)`. Eligible rows have `same=yes` in `../compare/joined.tsv` and are absent from `../adjudication/rows.tsv`; pool: 4116. The generated IDs exactly reproduce `agreed-sample.tsv` in order. The original sample is unchanged. All 60 rows have individual judgments, exact sentence quotes and evidence in `agreed-audit.tsv`.

Final counts: 48 supported decisions (46 MUST, 1 NOT, 1 UNKNOWN); 10 CONFIRMED:H1 agreed MUST decisions; 2 further agreed MUST decisions with insufficient factual evidence. The ten confirmed rows instantiate the existing setting-scope hole rather than ten new hole types. No additional hole type or outside-definition candidate was found.

The confirmed rows are:

- `nixos-9d49095d3c` — `systemd-tmpfiles-setup-dev-early.service`
- `coreos-e036cccfe6` — `tmp.mount`
- `coreos-46b677ba51` — `systemd-ask-password-console.path`
- `nixos-7c603aff27` — `systemd-soft-reboot.service`
- `freebsd-9a8da13e5c` — `/etc/newsyslog.conf`
- `nixos-2e48b3e05f` — `reload-systemd-vconsole-setup.service`
- `nixos-2353155ce2` — `/nix/store/y9r370z00fbjbc6alp311w3rymibqmbx-unit-systemd-journal-flush.service`
- `coreos-2dbd62590f` — `user@1001.service`
- `coreos-0325994aec` — `proc-sys-fs-binfmt_misc.automount`
- `debian-05069d5c04` — `systemd-update-utmp.service`

These rows match CONFIRMED-STANDALONE entries of `hole-1-extent.tsv`. The full-table search and extent are maintained there. Both stored settings and file-backed system-unit rows are affected: their evidence identifies unit fragments, and the original classifications reason about removing those definitions. Relabeling them as pure runtime operations would not answer the classified object. The text does not determine whether S2.2-7 refers to the consumer or to the reach of a setting's effects. S2.2-1/2 do not resolve that exception; S2.2-13 calls the files settings. None is established as executable code or an explicit account, superuser, firewall or other separately mandated object. S2.5-1 does not put this definition boundary outside scope.

Two factual limitations remain. `arch-18fb2985ed` (unpackaged mounts) lacks per-member provenance distinguishing generated, file-backed and runtime-reflected units; the whole-table extent likewise marks it FACTUAL-UNKNOWN. `coreos-160df5d64d` (nftables-services) has a service-file example in the joined row and configuration filenames in the allowed inventory, but their contents are not supplied. The filenames alone do not prove explicit firewall rules, and the service-file example does not establish c2's executable/library rationale. Its service/configuration members are H1 candidates, but a package containing explicit firewall rules could independently require recording. These two uncertain facts do not establish additional textual holes.

The other overlaps were tested individually. The sudo PAM object concerns the explicit right to become superuser; executable Scheme service definitions and shell scripts fall under the own-rights code clause; the authorization-rule object supplies administration rights and code. `/etc/hosts` supplies resolution across programs. The manual-directory link only provides access to documentation. `silverblue-bf56b0bc9b` remains correctly UNKNOWN under S3-2 because the legacy network file's consumer is unestablished. Actual executable packages remain recordable even where an illustrative file path names a service instead of the binary.

Inventory limitation: older raw-X1/raw-X2/raw-E6 references survive as evidence fields in `../compare/joined.tsv`; those raw directories are not supplied under `A1/in/raw/`. Available current inventories were checked. The review claims no fresh removal experiments or reconstruction of unavailable historical contents. Store-closure membership alone was not used to infer executable behavior.

Evidence correction: the initial follow-up inspected classification-folder metadata outside the authorized input set. Those references have been removed, and the final judgments rely only on the authorized joined row and supplied raw inventories. No further use of those metadata files was made.
