# Checks for the source-built ConfOS system

This set ports the stand's checks to a small system built from source, with
`confpkg` and a terminal. Its portable cases, semantic declarations and checking
programs were fixed before the system was built and before its first complete
run. No operating-system result is reported by this freeze.

Start with PROGRAMS.md for the minimum program set, PORT.md for the old-to-new
case mapping, and CASES.md for the cases. READY.md and PUBLICATION.txt define the
frozen public set; SHA256SUMS records its input checksums.

Run from this directory, using Python 3, a POSIX shell and a C compiler (`cc`):

```sh
sha256sum -c SHA256SUMS
./selftest/run.sh
```

The self-test uses only files in this set and local temporary fixtures. It needs
no network, system image or neighbouring repository files. It tests the checking
programs, not operating-system enforcement. SELFTEST.md records the results.

References such as `confos/`, `confos-check/`, `confos-check-extra/`,
`records-confos/`, `fifth-paper/` and `sixth-paper/` name top-level folders in the
repository of records. The specification is `sixth-paper/paper6-en.md`, Sections
5 and 7, with the earlier checking plan in `fifth-paper/paper5-en.md`, Section 9.
STATEMENT-LABELS.json includes the 34 statement labels from
`records-confos/TABLE.md` and that source's SHA-256 checksum. Evidence-set labels
E1–E3 are excluded. This snapshot makes catalogue validation self-contained.

The optional historical generator `tools/make_port.py --records-root PATH`
reads `confos-check/` and `confos-check-extra/` under PATH; its default is the
parent of this set. It is not part of the self-test. Its generated PORT.md and
port.json are already included.

The native binding to release 0.80 is BINDING.md (adapter_native.py,
adapter_disk.py, bindings/). It was generated from the builder's interface of 0.80, the
release named for run 4, with its update states 0.80.1 and 0.80.2, and tried on that
release before the freeze (trials are not
runs and report nothing about the system); CORRECTIONS.md lists every change since the
first publication. Facilities that 0.80 does not have give unobserved rows with the
documented reason. ASSUMPTIONS.md records how each assumption was resolved.
Real Wi-Fi and Bluetooth actions require later hardware observations. Fixture
success supplies none of these observations.

Working correspondence, local settings and session state are excluded from the
public set. The code is under the MIT licence; see LICENSE-CODE at the top of the
repository.
