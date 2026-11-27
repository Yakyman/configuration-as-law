# Open questions and conservative treatment

2026-11-26 UTC. The definition and plan are unchanged. No decision is requested
from the owner. These entries preserve limits in results.

1. **Q-OPTIONAL — §5.3 many files / open values; §5.4 Q9 external accounts.**
   Reading A: these examples permit designs without the corresponding grammar.
   Reading B: testing every statement needs a real instance. Follow B for coverage:
   W1d-MULTI, W3d-OPEN, W3d-LATEST and Q9-SOURCE are unobserved if unsupported.
   Do not add a fake account provider merely to make a row pass.
2. **Q-LOGIC — §5.2 “There are no degrees”, §5.3 default and breaking.**
   Reading A: reasoning rules are not empirical cases. Reading B: case-party
   classification can be checked on controlled evidence. N-VERDICT and W4c-DEFAULT
   check the reporting logic with fixtures; W5-BREAK requests a guest-only event
   and separate review. Report logic separately; it cannot establish an OS property.
3. **Q-BREAK — §5.3 “superuser privileges and outside the system's tools”.**
   Reading A: successful deliberate raw root mutation is breaking and excluded.
   Reading B: the means were still a system tool or the mechanism was an ordinary
   path. Keep candidate evidence, label undecided pending independent review; do
   not automatically excuse any root command. Q2 installers are never excused.
4. **Q-DERIVE — Table 9 Understanding vs §5.3 obtained/built objects.**
   Reading A permits reading dependencies and outputs of source recipes named by
   a line; strict Table 9 limits packages to those named and disallows machine
   products. Follow the strict reading; underived values cannot pass. If both
   readings are evaluated and only the broader succeeds, mark undecided, not fail.
   No reference installation supplies expected values (review's undecided D1–D6).
5. **Q-UPDATE — terminal base frozen set, ordinary work's two system updates.**
   Reading A permits two real transitions of the system source/recipe lock within
   the named release's test inputs. Reading B requires successive released bases.
   Require two actual source/recipe system transitions with boot and conformity
   evidence; if only payload versions change, OW-2/3 are unobserved. Bound from 0.66:
   T1 and T2 are the builder's update states 0.66.1 and 0.66.2 (INTERFACE 9), each a
   base release of its own tree (`base 0.66.1 FOLDER SHA256`, `VERSION_ID`, `CONFOS BOOT
   DONE 0.66.1`) that changes sources and recipes (tzdata 2025b -> 2026f, then file
   5.46 -> 5.48) and the system's own packages (base-files, confos); both readings ask
   no more than this, so the rows are judged as observed.
6. **Q-PLAN — review R8 / paper 5 §9.3 recorders written for the implementation.**
   Version 5 allows refusal or recording. Record text and strict-plan outcomes
   separately if an actual recording tool causes that distinction. Do not revive
   the withdrawn affirmative recording duty in X-REC; refusal alone cannot supply
   a positive installation, which must still be performed through manual lines.
7. **Q-OPEN-BOUNDARY — §5.4 Q1 “exactly as far as that line opens”.**
   Lexical pathname vs resolved target/inode are possible readings for aliases.
   Use resolved-target containment for success; test symlink out, prefix sibling,
   moved file and removal. If the line documents broader inode effects, retain
   an undecided row pending the text's application; do not silently widen scope.
8. **Q-PRODUCT — removed browser/container/VM product cases.**
   The small base has no such consumers. General bring-in and code/configuration
   cases preserve default-law checks; they do not empirically demonstrate Q5/Q6
   inside those absent products. Mark dedicated cases unobserved until facilities
   exist. This is a coverage limitation, not an instruction to grow the base.
9. **Q-GENERATION — §5.2(2)/(4) "not on the computer" vs §5.5 "generations and rollback".**
   The system partition keeps, besides what the declaration in force brings, the generation
   before the one in force, archives of packages no line names any more, the trees of releases
   no `base` line names, and sources of such releases. Reading A: these are the system's own
   records of itself (§5.5 leaves generations to the design); what is not in force is not
   installed. Reading B: bytes of a removed program are still on the computer, so a removal
   (§5.2(4)) is not complete while they remain. What a line brings is not part of this
   question (§5.3 "written": what the system obtains or builds from a line comes by the
   declaration): the archive of every named package, the tree and the sources of the release
   the `base` line names and the generation in force are derived from the lines and compared
   as `pass` or `fail`. Followed meanwhile: what no line names is neither dropped nor passed;
   the comparison reports it as undecided (core.compare UNDECIDED), and each kind is a request
   to the builder (REQUESTS.md), since only the system can make both readings agree.
10. **Q-AUTOMATIC — §5.3 "what the system itself obtains or builds from a line".**
   The kernel gives an interface brought up by a `network` line an IPv6 link-local
   address. Reading A: it is obtained from that line. Reading B: it is a network setting
   no line names. The case party cannot derive it from the text of the line alone.
   Followed meanwhile: observed and reported undecided.
11. **Worth doing (not in the task): the identity of a description and its inputs.**
   INTERFACE 5 makes the identity from the declaration files only; a `package NAME
   VERSION RECIPE` line names its recipe file but not its checksum, and `confos apply`
   only prints the status when the identity is already in force (INTERFACE 6). A
   changed recipe beside an unchanged line would then not be applied. To be observed in
   run 1 (an edit of a recipe alone, then apply); not alleged before it is observed.
