# Control evidence and its limits after review

Recorded 2026-11-22 UTC. Role: operator. Source analysis only; no mechanism probe or testbed. This addendum supersedes contrary closure claims in the original research notes.

## F and I: available API is not a relevant adopter

- Source: https://raw.githubusercontent.com/torvalds/linux/v6.14/samples/check-exec/inc.c . The source describes two commands: “to initialize a counter from user's input” and “to increment the counter”. Its `interpret_buffer` switch implements only those commands and comments. Descriptor checks and interactive rejection demonstrate the API. They do not establish refusal of own-rights code for the S2.2-10 interpreter class. The old inference from this sample to C7.03–06/17 and C8.03/06 is withdrawn.
- `../raw/python-securebits-output.txt` records argument code executing under mask `0xf00`. It is negative evidence about the one recorded binary/route, not evidence that another relevant cooperating implementation exists.
- `../raw/c7-sources.md` E6–8 records the documented limits of verified-open/audit hooks. These integration points do not prove coverage of custom interpretation by admitted scripts.

Therefore C7.03/04/05/06/17 and C8.03/06 are UNKNOWN. The same dependency also changes C4.5, C7.11 and C8.05 to UNKNOWN. This is an evidence verdict, not a theorem that these inputs can never be mediated. For C7.17, deleting interactive-shell input is a removal option, but no evidence proves removal is the only possible solution; choose the review's permitted UNKNOWN alternative. No CLOSABLE-ONLY-BY-REMOVAL claim is made.

## D: bounded file-open denial, with lost data access

Source: https://docs.kernel.org/6.12/userspace-api/landlock.html . The example handles `LANDLOCK_ACCESS_FS_READ_FILE`, grants selected hierarchy access, and enforces the ruleset before the program runs. In “Filesystem flags”, the documentation states: “Files or directories opened before the sandboxing are not subject to these restrictions.” Its inheritance section describes enforcement on descendants.

The supported bounded inference is that denying an unrecorded file open prevents that file from entering an interpreter through that open. Permit only immutable recorded file content; allowing a whole mutable project directory would not have this property. This supports C7.01/02/07/08/09 and the added C7.24 file route, and the corresponding file-input components of C2.6/C4.4/C7.12/C7.23/C8.01/02. No cooperating F implementation is used as evidence for those conclusions.

A clean boundary before this open is essential. Landlock does not erase arguments, environment, memory or inherited descriptors. It does not identify whether read bytes will become code. Any claim of a complete launcher that sanitizes all those inputs is still unestablished. In particular, C7.05 combines a file-open case with inherited stdin and therefore remains UNKNOWN as a whole. Closure of a bounded file-input route does not imply closure of its interpreter's other routes.

All these D claims sacrifice unrecorded file data reads, including ordinary documents and project data. A mediated reader returning arbitrary bytes to a full-capability custom dispatcher would reproduce the same issue. The record contains no implemented data-reader/language constraint proving retained arbitrary data processing safe. Q3 states that loss explicitly. See `text-audit.md` for the capability premise in the conditional failure argument; a small value parser is not automatically an own-rights interpreter.

## Declaration mutation: primitives versus the unbuilt broker

The original `../raw/install-sources.md` E1/E2/E4–6/E8/E15–20 and `../raw/mechanics-sources.md` E9–12 document package, service, container and privileged mutation interfaces. Install E10 documents mandatory access-control denials. None of their quoted passages establishes a component or complete policy that turns all the named managers' mutations into declaration application while retaining their positive operation. General denial capability does not evidence a correct declaration writer, authorization path, activation transaction, or a policy covering all backend APIs.

The eleven rows named by finding 9 therefore become UNKNOWN: C1.1/1.2/1.4/1.5, C3.1, C6.2/6.3, C9.1/9.5, C10.1/10.2. The same standard propagates to C2.1/2.2/2.5, C3.2/3.3/3.5, C4.3, C5.2/5.5, C6.1/6.4/6.5 and C9.2/9.3/9.4/9.6. Their previous affirmative workflow text is now explicitly a candidate, with missing integration recorded. No new experiment could establish a broker that has not been built; building one is outside TASK-B1.

Bounded native artifact-denial rows remain distinct: their evidence concerns execution/mapping restrictions on an already selected immutable closure, not a functioning install/update broker. Similarly, the bounded M rows concern staging, durability, removal or finite comparison; they do not certify the full lifecycle composition. C6.6 and M4.03 retain only the bounded withdrawal obligation for a fixed controlled activation graph; they do not prove C6.2/6.3's mutation integration. Text and evidence about primitives are not rewritten as whole-system success.

## Runtime changes and counting

R now includes S2.2-15. C7.25 analyses the runtime listening-port change shared by C2/C3/C5/C7/C9.2, with primary source evidence in `evidence-addendum.md`. It is UNKNOWN as a complete route; explicit denied TCP binding is the documented bounded subcontrol. In particular, N and D do not close port changes. The table's CLOSABLE verdicts describe their named bounded route, not every obligation in R or an entire channel; the unresolved common mechanics, listener control and other input variants remain applicable. No channel-wide or system-wide 1 follows from these counts.

The new entries are refinements requested by findings 1/5/8 within existing C7/C10 channels, not extra channels or Check 2 observations. Q2 remains a separate author question about requirements; it is not added as a channel/mechanic count. See `variant-inventory.json` and `row-changes.json` for the updated rows and traceable changes.
