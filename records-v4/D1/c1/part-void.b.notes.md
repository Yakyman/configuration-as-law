# Stored groups, part b

Scope: positions 1016–2029 within the source-ordered `L2:stored-ownership-unresolved` rows, 1,014 rows. Only the prescribed text, sentence index, fact index, this part's inventory, and its action logs were consulted. No other classification was consulted.

## Evidence and order

Every complete member table was read, not sampled. All 8,059 immediate members are persistent: 7,177 regular files, 862 directories, 20 symlinks. None has an entry in the retained package-file integrity table. Absence is not negative ownership evidence because `D1/in/raw/void/metadata.json` explicitly reports incomplete ownership. Filesystem prefix hashes and timestamps cannot replace installation integrity. Directory execute bits mean traversal, not executable code. Groups mean their listed immediate members, not recursive descendants.

`part-void.b.build.py` checks each complete member count, joins every path against package-files.tsv, checks persistence, applies the rules below, and appends and flushes each completed row. Raw member files cited in output provide the exact objects; evidence below provides the additional deciding provenance. The generation checks distinguish caches with logged creation from merely suggestive filenames.

Deciding published sentences, quoted exactly:

- S8.2-6: What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.
- S8.2-7: Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?
- S8.2-8: Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.
- S8.2-9: Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?
- S8.2-10: Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.
- S8.2-15: Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.
- S8.2-16: What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.
- S8.2-23: A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.

## U: unresolved stored namespace members

For persistent stored members lacking installation integrity and decisive instance provenance, Q1 cannot be established. An unchanged member delivered with an installed package gets INSTALLED-PACKAGE; independently created directory/data objects can instead be RECORD or MATERIAL, and independently obtained code can need a program line. Those possible facts do not yield the same decision: UNKNOWN, not a textual gap. This is a homogeneous evidence rule, not a rule that the collector's unresolved label decides the class. Logged generation overrides U. Actual package reasons are available but cannot establish member identity or unchanged delivery. Old module files are specifically under 6.12.11_1; package records instead show 6.12.118_1 and 6.18.64_1. The upgrade log confirms the version transition, not the integrity of retained old files.

Ten manual U checks, including their complete small member lists, were inspected for persistent status, file/directory type, and absence of package-file records:

| id | Checked immediate members |
|---|---|
| void-382fbc60146a798e8fafd883 | cxd2880-spi.ko.zst |
| void-bb76b4dd0498ed1da98b1fd9 | airspy.ko.zst |
| void-9b5b61ee236de39872fa3b38 | dvb-as102.ko.zst |
| void-961ac4786e9fd37a5d788365 | gspca_gl860.ko.zst |
| void-aaf0e760f731f81d9e83e657 | core and host directories |
| void-84418b4f909b539f283a2375 | fusion directory |
| void-b366235856adfd5bcab10fe0 | vmw_vmci.ko.zst |
| void-6534b2e68c413909b4f5884a | altera-stapl.ko.zst |
| void-f55caee51b24e2f83c16c835 | genwqe_card.ko.zst |
| void-2ae05a8a4b35f79781ae03ae | st_drv.ko.zst |

## P: generated Python bytecode

All 101 __pycache__ groups consist only of .pyc files. `D1/in/control/void/actions-logs/actions-logs/browser_extension.log` lines 782–785 explicitly report byte-compilation of Python 3.14 and pip. Source paths are obtained by removing __pycache__ and the cpython-314 optimization/version suffix: every resulting source occurs in package-files.tsv (1,924 unchanged-source correspondences, four changed-source correspondences). Changed source still has a source line; no unchanged-package claim is made for those copies. Q2 precedes the program-record question, so PROGRAM-DERIVED by S8.2-9,10,16. These are native interpreter modules with its rights, not sandboxed guests.

Primary documentation: https://docs.python.org/3/tutorial/modules.html#compiled-python-files — “Python caches the compiled version of each module in the `__pycache__` directory”. The documented optimization suffix and executable compiled-file behavior match the retained names. Generation is established by the local log, not inferred from documentation alone.

Ten manual P checks: void-108c53d220991b17d7ab6592 (__init__, spam); void-8ecc846bbac14bce37c30a60 (__init__); void-1ead24432d8c0c3047f1b640 (__init__, _streams); void-f201dfd8f177a995b2944ada (__init__, _zstdfile); void-eea18c2af51440f2e65e7a73 (__init__); void-0b56f6084362b3816f50c382 (python-config); void-2c567203c09929530f574347 (__init__, connection); void-368b3d866bc3c87cb0a7157d (__init__, wheel); void-a38eb948c40e195c142185e0 (__init__, base); void-7f3045f990f053f7190d2519 (__init__, resolver). Each listed module has ordinary and opt-1 persistent .pyc copies and no other immediate member.

## M: generated MIME descriptions

`D1/in/control/void/actions-logs/actions-logs/application_package.log:448` says “Updating shared-mime-info database...”. The 13 MIME subtype directories contain only persistent XML outputs. These are noncode lookup records written by the update program; no person-chosen system value is evidenced. Q4 gives RECORD. S8.2-16 describes lines for already classified installed objects and does not move generated noncode records ahead of Q4.

Primary specification: https://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html, section 2.1. Quoted passage: “The files created by `update-mime-database` are:”. The enumerated outputs include `<MIME>/MEDIA/SUBTYPE.xml`, globs, magic, aliases, icons, XMLnamespaces and mime.cache.

Ten manually checked M rows (complete listing checked for XML-only membership, persistent status, category and endpoint names): void-4ab73c90e99c24b1fb10c341 (application, 505); void-9f71a3d05aa0b8883e429a2d (audio, 62); void-1b76f2b44c6677eaadefc56f (chemical, 1); void-3c53d5a2bea4b5ffdd8b3725 (font, 5); void-62cbe2c6a73779ab7c8c9935 (image, 101); void-f185ac6a8236aa68ceb0513b (inode, 7); void-aa5952247dee0726fa4a93ed (message, 7); void-e237d9083ceefc9ed7a744a0 (model, 8); void-9539a40ad287b2cb3c008cc9 (multipart, 9); void-dacbbaea5fd0e1584cb3ce83 (text, 150).


## Individual tail rows

Tail groups were inspected individually. Their recorded what/why descriptions are retained in the output. Specific positive evidence:

- Adwaita and hicolor icon caches: browser_extension.log lines 777 and 780 record their updates. GSettings compiled schema database: line 779 records the refresh. These three noncode generated lookup databases get RECORD.
- /usr/share/mime: all immediate regular files are database outputs, RECORD; immediate directories remain UNKNOWN because the inventory does not establish directory creation provenance or original package state. This is MIXED, with complete assignment by member type in its own member table.
- /var/cache/xbps: all 588 filenames (294 archives and signatures) individually match download messages in the action logs. All get RECORD: these are cached downloads, not the unpacked installed contents. Primary documentation https://docs.voidlinux.org/xbps/index.html distinguishes “installed packages” from “cached package files”.
- /usr/share/man/man1: the action logs explicitly say `Creating ... symlink:` for apropos.1, awk.1, find.1, hostname.1, logger.1, man.1, python.1, sh.1, whatis.1 and xargs.1. These generated documentation pointers are RECORD. ex.1, vi.1, view.1 retain UNKNOWN provenance. MIXED.
- /usr/share/man/man8: ntpd.8, ping.8, ping6.8 have explicit creation messages and are RECORD; traceroute.8 has no such retained evidence and is UNKNOWN. MIXED.
- Names suggesting caches, leases, secrets, logs or identities do not establish the instance's creation origin. The remaining tail UNKNOWN reasons name the missing fact explicitly. The generic logged ldconfig cache update does not identify regeneration of its auxiliary cache.
- No runtime classification is inferred from symlink destinations: the inventoried symlinks themselves are persistent objects.

Section 8.5 excludes storage/removal mechanisms and declaration form from the definition; no gaps were introduced for those design choices.
