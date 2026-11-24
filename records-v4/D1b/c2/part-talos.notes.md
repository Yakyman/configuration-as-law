# c2 — part talos: notes

2026-11-23 UTC. Input `D1b/in/part-talos.tsv` (43 rows). Inventory facts were read from the handoff copy
`D1b/handoff/talos/`. Output `D1b/c2/part-talos.tsv`.

## Rules applied by script

None. I decided every row by hand. The scripts in (not published: scratch) ((not published: orchestration or scratch), (not published: orchestration or scratch)) only format the
rows I decided by hand; `verify.py` checks ids, decisions and field lengths. Because no rule was applied by a
script, I did not need a 10-row hand check.

## Facts established and their sources

All source links point to the public Talos source at tag v1.14.6. That is the version reported in
`raw/0002-talos-version.out`. A copy of the tag tarball was read under (not published: scratch).

1. **Image root.** `/` is a read-only overlay with lower layers only (`lowerdir+=/layers/layer0,lowerdir+=/layers/root`,
   `ro`) (`talos-mountinfo.tsv`). Its content is the installed image (package `talos-installed-image`, reason
   `explicit`, `objects.tsv`). Entries come from the `fhs` package (https://github.com/siderolabs/pkgs/blob/e6ad19d/fhs/pkg.yaml)
   and the rootfs stage of https://github.com/siderolabs/talos/blob/v1.14.6/Dockerfile (mkdir of boot/EFI, mnt,
   system, opt, .extra, opt/containerd/{bin,lib}, etc/cri/conf.d/hosts, etc/ssl/certs, etc/selinux/targeted/contexts;
   the symlinks etc/localtime, etc/pki, etc/ca-certificates, etc/ssl/certs/ca-certificates).
2. **/etc composition.** (not published: orchestration or scratch): "A managed tmpfs (the overlay
   UPPER) is layered over the existing rootfs /etc (the squashfs static defaults, the lower) … controllers write
   managed files THROUGH it (into the upper)". `/etc/cni` and `/etc/kubernetes` are separate tmpfs mounts (same
   file; `talos-mountinfo.tsv`). So the files the controllers write exist only while the computer runs.
3. **Files Talos writes into the tmpfs upper** (EtcFileSpec writers): hosts and resolv.conf
   ((not published: orchestration or scratch)); machine-id ((not published: orchestration or scratch));
   iscsi/initiatorname.iscsi ((not published: orchestration or scratch)); nvme/hostid and nvme/hostnqn ((not published: orchestration or scratch));
   cri/conf.d/cri.toml ((not published: orchestration or scratch)); cri/conf.d/base-spec.json
   ((not published: orchestration or scratch)); ssl/certs/ca-certificates.crt ((not published: orchestration or scratch)).
   The machine configuration's user `EtcFileConfig` may not target resolv.conf, hosts, machine-id,
   extensions.yaml, localtime, os-release, xattr.conf, or anything under apparmor.d/, apparmor/,
   ca-certificates/, cni/, cri/, iscsi/, kubernetes/, lvm/, nvme/, pki/, selinux/ or ssl/
   ((not published: orchestration or scratch), `validateEtcFilePath`). The source contains no other writer to
   these image files.
4. **Byte equality with image build inputs.** These SHA256 values in `talos-content.tsv` equal the files the Dockerfile copies
   into the rootfs: /etc/containerd/config.toml = hack/containerd.toml (0232be6c…); /etc/cri/containerd.toml =
   hack/cri-containerd.toml (7195d0ce…); /etc/cri/conf.d/00-base.part = hack/cri-plugin.part (e1088f58…);
   /etc/lvm/lvm.conf = hack/lvm.conf (8c23b965…); /etc/nfsmount.conf = hack/nfsmount.conf (04be3cc1…).
5. **extensions.yaml.** The imager writes it into the initramfs ((not published: orchestration or scratch)), and init
   bind-mounts it read-only onto /etc/extensions.yaml ((not published: orchestration or scratch); the `rootfs` bind row in
   `talos-mountinfo.tsv`). It is part of the installed image.
6. **/opt.** /opt is an overlay with lower `/opt` from the image and upper `/var/system/overlays/opt-diff`
   (`talos-mountinfo.tsv`). The upper lists 0 members (`talos-listing-coverage.tsv`, `raw/0138-s4-talos-list.out`), so
   every /opt entry is image content. The CNI plugins come from `pkg-cni-stripped` and `pkg-flannel-cni` (Dockerfile rootfs stage).
   Extensions may not place files in /opt or /etc outside the paths in (not published: orchestration or scratch).
7. **Container images.** `talosctl image list` (`raw/0021-talos-images.out`) shows three records per image: tag,
   digest and image ID. The kube-apiserver, kube-controller-manager and kube-scheduler images are named by the Talos StaticPods resources
   (`talos-image-sources.tsv`). Talos takes them from the control-plane configuration, defaulting to
   `<image>:v<DefaultKubernetesVersion>` = 1.37.1 ((not published: orchestration or scratch),
   `constants.go`). The pause image `registry.k8s.io/pause:3.10.2` is containerd's built-in sandbox default
   ((not published: orchestration or scratch): "DefaultSandboxImage is defined as a constant in cri package of containerd"). Talos does not
   configure a sandbox image ((not published: orchestration or scratch)).
8. **Installer wording.** The containerd README (https://github.com/containerd/containerd/blob/main/README.md)
   describes "image transfer and storage, container execution and supervision". The README never uses "install" for images.

## The gap (12 rows: the container image records)

S8.1-4 makes an installer a program "whose purpose, according to its documentation, includes installing and removing
programs". containerd documents "image transfer and storage", and the kubelet pulls images and deletes them in
garbage collection. The text does not say whether pulling and deleting executable images counts as installing and
removing programs.
- Reading A: it does count. The image is a package (S8.1-6), so question 1 answers yes. The image is an installed
  object, obtained by the system from a line, so the decision is INSTALLED-DERIVED.
- Reading B: it does not count. Question 1 answers no. Question 2 answers yes: the image is code run as its own
  process in a container (S8.2-9, S8.2-22). The decision is PROGRAM-DERIVED.

The two readings give different decisions, and no sentence chooses between them. Both readings put the object under
the line from which the system obtained it (S8.2-16). The same gap applies to the image-content members of
/var/lib/containerd. The MIXED row reports this.

## Persistence

Every member row has `persistence=unknown`. For Talos I used, as FACTS.md directs, the mountinfo candidates together
with the Talos source cited above: tmpfs (/etc upper, /etc/cni, /etc/kubernetes, /run, /system, /tmp) and the XFS
`/var` on `/dev/vda6`.

## Leftovers

(not published: scratch) (an aborted blobless clone) and (not published: scratch) (the source tarball and its extraction)
are reading copies of public source. Recursive deletion is blocked by a guard on this host, so the operator must
remove them.
