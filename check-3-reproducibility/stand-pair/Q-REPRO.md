# BQ1 — Check 3: independent bootstrap supplement

Performed by the executor. Fixed conditions in `PROTOCOL.md` and `PAPER.html` are unchanged.

## Classification before rerun

| Previous reason for `?` | Kind | Work |
|---|---|---|
| Most equality inherited from one prepared instrument | (a) insufficient stand coverage | Build two instruments independently from stock Debian, same cloud-config, source and bootstrap inputs; no prepared B image as parent. |
| `base-*` inventory snapshots do not reconstruct the base | (a) limited procedure | Capture stock baselines and post-bootstrap deltas. The scripts reconstruct the added instrument; stock distro internals and mutable apt resolution remain explicit scope limits. |
| `kworker` names/workqueue labels differ on equal virtual hardware | (b) paper does not decide granularity | Keep full records. Do not reinterpret identical kernel executable as an automatic exemption for internal tasks. |

## Inputs and procedure

See `raw/q/repro/INPUTS.md`, `prepare.sh`, `bootstrap.sh`, `run.sh`, `collect.sh`, `finish.sh`, and `src/`. Each overlay is directly backed by `B/debian-base.qcow2`; no B/pristine or B/clean image is used. Both install the same package list and compile the same controller sources independently, then apply `src/repro-root.json` without bypass lines. `inputs.sha256` records shared input bytes.

Initial launch attempts exited 75 before any VM started; a successful `systemd-run` submission alone was **not** a running VM.

## Difference policy fixed before comparison

The exact §9.4 failure sentence is: “The running components differ, and the difference is not explained by differences in hardware.” Therefore only a difference explained by hardware is an allowed **component** difference. Equal virtual hardware cannot excuse a component difference merely because it is transient or nondeterministic.

PID, timestamp and machine-ID values are retained as raw runtime/identity data; they are not in themselves different program/driver/service/user components. The inventory preserves process multiplicity, executable target, UID, arguments and kernel task labels. It gives installed-package and launched-process scopes separately; neither silently replaces the other. Groups and generated policies supplement the accounts comparison. Collector/connection metadata exclusions are disclosed in each census's `NORMALIZATION.md`; the full raw records remain available. Derivative/data bytes are outside §5.3's transfer claim (O8), not an exemption for a difference in running components.

## Result: `?` overall; independent-bootstrap coverage repaired

Both independent bootstraps and declaration applies succeeded. The initial harness had a relative-path error (`run.sh` in systemd's default directory); corrected units used the absolute script path, without modifying the bootstrap. Each machine used 4 GB RAM and 2 vCPU. Both were powered off and their disposable disks and seeds deleted (`raw/q/repro/cleanup.log`).

| Comparison | A / B | Result |
|---|---|---|
| Stock package records before installation | 324 / 324 | Same stock input; inherited baseline explicitly measured |
| Independently added package records | 777 / 777 | Same names/versions/statuses; no changed or removed baseline records |
| Final package records | 1101 / 1101 | Identical (1100 installed; figlet retained as config-files record) |
| Accounts; active units; unit-file states | 31; 43; 138 each | Identical |
| Kernel; loaded modules; PCI devices | same kernel; 52; 8 each | Identical compared fields |
| Groups and generated rules; unit links | exact bytes | Identical |
| Root declaration and compiled/controller/catalog artifact hashes | exact bytes | Identical |
| Userspace process records | 20 / 20 | Identical exe, UID, argv, comm and multiplicity |
| Kernel process records | 68 / 69 | Different `kworker` labels **and count** |
| Machine IDs | `f0a71939…` / `f7b21a2c…` | Distinct identities, preserved raw |

Evidence: `raw/q/repro/{a,b}.evidence/bootstrap.log` records each independent apt/compile/apply; `{a,b}.evidence/baseline/` and `census/` retain command outputs and inventories. `comparison.txt` is the exact inventory diff; `summary.json` lists every added package and every differing task record. `applied.sha256`, `catalog-artifacts.sha256`, `rules.txt` and `unit-links.txt` under each evidence folder are byte-identical. Collection errors are empty on both machines.

Only kernel worker identities/multiplicity differ in the compared running-process records. This is not explained by hardware. **The executor does not exclude those differences:** if those internal tasks are separate running components, §9.4's raw failure condition fires; if they are instances within the same kernel component, this observation is not a component difference. The paper does not choose that granularity. Thus the clean-bootstrap mechanism has withstood its finite comparison for the unambiguous package/account/service/driver/userspace scopes, while the fixed overall Check 3 remains `?`.

What changed since `RESULTS.md`: the 777 added records, compiled controller and policy generation are now independently produced twice, so prepared-instrument inheritance is no longer the reason for their equality. Remaining (a) limit: the stock distro's 324 records are still a fixed input, and `base-*` snapshots remain outputs rather than a controller language reconstructing all stock behavior. Mutable apt sources were identical and resolved identically in this run; no claim is made about future dates or independent builds from an empty disk. These limits and the (b) kernel-task question are explicit; no stand defect has been proved inherent in the hypothesis.

## Question for the author: internal kernel tasks

§5.1 says “Running components—users and the rules under which they operate, programs, drivers, and services.” P1 says “Everything that runs on the computer is recorded in the declaration.” O9 asks “Do running components include everything installed or only what has been launched?” §9.4 requires comparison of running components with hardware as the sole stated justification for differences.

The new independent-bootstrap evidence has equal kernels/modules/PCI devices and userspace records but different `kworker` labels and counts, 68 versus 69 total kernel tasks (`raw/q/repro/summary.json`, `raw/q/repro/comparison.txt`). Does a dynamically created kernel worker/workqueue identity count as a separate running component, or an internal execution instance of the recorded kernel? These sentences leave the granularity open; they are not themselves proven contradictory. The executor cannot select a normalization rule to turn this into `1` or `0`.
