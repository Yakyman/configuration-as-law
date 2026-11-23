# Sample audit for fix round 1

Recorded 2026-11-22 UTC. This is a bounded correction audit, not final acceptance. Frozen samples, seeds and ordered ids are preserved. No probes or new cases were added; no files under the adjudication work directory were read.

Evidence: `../review/resolved-sample.tsv`, `../review/agreed-sample.tsv`, their companion reports, `../review/card5-challenge.md`, and the matching ids in `../adjudication/rows.tsv` and `../compare/joined.tsv`. The latter two are the factual record used here; this audit does not claim independent revalidation of their underlying package file lists.

## Decision grounds

M (findings 2 and 3): CONFIRMED hole candidate, existing card 3. Treating package metadata as an independent behavior test permits MUST, while removal of the record alone leaves payload consumers/dependencies or generated state unchanged and permits NOT. No quoted sentence decides that scope. Dropping automatic MUST does not establish automatic NOT for the whole package. Content or single-program payload exemptions do not themselves decide the separate package-record question.

H (findings 4 and 5): CONFIRMED hole candidate, existing card 5. The known function requires a different hardware/boot environment. A fixed-environment comparison permits NOT; allowing that environment in the capability comparison permits MUST. The published removal test does not choose the scope. This is textual uncertainty, not missing knowledge of the object's role; do not use S3-2 to hide it.

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-16: “the boot order and device firmware must be recorded where the system is able to change them.”

S3-2: “If what the object does remains unknown, the case yields ?.”

## Affected resolved rows

| Index | Id | Name | Ground | Row-specific reason |
|---:|---|---|:---:|---|
| 3 | `tumbleweed-1a2ff00a85c08b7185dc99db` | `root:man-pages` | M | Manual pages are documented content. A recommendation from another installed package is not a demonstrated lost operation on removal. |
| 4 | `fedora-3f32895ef5232a9ecb90302a` | `user:rdma-core-common` | M | Licence documents and directory ownership do not demonstrate a lost operation. The installed reverse requirement supplies the disputed metadata ground only. |
| 6 | `mint-488c9c6152f9a5f984d35271` | `root:libreoffice-uiconfig-common` | M | The saved account describes single-program UI values. The installed reverse dependency cannot override that exemption without deciding the metadata question. |
| 11 | `tumbleweed-fb68f8c55638ce0185db1206` | `user:displaymanager-sysconfig` | M | The source note says the fillup template has already produced a retained configuration. Its own requirements do not prove removal stops behavior. |
| 12 | `fedora-041e3807da84dd9e46186c79` | `root:kf6-filesystem` | M | Directory ownership and a licence are the recorded payload; requiring another directory package is not a lost capability. |
| 13 | `flatcar-148193fc319dd99b4186c9e5` | `/boot/boot` | H | Known platform-specific boot menu; the prior NOT proof holds the observed boot environment fixed without a selecting sentence. |
| 14 | `flatcar-2a8ca562df17fe66a53a012d` | `/boot/flatcar/grub/x86_64-xen/macbless.mod` | H | Known platform-specific boot module; the prior NOT proof holds the observed boot environment fixed without a selecting sentence. |
| 15 | `flatcar-86b4b62afd038f8594ff2eb3` | `/boot/flatcar/grub/x86_64-xen/search_label.mod` | H | Known platform-specific boot module; the prior NOT proof holds the observed boot environment fixed without a selecting sentence. |
| 17 | `flatcar-0578cc5491998eeb2acff972` | `/boot/flatcar/grub/x86_64-xen/reiserfs.mod` | H | Known platform-specific boot module; the prior NOT proof holds the observed boot environment fixed without a selecting sentence. |
| 18 | `flatcar-da06825ad4492564f1dfb14d` | `/boot/flatcar/grub/x86_64-xen/afsplitter.mod` | H | Known platform-specific boot module; the prior NOT proof holds the observed boot environment fixed without a selecting sentence. |
| 19 | `mint-799ef1effb65ec56ca44deb1` | `root:nautilus-data` | M | The source note establishes the consumer program is absent. The prior MUST decision rests on requirements of this data package, not an established present consumer. |
| 20 | `mint-11ea76b71b17cb2a11ce5b11` | `root:pix-data` | M | The source note describes single-program UI resources and an unavailable macro consumer. Forward and reverse dependencies supply the disputed ground only. |
| 21 | `fedora-2e21e6fd047c2a682612c2e0` | `user:liblangtag-data` | M | The source note describes a language registry used inside the office program. Reverse dependency metadata does not select between the cited content/settings and capability readings. |
| 22 | `flatcar-09e1b0c16fe478d53732fd21` | `/boot/flatcar/grub/x86_64-xen/gcry_md5.mod` | H | Known platform-specific boot module; the prior NOT proof holds the observed boot environment fixed without a selecting sentence. |
| 23 | `tumbleweed-a37f16df0ff2b0a685408d5f` | `root:system-group-kvm` | M | The source note establishes existing groups survive removal of their creation template. Its own requirements do not establish a lost operation. |
| 27 | `flatcar-697c018a7eec871e90bb01f3` | `/boot/flatcar/grub/x86_64-xen/part_bsd.mod` | H | Known platform-specific boot module; the prior NOT proof holds the observed boot environment fixed without a selecting sentence. |
| 28 | `flatcar-c14413689e4e173b4bd79592` | `/boot/flatcar/grub/x86_64-xen/backtrace.mod` | H | Known platform-specific boot module; the prior NOT proof holds the observed boot environment fixed without a selecting sentence. |
| 29 | `fedora-19ba884b9098cd28a76920a5` | `user:microcode_ctl` | H | Known CPU firmware payload; the recorded mismatch and hypervisor exclusion establish inactivity in the observed environment, not the permitted scope of the removal comparison. |
| 35 | `flatcar-439542c6589752b405f1a8b6` | `/boot/flatcar/grub/x86_64-xen/gzio.mod` | H | Known platform-specific boot module; the prior NOT proof holds the observed boot environment fixed without a selecting sentence. |
| 40 | `flatcar-586c641c1b9388b446605f5e` | `/boot/flatcar/grub/x86_64-xen/newc.mod` | H | Known platform-specific boot module; the prior NOT proof holds the observed boot environment fixed without a selecting sentence. |

## Affected agreed rows

| Draw position | Id | Name | Recommendation |
|---:|---|---|---|
| 45 | `mint-707cb6be107ec462ef11c223` | `root:gnome-terminal-data` | M: CONFIRMED; documented help-only payload, with the prior correction relying on forward/reverse metadata. |
| 50 | `fedora-fe662177103b7d48f6e25461` | `user:default-fonts-syr` | M: CONFIRMED; dependency-selection metapackage, whose removal leaves selected packages in place. |
| 53 | `fedora-4ffd8592f62f9410b26561b5` | `root:default-fonts-el` | M: CONFIRMED; dependency-selection metapackage, whose removal leaves selected packages in place. |

## Counts and limits

- Resolved seed `2026112201`, population 888, draw 40: 20 affected (9 metadata corrections and 11 hardware/boot rows). Revised dispositions: 10 UPHELD, 20 CONFIRMED candidates in existing cards, 7 OUTSIDE, 3 UNKNOWN. The 20 unaffected rows retain their prior disposition; they were screened for the two withdrawn grounds, not reprobed.
- Agreed seed `2026112202`, population 14681, draw 60: 3 affected metadata corrections; 57 unchanged UPHELD. Revised dispositions: 57 UPHELD, 3 CONFIRMED candidates in existing card 3, zero UNKNOWN.
- These are counts of sampled rows, not counts of distinct holes. The ten boot rows include the seven additional rows missed by the three-row example in finding 5. The firmware row must also change for the same reason.
- Finding 4 also removes the two named original firmware rows from the additional UNKNOWN set; they are not in either sample. The whole-table card extent belongs to the separate extent audit.
- No affected row receives MUST merely because it requires, recommends, or is required by another package. No affected row receives NOT merely because its hardware or boot environment is absent.
