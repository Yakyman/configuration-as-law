# c2 — classification of part `server` (A3): notes

Input: `A3/in/part-server.tsv` (1325 rows). Output: `A3/c2/part-server.tsv` (1325 rows, one per input id).
Per-member decisions of the 366 group rows: `A3/c2/part-server.members.tsv` (4086 members; columns
`group_id, path, decision, sentences, reason`). A group row is `MIXED` when its members get different decisions; which
member gets which is in that file, rows with the same `group_id`.
Scripts: `A3/c2/scripts-server/` — `decide.py` writes both files (reproducible: a second run into a scratch file was
byte-identical), `check.py` validates the output, `pkg.py`/`readraw.py`/`groups.py`/`show.py`/`sample.py` read the
inventory. Only the text (TEXT.md 8.1–8.3, SENTENCES.md), `A3/in/` and public documentation were read.

## Facts used and where they are

- Package reason (explicit/dependency): `objects.tsv` package rows (`raw/0022`, `raw/0023`).
- File change since installation: `package-files.tsv` (`unchanged`/`changed`/`unknown`). Notable: `/usr/bin/dockerd`,
  `/usr/bin/containerd`, `/usr/lib/systemd/systemd-udevd` are `unknown`; files under `/var/lib/dpkg/info/` are not in
  `package-files.tsv` at all.
- Persistence of members: member tables (`runtime` = tmpfs). `/run/docker/netns/*` is `persistent` but has filesystem
  `0x6e736673` (nsfs) in `raw/0004-filesystem.out`: namespace mount points.
- Who created a configuration file: maintainer scripts read by the collector (`raw/0108`–`0113`, decoded with
  `readraw.py`), `configuration-origin.tsv`, mtimes, and the deb-systemd-helper state directory. The operator action
  logs (`A3/in/operator/server/actions-logs/`) show what the person's actions did (e.g. bsd-mailx alternatives
  "in auto mode", k3s install script steps, enablement symlinks).
- Contents of the person's files (`compose.yaml`, `Caddyfile`, `workload.yaml`, `/etc/cal-firewall.nft`, unit files,
  `/etc/cron.d/cal-maintenance`, `/etc/logrotate.d/cal-maintenance`) were NOT read by the collector; only
  metadata exists. Docker container labels (`raw/0084`) name `compose.yaml` and the bind-mounted `Caddyfile`.

## Documentation used (quoted)

- Docker, https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/ — "A container image is a
  standardized package that includes all of the files, binaries, libraries, and configurations to run a container."
  The docs describe pulling and removing images; they do not describe Docker as installing programs.
- k3s, https://docs.k3s.io/installation/packaged-components — "any file found in /var/lib/rancher/k3s/server/manifests
  will automatically be deployed to Kubernetes"; packaged-component manifests "are re-written to disk whenever K3s is
  started".
- k3s, https://docs.k3s.io/blog/2025/03/25/K3s-initialization — K3s embeds Linux userspace binaries in its executable;
  they are deployed in /var/lib/rancher/k3s/data, each subdirectory named by the SHA256 of the embedded tarball;
  `current` points at the active one; `cni` holds CNI plugin symlinks to one multi-call binary.
- k3s ports, https://docs.k3s.io/installation/requirements (6443 API server, 8472/udp flannel VXLAN, 10250 kubelet).
- nftables, https://wiki.nftables.org/wiki-nftables/index.php/Scripting — "nftables provides a native scripting
  environment"; scripts are loaded with `nft -f`.
- crontab(5), https://manpages.debian.org/trixie/cron/crontab.5.en.html — "The entire command portion of the line …
  will be executed by /bin/sh".
- Maintainer scripts: https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html and deb-postinst(5),
  https://manpages.debian.org/trixie/dpkg-dev/deb-postinst.5.en.html — postinst etc. are control information files of
  the package ("its control archive").
- PrivateTmp: https://systemd.io/TEMPORARY_DIRECTORIES/ — per-service private temporary directories are removed when
  the service shuts down.
- systemd-resolved: https://www.freedesktop.org/software/systemd/man/latest/systemd-resolved.service.html (stub
  listeners 127.0.0.53/127.0.0.54:53, LLMNR 5355).

## Readings applied (each is a reading of the cited sentences, not a new rule)

1. Order of questions (S8.2-6). Q1 is asked first: a package row is always Q1 "yes"; a file obtained with a package is Q1
   "yes" only if recorded `unchanged`. Default setting values shipped as package files are installed objects (S8.2-8
   lists "default setting values"); `SETTING-DEFAULT` is used only for defaults *created during installation* (S8.2-17)
   — maintainer-script accounts, groups, enablement links, generated config files.
2. Packages: `explicit` → `INSTALLED-OWN`; `dependency` → `INSTALLED-DERIVED` ("a package installed as a dependency of
   a recorded package", S8.2-16). The inventory's reason is used as the fact.
3. Services (S8.1-11 "in force if enabled"): a service row is decided by its enablement value. Enabled by a person →
   `SETTING-OWN`; enabled by the package's deb-systemd-helper during installation (state file present in
   `/var/lib/systemd/deb-systemd-helper-enabled`, mtime in the installation) → `SETTING-DEFAULT`; static units with no
   enablement value, wired only by unchanged package files → `INSTALLED-PACKAGE`. Unit-file rows are decided as files
   (Q1 for unchanged package files; person's unit files are values read by systemd, S8.2-23, so `SETTING-OWN`).
   A person re-running `systemctl enable` on a package-enabled service (cron, docker) is an action (S8.2-4); the value
   stays the installation default.
4. "Not-found" units and kernel netfilter tables/chains/rules, processes, ports, loaded modules, tmpfs files, sockets,
   nsfs mount points and PrivateTmp trees exist only while the computer runs → `RUNTIME` (S8.2-5), reason names the
   creator and its decision. Where the creator is not recorded but every candidate gives `RUNTIME`, `RUNTIME` is given
   (task rule) and the candidates are named.
5. Lines of `iptables-save` output that are not kernel objects (`# Generated …`, `# Completed …`, `COMMIT`) are text
   produced by the collector's own command: `ACTION` (S8.2-3 the rule applies to objects on the computer; S8.2-4).
6. "The system itself built or obtained it" (S8.2-16) is read as: a program on the computer produced the object from
   something a line records — docker compose creating containers from `compose.yaml`; k3s extracting its bundled
   binaries; useradd/cloud-init copying `/etc/skel`; base-files copying `/etc/profile`, `/root/.bashrc`; Python
   compiling netplan bytecode (8.6 "compiled copy"); grub-install/update-grub producing `/boot/grub`.
7. The k3s install script (get.k3s.io) is downloaded and piped to a shell: it is not "a program of the system" (S8.1-4),
   so `/usr/local/bin/k3s`, its helper scripts and links are `PROGRAM-OWN`. `node_exporter` likewise.
8. A file executed as code is a program even with settings inside (S8.2-23): shell startup files, `/etc/profile`,
   `grub.cfg`. Unit files are read as values. A cron file is read as values but its command field is run by /bin/sh →
   two readings (`GAP-TWO`).
9. Q3 needs "a value chosen by a person". Values written by a program on its own (k3s certificates, kubeconfigs,
   packaged manifests rewritten at each start, SSH host keys, machine-id, apt/debconf/man caches) are not chosen by a
   person → Q4 → `RECORD`. Values the operator supplied through cloud-init (hostname, netplan, mirrors,
   authorized_keys, sudoers) are settings "however entered" → `SETTING-OWN`.
10. Directories as members: a directory is neither code nor a value; one created by a program as it ran → `RECORD`,
    one created by a person's action → `MATERIAL` (S8.2-15).
11. Image-build files (mtime 2026-11-16, the clean installation): where a package script could have created a setting
    but the image builder could also have written or changed it (no installation-time evidence), the decision between
    `SETTING-DEFAULT` and `SETTING-OWN` depends on an unrecorded fact → `UNKNOWN` (member level). Alternatives in
    `/etc/alternatives`: auto mode → default, manual mode → person's choice; the mode is in
    `/var/lib/dpkg/alternatives/*`, whose contents were not collected → `UNKNOWN`, except bsd-mailx links whose
    action log says "in auto mode".

## Rules applied by script (homogeneous kinds) and hand checks

Each rule follows from the sentences named; 10 rows per rule were checked by hand against the input row and the
inventory (ids below).

- R1 packages (42 rows) — S8.2-7, S8.2-8, S8.2-16; reading 2. Checked: server-4830b005c5e95a80b9f05ea4
  server-dd035f97841eb9c1044b6a0a server-ac29b0440441e8288cfb4d98 server-432558e6ee13c4ec81b82376
  server-782dc55f63d522e95b4a4ebe server-67238d837a2ad06214f75a3d server-ad76c0b55bee5637e4b06538
  server-95a3b8a7bb3ae5310e7998a5 server-6cca8d4ecad12a14f131e6dc server-ff29ce6e7dc87743d95a6a3c
- R2 nftables tables/chains/rules (297 rows) — S8.2-5; creator by table/chain name and expression (cal_filter →
  cal-firewall.service; KUBE-*/FLANNEL-*/10.42/10.43 → k3s; DOCKER*/docker0/br-91deedb1c880/172.17–18/18081 → dockerd;
  shared built-in tables/base chains → dockerd or k3s, not recorded). Checked: server-df39c40167f8ea0d545dc239
  server-2d0312e06791afc925c567d0 server-fe94b08e4e9cb97bcd18973d server-cbe6049bab649b93cf0cad18
  server-2e1190b90fcf668489c388b7 server-f890ce88ce23da1e28aeea07 server-9f123192906422d782aa700a
  server-04ad807d8a3a942191872953 server-74c5e7251d099477288ac098 server-e58cd42496b7bdcb0f291c3c
- R3 iptables-save lines (321 rows) — S8.2-5 for tables/chains/rules (same creator rule), S8.2-3/S8.2-4 for header,
  completion and COMMIT lines (reading 5). Checked: server-5502da6830c10a1165a74676 server-fb05bb775c8f71bf755135df
  server-aa00ace54669d924cd3eae4d server-60d8b168edc26812b1f1f69b server-4fb247f999c81a54e78611e8
  server-210d0a8c734e238223856799 server-be7b0735ff0a0ae2d1b91848 server-af53a39024fc000d54038ad2
  server-e3e9bf3a767aca66747aa438 server-03bce9c0340367752723ad33
- R4 processes (81 rows) — S8.2-5, S8.2-22; executable's package and integrity from `package-files.tsv`; container
  executables belong to their image; k3s data-dir executables to the extracted binaries. Checked:
  server-cabd2fe206a1d620b3e41bad server-eb5512b7d87a9d73d71980ba server-4ee952c534b1127162151e32
  server-6e2f004cb8fc03dbacfbb622 server-1421586b181f55637bdde0b8 server-5328ae6ea261addd2d5c2cb5
  server-7fe924d095e53dae4a99f8e9 server-78e6bce75d501759ddc81955 server-82a020220e4fab69bebe0b17
  server-bd383f6adda5449ee17f182b
- R5 loaded kernel modules (41 rows) — S8.2-5; loader not recorded, every candidate gives RUNTIME. Checked:
  server-cafbb167cd3c3263e11c45af server-72df891f8e9fbb3c82e182aa server-ef17b770682f7c6d48df36ef
  server-81c82a1e10a33a9ec991ba8d server-7d5779b77057f6d8e522bbce server-820b6ffacd170a3a74f3a610
  server-eb412d6403b0bc1457e35413 server-443f97e416cabdd6b6d30460 server-ab26cfb98955a4597f6db852
  server-9a13b95e77fca3a626a8d8ec
- R6 executable code outside packages (80 rows) — S8.2-9, S8.2-10, S8.2-16, S8.2-20, S8.2-23; skel copies
  PROGRAM-DERIVED; k3s/node_exporter files PROGRAM-OWN; k3s data-dir tools PROGRAM-DERIVED; dpkg maintainer scripts
  UNKNOWN (control-area files obtained with the package, change not recorded: unchanged → INSTALLED-PACKAGE, changed →
  PROGRAM-OWN); empty CNI lock RECORD. Checked: server-e4c3ed3ee7b5250779b17adc server-b7536bc29b5ce243d12db8a1
  server-aa083d0541e76f74f735461c server-1a13ca9fdf27fad418171dfa server-a571b0e949012a15875c9506
  server-84095978ac2bf4ed8efa4b8f server-865d0fe7c337db68ec227ca1 server-0d0463028c57f32f625452e0
  server-9c59629a43e8b28a746de9d5 server-d02335598a28a16dbeb2a382
- R7 stored groups (366 rows) — member rules in `decide.py` (`mrule`, readings 1–11), group decision = the common
  member decision, else MIXED. Hand-decided member paths are listed explicitly in `mrule` (table `E`). Checked:
  server-cca0029351b5e4b721d68865 server-1a966a27f7e9eebca9449b02 server-cd2ba6c2bdf8133829fa82fb
  server-06fd9ee1da1feafeefe2baad server-1e2ef8696a309684075fb3f2 server-9521fd9b8cafa417c9e6d898
  server-f65a408f640f236c4b866919 server-f4129404be29efd4adee3768 server-36c739acd4fca7ff1acad656
  server-a4edd37b5e963529a71018fc

Decided row by row (not by rule): accounts, groups, services, timers, unit files, user services, sudo-access,
access rules, docker containers and images, image/container stores, and the 26 ports (one entry per port number in
`PORTS`; the inventory's `ss` output has no owning process, so the listener is named from the documented use of the
port; RUNTIME holds for any listener).

## Gaps and unknowns (what the text or the inventory lacks)

- GAP-TWO, docker images (3 rows): S8.1-4 makes an installer "a program of the system whose purpose, according to its
  documentation, includes installing and removing programs". Docker's documentation calls an image "a standardized
  package" of binaries and pulls/removes it as a whole, but never says it installs programs. Reading A: Docker is an
  installer, the image a package obtained for `compose.yaml` → INSTALLED-DERIVED. Reading B: not an installer, the
  image is code obtained by the system from `compose.yaml` → PROGRAM-DERIVED. No sentence decides.
- GAP-TWO, `/etc/cron.d/cal-maintenance` (group row server-c354536d6d9a738329571706): cron reads the file as schedule
  values but hands its command field to /bin/sh; S8.2-23 distinguishes "executes as code" from "only reads as values"
  and the file is both → PROGRAM-OWN or SETTING-OWN.
- GAP-TWO members `state.db`, `state.db-wal` of k3s: the datastore holds the person's applied Deployment/Service
  (a setting "whatever file stores it", S8.2-12) and k3s working state (S8.2-15); one file, two answers.
- UNKNOWN rows: dpkg maintainer scripts (control-area integrity not recorded); the four unexpanded image/container
  stores (member list not recorded); `/etc/logrotate.d` group (content not recorded: a pre/postrotate script would make
  it code).
- UNKNOWN members (inside MIXED groups): `/etc/cal-firewall.nft` (content and how cal-firewall.service loads it not
  recorded); image-build settings whose creator (package script vs. image builder) is not recorded; alternatives whose
  mode is not recorded; dpkg control-area files; `/var/lib/dpkg/statoverride`.
