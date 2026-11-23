# Three resolved-row fact challenges

All three sampled RESOLVED:NOT decisions fail their quoted justification. The hole candidates are FACT-WRONG rather than confirmed textual holes: the inventory plus documented capabilities supplies the missing factual correction, and S2.2-2 decides MUST. No probe was run and the sample is unchanged.

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”

## debian-9e34733f17 — python-apt-common

FACT-WRONG; corrected decision MUST. `../in/raw/debian/packages.tsv` records python3 3.11.2-1+b1 and python3-apt 2.6.0 installed; `../in/raw/debian/package-files.txt` lists the importable (not published: external working record), `sourceslist.py`, and `__init__.py`. (not published: adjudication scratch) establishes only that unattended-upgrade does not import aptsources, not that no available caller can use it.

The exact installed-version [source archive](https://deb.debian.org/debian/pool/main/p/python-apt/python-apt_2.6.0.tar.xz), (not published: external working record) lines 88–92, checks `self.source_template is None` and raises `NoDistroTemplateException`, with the message "Error: could not find a distribution template for %s/%s". The [official API documentation](https://apt-team.pages.debian.net/python-apt/library/aptsources.distro.html) exposes `Distribution.get_sources`, `add_source`, and `change_server`; it describes `get_sources` as "Find the corresponding template, main and child sources for the distribution". The available interpreter and library can use this capability whether or not an installed application currently calls it. Removing its templates loses that capability, which S2.2-2 covers without requiring a currently executing caller.

## guix-68f88fa3ed — xorgproto-2024.1

FACT-WRONG; corrected decision MUST. `../in/raw/guix/system-closure.txt` lists both xorgproto-2024.1 and gcc-14.3.0 (the compiler output as well as library outputs). (not published: adjudication scratch) acknowledges GCC but invokes absence of binutils; the adjudication row concludes that nothing can compile against the headers.

The [GCC manual, Overall Options](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html) states for `-S`: "Stop after the stage of compilation proper; do not assemble." It separately documents `-E` as stopping at preprocessing. Thus neither an assembler nor a linker is necessary for the preprocessing and compilation-to-assembly capabilities provided by GCC. Removing the headers prevents those operations on inputs that include them. S2.2-2 decides MUST; this does not depend on building a complete linked executable, and no new input or compilation was executed.

## ubuntu-b20e807939 — /var/lib/apt

FACT-WRONG; corrected decision MUST for the group containing the indexes. The `../compare/joined.tsv` evidence identifies 69 members including actual `noble-backports` Packages indexes, Commands indexes, and `extended_states`. `../adjudication/rows.tsv` calls the indexes cache because apt can fetch them again, without establishing that removal merely slows the same operation.

The [APT manual](https://manpages.debian.org/bookworm/apt/apt-get.8.en.html) distinguishes `update` from `install` and states: "update is used to resynchronize the package index files from their sources." Index downloading is a separate command; it restores the package availability information needed for package selection. Removing the local indexes removes selection/lookup capability until they are refreshed, not merely performance. That is the same asserted mechanism as original card 3's Debian /var/lib/apt example, already resolved by S2.2-2 in `cards.md`. Automatically installed marks in `extended_states` are program state; their treatment does not make the accompanying functional indexes a speed-only cache. No claim is made that every package installation fails: already-installed package information and explicit local package files are distinct paths.

Counts: three sampled justifications fail; three factual/inference corrections; zero confirmed holes from these challenges. The negative existence claims in the first two adjudication notes and the speed-only inference in the third do not follow from their evidence.

## Additional challenge: guix-0abb5d3f0a — alsa-topology-conf-1.2.4

The adjudication's no-tool-use argument does not establish NOT. `../in/raw/guix/system-closure.txt` contains alsa-utils-1.2.11. The [matching upstream manual](https://raw.githubusercontent.com/alsa-project/alsa-utils/v1.2.11/topology/alsatplg.rst) documents compiling topology configuration to a binary file, normalization and decoding, all with file arguments. These operations do not require the described sound device to exist.

However, the available inventory does not enumerate `bin/alsatplg` inside that store output, and the fetched current package recipe is a newer version. Accordingly the exact installed compiler availability is not established by this review. Mark the factual result UNKNOWN pending that evidence, not a confirmed hole: if the compiler is available, losing its supplied topology inputs invokes S2.2-2; if what the object does remains unknown, S3-2 supplies the result. No hardware probe or compilation was run.

S3-2: “If what the object does remains unknown, the case yields ?.”

## Additional challenge: debian-4a04681652 — package-owned /var/log/apt directory

S2.2-6 does not literally describe this row's sole member: a directory is not itself a past log record. The suspected future-logging hole has contrary source evidence: the [APT 2.6.1 source archive](https://deb.debian.org/debian/pool/main/a/apt/apt_2.6.1.tar.xz), `apt-pkg/deb/dpkgpm.cc` lines 996–1002 (`pkgDPkgPM::OpenLog`), calls `CreateAPTDirectoryIfNeeded(logdir, logdir)` before opening logs. `apt-pkg/contrib/fileutl.cc` lines 408–422 implements that helper and creates a missing apt subdirectory from its parent. Thus in this source version, removal of /var/log/apt alone is repaired automatically before subsequent logging; unlike journald Storage=auto, existence is not the logging-mode switch. Under that behaviour S2.2-2 identifies no lost functionality, although the original quote is wrong.

Version limitation: `../in/raw/debian/packages.tsv` records apt 2.6.2. Attempts to retrieve the matching archive and matching public source tag returned 404; no exact-version assertion is made. The close-version source refutes the claimed general analogy to journald, but exact installed behaviour remains an evidentiary qualification rather than a confirmed text hole. No APT process was run.
