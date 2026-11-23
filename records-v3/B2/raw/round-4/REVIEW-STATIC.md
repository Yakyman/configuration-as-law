# BC4 independent static review

Status: pending fresh-VM evidence. Source review does not close variants or accept the testbed.

Scope: C2.1–C2.6, C3.1–C3.5, C9.1–C9.6 and the ordinary-work paths. Reviewed the governing text and sentence identifiers, TASK-B2, B1 channel rows, existing stand/how-to/self-test and build reports, new channel modules, fixture producers, integration and guest self-tests. No VM probes were run by review.

## Findings sent to builder

1. `build/stand.py:frontend` omits `stand-appimage` from its generic removal dispatch, while `../../build/app-selftest.py` expects `stand-appimage remove ID` to succeed. This prevents the exact supplied AppImage removal workflow and its self-test from succeeding. The fix must be present in the final rebuilt source and its positive removal/negative retained-entry tests.
2. `../../build/app-fixtures.py` attempts execution of `/unrecorded`, which is absent from the fixture, and accepts ENOENT. That result alone is not evidence of mandatory execution refusal: an unconstrained process would also fail. The same fixture's write attempt uses a root-owned root directory; ordinary DAC explains refusal. These tests must be described at their actual strength. An existing non-entry executable or an actual retained unrecorded path must be attempted to substantiate the execution boundary, alongside the existing namespace/bind/frontend negatives and previous common-boundary regression.
3. `../../build/app-selftest.py` runs a short-lived container to completion before removing its declaration. It checks revoked entry/name requests but not removal of a living container process. C9.6's complete lifecycle closure requires a live process and any descendants to be observed before removal and absent afterward, with retained image content unable to restart it. The shared `codeboundary.revoke` mechanism is present; the application suite needs evidence that it applies to the new container mode.

## Mechanisms supported by source inspection

- Language admission reconstructs complete locks, checks archive contents and dependency edges, embeds exact archives and lock bytes, and never starts package install hooks. Unsupported source backends, lifecycle commands and mutable environment operations refuse. Recorded project execution uses the existing sealed root and fixed interpreter arguments; node receives disabled JIT/WebAssembly options. These are finite supported formats, not full upstream package-manager compatibility.
- Repository admission selects exact catalog payloads with dependency-state records. The base-update catalog is made by real old/new package transactions during image construction; runtime selects exact changed bytes and the full package-version map, and readback uses actual files and package versions. This is one concrete update path, not arbitrary future package transaction support.
- Flatpak validates genuine OSTree app/runtime commits; AppImage imports a real Type-2/SquashFS artifact without running its runtime; OCI verifies content-addressed descriptors and exact process configuration, with a distinct image line. All select a static entry and an immutable own-root launch. Existing AppArmor, identity drop and inherited seccomp remain in the common launcher.
- Direct import records file content before launch. Fixed source compilation requires recorded source and a checked recorded compiler, uses an unprivileged compiler domain and publishes inert output for separate import.
- User jobs pass the existing unit validator and application path. Saved Wi-Fi and prepared/paired Bluetooth line handling exists; prepared state must not be presented as pairing. Hardware is not tested.

## Remaining acceptance conditions

The final rebuilt-image logs must show actual positive channel runs, negative attempts as ordinary user and through root frontends, full line readback, removal evidence, and previous suites passing. Exact declaration lines and commands must be exported into CHANNEL-PATHS, with finite format/default restrictions and hardware limitations stated. A static reading is not a result for these runtime conditions. The evidence cannot justify `STAND: built` while the already documented TASK-B2 limitations persist.

S2.1-4: “For a recorded object, its line states the required state; whether a recorded program is running at a given moment does not matter unless its line requires it.” The review distinguishes import-request specifications from actual emitted declaration rows and requires the latter for Check 2 assembly.

The identified issues concern this implementation and its test strength. No definition-only argument establishes an obstacle for every possible system. Review outcome at this stage: ?.

## Reviewed source identity

Recorded 2026-11-22T10:36:34Z. Later edits require re-review.

```text
cb5af92e62222825190b9c565bda20d378946e518955519047faba6a4e3ff67c  B2/build/stand.py
c540eba0d617267a90fcf5e0174b07d5adcec5e6782271fd2800311ff78699e2  B2/build/guard.py
8a27ab5f45ed7eb48c4d2d013d9a498906e452fc093bdf7c07b7682447a0d575  B2/build/codeboundary.py
7cc464e31538bc0dd28dc87c9ec61da9da27c090a68165861e21756d78d60245  B2/build/session.c
2d189d702adc7b392710f4210189b8b03b29c79dd612ebaabd76c5290c05eb97  B2/build/build.py
9f2226384895fff35d542f881331f2102da397edda3cc7d03f3ad35af70adcb0  B2/build/transactions.py
bf5523f083eb162c60ec2f4341b2a676e11b68419b2c6b6068b912a53d429b32  B2/build/install-channels.py
19c0141627a231fc186be4726f358b23008f44af88472b437b1918900dc72269  B2/build/language_channels.py
75d12450b7982577eeb6bfb5e55c0e73b0432e057a08844f1a2c27386cddd0bb  B2/build/app_channels.py
bd1c28b847ca5826362fa06953b80c70054468f4e1b5be1538132e13fb596985  B2/build/system_channels.py
0e9fff9e938a29e9f9006a32dca15b7e5b36d127b1ec762b6dae8a4004d90a34  B2/build/import_channels.py
107078eeba18183b9f964ad0c9209a10bf7268ed23a37033902fddfe859af8de  B2/build/job_channels.py
a8aeb5755a664a555e723f9802d5104b524efd009ca2bb5600aa0d137e2d59bc  B2/build/app-fixtures.py
a5d9c0a7c107c2d59a4901cffe4e719eadfc91a6e170e3164bb12f203c8e7b8a  B2/build/app-selftest.py
bc49c78bcbacb8b20c45d90db3e31e8d80fde2c60b87a00582303fc90af64417  B2/build/language-selftest.py
ac8714bf9a37761fce4aa37c10f51a4107e0795767fe23d03a82bdbcb248328a  B2/build/system-selftest.py
c010fb442173466f89500c08b26205452318637b02f7e650ea5e43ccc69b4355  B2/build/round4-selftest.py
```
