VERDICT: DISAGREE

Review of `CHANNELS.md` and `DESIGN-INPUT.md` (task B1), 2026-11-22T05:03Z UTC. Role: review; took no part in B1.
Read: `../TEXT.md` Sections 2, 3, 4.1, 4.3; `../SENTENCES.md`; (not published: orchestration and working notes); `CHANNELS.md`; `DESIGN-INPUT.md`; for checked
claims `MECHANICS-research.md`, `raw/c7-sources.md`, `raw/install-sources.md`, `raw/ordinary-sources.md`,
`raw/PROBE-DISPOSITION.md`, the P01 files, and the cited URLs named below. The file previously at this path was B1's
own internal review. It is kept unchanged as `REVIEW-B1-internal.md`, and the link to it at `CHANNELS.md` line 204 now
means that file. No experiment was run for this review.

## Findings

1. **C10.4 (root editor with a documented package installer), excluded from the table as breaking.** The exclusion
   is unsupported. The text decides the case both ways. S3-6 makes a program a built-in tool when "its purpose,
   according to its documentation, includes changing what must be recorded: a package manager, including package
   managers of programming languages". The Emacs manual documents `package-install`, which "then downloads and
   installs it" (O6 / MECHANICS C10.4). It installs Emacs Lisp code that the editor runs with its own rights, which
   S2.2-10 requires to be recorded. S3-7 says "an editor … [is] not a built-in tool". On the first sentence a root
   `package-install` past the declaration is a P4 failure. On the second it is breaking. COMMON counts "decides it
   both ways" as a hole. The internal review that led to removing the card relied on S3-7 alone and never dealt with
   S3-6's documented-purpose clause. The original card in `MECHANICS-research.md` was right. **Fix:** restore C10.4 as
   TEXT-OPEN, with the two readings already written in `MECHANICS-research.md`. The first line then reads
   74 / 0 / 0 / 4 / 8.

2. **C8.07 (browser extension with browser-equivalent rights), TEXT-OPEN.** The text is not silent. S2.2-13 decides
   the overlap between settings and code: "A file that a program executes as code counts as code even when it holds
   settings". The object in the card is the implementation of a privileged extension API. O10 documents that it "runs
   with full chrome privileges". So the browser executes it as code, it is not a setting, and the settings exemption
   of S2.2-7 does not reach it. S2.2-10 then requires it to be recorded, because it runs with the program's own
   rights. Neither step uses the "effects" condition that the card's answer to its strongest objection relies on.
   **Fix:** make C8.07 a requirement row (must be recorded, S2.2-10 and S2.2-13) and give it a closability verdict
   with evidence. B1 collected no evidence on closing it, so the verdict is UNKNOWN until such evidence exists.
   TEXT-OPEN count −1.

3. **C7.03, C7.04, C7.05, C7.06, C7.17, C8.03 and C8.06 (rows whose mechanism is "I"; for C7.05 the stdin route
   through "F"), CLOSABLE.** The evidence does not show that the mechanism closes these variants for code of the kind
   S2.2-10 covers.
   - The only cited adopter is the kernel sample `samples/check-exec/inc.c`. Its header in the pinned v6.14 file says
     it evaluates two commands: "?" (read a number from stdin) and "+" (increment a counter). Its scripts cannot "do
     whatever the program can do", so they are not S2.2-10 code at all, and the sample proves nothing about refusing
     own-rights code.
   - The one real interpreter that was probed refuses nothing. P01 recorded `PYTHON_CODE_RAN` under the locked mask
     `0xf00`.
   - D (the Landlock read restriction, E12) does not reach argv, inherited stdin, a terminal, or the environment.
   - Concrete bypass, in the channel and without superuser: `python3 -c '<code>'`, or `cat file | python3`, on exactly
     the configuration that DESIGN-INPUT pins. The rows answer it only with "a cooperating interpreter is required",
     and the evidence contains no such interpreter for any language able to do what its program can do.

   This is also a double standard. C7.08, C7.10 and C8.04 are UNKNOWN because integration "was not established";
   these seven rows lack an established integration in the same way. **Fix:** mark these rows UNKNOWN, or cite an
   existing interpreter of the S2.2-10 class that refuses these inputs. Separately, C7.01, C7.02 and C7.05 (file
   route) are supported only through D. They cite F, which has the same missing adopter, so the evidence should be
   E12 (D).

4. **C7.17 (command line typed into a shell).** There are two proposed mechanisms.
   - "I denies unrecorded shell input": it closes the variant only by removing the interactive command shell. That is
     the definition of CLOSABLE-ONLY-BY-REMOVAL, with the loss to state: no interactive shell at all, although S3-7
     itself names "the command shell".
   - "Records command before interpreting": no source or probe is cited.

   **Fix:** CLOSABLE-ONLY-BY-REMOVAL (state what is lost), or UNKNOWN.

5. **C7 data-to-code without an evaluator entry (affects C7.07's "or F" alternative, C7.08, C4.4, C2.6, and Q1).**
   This is a concrete bypass inside C7, with no superuser, that no row answers:
   - The person records a script M for a recorded full-rights interpreter. M reads a file line by line and carries out
     each line (open or write a file, launch a recorded program).
   - M is then run on an unrecorded file F that the person wrote.
   - No exec, eval, import, source, or AT_EXECVE_CHECK point is ever reached, so F and I cannot see the route.
   - Under S2.2-13, F "counts as code", and it runs with the interpreter's rights. So it must be recorded (S2.2-10), it
     is in force (S2.1-3), and it is not recorded: P1 fails (S2.3-4). This is not breaking (S2.1-7).

   The argument uses only the definitions and holds for any system that both admits arbitrary scripts for a
   full-rights interpreter and lets those scripts read unrecorded files. The system cannot tell which admitted scripts
   behave like M without analysing what the script means. So only D, or a restricted admitted language, closes the
   route. Consequences:
   - C7.07 is supported only through D.
   - C7.08's UNKNOWN ("complete mediation … not established") is misplaced either way. With D, the cost B1 already
     accepts for C7.07 and C7.09, the row is CLOSABLE at that cost. With data access kept for arbitrary admitted
     scripts, the argument above shows no mediation of evaluator entries can close it.
   - Q1's list of possible controls includes "a cooperative evaluator checking every file and refusing unrecorded
     snippets/streams", which does not close this route.

   **Fix:** add the variant; set C7.08 to CLOSABLE via D, with the stated cost and a note that the combination "data
   access + arbitrary admitted scripts" is excluded by this argument; remove that control from Q1.

6. **Q3 items 7–8 (writing and running one's own scripts, project dependencies).** These items do not match the
   table. The only evidenced closure of C7.07, C7.08 and finding 5 is D. Under D, admitted scripts cannot read
   unrecorded files, and documents and project data are exactly such files (S2.2-4 exempts them from recording). Q3
   says a "cooperating restricted interpreter retains this route" and never states that admitted scripts lose read
   access to user data. That interpreter has no evidenced adopter (finding 3). **Fix:** state the loss: scripts that
   read user documents or project data either go through a mediated reader or are unavailable.

7. **Q2 (an algorithm computing the declaration from directory D).** The answer chooses between readings that COMMON
   reserves for the author.
   - `MECHANICS-research.md` concludes: "The supposed consequence does not follow merely from allowing an
     external-state algorithm plus P1/P2/P4".
   - B1's own two-computer construction (CHANNELS Q2, steps 1–3) has the same declaration files, no breaking, and P1
     and P2 stated to hold on each computer. Nothing in it shows P4 failing. Yet Understanding fails, even though
     Section 2.4 lists Understanding among "Consequences".
   - CHANNELS and DESIGN-INPUT nevertheless conclude "not a fourth hole" and "S2.5-3 does not compel accepting that
     algorithm". That treats Understanding as a filter on which declarations are admissible.

   The other reading is that Understanding is a consequence claimed to follow from P1, P2 and P4 under any form
   S2.5-3 allows. On that reading B1's construction is a requirement that contradicts another (Section 4.1). The
   reading of "read" as concrete objects versus a rule is a second open choice, which CHANNELS mentions but then
   overrides. **Fix:** record Q2 as an author question with both choices of reading. Remove "not a fourth hole" from
   both files.

8. **Requirement column for the C2, C3, C5 and C7 rows (and C9.2): the "change" part is dropped.** Section 4.3: "an
   attempt is made to install, launch, or change what is not recorded". S2.2-15 says "ports open for connection must
   be recorded". The rows cover only admission of code. A recorded, admitted script that binds a listening TCP port
   on a number taken at runtime changes something that must be recorded, past the declaration, with no superuser.
   Only C9.5 mentions ports. An existing candidate mechanism is Landlock network rules: the Linux Landlock document
   (https://docs.kernel.org/userspace-api/landlock.html) lists `LANDLOCK_ACCESS_NET_BIND_TCP`. **Fix:** add S2.2-15
   to R for these rows and give the runtime-port route a verdict with evidence.

9. **Broker-dependent rows (C1.1, C1.2, C1.4, C1.5, C3.1, C6.2, C6.3, C9.1, C9.5, C10.1, C10.2): CLOSABLE rests on an
   unbuilt component.**
   - The cited passages describe the surface that must be mediated: apt overrides (E2), systemd-run (E16), rootless
     Podman (E19), the existence of NetworkManager and nft. They also state that SELinux enforces denials in general
     (E10).
   - No source shows a policy or component under which these managers' live-state changes can happen only through a
     declaration.
   - C10.3 and M1.02 are UNKNOWN for "no complete mediation proof". C10.1 and C10.2 make the same mediation claim at
     the mutation sink and are CLOSABLE.

   **Fix:** apply one standard. Either UNKNOWN for rows whose closure needs the unbuilt broker, or cite an existing
   system in which the named manager's mutation is reachable only through declaration application. Native-execution
   rows backed by IPE with dm-verity are not affected (see the closing paragraph).

10. **C7.20 (pickle, macro-bearing document), requirement column.** "S2.2-4 versus S2.2-10,13" presents as a
    conflict something that S2.2-13 decides: a file that is executed as code counts as code. The verdict is right,
    but the requirement column misstates the text. **Fix:** cite S2.2-13 as the deciding sentence.

11. **Scope, P01.**
    - No testbed was built and no channel was added. Variants are inside C1–C10, M1–M5.
    - The expected result was written before the run: the plan file was last written 04:50:40Z, the output 04:52:27Z.
    - The question "does Debian Python 3.13.5 refuse `-c` under the bits" could be answered from primary sources
      without a VM: the Debian `python3.13` source package and its patches, and the CPython 3.13 sources. The ledgers
      show no such check. Only two CPython v3.15.0 files and the Debian linux sources were inspected.
    - The result changed no verdict: C7.03 stayed CLOSABLE.
    - The plan says "Prerun refinement at 2026-11-22 04:51 UTC", but the file's last modification is 04:50:40Z. The
      recorded time is wrong, although the refinement does come before the run.

    **Fix:** note in `PROBE-DISPOSITION.md` that the source-package route was not consulted, and correct the time of
    the refinement.

12. **First line and DESIGN-INPUT list.** The arithmetic of the current table is correct: 85 rows = 74 + 3 + 8. It
    must change with findings 1–5 and 9. The "What this design cannot certify closed" list in DESIGN-INPUT must take
    in the rows that become UNKNOWN or CLOSABLE-ONLY-BY-REMOVAL, and C10.4.

## Verdicts established beyond doubt

**TEXT-OPEN:**
- C7.18: I found no sentence that gives priority between S2.2-5 and S2.2-10 for a cache that only changes speed.
- C7.21: S2.2-10 does not reach code with fewer rights than its program, and no sentence defines "own interface"
  in S2.2-11.

**CLOSABLE native-execution rows,** closed by IPE with dm-verity and memfd noexec, which are documented kernel
enforcement rather than an unbuilt component: C1.3, C3.4, C4.1, C4.2, C5.1, C5.3, C7.13, C7.14, C7.15.

**CLOSABLE mechanics rows:** M1.01, M2.01, M3.01, M4.01–M4.04 and M5.01, as bounded mechanics.

**UNKNOWN:** C7.10, C8.04, C10.3, M1.02, M2.02, M3.02 and M5.02.

**Q1:** the conditional failure argument holds.

**No-NOT-CLOSABLE conclusion:** it stands for every variant in the table, and the whole-system outcome stays ?.
Finding 5 adds an impossibility only for the combination "arbitrary admitted scripts with access to unrecorded data".
It does not add one for any channel as a whole.
