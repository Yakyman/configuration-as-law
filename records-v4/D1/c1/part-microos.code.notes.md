# Code, image, and snapshot slice

Read (not published: orchestration), TEXT.md Sections 8.1–8.3 and 8.5, SENTENCES.md, and the microos fact index. No other classification was consulted. The output contains 1,896 assigned rows. All are explicitly persistent in their retained metadata; none qualifies as RUNTIME merely because a disposable installation was inventoried.

## Homogeneous rule: retained snapshot files

Applied only to the 1,875 individual files below snapshot 1. Decision: UNKNOWN. S8.2-7 asks whether the object "was it obtained as part of such a package and does it remain as received?" S8.2-16 distinguishes the package line from a source line. Snapshot-specific package provenance and installation integrity were not collected. The current-root package-files table cannot be applied to a different snapshot by removing the prefix. Mode bits and shebang flags are not package provenance. A prefix digest does not establish full-file integrity. Equal full-file contents establish equality, not how a copy was obtained. These are missing facts, not a textual gap.

The script checks persistence for every row. Of these snapshot files, 1,873 have a current-root counterpart with unchanged integrity; one counterpart has unknown integrity and one lacks an entry. Exactly 465 also match full-file size and signature against a current-root unchanged counterpart. These stronger matches still do not identify actual snapshot-copy provenance. No independence or source-generation assumption is added.

Ten hand-inspected rows, including scripts, binaries, and shared libraries:

- microos-900b60a922695141d874da92: theme activation script; persistent, 1,748 bytes, no exact snapshot package entry.
- microos-9d3252cb482db18294bcb635: egrep wrapper; persistent, 102 bytes; full equality still lacks snapshot provenance.
- microos-171b4cdc14cf247f11ca2b46: nsenter executable candidate; persistent, 39,440 bytes; only 4,096 hashed.
- microos-31797ce7bc86785e054b07c0: unlink executable candidate; persistent, 39,312 bytes; only prefix retained.
- microos-7cdfdd40f0fcf7b8e2d81b3b: dracut module setup script; persistent, 3,502 bytes; missing snapshot provenance.
- microos-5faf66d2cfde8d08355a62b4: dracut pollcdrom setup script; persistent, 217 bytes; missing snapshot provenance.
- microos-0ff4c854405acc4194570659: modem plugin library; persistent, 26,832 bytes; prefix cannot certify integrity.
- microos-9eca87132c50b87369acf227: transport crypto library; persistent, 59,520 bytes; prefix cannot certify integrity.
- microos-c4f62b944c241e9a017e3b4f: filesystem plugin library; persistent, 18,520 bytes; prefix cannot certify integrity.
- microos-d56723cb64ff372b378c8463: SELinux boolean utility candidate; persistent, 14,520 bytes; prefix cannot certify integrity.

Checks used the exact object JSON in D1/in/part-microos.tsv, D1/in/raw/microos/raw/0004-filesystem.out and exact-path lookup in D1/in/raw/microos/package-files.tsv. The rule stops at the unresolved first question; it does not assume all executable-mode objects actually execute.

## Individually decided rows

The nine live GRUB image files under the packaged share directory each have an exact-path unchanged integrity record. Each is INSTALLED-PACKAGE by S8.2-6–8 and S8.2-16, regardless of executable mode: boot.img, boot_hybrid.img, cdboot.img, diskboot.img, kernel.img, lnxboot.img, lzma_decompress.img and pxeboot.img for the BIOS target, and kernel.img for EFI. These nine records were individually checked, not sampled.

The two opaque subvolume rows have no complete member lists; classifying them as homogeneous package content or material would require missing facts. The collector calls the live configuration directory a snapshot, but its label alone does not establish its semantic class. Both are UNKNOWN.

The ten other individual rows comprise four EFI-directory files, two boot images, a GRUB module information script, a theme script, and two shell startup files. Their identity can be described, but no retained record establishes package delivery or whether system generation from a source rather than independent copying supplied each object. These are UNKNOWN for the recording line. Matching packaged bytes in startup skeleton files or the boot image is not a provenance record. No runtime inference is made from boot-time use.

## Public documentation used for identities and limits

- https://kubic.opensuse.org/documentation/transactional-update-guide/tu-howitworks.html : "In the first step, a new snapshot of the current root file system will be created." Its workflow permits later modification; it cannot certify this snapshot's actual per-file origin or integrity.
- https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files : "it reads and executes commands from" the startup file. This establishes that shell startup files are code under S8.2-9 and S8.2-23, not merely values.
- https://www.gnu.org/software/grub/manual/grub/grub.html : "images for booting from CD-ROM drives are now constructed using" the documented boot images. The manual describes boot image roles and construction, but does not establish the origin of an observed copy.

The direct GNU subsection fetches timed out; the indexed official manual excerpts supplied the quoted material. No machine query or experiment was run.
