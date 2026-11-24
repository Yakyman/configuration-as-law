# Review of 60 unadjudicated agreements

Seed: `112360`. Selection: `random.Random(112360).sample(pool, 60)`, with `pool` sorted by `id`, restricted to `c1_decision == c2_decision` and excluding every id in `D1/adjudication/rows.tsv`. Pool size: 8,667. The TSV preserves sampling order, every id and name, both original citation sets, the audit result, and saved evidence.

Results: 58 definite decisions supported, 2 agreements on UNKNOWN retained as FACT_UNKNOWN, 0 confirmed new gaps, 0 fact-wrong decisions, 0 outside-definition candidates. One generated-list candidate was tested and refuted. The sample decisions comprise 28 RUNTIME, 14 INSTALLED-PACKAGE, 8 INSTALLED-DERIVED, 6 RECORD, 2 UNKNOWN, 1 PROGRAM-DERIVED and 1 INSTALLED-OWN.

The four sampled Alma module directories contain respectively 31, 12, 2 and 1 files; every one has unchanged package integrity under the documented /lib to /usr/lib alias. All sampled access-policy and unit files have unchanged package integrity. The npm common-ancestor-path directory contains three unchanged native-package files. Dependency/explicit decisions use the recorded installation reason, not inferred package purpose. All sampled second-level runtime members have persistence=runtime in their member inventories.

RUNTIME is a classification of the observed process, registration or live state, not a claim that an unidentified creating executable has a known recording line. Where process identity or kernel provenance is missing, that inherited decision remains fact-limited. S8.2-5 still directly decides that the runtime observation is not a separate object; no extra recording rule is supplied.

The two UNKNOWN rows are `microos-096324109c9ac8e994ba0d84` (snapshot pads) and `microos-0915d2ed36ef7dc450ed046e` (snapshot rshim). Their hll members are 10,478 and 9,939 bytes while only a 4,096-byte digest prefix was retained; the full unchanged-package fact is missing. No conclusion about all snapshot policy files is inferred from these two rows.

## Candidate challenged: generated manual-page index

`alma-3827efd6d880bbf3bcd0736f`, `/var/cache/man/id`, contains `index.db`, `CACHEDIR.TAG` and cache directories. This is a further test of gap card 2 beyond its adjudicated examples. Verdict: REFUTED. A generated list is not made installed merely by being mentioned in a sentence whose subject is what is installed; the four questions classify the object first. A generated cache is decided by Q4. The same reasoning does not exempt executable compiled caches from Q2.

S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

S8.2-15: “Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person created or brought the object, it is material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”

S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

## Sample ids in draw order

- `alma-0c65c3ff2333b5855dfa1218`
- `alma-092f0035b2faaf64ffcb2dad`
- `alma-c6f411a4c2bd699681366498`
- `microos-c9684e80e8b3d52e7ee418f4`
- `alma-2821642a5edb59bff25e15af`
- `alma-d27db61c6b579e648ef02a71`
- `microos-b3730333205a9f6ad2cda9a2`
- `void-c0400ee6edce764cdebdd0db`
- `void-12e180114eab4f7fde0d5c96`
- `alma-087a1813400649dd9e56e473`
- `alma-72edf6df1bee60a1fcddb1e9`
- `alma-471b5be015173cd1cb9865dc`
- `alma-48a72413b1d24b9311047c12`
- `void-3f37ece565e36d2600a0d000`
- `alma-bc4d91d8c3d76ff0ba162f46`
- `alma-c229307d1daea5d6434ecd00`
- `microos-5ed5af72cb73f4b8e2b40626`
- `alma-8a1982f8de3a90582f69dc3e`
- `alma-d69cbca7fd0f0a2612457bca`
- `alma-33377b95aa2d78a301956e23`
- `alma-ec53ac2f1492971be4620e70`
- `void-00ce986c3c527a39faf4633b`
- `microos-b9d5df898e3b476d5283db7d`
- `alma-019b22aefbb768fb5c779770`
- `alma-a3b13ac865ddf7b5f1a565f5`
- `alma-aa123bb6c4ca693c57e4f776`
- `void-447523ccb77c9130d5f23d47`
- `void-c8e0d681ca168522d7f71b09`
- `void-47b7fc02c663d9e4e3febc04`
- `microos-85978a69929daf05c51e0994`
- `microos-a30863e2f0d00a92030a899f`
- `alma-b7c72146a0e1e07f4dfd1c96`
- `microos-a0ea4cd28ea51fad3f0ae215`
- `alma-c836ce9165ed36a9db9aa0eb`
- `microos-e683c38f4a3f899ced631a79`
- `alma-3827efd6d880bbf3bcd0736f`
- `alma-7b89b2ac185727d3dd0b3299`
- `alma-39b55c47ca716642f1777a43`
- `alma-cd50d3a56025fd5b1023e76b`
- `alma-eaebee7a7eb0245251323030`
- `alma-b6f4bec0a32747b66985f023`
- `alma-be4c32ab04af87c5779a4749`
- `microos-a4442818b5e5794a4c328dab`
- `void-37db6a13b194238bfc8fd51e`
- `microos-096324109c9ac8e994ba0d84`
- `microos-9c815c410ccc3c953dfcad89`
- `microos-f3587b7e1ddffa58ad812db4`
- `alma-2d715191e8b741a572ba5b4f`
- `microos-e4c77b917726af3c125ced2a`
- `alma-7af9f755a724c38d5ce36106`
- `alma-7b2963fd52580bd789eadd6b`
- `alma-2ef3dae64154b22228d95f21`
- `microos-404b39a1aac216cfdc436d03`
- `microos-0915d2ed36ef7dc450ed046e`
- `microos-cf59a7f574436cacfebf1ba0`
- `alma-fddaffb857e71d8cd8617517`
- `alma-16dd34e2bdaaababf4c40f8f`
- `alma-b326711741fcc91fc83702fa`
- `microos-81be6e697d930a910edddcde`
- `void-a49de98fffdc1bbcbe657853`
