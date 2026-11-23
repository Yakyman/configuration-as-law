# Review exposure record

Recorded 2026-11-23 UTC from the review transcript and retained memory only. No raw file was reopened to prepare this record.

## Accidental guest-inventory exposure

A broad source-name search was intended to exclude raw trees, but its exclusion pattern did not exclude `C1/raw/**`. The tool output was truncated. The visible raw matches all named one file:

- `C1/raw/debian-final/raw/0004-filesystem.out`

The following lines and facts from that file were visible:

- Lines 8112, 8177, 8312, 9579, and 9678: JSON filesystem metadata for localized `apt-extracttemplates.1.gz` manual pages under Italian, Dutch, German, default, and Spanish manual-page directories. The records exposed paths plus metadata fields including timestamps, device/inode, mode, owner IDs, filesystem identifier, regular-file type, SHA-256 prefix signatures, signature byte counts, sizes, executability, persistence, read-only state, shebang state, and startup state.
- Line 11853: the same class of JSON metadata for `/usr/share/vim/vim91/syntax/template.vim`.
- Lines 19188–19198: JSON metadata for the `/usr/share/python-apt/templates` directory and the files `debian.mirrors`, `gnewsense.mirrors`, `gnewsense.info`, `ubuntu.mirrors`, `blankon.info`, `blankon.mirrors`, `kali.mirrors`, `debian.info`, `ubuntu.info`, and `kali.info`. The directory record identified a directory; the file records exposed the same metadata field classes described above.
- Line 19572: JSON metadata for the `/usr/bin/apt-extracttemplates` symlink, including its target `/lib/apt/apt-extracttemplates`.
- Line 21018: JSON metadata for a `cpufreq_conservative.ko.xz` kernel-module file beneath a versioned `/usr/lib/modules` tree.
- Line 21259: JSON metadata for the regular executable `/usr/lib/apt/apt-extracttemplates`.
- Lines 23300 and 23429: JSON metadata for a compiled `cloudinit` `templater` cache file and `cloudinit/templater.py`.
- Lines 23776 and 23779: JSON metadata for a compiled `cloudinit.handlers.jinja_template` cache file and `cloudinit/handlers/jinja_template.py`.

Immediately before the first fully visible named match, truncation left only the tail of one JSON record. Its visible tail contained a hexadecimal signature ending in `d2d990e12d85fbd9048bf202121c3d224cf98d4`, `signature_bytes` 2267, `size` 2267, `startup` false, `type` `file`, and `uid` 0. The tool omitted that fragment's file name, line number, path, and preceding fields. They cannot be identified from the retained view without reopening raw data, so none is inferred here.

No fact from these guest-inventory lines was used in the source findings or verdict.

## Source document under `C1/raw`

`C1/raw/plan.md` was intentionally read as a directly relevant source document rather than as a guest inventory. Visible lines 25–38 stated that an earlier review's scope was recorded elsewhere; described a no-execute bootstrap failure and staging correction; described a later filesystem traversal and native-manifest reconciliation for Python metadata ownership gaps; and described a source adjustment concerning a Go startup sysfs huge-page hint and exceptional fallbacks. Earlier search output also displayed lines 31–32 about native manifests explicitly owning the reconciled metadata. No guest object, member, package-file, or query-stdout row was read from this document.

The truncated portion of the broad search output was not displayed and therefore was not an exposure to the reviewer.
