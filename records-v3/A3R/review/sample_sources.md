# Additional evidence for the sample audit

Reviewed 2026-11-22 UTC. These are documentation checks, not removal experiments.

## Python distribution metadata

The three sampled METADATA files are present in the tar stream saved as
(not published: outside selected checks and direct evidence) (literal `\u0000` represents NUL).
Members are the sampled object names with the leading slash removed. Their relevant fields are:

| Resolved sample | Distribution | Saved fields |
|---|---|---|
| 4 | wheel 0.46.3, bundled with setuptools | Requires-Python >=3.9; Requires-Dist packaging >=24.0; optional test dependencies |
| 15 | defusedxml 0.7.1 | Requires-Python >=2.7 with excluded early Python 3 versions; no Requires-Dist |
| 16 | autocommand 2.2.2, bundled with setuptools | Requires-Python >=3.7; no Requires-Dist |

The adjudication establishes loss of a metadata query, not which installed operational consumer
depends on these particular files beyond reading their descriptive contents. A missing description
alone does not distinguish S2.2-2 from the qualified content exemption. Package installation or
dependency checking can depend on metadata, but the function of these particular copies must be
established rather than inferred from all possible consumers.

The current [importlib.metadata documentation](https://docs.python.org/3/library/importlib.metadata.html)
describes metadata retrieval and MetadataNotFound. The inventoried paths are Python 3.13; its
[source](https://raw.githubusercontent.com/python/cpython/3.13/Lib/importlib/metadata/__init__.py)
has a different implementation: Distribution.metadata reads METADATA, then PKG-INFO, then the
legacy path, and passes the result to the email parser. The exact exception cited for sample 15
therefore cannot simply be transferred from the current documentation to that installation.
This correction does not prove that the file is exempt: the functional role remains insufficiently
established, so the coverage decision is ? under S3-2.

## Ghostscript font maps

Sample 38 is `6ced0da250f732e181bc4cc0`, `/var/lib/ghostscript/fonts`, with members Fontmap and
cidfmap in the saved filesystem inventory. The adjudication describes both as values-only tables.

The [font documentation](https://ghostscript.readthedocs.io/en/latest/Fonts.html) explains their
mapping role, but a mapping role does not establish that both are read only as values. The
[Fontmap reader](https://raw.githubusercontent.com/ArtifexSoftware/ghostpdl/master/Resource/Init/gs_fonts.ps)
uses token parsing in .readFontmap. In contrast,
[gs_cidfm.ps](https://raw.githubusercontent.com/ArtifexSoftware/ghostpdl/master/Resource/Init/gs_cidfm.ps)
sets MapFileName to cidfmap and invokes MappedCategoryRedefiner; the
[map reader](https://raw.githubusercontent.com/ArtifexSoftware/ghostpdl/master/Resource/Init/gs_resmp.ps)
contains `mark exch cvx exec .dicttomark` in the branch reading MapFileName.
Thus the categorical values-only rationale is factually wrong. S2.2-13 explicitly distinguishes
an executed settings file from a values-only settings file; no new textual hole follows.
The saved local map contents and execution restrictions are absent, so this source check does
not silently substitute a fully verified local MUST/MIXED verdict for the original NOT.

## Netdata manifest

Sample 12 contains four named shell scripts and package-manifest. The scripts satisfy S2.2-10.
Neither their filenames nor the manifest's single reported reader establish whether the manifest
only describes files or governs changes to installed files. The raw inventory gives names and
file metadata, not its contents or reader implementation. The asserted whole-row MIXED verdict
therefore exceeds the available functional evidence; S3-2 decides the unresolved member as ?.

## Other sample facts

The eight sampled project package.json script fields are transcribed in `settings_cards.md` from
the saved npm-manifest tar. Removing their dispatch definitions removes the corresponding named
operations, even when runtime import would fall back to index.js. The ordinary module/package,
maintainer-script, unit, group, device-binding and access-policy rows were checked against their
listed members and matching raw inventories; their cited positive rules apply to the identified
code or external effects.

Six sampled Go build-cache directories contain action indexes and/or build artifacts; three Mesa
cache directories contain shader cache data. Regeneration is the cited function. Neither the
table nor the raw inventory establishes execution of those artifacts with the executing program's
full rights, so they do not demonstrate the overlap confirmed for editor/interpreter caches.
The Go directory cf contains only action-index (-a) files. These nine rows retain S2.2-5 on the
available cache-function descriptions; no assertion that arbitrary compiled bytes are unrestricted
executed code is added.
