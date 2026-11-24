# c1 code and image shard

No participation in preceding preparation or rehearsal tasks. Only the authorized text, sentence list, facts description, this input part, and this machine's handoff were used. No classification from another task was read.

## Rule A: unchanged supplied files

S8.2-6 gives the first question priority; S8.2-7 and S8.2-8 classify unchanged supplied objects, and S8.2-16 covers them by their supplying package. Exact package-files comparisons are unchanged for 251 rows. Package installation reason was consulted in objects.tsv: whether that supplying package is explicit or a dependency does not change the member's package coverage.

The complete filesystem scan records actual symlinks /bin and /sbin to usr/bin, /lib to usr/lib, /lib64 to usr/lib64, and /usr/sbin to bin. These resolve the otherwise apparently missing exact package paths. No equality of hashes alone was used to infer provenance. All these input objects have persistent backing. The eight direct GRUB image members and 243 alias members obey this rule.

Manually inspected IDs, comparing persistent metadata, exact alias and unchanged package record:

- d1b-gentoo-8f6945623c206e0ded79c948: agetty, /sbin manifest alias.
- d1b-gentoo-120b2a9358fefbd2c3cd47a9: dhcpcd, /sbin alias.
- d1b-gentoo-e5f6b730cbc2fe00acc04acf: genl, /sbin alias.
- d1b-gentoo-266b0fb4c5eeab755b2eee56: killall5, /sbin alias.
- d1b-gentoo-fba66f0d14b29bd79288a1c0: nft, /sbin alias.
- d1b-gentoo-2dd528d744754e75ffec3b13: rtmon, /sbin alias.
- d1b-gentoo-a607e502c298e194d7978dfc: vdpa, /sbin alias.
- d1b-gentoo-9e3ea9ac9b5fdfc7281c6e94: librt, /lib alias.
- d1b-gentoo-f771ad1a15de095e38253431: libpthread, /lib64 alias.
- d1b-gentoo-35bceff2764ca2688e5f4987: pam_localuser, /lib64 alias.

Evidence: (not published: over 20 MB); objects.tsv; raw/0004-filesystem.out. Each package-files row retains its original manifest and digest evidence.

## Rule B: repository script provenance unresolved

1358 persistent repository files carry shebang markers. They are not assumed material just because they occur in a source repository. S8.2-9 precedes the fourth question. No exact or alias package comparison exists. The full-digests table establishes current bytes, not historical acquisition. Neither an interpreter marker nor a repository directory establishes whether a person supplied the file independently or the system obtained it from a source line. S8.2-16 permits materially different recording lines for these factual possibilities. UNKNOWN records that missing fact; it is not a textual gap. No assumption that all code has an own line was made merely from missing ownership.

Ten manually inspected persistent shebang rows, with absent exact/alias package comparisons:

- d1b-gentoo-d1a1869b5087cbcc4f6df688: brltty startup script.
- d1b-gentoo-23bbb40d652f108ca13fd6c3: xendomains startup script.
- d1b-gentoo-3e2e302d1ec4f9c631549bbe: mysql log-s6 script.
- d1b-gentoo-0ae660cc0e13306f1496504f: minecraft-server startup script.
- d1b-gentoo-042cbc03a8da5fa4d141ce5d: srs init script.
- d1b-gentoo-9e103ab513022fb651570e90: shorewall startup script.
- d1b-gentoo-997cc2b89a096a2103cb06c4: icingadb startup script.
- d1b-gentoo-1d78bcd5b5ce8439ea750064: havp startup script.
- d1b-gentoo-c4180608424019fe720438c0: man-db cron script.
- d1b-gentoo-c62f739e6cbc0cbddec9ccb7: rpc.rquotad startup script.

Evidence: input metadata, raw/0004-filesystem.out, package-files.tsv, object-fact-index.tsv and full-digests.tsv. The index supplies only full-digest references for these objects. Public documentation cannot establish their historical acquisition.

## Individual cases

The remaining 24 rows were considered individually. The boot directory images lack package references and recorded generating input lists. The GRUB manual identifies first-stage boot code and core-image generation, but does not establish this machine's generating inputs: https://www.gnu.org/software/grub/manual/grub/grub.html . Relevant exact passage: “It is built dynamically from the kernel image and an arbitrary list of modules”.

The initramfs archive has no expansion, so executable membership and generation inputs remain unknown. Shell startup files, local service scripts, command wrappers, Python command entry scripts and the AppImage each have no recorded comparison or historical producing line. Python package presence alone does not prove entry-script integrity. configuration-origin.tsv explicitly records unknown creation for profile.env and the local command script. Prefix signatures and timestamps do not close these missing facts.

The Firefox times.json row is not code simply because a collector marked it as startup-related. Mozilla documents a profile timestamp written during creation: https://docs.telemetry.mozilla.org/concepts/profile/profile_creation . Exact passage: “a `times.json` containing a timestamp of the current time is stored inside that profile directory”. This is program state under S8.2-15.

Both complete store-member tables were consumed: 493 containerd entries and 37 Docker entries, all persistent; traversal_complete is 1 for both in store-coverage.tsv. Each member was checked for type, persistence and role. The containerd keep file has an unchanged package comparison. Metadata databases and UUID are program records; snapshot payloads and content blobs lack recorded image-member comparisons and source lineage. Docker logs, caches and engine identifiers are program records; saved host and container configuration controls launch parameters; remaining database or special members lack sufficient contents or originating-value facts. These heterogeneous stores therefore receive MIXED, with unresolved subsets explicitly identified, rather than inventing homogeneous image coverage.

## Completion

The append script is classify-gentoo-2.py. It verified exactly 1633 distinct input IDs, exactly the same output ID set and count, allowed decisions, and field word limits. Counts: INSTALLED-PACKAGE 251; RECORD 1; UNKNOWN 1379; MIXED 2. The classification table is frozen. PROTOCOL.md Section 2 was then read; there are no GAP-NONE or GAP-TWO rows, so the meaning table contains only its required header.
