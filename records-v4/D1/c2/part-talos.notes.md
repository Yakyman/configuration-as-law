# D1, classification c2, part talos — notes

Input: `D1/in/part-talos.tsv` (278 rows). Output: `D1/c2/part-talos.tsv`. Generator: `D1/c2/talos-bin/decide.py`;
check: `D1/c2/talos-bin/verify.py` (ids equal to the input, each once; every decision one of the fifteen words).
Fetched public sources are saved under `D1/c2/talos-raw/` (Talos v1.14.6 source files, the Talos v1.14 architecture page,
the containerd README). The machine ran Talos v1.14.6 (`raw/0002-talos-version.out`).

## Facts established from public documentation (and used below)

- Root filesystem: “At its core the rootfs is a read-only squashfs. The squashfs is then mounted as a loop device into
  memory.” “at boot Talos will write `/system/etc/hosts` and then bind mount it over `/etc/hosts`.” “All files under
  `/system` are completely recreated on each boot.” — https://docs.siderolabs.com/talos/v1.14/learn-more/architecture
  The mount table (`raw/0004-talos-mounts.out`) shows `/run`, `/system`, `/tmp`, `/etc/cni`, `/etc/kubernetes` as tmpfs,
  `/dev` devtmpfs, `/var` on `/dev/vda6`, `/` and `/opt` overlay.
- `/etc`: “/etc is a writable overlay (upper = a managed tmpfs …, lower = the static rootfs /etc) bind-mounted read-only at
  /etc” — `internal/app/machined/pkg/runtime/v1alpha2/v1alpha2_controller.go` at tag v1.14.6. Files written at runtime
  through that upper: `hosts`, `resolv.conf` (network EtcFileController), `machine-id` (node identity controller),
  `iscsi/initiatorname.iscsi` (iqn.go), `nvme/hostid`, `nvme/hostnqn` (nqn.go), `cri/conf.d/cri.toml` (cri_config.go),
  `cri/conf.d/base-spec.json` (cri_base_runtime_spec.go), `ssl/certs/ca-certificates.crt` (secrets/trusted_roots.go).
- Image contents of `/etc`, `/boot`, `/opt` come from the v1.14.6 `Dockerfile`: `etc/nfsmount.conf`, `etc/cri/containerd.toml`,
  `etc/cri/conf.d/00-base.part`, `etc/lvm/lvm.conf`, `etc/os-release`, `etc/localtime`, `etc/extensions.yaml` (later
  bind-mounted read-only from the boot image, `internal/app/init/main.go`), the symlinks `etc/pki`, `etc/ca-certificates`,
  `etc/ssl/certs/ca-certificates`, directories `boot/EFI`, `etc/cri/conf.d/hosts`, `etc/selinux/targeted/contexts`,
  `etc/ssl/certs`, `opt/containerd/{bin,lib}`, and the CNI plugins `opt/cni/bin/{bridge,firewall,host-local,loopback,portmap}`
  plus the flannel CNI package. Observed sizes of `nfsmount.conf` (44), `lvm/lvm.conf` (223), `cri/containerd.toml` (376),
  `cri/conf.d/00-base.part` (440) equal the sizes of the v1.14.6 source files.
- `/opt` is an overlay whose writable upper lies on `/var` (`constants.Overlays`, `VarSystemOverlaysPath = "/var/system/overlays"`
  in `pkg/machinery/constants/constants.go`); the inventory records integrity `unknown` for its files.
- Service start conditions (`v1alpha1_sequencer.go`, `v1alpha1_sequencer_tasks.go`, `controllers/cri/service.go`,
  `controllers/k8s/kubelet_service.go`, `sandboxd/enabled.go`): machined, udevd, apid, auditd, syslogd, containerd,
  sandboxd start in every metal boot (auditd and dashboard can only be switched off by kernel parameters, which are not set
  here: both run); cri and kubelet start once any machine config exists; trustd and etcd start only when the machine
  config type is `init` or `controlplane` (`switch t := r.Config().Machine().Type()`).
- Ports: apid 50000, trustd 50001, KubePrism 7445, host DNS 169.254.116.108 (`constants.go`); etcd 2379/2380/2383 from its
  process arguments (`raw/0008-talos-processes.out`); kubelet 10248/10250 defaults
  (https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/).
- containerd’s own description: “manage the complete container lifecycle of its host system: image transfer and storage,
  container execution and supervision, low-level storage and network attachments, etc.” —
  https://github.com/containerd/containerd/blob/main/README.md. It does not say “installing and removing programs”, so under
  S8.1-4 read strictly it is not an installer and a container image is not a package (Q1 no); the image is code (Q2).

## Rules applied by script (each follows from the cited sentences)

- **R1 processes (34 rows) → RUNTIME** (S8.2-5: a process is not a separate object). Owner named from the command path:
  programs in the Talos image → INSTALLED-PACKAGE; kubelet and etcd run from pulled container images → PROGRAM-DERIVED if
  the system pulled the image, PROGRAM-OWN if a person did (puller not inventoried; RUNTIME either way).
  Checked by hand: 01604da7d6bb671facc1d88a, 0bc874346da246e30e75149c, 125c353a5a649ae6d2736beb, 1ce10ed6a60467097a0e8954,
  1e05c650cc8db9c4b17b7a14, 2f1080e911cdceb7ce8af761, 394a1f54323cd0848f6846f4, 466c019323ca75c7a29014a7,
  51b776c6f9be715dfa873425, 558e62df9930df487f1fcc53.
- **R2 sockets (66) → RUNTIME** (S8.2-5: an open port). Owner by documented port; where the inventory has no owning process
  (ephemeral client ports, two loopback listeners, TIME_WAIT, outbound connections) every possible owner still gives RUNTIME.
  Checked: 036b485511319d498de7b1c3, 04dfc8d284fa6b7475781e80, 080a64cc771dc66e8cd3c08b, 0ac365de51a661c1e2e62249,
  0ae6dff67130ece07e9e4a97, 0c904fbb3a517f263f49b511, 0e666ce31003f24d1bedd075, 11fc46ed83f15ebd0aaa6b3e,
  136b59f7d15ee673faf992ed, 20990fb8677f15b2354a3e41.
- **R3 network state and network specs (53) → RUNTIME** (S8.2-5). Kernel links/addresses/routes and machined in-memory
  spec resources exist only while running; default-layer specs belong to built-in defaults of the image, operator-layer specs
  to a machined network operator (whether its enablement is a built-in default or a machine-config line is not inventoried;
  RUNTIME either way). Checked: 07fd45398afa808b12852ac0, 0d356dbed0f7fff446f4f8e5, 202403069a53c026f26088a6,
  26b02098e721b15ae85cc44e, 2b8a5aacbc6b2dde050c6327, 2f36d1463959ee3f8c73cb86, 37f5b08127cb39525bcde935,
  39e911e8d94ef57dd10c557c, 3a372dbbd8996d951d2d9ff6, 53029dc0a8684c3e0010bb45.
- **R4 mounts and mount statuses (31) → RUNTIME** (S8.2-5: a mount point). Checked: 016636da9c246655145b92ca,
  112f6ce3cb5100c97870cc46, 179af8e436d0ab96c2c99c16, 197ca8731d6ee56837aa3775, 375b96b2181a4093f5d06955,
  376f3d958c59866907a4a115, 47175859997987bc259f9388, 4adb7ee22e4573244c86f62f, 66ac39ac276a85f6d4cfb987,
  9b94d718f96a2640d02f8dfc.
- **R5 loaded kernel modules (10) → RUNTIME** (S8.2-5): the loaded state belongs to the module file of the image.
  All 10 checked by hand.
- **R6 block devices (4) → RUNTIME** (S8.2-5): kernel device registrations (loop devices of the squashfs images, the
  virtual disk and DVD drive). All 4 checked by hand.
- **R7 container images (12 = 4 images × tag, digest and id references) → UNKNOWN**. Q1 no (containerd is not an installer
  by its documentation, S8.1-4), Q2 yes (S8.2-9, S8.2-22). By S8.2-16 the line depends on who obtained it: pulled by
  kubelet/CRI for Talos-generated pods → PROGRAM-DERIVED; pulled by a person (e.g. an image-pull command) → PROGRAM-OWN.
  The inventory does not record the puller (the `io.cri-containerd.image=managed` label is set for any CRI pull).
  Checked: 4e385729d820ae8a12c281ea, 5defa9092f0736a78e47ecd5, 655133309975caeeb6640386, 70f7ef9c1053aac7ea64a328,
  8902324d1e310aff27d85eec, a004b567792051e3e6965bc9, a20f4b312088c2c878ded20c, ad5f9ee7ce61d8724bb1f543,
  c2b615022e7beec6f21748c3, d86e87c3a94d6d057da0ab83.

## Rows decided one by one (68)

Package (1), services (12), containers (2), all L2 rows (53). Reasons are in the output. Points worth stating:

- The installed image: package by S8.1-6, reason `explicit` → INSTALLED-OWN.
- Services: a service whose enabled state is fixed by machined code in the image is a default setting value obtained with
  the package and as received → Q1 yes (S8.2-8) → INSTALLED-PACKAGE. etcd and trustd are enabled only by the
  control-plane machine type, a value of the machine configuration → not as received; a service is a setting (S8.2-13)
  → SETTING-OWN.
- Read-only image files (squashfs root, `/etc` lower layer with no controller writing the file) → INSTALLED-PACKAGE:
  the documentation establishes the read-only base. Residual not established by the inventory: an `EtcFileConfig`
  document of the machine configuration (not inventoried) could place a file of the same name in the tmpfs upper; the
  image file itself would stay unchanged below it. The four checked sizes match the source.
- Files written by machined into tmpfs (the `/etc` upper, `/etc/kubernetes`, `/etc/cni`, `/run`, `/system`) → RUNTIME:
  they exist only while the computer runs.
- `/opt/cni/bin/*` and the groups `/opt`, `/opt/cni`, `/opt/cni/bin` → UNKNOWN: shipped in the image, but `/opt` has a
  writable persistent upper and integrity is unknown; unchanged gives INSTALLED-PACKAGE, rewritten gives a program decision.
- Opaque directories: on tmpfs or pseudo filesystems → RUNTIME for every possible content; on persistent storage or the
  `/etc` overlay → UNKNOWN (contents not inventoried).
- `/var/log` → RECORD (all members are logs or log directories). `/var/lib/cni`, `/var/lib/etcd`, `/var/mnt`, `/var/run`:
  written or created by programs as they ran → RECORD (members of MIXED groups).

## MIXED rows in full

- `/` (d82085fcdfd8922534b0400b): `/.extra /bin /boot /lib /lib64 /mnt /root /sbin /usr` INSTALLED-PACKAGE;
  `/dev /proc /sys /run /system /tmp` RUNTIME; `/etc` MIXED; `/opt` UNKNOWN; `/var` MIXED.
- `/etc` (79eb0f8bca299bc0071046b6): `apparmor apparmor.d lvm selinux ssl ca-certificates localtime pki os-release
  nfsmount.conf xattr.conf extensions.yaml` INSTALLED-PACKAGE; `hosts resolv.conf machine-id cni kubernetes iscsi nvme`
  RUNTIME; `cri` MIXED; `containerd` UNKNOWN.
- `/var` (170147a6d5dc76a88b74d35e): `log mnt run` RECORD; `lib` MIXED; `system` UNKNOWN.
- `/var/lib` (b106dcdb914f18f62f868511): `cni etcd` RECORD; `containerd kubelet` UNKNOWN.
- `/etc/cri` (c5c75b80d7d84f871fdd7d89): `containerd.toml` INSTALLED-PACKAGE; `conf.d` MIXED.
- `/etc/cri/conf.d` (031345862da2c66a525d289e): `00-base.part hosts` INSTALLED-PACKAGE; `cri.toml base-spec.json` RUNTIME.
- `/etc/ssl/certs` (6dd18ebf778907d1984a1cfc): `ca-certificates` INSTALLED-PACKAGE; `ca-certificates.crt` RUNTIME.

`xattr.conf`, `lvmlocal.conf`, `lvm/profile/*`, `apparmor/parser.conf`, `apparmor.d/abi/3.0`: no Talos controller writes them
(source of the v1.14.6 tree), so they are in the read-only lower layer that the image build fills; their exact package
inside the image was not traced.
