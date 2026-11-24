# Instrument expectations

2026-11-23 UTC, before the shared helper build and any extended-collector rehearsal.

The source of C1/collector/probe.go records only a 4096-byte prefix during traversal and refuses full digest requests over 16 MiB. The extended helper is expected to hash complete regular files up to 1 GiB, reject unstable reads, and retain unknown on failure. No digest alone establishes origin or unchanged receipt; a surviving full package record is required for that comparison.

The active /etc subvolume is expected to be traversed while retaining its snapshot row. Other atomic stores retain their original rows; a second bounded inner traversal records member metadata separately. A successful traversal is not a claim that opaque nested images have been extracted or that creator history exists.

Sources checked before these changes:
- https://man7.org/linux/man-pages/man2/openat.2.html: "O_NOFOLLOW"; the existing component-wise no-follow opening is retained.
- https://man7.org/linux/man-pages/man2/stat.2.html: "fstat() is identical to stat()" except its descriptor interface; before/after metadata and current-path inode identity detect ordinary concurrent modification, not an atomic snapshot guarantee.
- https://btrfs.readthedocs.io/en/latest/Subvolumes.html: "A snapshot is also subvolume"; a subvolume marker does not justify excluding an active configuration namespace.

No quota/remaining-limit endpoint is exposed to this session; no account credential files were opened. The task deadline is 2026-11-23 17:58 UTC. No hypothesis outcome is assigned by this preparation task.

Before the first extended-collector run, the five further source/content extent candidates explicitly named by D1/RESULT.md are included. Their IDs are identified from that report's referenced generated/dispositions.tsv, without creating a new decision set. Fontconfig fc-cat is expected to expose cached directory and font names; exact scanned font paths then join to native owner/package-file records. Source: the installed fc-cat(1) manual, read before rehearsal, says "read font information cache files" and documents -v. The published fontconfig user guide https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html documents cache paths and the file font property; the fc-cat web page was inaccessible. This exposes present cache sources, not the event that produced the cache.

Before a final fresh Gentoo run, the shared object-to-fact index is changed from repeated whole-table scans to a single parent-directory index. Both methods select exactly the same unowned immediate paths. The expected output is byte-identical for the same in-memory objects and entries; the change addresses excessive CPU time on the large source-build tree. A synthetic equivalence test covers overlapping groups, owned members, standalone objects and quoted paths. Existing runs retain their earlier-source evidence until replayed with this source.
