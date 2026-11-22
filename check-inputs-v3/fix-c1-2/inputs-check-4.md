# Check 4 concrete inputs

Prepared 2026-11-22 UTC. Publication date is taken in UTC by the binding
TASK-C1 decision: cutoff 2026-11-21T23:59:59Z. Last joint look of the seven release
pages completed at 2026-11-22T05:14:22Z (`../fix-c1-1/raw/release-recheck.md` and JSON).
The later openSUSE look was 2026-11-22T05:15:24Z
(`../fix-c1-1/opensuse/raw/release-evidence.md`); the selected release is unchanged.
This versioned input record has not yet been committed to the repository of
check records. Commit these exact files before any first check observation.
No classification or property assessment is performed by laboratory preparation.
Runner version and system-by-system validation: `RUNNER-VALIDATION.md`.

No test declaration or channel is added beyond the installations and facts
specified by Section 4.5.

## Releases and verified images

| System | Release | Image checksum | Release evidence |
|---|---|---|---|
| nixos | 26.05 / 26.05.14979.94c3211b0ee8 | SHA256 `54034d71971b8937c8e5d85c252053be1a4e010d613d197ba3587dca7548618e` | [2026-11-21T21:58:18Z](https://releases.nixos.org/nixos/26.05/nixos-26.05.14979.94c3211b0ee8): Released on 2026-11-21 21:58:18 UTC |
| guix | 1.5.0 | SHA256 `107e0a8082f03a10b15c1fb9383d2d752c1cdeda41b8db575a15550e1c2d8b4a` | [2026-01-23T12:53:15Z](https://lists.gnu.org/archive/html/info-gnu/2026-01/msg00004.html): This is to announce guix-1.5.0, a stable release. |

Image URLs, signature URLs and checksum references: `releases.tsv`, SHA256 `b289d1c8428eab859cfa36db6dda9c719d3f696a40438f64905cfaa89df4f08d`.
Original image verification is retained under `../raw/`; new openSUSE evidence is
under `../fix-c1-1/opensuse/raw/`. Mint command provenance: `STATUS-mint.md`.
NixOS has a published checksum; no ISO signature was linked by the consulted page.

## Installation recipes and declarations

The NixOS declaration includes both `configuration.nix` and the exact generated
`hardware-configuration.nix`, captured before installation on the fresh replacement
disk. Guix uses the original saved `config.scm` and installation recipe.

| Selected installation input | SHA256 |
|---|---|
| `../fix-c1-1/nixos/README.md` | `31755c2ec329bda0e44be354f3fae5d36e48788673c67def9a75bcda531ae1ce` |
| `../fix-c1-1/nixos/configuration.nix` | `45f4f0c5de2b4bb4e49b6870915e7a66053f4feac30102d695778bc8737c9901` |
| `../fix-c1-1/nixos/hardware-configuration.nix` | `cebc3637167ab8ece0fd8cd18dac47522548b8e2cb47968f2d246bde04fbd7d5` |
| `../fix-c1-1/nixos/install.sh` | `c68fe736907d114490a2306a9098bfb1584477f9575543e022fd1da66fc3c7d4` |
| `../fix-c1-1/nixos/prepare.sh` | `0ca9d511994349992523b95e7f2df2fde3b370b3681b2de0c508643309d43b88` |
| `../fix-c1-1/nixos/launch.sh` | `c85deeb2279f30bf2fd6eac41a73fcc4d2cf96a55c6c94eafa37f90ee44a5842` |
| `../fix-c1-1/nixos/drive-install.py` | `75a51715591e17654cbac0527b623da2e696c29a4e00f53e58b6da920250493a` |
| `../install/guix/README.md` | `41ed64ea8abaea9dabd343a1099a08b68e989316224bf3f09543ac5c183e1d76` |
| `../install/guix/config.scm` | `442f088ab713e68721c4156793f2316a04b785b1c8d8e6dffb11efe31726b886` |
| `../install/guix/drive-install.py` | `ce4c63c94a9093fdfb6cb30b10e1cfe4472e867a4e6711ffdda15a7721cbbec0` |
| `../install/guix/install.sh` | `cad0e6b9348a40db325e9025977e704a04463a3b6e30fe53ae92d824b51880a3` |
| `../install/guix/launch.sh` | `75f9468b92ed1a1013cd4c87628561346920717553b7d71464e19a7f9cb200f9` |
| `../install/guix/prepare-media.sh` | `98a7e81a4e592b806b489fba2d37bdcd8eba58db37c482d68fcb14ec74f830bb` |
| `../install/guix/shutdown-installer.py` | `6951df17961d8e4f19d807fc2c12b155c3a70048d13d63889f3e9c3398d50099` |

Only files in this table are selected installation inputs. Other files preserve
preparation history. Installation system defaults remain as recorded in recipes.

## Known before the first observation

`C1/raw/nixos-install-transcript.txt` and `C1/raw/guix-install-transcript.txt`
contain installed package closures in installer output. The records are retained,
were not read for any property assessment, and are explicitly disclosed here.
New installations retain only exit statuses, apart from the generated NixOS
hardware declaration captured as an input before installation. TASK-C1's binding
05:20 UTC decision settles their status without an outstanding author question.

| Facts exposed | Preserved evidence relative to C1/ |
|---|---|
| NixOS sudo printed its standard lecture (privacy, thinking before typing, responsibility) and that the password would not be visible; constant user/root smoke messages also appeared. | `fix-c1-1/nixos/raw/smoke.txt`, timestamp `2026-11-22T05:18:26Z` |

The NixOS timestamp precedes the 05:20 UTC retention decision; the review's
claim that this record was made after that decision is not supported. Its omission
from the disclosure was still a gap. No property assessment was made from it.
The openSUSE diagnostic, including the rescue text and subsequent prompt
observation, was retained after the decision; this was a preparation deviation.


## Facts to be established per property

The following wording is taken exactly from Section 4.5:

- P1: whether objects that must be recorded can be in force without being recorded
- P2: whether recorded lines are in force after application
- P4: whether a built-in tool can change, past the declaration, what must be recorded

Each pair of a system and a property is a case. The six cases are NixOS/P1,
NixOS/P2, NixOS/P4, Guix/P1, Guix/P2, and Guix/P4. No case has been assessed here.
The independent assessments, sufficiency rule, adjudication and outcomes remain
exactly those of Sections 4.1 and 4.5; no additional decision rule is introduced.

`../fix-c1-1/lab.sh` SHA256 `0439b40388810002c9c9cb67be444e57f706d71e07ccd288542f7eeb5d0834db`.
