# Initial independent review of C1-KIT

Reviewed 2026-11-23 UTC. Scope: the published rules, the laboratory runner and
documentation, the Debian instrument records, and the available Void recipe and
status records. This review used host-authored files only. It ran no guest command
and inspected no guest disk or guest state.

## Findings

1. **The Void installer does not implement the required shared-slot allocation rule.**
   `install/void/start-installer.sh:4-5` locks only `slots/slot-5.lock` and exits 75
   when that one slot is occupied. `COMMON.md` requires trying slots 1 through 12
   and treating the pool as unavailable only when all slots are busy. The completed
   run did hold one slot, so this does not invalidate that run, but the published
   recipe is not repeatable under the stated shared-pool conditions.

2. **The runner validation is not self-contained and does not substantiate all of
   its stated expectations.** `raw/runner-expectations.md:10-13` begins with creation
   of a Debian VM. `install/debian/validate.py` instead assumes `kit-debian` already
   exists and its first operation is `run`; `raw/debian/runner-validation.json`
   consequently has no Debian `new` result. The same validation does not exercise
   the documented timeout while reading standard input or waiting for `run.lock`.
   It establishes output/status propagation, a running-command timeout, copy-out,
   stop/start/destroy, and the two-slot server variant, but not the full claim in
   `LAB.md:28-36`.

3. **Void's signature trust anchor has incomplete provenance.**
   `install/void/download.sh:9` fetches the verification key from the mutable
   `master` branch of the upstream source repository. The records preserve the key
   and successful minisign result, but give neither an immutable source revision nor
   an independently published fingerprint tying that exact key to the release.
   Therefore the records prove that the image checksum list matches the downloaded
   key, but do not make the authenticity of that key reproducibly auditable.

4. **`stop` and `kill` are outside the per-machine lifecycle lock.**
   `lab.sh:227-229` serializes only `new`, `start`, and `destroy`. A concurrent
   `stop` or `kill` can race with `start` or `destroy`, despite all being lifecycle
   operations on the same machine. The normal sequential use recorded here is not
   affected, but the command interface does not enforce its own lifecycle safety.

5. **The pre-observation commit condition remains an unverified gate.** The available
   records contain no commit identifier covering the exact runner, recipes, release
   selections, and ordinary-action inputs. This is not yet a check failure because
   the reviewed activity was preparation and status-only smoke testing. Before any
   check inventory or other observation, Appendix A.4.1 and Section 9.1 require a
   repository commit of the concrete inputs, and its identity should be recorded.

## Confirmed properties and boundary

- The runner's disposable disks are qcow2 overlays over a top-level backing whose
  writable mode bits are rejected by `lab.sh:191-195`. The Debian recipe also makes
  both the downloaded image and intermediate base read-only. The Void status and
  successful `new` record are consistent with a read-only registered base; the
  reviewed files do not contain a saved mode/chain dump for independent confirmation.
- QEMU inherits the acquired slot descriptors, so shared runner slots remain held
  for the VM lifetime. The two-slot Debian server metadata is exercised by the saved
  validation. The runner uses loopback-only forwarded SSH with key authentication;
  it disables guest host-key verification and has a small close-before-bind race
  while allocating the forwarded port, but no failure from either condition is in
  the available record.
- The Void bootstrap discards console bytes. Its later console reader retains only
  the predeclared `LAB_STATUS=<number>` marker. The saved timeline contains exit
  statuses and planned setup facts, not an inventory or diagnostic guest output.
  On the reviewed evidence, the preparation stayed within the no-observation
  boundary.
- All reviewed shell and Python sources parse successfully. No guest-side test was
  run by this review.

Initial review status: **changes required before the kit is treated as fully
reproducible; no evidence of a prohibited check observation in the reviewed portion.**

## Follow-up review, 2026-11-23 UTC

This follow-up reviewed the corrections, the completed AlmaLinux artifacts, and
the pre-execution Talos recipe. It used host-authored records and primary
documentation only. It ran no guest command and inspected no guest disk or guest
state.

### Disposition of initial findings

1. **Resolved.** `install/void/start-installer.sh:4-10` now scans all twelve
   shared slots, closes each unsuccessful descriptor, and retains the successful
   descriptor through QEMU execution.
2. **Resolved in the published implementation; one evidence limitation remains.**
   `install/debian/validate.py:11` now creates the ordinary Debian test VM itself.
   `install/debian/timeout-host.py` and `raw/debian/timeout-supplement.json` add
   host-only tests for an incomplete standard-input stream and a held `run.lock`;
   both return 124 in approximately two seconds. The old
   `raw/debian/runner-validation.json` still predates the new creation row, and
   `raw/debian/new.log` is empty rather than recording a status. Thus the current
   driver is self-contained and the old subsequent operations indirectly establish
   that its VM existed, but there is no direct saved status field for that original
   `new` invocation. No guest rerun is required for this documentary limitation.
3. **Resolved.** `raw/void/key-provenance.txt` pins the key to upstream revision
   `1f6d0fb0197aae91ff2b9f1c52cacbdd9b1f37ec`, dated before the cutoff. The saved
   pinned key and the key used for verification are byte-identical with SHA256
   `add872570b2c0f3db1a676a752b5989fa1fe7ac38ee8991cad70ef6aaedb04d4`.
4. **Resolved.** `lab.sh:227-229` now places `new`, `start`, `stop`, `kill`, and
   `destroy` under the same per-machine lifecycle lock.
5. **Correctly remains a downstream gate, not a current defect.** No check
   observation is authorized in this preparation task. The exact runner, machine
   inputs, and downstream ordinary-action inputs must be included in a manifest and
   committed before the first later check observation. The present non-repository
   folder cannot itself demonstrate that future commit.

### AlmaLinux completed artifacts

- **Accepted for the reviewed scope.** The release record identifies AlmaLinux
  10.3 at the cutoff. The saved GPG result names fingerprint
  `EE6D B7B9 8F5B F5ED D9DA 0DE5 DEE5 C11C C2A1 E572`, matching the fingerprint
  independently quoted from the official security page, and the DVD matches the
  pinned SHA256.
- The Kickstart uses `%packages --default`. The primary Pykickstart documentation
  defines this as the default environment corresponding to an interactive install
  with no other package-screen selections. Automatic partitioning is delegated to
  the installer; the documented check choices cover architecture, firmware mode,
  language, keyboard, timezone, and required user. SSH, firewall access, and the
  sudo rule are identified as instrument additions.
- The installer acquired one shared slot, discarded installer output, and retained
  only timestamps and statuses. The backing was made mode 0444 before registration.
  The disposable boot/login, selected-status, root, stop, and destroy records are
  all successful. No package, service, file, account, process, or disk-content
  observation appears in the reviewed AlmaLinux records.

### Talos pre-execution findings

1. **Installed-payload provenance must be recorded before completion.** The
   verified ISO boots Talos maintenance mode; the generated machine configuration's
   `machine.install.image` selects the image actually written to the disk. The
   current release and verification records authenticate the ISO and `talosctl`,
   but do not yet identify or verify that installer image. After host-side config
   generation and before `apply-config`, record the exact image reference and an
   immutable digest or equivalent published verification evidence. This is a
   host-created-input check and does not require a guest query.
2. **Essential operations should not depend on Python assertions.**
   `install/talos/install.py:12-13,26,29,37-41` places command execution or success
   checks inside `assert` statements. Optimized Python execution removes assertion
   expressions, including several commands. Replace these with unconditional calls
   and explicit failure checks so interpreter flags cannot change the recipe.
3. **Failure cleanup and endpoint allocation are fragile.** The recipe fixes API
   port 23500 without first reserving it. Its `finally` block sends only terminate
   and waits 15 seconds; it has no kill fallback, and an exception there can skip
   explicit lock closure. A failed attempt also leaves the partial disk and generated
   credentials, preventing a clean repeat unless the operator removes them. These
   are preparation robustness issues, not evidence of a check observation.
4. The intended Talos operations remain within the observation boundary:
   configuration application, authentication readiness, one bootstrap, shutdown,
   and selected script status all discard command output. The retry log stores only
   step names, UTC times, and exit statuses. No inventory or property assessment is
   requested. The recipe must be run from its documented server-side
   `install/talos/` placement because its relative-root calculation assumes that
   layout.

Follow-up status: **AlmaLinux accepted; four initial implementation findings
resolved, with the original Debian `new` status retained as a minor evidence
limitation. Talos requires installed-image provenance and recipe hardening before
it is accepted. No prohibited check observation was found.**

## Completed-kit review, 2026-11-23 UTC

This pass reviewed only kit-owned host artifacts: the streaming runner, Debian
instrument validation, the completed NixOS and Talos records, aggregate releases,
choices, prepared-input boundary, and readiness report. It ran no guest command
and inspected no guest disk or guest content.

### Runner and Debian instrument

- **Accepted.** `lab.sh:113-123,200-211` streams SSH and Talos output through the
  runner's inherited output descriptor while preserving combined-output and status
  semantics. Internal lifecycle probes still discard output; serial fallback and
  `copy-out` retain their documented bounded purposes.
- The rerun `raw/debian/runner-validation.json` now directly records successful
  Debian creation, exact two-line output, status 37, root execution, status 124 at
  approximately two seconds, exact copy bytes, stop/start/destroy, and the two-slot
  server variant. The prior missing-creation evidence limitation is resolved.
  `raw/debian/timeout-supplement.json` separately continues to cover timeout before
  standard input completes and while the run lock is held. All recorded assertions
  pass.

### NixOS

- **Accepted.** The aggregate release row, official release record, and reused-image
  checksum agree on build `26.05.14979.94c3211b0ee8` and its published SHA256. Reuse
  is expressly permitted for this unchanged release.
- The saved declaration diff adds only OpenSSH enablement, the laboratory public
  key, and passwordless wheel administration. `access.sh` installs that exact
  host-authored declaration while discarding output. The initial serial access and
  subsequent SSH probes retain statuses only.
- `raw/nixos/access-status.log` records successful declaration application,
  ordinary and administrative SSH statuses, flattening to a read-only base, fresh
  clone creation, ordinary/root selected statuses, stop, destruction, and cleanup.
  No NixOS property assessment or inventory appears in the reviewed artifacts.

### Talos

- The previously requested implementation changes are present. The installation
  image is fixed by digest in both `install.py` and the generated configuration;
  the saved signature result names the same digest. Essential operations now use
  unconditional calls with explicit checks. A dynamic loopback port is selected,
  and final cleanup has a terminate-then-kill fallback and closes slot descriptors.
- Installation and smoke evidence is internally consistent. The accepted attempt
  starts with a blank disk, authenticates the maintenance and disk-only boots,
  bootstraps once, shuts down, registers a mode-0444 base, then creates and destroys
  a disposable clone whose selected status is 37. Only step names, UTC times, and
  statuses are retained; the failed readiness retry status is not a guest-content
  observation.
- **One provenance record remains incomplete.** `install/talos/verify.sh:9` fetches
  `trusted_root.json` from the mutable `main` branch of the trust-root repository.
  The exact file used, its digest, and an immutable source revision are absent from
  the kit records. The signature commands do constrain the expected workflow and
  factory identities, and their outputs report successful certificate and
  transparency-log verification, but an independent reproduction cannot establish
  which trust-root bytes produced those results. Retain the already used host file,
  record its digest, and tie it to an immutable upstream revision. Until then Talos
  is functionally ready but its provenance evidence is not independently complete.

### Aggregates and current readiness

- `releases.tsv` has one row for each of the seven fixed systems, with cutoff,
  release source, image, digest, and verification reference. `CHOICES.md` distinguishes
  installer defaults, explicit check choices, and instrument access. `INPUTS.md`
  correctly states that the repository commit is a downstream pre-observation gate
  and does not claim that downstream ordinary-action inputs are already committed.
- `KIT-READY.md` honestly reports **4 of 7 systems ready** in the builder's current
  record. Gentoo, MicroOS, and Guix are explicitly not ready and remain outside this
  acceptance pass. Fedora and Mint are auxiliary pending systems, also reported as
  such. Under this independent review, AlmaLinux, Void, and NixOS are accepted;
  Talos boot/run behavior is accepted but its trust-root provenance record requires
  the correction above before full evidence acceptance.
- No personal name, machine name, private machine path, or prohibited system/model
  reference was found in the reviewed published kit records. No prohibited check
  observation was found.

Completed-kit review status: **runner and Debian instrument accepted; NixOS
accepted; Talos functionally accepted with one concrete trust-root provenance
defect; Gentoo, MicroOS, and Guix not yet ready and not accepted in this pass.**

## Talos trust-root follow-up, 2026-11-23 UTC

- **The trust-root provenance defect is resolved.** The exact retained
  `raw/talos/trusted_root.json` hashes to
  `6494e21ea73fa7ee769f85f57d5a3e6a08725eae1e38c755fc3517c9e6bc0b66`.
  `raw/talos/trust-root-provenance.txt` records byte equality with immutable
  upstream revision `c9bda74ad2221f938f7d2e0295ca3aad2da710a8`, dated before use.
  `install/talos/verify.sh:9-10` now downloads that immutable revision and checks
  the retained digest before signature verification. Because the retained bytes
  are the bytes used by the successful prior verification, repeating either a
  signature verification or guest operation is unnecessary.
- **Talos is accepted for kit readiness and evidence completeness**, subject to
  the publication-hygiene issue below. Its release ISO, client, installed payload,
  trust root, clean installation, immutable backing, API transport, selected
  status, and cleanup all have consistent host-side evidence. No prohibited guest
  observation is present.
- **Publication hygiene requires one correction.**
  `raw/talos/trust-root-source.json` is a full upstream commit API response and
  includes personal author identity fields. This conflicts with the record rule
  prohibiting personal names in published files. Preserve a reduced evidence record
  containing the revision, date, immutable source URL, upstream verification status,
  and file digest without identity fields. The same hygiene check should cover other
  full upstream API dumps before publication; this finding concerns record content,
  not Talos provenance or readiness.

Updated completed-kit review status: **runner, Debian instrument, AlmaLinux, Void,
Talos, and NixOS accepted; Gentoo, MicroOS, and Guix remain not ready pending their
active preparation. One Talos source-record redaction is required before
publication.**

## Auxiliary bases and sanitization review, 2026-11-23 UTC

This pass reviewed only the host-authored Fedora/Mint access recipes, their status
records, the host image-chain audit, the sanitized provenance records, and the
current partial readiness report. It ran no guest command and inspected no guest
disk content.

### Fedora and Mint

- **Fedora accepted as an auxiliary base.** The retained initial driver and status
  show that access setup, ordinary SSH status 37, administrative status 0, and
  shutdown succeeded before the first clone failed. The recorded cause is fully
  host-side: changing the registry link after overlay creation made the overlay's
  backing filename resolve to itself. `repair-status.txt` records successful
  metadata-only rebasing to the direct prior immutable base and cleanup of the
  failed clone. The final smoke record then shows successful fresh-clone creation,
  ordinary and administrative status 37, stop, and destruction.
- **Mint accepted as an auxiliary base.** It used the corrected driver on its first
  attempt. The record shows successful access setup, ordinary status 37,
  administrative status 0, shutdown, final clone creation, status 37, and
  destruction. The access scripts for both systems discard package-manager and
  service output and install only the stated SSH key, SSH service, and administrative
  rule into their new access overlays.
- `install/reuse-base.py` checks that each prior source is read-only, pins that
  source's direct filename with `qemu-img rebase -u` before changing the registry
  link, makes the completed access overlay read-only, and removes disposable VM
  directories. The correction prevents recurrence of the Fedora link cycle.

### Host metadata audit

- **Accepted.** `install/audit-host.py` reads only host file modes, registry
  metadata, and qcow2 backing headers. Its saved runner digest equals the reviewed
  `lab.sh` digest. Every registered chain resolves successfully and every listed
  layer is mode 0444. Fedora and Mint each have exactly two layers: the current
  read-only access overlay and the direct previous-laboratory read-only source.
  The audit shows no backing cycle.
- The audit honestly reports Gentoo and MicroOS as unregistered at its timestamp and
  Guix as registered with serial transport, without converting those facts into a
  readiness claim. These active systems remain outside this pass.

### Published-record sanitization and partial readiness

- **The earlier identity-field finding is resolved.** The trust-root and Void key
  commit records retain immutable revision URLs and dates without personal name or
  email values. The Talos and verifier release records retain release metadata and
  artifact names, URLs, sizes, dates, and digests; contributor bodies and account
  identity fields have been removed. A targeted scan found no private machine path,
  email address, or account-identity field in these sanitized records.
- `KIT-READY.md` correctly remains **4 of 7 systems ready**: auxiliary Fedora and
  Mint readiness does not change the seven-system numerator. Gentoo, MicroOS, and
  Guix are explicitly still active and not ready. Debian, Debian server, Fedora,
  and Mint are separately and accurately reported as auxiliary/instrument systems.

Auxiliary review status: **Fedora accepted; Mint accepted; host backing-chain audit
accepted; API sanitization accepted. Overall kit readiness remains honestly partial
at 4 of 7, with Gentoo, MicroOS, and Guix not yet accepted.**

## MicroOS AutoYaST static review, 2026-11-23 UTC

This pass inspected only host-authored installer inputs and public upstream
documentation. It ran no guest command and read no guest output or guest disk.

- **A concrete unattended-install blocker was found and corrected for the next
  clean attempt.** The retained attempt-5 profile set
  `confirm_base_product_license=true`. The official AutoYaST guide states that
  this value displays the base-product EULA and requires user acceptance; if it
  is not accepted, installation is canceled. This directly conflicts with the
  headless recipe and plausibly explains reaching the pre-script without reaching
  the chroot script. The current profile now uses `false`, while the attempt-5
  input remains retained. Sources:
  https://doc.opensuse.org/documentation/leap/autoyast/html/book-autoyast/cha-configuration-installation-options.html
  and the SLE Micro-specific guide at
  https://documentation.suse.com/sle-micro/5.3/single-html/SLE-Micro-autoyast/book-autoyast.html .
- **No XML structural defect remains.** The corrected profile validates against
  the official openSUSE `yast2-schema-micro` 5.0.3 AutoYaST `profile.rng` schema.
  The `chroot-scripts` placement and `chrooted=true` field match the documented
  AutoYaST interface.
- **The remaining static choices are consistent with their cited primary
  sources.** The four required patterns, optional `32bit` regex, disabled
  recommended packages, automatic product storage proposal, UEFI/systemd-boot,
  Combustion fw_cfg name, missing-machine-id first-boot trigger, and non-host-only
  initramfs rebuild agree with the retained MicroOS control file and upstream
  AutoYaST and Combustion documentation. The access script's required `curl`,
  SSH, sudo, and SELinux tooling are present in the selected product patterns.
  No second concrete static blocker was found.

MicroOS static-review status: **corrected profile structurally and semantically
accepted for a clean retry; runtime readiness remains unaccepted until host-side
status evidence records successful completion.**

## Talos runner interpreter follow-up, 2026-11-23 UTC

- **The Talos shebang/interface mismatch is corrected statically.** The Talos
  branch now calls the common interpreter selector, passes the unchanged script
  on standard input, and puts a per-machine executable `talosctl` wrapper first
  on `PATH`. The wrapper supplies the fixed configuration, endpoint, and node to
  the verified client, so shell and non-shell interpreters receive the same API
  context. Its temporary file is mode 0700 and atomically replaces the prior
  wrapper. The shell wrapper and embedded Python both parse successfully.
- Combined stdout/stderr handling, inherited streaming, selected exit status,
  the 300-second default, `--timeout`, and status 124 handling remain on the same
  runner path. The correction does not introduce guest inspection: Talos scripts
  still run on the host against its API, and output can be discarded.
- `raw/talos/interpreter-expectation.md` is an adequate pre-execution test plan:
  a Python-shebang script discards authenticated version output and selects status
  37, followed by stop and destruction. Acceptance of the deployed correction
  remains conditional on the planned status-only smoke record and refreshed host
  runner digest.

Talos interpreter-review status: **static correction accepted; deployed evidence
pending the planned status-only smoke and host metadata refresh.**

## Talos interpreter evidence closure, 2026-11-23 UTC

- `raw/talos/interpreter-smoke.json` matches the prewritten expectation: fresh
  clone creation returned 0, the Python-shebang script authenticated with output
  discarded and selected status 37, and stop and destruction both returned 0.
- The refreshed `raw/host-base-audit.json` runner digest is
  `51f336a5ea0e0b856764c1d66518d5db7fa1b9431398cd362a459b49b9e37ae9`,
  exactly matching the reviewed `lab.sh`. The audit continues to report resolved,
  read-only registered backing chains.

Talos interpreter-review status: **accepted; the prior evidence conditions are
closed.**

## Guix access static review, 2026-11-23 UTC

This pass inspected only host-authored declarations, recovery scripts, retained
status values, and the official Guix 1.5 manual and source excerpts. It ran no
guest command and read no guest output or guest disk.

- `config.scm` is a syntactically balanced extension of the retained original
  declaration. Its only substantive additions are the documented OpenSSH service
  with a file-like authorized key and the instrument sudo rule. The retained
  manual documents the same `openssh-configuration` and `authorized-keys` form;
  DHCP, serial agetty, BIOS GRUB target, root label, users, locale, and packages
  otherwise remain the original pre-observation inputs.
- The current recovery recipe follows the official “Chrooting into an existing
  system” sequence: known root mount, recursive proc/sys/dev binds, system-profile
  environment, a minimal daemon with the documented flags, and `guix system
  reconfigure`. Its added temporary `/run` supplies `current-system` and
  `booted-system` links to the preserved system generation. Tagged Guix 1.5
  installation source confirms that `/var/guix/profiles/system` is the system
  generation link; therefore the executable and profile paths under its
  `profile` child are structurally correct. Shell and Scheme-reader syntax checks
  pass.
- No concrete declaration or documented-chroot-step defect was found in the
  current inputs. Prior statuses 1, 255, 82, and 127 do not identify a cause
  because output was deliberately discarded; they cannot support a static
  readiness claim. Per-stage statuses may localize a future failure without
  observing guest contents.

Guix static-review status: **current recovery inputs accepted for another bounded
attempt; Guix remains not ready until host-side status evidence records successful
reconfiguration, fresh SSH status checks, shutdown, and cleanup.**

## MicroOS system-role clarification, 2026-11-23 UTC

- **The earlier first-role description required a documentation correction, not
  an installer change.** The pinned product control has separate workflows: the
  interactive `installation` workflow includes `system_role`, while the
  `autoinstallation` workflow omits it. AutoYaST's profile schema and implementation
  provide no `system_role` field. Thus the documented first-role preselection
  applies to the interactive selector and does not establish that AutoYaST selected
  or inherited `micro_os_role`.
- This does not create a missing installation input. `micro_os_role` has no static
  partitioning, software, network, global, or service override; it only names an
  additional interactive dialog. The profile explicitly transcribes the top-level
  product patterns, and automatic storage uses the top-level product defaults.
  `parts/microos-choices.md` now accurately describes the result as
  configuration-equivalent to the first interactive role and does not invent an
  unsupported profile field.

MicroOS role-review status: **documentation corrected and accepted; MicroOS remains
runtime-not-ready for the independent reasons already recorded.**

## Guix profile nounset follow-up, 2026-11-23 UTC

- **A concrete likely cause of the prompt chroot status 1 was found in the host
  input.** `chroot-access.sh` enabled `set -u` before sourcing the generated
  system-profile environment. Official Guix 1.5 source builds that profile with
  prefix expressions of the form `value${VAR:+separator}$VAR`. The guarded
  expansion is safe for an unset variable, but the final bare `$VAR` is not safe
  under Bash nounset. A normally unset search-path variable can therefore stop
  the script at the source step. The official chroot procedure does not enable
  nounset before sourcing this profile.
- The bounded correction is to use `set -e` while sourcing the profile and, if
  desired, enable nounset only afterward. This conclusion comes from public Guix
  1.5 source (`guix/build/profiles.scm` and `guix/search-paths.scm`) and host input;
  it required no guest access.

Guix follow-up status: **current nounset use requires correction before another
recovery attempt; runtime readiness remains pending.**

## Gentoo completed-kit review, 2026-11-23 UTC

This pass reviewed only host-authored recipes, published source records, numeric
status evidence, and host image metadata. It ran no guest command and read no
guest output or guest disk.

- **Release and repository provenance accepted.** The plain amd64 OpenRC stage3,
  its detached signature, and signed digest precede the cutoff and verify against
  the recorded official service-key fingerprint and SHA-512. The signed Portage
  20261122 snapshot was published before the cutoff and independently verifies.
  The records honestly preserve the successful initial default `emerge-webrsync`
  invocation separately from the later explicit `--revert=20261122` pin. The pin
  and source-only update of every explicitly required package returned 0.
- **Recipe and choices accepted.** The stage profile remains the selected plain
  multilib OpenRC profile. The recipe disables binary package hosts and both
  binary-package acquisition paths, builds `gentoo-kernel`, selects dracut through
  `installkernel`, installs BIOS GRUB on the fixed MBR target, and declares ext4,
  swap, locale, DHCP, SSH, and instrument access. The consolidated recipe is
  clearly distinguished from the retained scripts actually used across corrected
  attempts. All host shell and Python inputs parse.
- **Readiness evidence accepted.** Source completion, finalization, BIOS/MBR
  alignment, explicit repository pin, bootstrap shutdown, backing creation, and
  cleanup returned 0. A clean clone returned 0 from creation/login and selected
  status 37 for both ordinary and administrative runs. The original QMP ACPI
  stop timed out without diagnostic inspection. The corrected runner uses the
  existing privileged SSH path for OpenRC `poweroff`, bounds that transport at 15
  seconds, tolerates its expected disconnect, and still requires QEMU to exit.
  The prewritten fresh retry then recorded new 0, stop 0, and destroy 0.
- The refreshed host audit digest exactly matches the reviewed runner. Gentoo is
  registered as a one-slot SSH base; its single 40 GiB qcow2 chain resolves with
  mode 0444. Build-time use of four slots is separately and accurately recorded.
  `parts/gentoo-status.json` and `parts/gentoo-ready.md` agree with the underlying
  evidence and cleanup status.

Gentoo review status: **accepted as ready, with complete source, installation,
runner, immutable-backing, and cleanup evidence.**

## Handoff metadata and manifest review, 2026-11-23 UTC

This pass reviewed only the kit-owned top-level release, choice, runner,
readiness, input-boundary, and manifest files. It did not inspect shared-task
artifacts, run guest commands, read guest output, or inspect guest disks.

- **The release table, consolidated choices, runner documentation, input
  boundary, and readiness count are internally consistent.** The table has one
  row for each of the seven check systems. The readiness record accurately says
  five of seven check systems and all four auxiliary systems are ready, while
  MicroOS and Guix remain unfinished. Talos names the immutable trust-root URL
  and all three verification records. The MicroOS role language and Gentoo
  duration agree with their reviewed system records.
- **The current checksum manifest is not a valid handoff manifest.** An
  independent `sha256sum -c` found seven changed files and two missing files.
  The missing entries are `raw/guix/profile-source.tmp` and
  `raw/guix/system-source.tmp`. `build-manifest.py` currently includes every
  file below the selected raw-system directories, so transient `.tmp` files can
  be published and later disappear. The enumerated scope contains none of the
  known shared-task readiness, collector, final-Debian, or RPM-record paths, but
  transient files must be excluded or deliberately retained. Because the
  manifest also hashes this review, it must be generated only after the final
  review append and all remaining system writes, then pass a complete checksum
  validation.
- **The Guix key provenance field names a file that the kit does not contain.**
  `releases.tsv` identifies `install/guix/release-key.gpg`, but that path is
  absent from the manifest and filesystem. The retained signature-status record
  identifies a valid-signature fingerprint, but it cannot replace the named
  key input or establish where that key came from. The final release record
  should retain the exact key with its provenance or name a stable public source
  instead of a nonexistent local path.

Handoff review status: **top-level metadata accepted subject to correcting the
Guix key reference and producing a clean final manifest after MicroOS, Guix, and
review records stop changing. The two systems' runtime readiness remains pending
separately.**

## Handoff finding closure, 2026-11-23 UTC

- **Guix key provenance is accepted.** The exact retained key is now included at
  `install/guix/release-key.gpg`. Independent parsing confirms primary
  fingerprint `A28BF40C3E551372662D14F741AAE7DCCA3D8351`, and its SHA-256 is
  `5f122137a46bbfe4e3173d7be08948a2c7fdbba4f0d584c1a8055a288473ff28`, both
  matching `raw/guix/key-provenance.txt`. The saved official announcement links
  the recorded public key URL, and `releases.tsv` now names that URL, the retained
  input, and the fingerprint.
- **Manifest scope correction is accepted.** `build-manifest.py` now excludes
  files whose suffix is `.tmp`, while preserving the explicitly bounded kit
  scope. `INPUTS.md` accurately requires final generation after installation and
  independent-review writes finish. The final checksum validation remains a
  handoff operation and is intentionally deferred until those writes are done.

Handoff-finding status: **both concrete metadata findings are resolved; MicroOS
and Guix runtime disposition remains unchanged and outside this closure.**

## Guix final disposition review, 2026-11-23 UTC

This pass used only host-authored recipes, numeric status records, readiness
text, and host metadata. It ran no guest command and read no guest output or
guest disk.

- **The final not-ready disposition is supported.** The verified 1.5.0 image and
  copied original clean installation remain available. Two disposable original
  boots recorded serial bootstrap login status 0. No SSH-ready installation was
  established: the final corrected application started at 06:55:20Z and returned
  timeout status 124 after its 900-second limit at 07:10:34Z, so the prewritten
  SSH smoke sequence did not run. The records correctly avoid attributing the
  noncompletion to a guest cause.
- **Failure retention and cleanup are supported.** The final status records
  cleanup 0, removal of failed candidate and helper disks, absence of the failed
  registry and disposable smoke VM, and retention of the original read-only
  backing plus image, signature, key, recipes, and status evidence. No failed
  candidate is presented as a usable base.
- **Final top-level synchronization is still required.** The current
  `raw/host-base-audit.json` predates cleanup and still describes Guix as a
  registered SSH base; this conflicts with the later final-cleanup record that
  the failed registry is absent. `KIT-READY.md` also still describes the final
  return as pending. These aggregate records must be refreshed after the final
  MicroOS disposition and before the checksum manifest is generated.

Guix review status: **accepted as not ready: image verified, copied original
clean installation boot demonstrated, final `lab.sh run` unavailable, failed
candidates cleaned. Aggregate host metadata and readiness text remain pending
final synchronization.**

## MicroOS final disposition and aggregate handoff review, 2026-11-23 UTC

This final pass reviewed only host-authored inputs, fixed-status logs, cleanup
records, readiness text, and host image metadata. It ran no guest command and
read no guest output or guest disk.

- **The MicroOS not-ready disposition is supported.** Snapshot20261121 remains
  verified. The corrected sixth attempt recorded profile delivery 0 and
  pre-install hook 0, then reached its fixed 2400-second installer limit with
  status 124 at 07:14:22Z. No installed-system boot or SSH success was recorded,
  so the readiness table correctly reports image verified yes, clean installation
  boot no, and `lab.sh run` no. The records correctly leave the internal cause
  unknown because installer and guest output was discarded.
- **MicroOS cleanup is complete.** The status log records disposable cleanup 0
  at 07:15:09Z. The failed partial disk, mutable firmware variables, extracted
  boot material, temporary keyring, and status FIFOs were removed. No MicroOS
  base or ready metadata is registered; the verified image, exact inputs, and
  numeric evidence remain.
- **The final aggregate is accepted.** `KIT-READY.md` closes preparation at
  07:15:09Z and consistently reports five of seven check systems ready, with
  Guix and MicroOS unavailable, plus all four auxiliary systems ready. The
  refreshed host audit is dated 07:15:01Z, marks exactly those two systems
  unregistered, and records all nine usable bases with read-only chains. Its
  runner digest exactly matches the reviewed local runner. The MicroOS cleanup
  made no registry change after that audit. Consolidated choices accurately say
  that Guix SSH preparation did not complete and identify recovery-only inputs
  without presenting them as installed-system choices.
- The earlier pending-synchronization note is now closed: the Guix row, overall
  readiness summary, and host audit reflect the final dispositions. The checksum
  manifest may now be regenerated after this append and must pass complete
  validation before handoff.

Final review status: **accepted for handoff with five of seven check systems and
all four auxiliary systems ready. Guix and MicroOS are explicitly accepted as
documented not-ready preparations, with no usable base registered and no check
observation claimed.**
