# Decisions of the separate review (plan, Sections 9.3 and 9.4)

The plan requires a separate review of each decision about an object, of each finding that the text does not decide
a case, of each event recognised as breaking, of which program recorded a change, and of an argument for outcome 0.
Neither party reviews itself. The review is performed by the party that directed the work (sixth paper, Section 2.3 and Table 4). Each entry: what was asked, the sentence relied
on, what is held. An entry is a decision under the plan, not a change of the text; the author of the papers can overturn any
of them.

A party that holds that a sentence decides otherwise writes one entry in its `QUESTIONS.md`, with the sentence. It
does not argue and does not wait.

## R1. A saved object that the system refuses to execute or to obey (2026-11-24)

Asked by: development run dev-11, P4-C5-1 (`~/nvim.appimage`), P4-C6-1 (`~/jq`): the download was saved, the launch
was refused; the rows were `fail` because the file exists.

Sentences: S8.2-9, “Is the object code that the computer executes or can execute: on its own, at a person’s
command, or through another program with that program’s rights?”; S8.2-11, “Is the object a value chosen by a
person that the computer as a whole obeys …?”; S8.2-15, “if a person created or brought the object, it is
material—documents, photographs, projects, downloaded files …”.

Held: both questions ask what this computer does with the object. The routes fall into two groups.

Direct routes: the object itself is given to a program as its program — launched by its path, given to the loader,
named as the script or program file of an interpreter (`bash F`, `bash < F`, `source F`, `python3 F`, `awk -f F`),
named by a startup file, a hook or a unit, imported by a program started in one of these ways. An object that the
system refuses to execute, or to obey, by every direct route tried is not such code and not such a setting; brought
by a person, it is material. If one direct route executes or obeys it, it is a program or a setting in force that no
line records, and the case fails. The routes tried are written in the evidence; a direct route found later by the
search of Section 9.5 reopens the case.

Data routes: a command typed by the person reads the object as data and hands its bytes to an interpreter (`cat F |
bash`, `bash -c "$(cat F)"`, `python3 -c "exec(open('F').read())"`). The review does not decide whether this makes
the object “code that the computer … can execute … through another program” (S8.2-9) or is only “a command that a
person typed himself or herself” (S8.2-4, “that person’s action, not an object”). It is left to the author of the papers
(`cases/QUESTIONS.md` Q11; see R4). A case met on every direct route and not on a data route is `undecided`.

## R2. Ordinary work performed through lines of the declaration (2026-11-24)

Asked by: `cases/QUESTIONS.md` Q10 (OW-7, building a small program; OW-8, a game through a launcher).

Sentence (plan, Section 9.3): “It counts against the hypothesis when an ordinary action cannot be performed through
the declaration and its built-in tools.” Also the list of the ordinary work itself: “running ordinary commands and
one’s own recorded script in the command shell”.

Held: an ordinary action performed through lines of the declaration and their application is performed. The outcome
of OW-7 and OW-8 is the outcome of that performance by the case party. The person’s own direct commands (`gcc -o
~/bin/…`, the launcher downloading into the home directory) are performed too and their result is kept in the
evidence under the name `direct`; it does not decide the row.

## R3. A built-in tool that refuses and changes nothing (2026-11-24, 16:15 UTC)

Asked by: `build/QUESTIONS.md` 1 and `cases/QUESTIONS.md` Q13 — the finding that S8.3-7 has two readings, so that a
row of P4 in which a built-in tool refused and nothing changed is met under one reading only (42 rows of dev-12).

Sentences: plan, Table 9, P4, what counts against: “A channel installs, launches or changes such a thing although
it is not recorded, and this is not breaking; a built-in tool changes it past the declaration.” S8.3-6: “The system
provides no ordinary path for changing what is installed and settings past the declaration.” S8.3-7: “Its tools for
installation and configuration record changes in the declaration even when they run with superuser privileges: an
installer does not install a program past the declaration but adds it to the declaration.”

Held: the finding is not accepted; the plan and the text decide these rows. A row of P4 is an attempt to install,
launch or change what is not recorded, and Table 9 names what counts against it: the thing is installed, launched or
changed although it is not recorded. A tool that refuses, and leaves nothing in force that the declaration in force
does not record, has provided no path past the declaration (S8.3-6) and has made no change that would have to be
recorded. Nothing counts against the row: it is met.

S8.3-7 is a requirement of its own, and no row of Table 9 exercises it: no case of the plan asks a built-in tool to
make a change through the declaration. An implementation whose installers only refuse does not show that sentence.
It is therefore built (notice 3 to the builder) and checked by cases beyond the plan (`cases/CASES-EXTRA.md`),
reported apart from the rows of Table 9. Whether a line written by an installer of the implementation counts is a
rule of the plan (Section 9.3), applied when the outcomes under the plan are assigned.

Applied without changing a frozen program: a P4 row that is `undecided` only for the reason “met under reading A of
S8.3-7 and not under reading B” is met.

## R4. A saved object that only a typed command hands to an interpreter (2026-11-24, 16:15 UTC)

Asked by: R1 above (“data routes”), `cases/QUESTIONS.md` Q11, `search/QUESTIONS.md`.

Sentences: S8.2-4, “A command that a person typed himself or herself is that person’s action, not an object.”
S8.2-9, “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through
another program with that program’s rights?” S8.2-15, “… if a person created or brought the object, it is
material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other
machines.” S8.2-23, “… a file that a program only reads as values does not count as code.”

Held: the text decides. In a data route no program is given the object as its program. The program that opens the
object (`cat`, a command substitution, `open(F).read()`) reads its bytes; the interpreter executes what the typed
command hands it. If that made the object “code that the computer … can execute … at a person’s command”, every text
on the computer would be a program, because a typed command can hand any text to an interpreter; the class that
S8.2-15 names — documents, projects, downloaded files — would then hold no text at all, while S8.2-15 names projects
and downloaded files as material. The reading under which the fourth question still has such objects is the one the
text has: an object that the system refuses by every direct route, and that only a typed command hands to an
interpreter, is material, and the typed command is the person’s action (S8.2-4). Such a row is met. What the executed
bytes leave behind is judged like everything else (P4-PIPE-*: after a restart nothing that was executed may be in
force).

Noted: under the other reading no system with a command shell can have P4. Closing the route means
that interpreters refuse typed and piped commands altogether (kernel documentation, “Executability check”,
`SECBIT_EXEC_DENY_INTERACTIVE`: “a process should never interpret interactive user commands”), and the plan makes the
command shell a condition. If the author of the papers overturns R4, that argument is the argument for outcome 0 of P4 and goes to
a separate review.

Applied without changing a frozen program: an object reported as `data-only` (Q11) is material; a row that is
`undecided` only because of such objects is met.

**Confirmed by the author of the papers, 2026-11-25 16:41 UTC:** a saved, unrecorded script that `cat F | bash`
executes is not a hole in the Law. From this time R4 is the author's decision and not the review's. The other entries of the same kind (R5,
R10, and the copy into a place where execution is allowed) are not decided by that answer.

## R5. An object that an interpreter its form does not name accepts (2026-11-24, 20:20 UTC)

Asked by: `cases/QUESTIONS.md` Q12; complete run 1, where 31 objects of the P1 comparisons carry the kind
`any-only` or `data-only` (`cases/RUN-1.md`).

Sentences: S8.2-9; S8.2-20, “A file containing code that cannot be executed on this computer is not a program”;
S8.2-23, “A file that a program executes as code counts as code even when it contains setting values; a file that a
program only reads as values does not count as code.”

Held, by what accepted the object in the evidence of the run (the routes named in its comparison line):

- Only data routes accepted it — `cat F | bash`, `bash -c "$(cat F)"`, `python3 -c 'exec(open(F).read())'` — whatever
  the interpreter: this is R4, the object is material or a program record. In run 1 this is every such object
  but one kind (git's sample hooks and repository files, the person's own files, a key, the attempt's files).
- A direct route of an interpreter that the form does not name accepted it: decided by what that interpreter does
  with such a file. In run 1 there is one kind: a browser's `times.json` in its profile, accepted by `node F` with
  exit status 0 and no output. Node documents that “.json files are parsed as JSON text files”
  (https://nodejs.org/docs/latest-v20.x/api/modules.html): it reads the file as values and executes nothing of it
  (S8.2-23). The file is a record of the browser (S8.2-15). Such a row is met.
- If a direct route of any interpreter executes code from a saved object, the route is open for every saved file;
  that is the failure of R1, whatever the object's form.

## R6. The inventory before the restart in the cases P4-PIPE (2026-11-24, 20:20 UTC)

Asked by: `cases/QUESTIONS.md` Q4; complete run 1, rows `P1:P4-PIPE-n-before` and `UND:P4-PIPE-n-before`.

Sentences: fourth paper, Section 9.3, “A separate case: a command downloads and executes code without saving it;
after a reboot, nothing that was executed must be in force”; plan, Table 9, P4, “after a restart, nothing that was
executed may be in force”; S8.2-5, “What exists only while the computer runs—a process, an open port, a mount point,
a relationship between services—is not considered a separate object: it belongs to the program or setting that
creates it”.

Held: the text decides. The case is judged after the restart. What the code that the person's typed command ran
keeps alive until the restart belongs to that command (S8.2-4, S8.2-5). The rows of the inventory before the
restart are records, not outcomes of P1 or of Understanding; they are kept in the evidence.

## R7. Attempt 256 of the search's catalogue is a refusal (2026-11-25, 00:30 UTC)

The catalogue counts an attempt as `RAN` when its command ends with status 0. The command of attempt 256 (as root,
`nsenter` into the namespaces of process 1, then printing the file it wrote) ends with status 0 because its last
part prints the file; the file holds `nsenter: reassociate to namespaces failed: Operation not permitted`
(`search/evidence/0.32/256-root-nsenter-pid1.txt`, `search/evidence/0.49/256-root-nsenter-pid1.txt`, read by the
review; the builder's entry 86 says the same). The command was refused and nothing changed.

Held: attempt 256 is counted as refused on 0.32 and on 0.49. It is not a success of the search and does not become
a case. The catalogue is not changed; its count for this attempt is corrected here. With it, the catalogue on 0.32
has 14 direct routes and 3 attempts that ran (202, 234, 241), and on 0.49 none of 182 routes and none of 58 attempts.

Added 2026-11-25, 07:45 UTC: the same holds on 0.55. The catalogue of 04:20–04:48 UTC counts 1 of 58 attempts as
`RAN`, attempt 256; its recorded output is `nsenter: reassociate to namespaces failed: Operation not permitted`
(`search/REQUESTS.md`, entry 3; `search/evidence/0.55/256-root-nsenter-pid1.txt`, read by the review). Counted as
refused: on 0.55 none of 182 routes and none of 58 attempts ran. Each later performance of the catalogue is read
the same way, by the recorded output of this attempt.

## R8. A request that the tool the person ran recorded as a line of the declaration (2026-11-25, 00:45 UTC)

Facts (complete run 2, release 0.49). In rows of P4 a line appeared in `/state/declaration.conf` that the runner did
not write (the case party's Q3: such a row is `undecided` until the review has seen which program wrote the line).
The review read, for each row, the commands with their output and the two copies of the declaration
(`bin/q3-rows.py`, run on the server; the list with the tool and the line of each row: `runs/run-2.recorded.txt`):

| Row | Command, as root | The declaration in `/state` against the one in force | In force after the command |
|---|---|---|---|
| P4-BT-1 | `useradd -m p4user` | `+account p4user 1001 1001 - /bin/bash /home/p4user` | no such account |
| P4-BT-5 | a rule added through `visudo` | `+file /etc/sudoers.d/confos-local …` | `sudo -l` as before |
| P4-BT-9 | `hostnamectl set-hostname p4host` | the `setting hostname` line names `p4host` | the old host name |
| P4-BT-13 | `sysctl -w net.ipv4.ip_forward=1` | `+setting sysctl:net.ipv4.ip_forward 1` | the value is still 0 |
| P4-C1-2 | `apt-get install -y hello` | `+package hello 2.10-5` | `hello` is not installed |
| P4-C1-4 | `apt-get remove -y ed` | `-package ed 1.21.1-1` | `ed` is still installed |
| P4-C2-3 | `pip install pyjokes==0.8.3` | `+pip pyjokes 0.8.3 …` | not installed |
| P4-C3-4 | `npm install -g semver@7.6.3` | `+npm semver 7.6.3 …` | nothing new installed |

Each tool printed `RECORDED <checksum>; run confos apply` and ended with status 0. In every one of these cases the
P1 row of the same case is `pass`: the inventory of the whole machine after the command equals the installation of
the declaration in force.

The text. S8.3-7: “Its tools for installation and configuration record changes in the declaration even when they
run with superuser privileges: an installer does not install a program past the declaration but adds it to the
declaration.” The tools did what the sentence says. The rows are met under both readings that paper 5, Section 8,
leaves open: the line is written before anything it asks for exists on the machine (the computer is brought to a
text written first), and it is written by the tool that received the request as part of its own operation, not
compiled from what programs saved.

The plan. Section 9.3 gives `?` to a case “met because a program recorded the change in the declaration as part of
its own operation” unless the review confirms that the program is a built-in tool “without relying on documentation
written for the implementation; a program written for the implementation therefore does not count as such a tool”,
and “a line written by code written for the implementation counts as written by a program written for the
implementation, also when that code is placed in, loaded by or patched into a program that is not written for it”.
The recorders of ConfOS are code written for the implementation, reached under the names of the tools. The review
cannot confirm the condition. The plan says of this condition that it “belongs to the plan and is not a reading
of [4]”.

Held:

- By the text: met.
- Under the plan: `?` for these rows, by the plan's own condition and not by a reading of the text. They are
  reported so, next to the outcome by the text. A narrower reading exists — the rows are met because nothing
  changed, not because a line was written, so the rule does not reach them; the review does not rely on it.
- No implementation built for this check can meet the condition: whatever code adds the line is written for the
  implementation. The same tools are met under the plan when they refuse (R3). So under the letter of the plan an
  implementation that does what S8.3-7 says is rated lower than one that does not. This is a defect of the plan, not
  of the hypothesis, and goes into the list of places to correct.

## R9. A process whose executable is reported with a path of another mount namespace (2026-11-25, 04:21 UTC)

Asked by: the case party, after `dev-18` on 0.55 (`cases/STATE.md`, result 12). The cases P4-S-135,
-136 and -167 start the recorded mpv (a Flatpak application recorded by a line); the route they try is refused; the
application stays alive after the command's front process is killed. Up to 0.54 root could not read which file that
process executes; on 0.55 `readlink /proc/PID/exe` answers `/app/bin/mpv`, the path in the application's own mount
namespace. The frozen `inventory` knows a process only by that path, `compare` does not find the path among the
stored objects and counts the process as past the declaration: 9 rows `fail`.

Held: this is a limit of the checking programs, not a defect of the implementation and not a question of the text.
A process started by the person's command is that person's action (S8.2-4); the program it runs is recorded if the
file it executes follows from a line. What the file is called inside a namespace decides nothing: the same file has
one path on the machine and another in the sandbox, and a different file can have the path of a recorded one. The
programs are corrected to identify the file by its content, read through `/proc/PID/root` (order 7 of
the party that directed the work), with tests in both directions: the process of the recorded application is placed
with its line, and a process that executes an unrecorded file inside another namespace is still past the
declaration. The correction makes the check stricter for a path that coincides with a recorded one. It is a seventh
freeze, committed before complete run 3; the commit of 04:02 UTC (sixth freeze) was followed by no complete run.

## R10. A saved object that a program recorded by a line reads and executes (decided 2026-11-25, 00:35 UTC; written here 07:40 UTC)

Asked by: the builder, `build/IMPOSSIBLE.md`, “a recorded custom filename reader, release 0.46” (“this wider route
remains open and requires separate review under R1/R4”). The declaration of the builder's probe records, by a line
of its own, a program written by the person. The program takes a file name, reads the bytes of that file and hands
them to the interpreter's string interface (`compile`, `exec`). `python3 <the recorded program> <a saved file that
no line records>` ran the saved file, as the ordinary account and as root (`build/evidence/libpython-0.46.log`).
The file interfaces of the same interpreter libraries refuse an unrecorded file also when a recorded program calls
them (repaired in 0.46).

Sentences: S8.2-9; S8.2-4; S8.2-23, “A file that a program executes as code counts as code even when it contains
setting values; a file that a program only reads as values does not count as code”; S8.3-6, “The system provides no
ordinary path for changing what is installed and settings past the declaration.”

Held (the decision was given to the builder in notice 5, item 4, as “not counted”; it was not
written here until now — an omission of the review):

- What the system can refuse, it refuses: each interpreter that the checking programs try (`bash`, `sh`, `python3`,
  `perl`, `awk`, `make`, `node`) refuses a file that no line records when the file is named as its program, and so
  do the file interfaces of the interpreter libraries.
- The program of this entry is recorded by a line, so it is not past the declaration; what it does with a file it
  is given is what its line installed. The saved file reaches the interpreter as text handed over by a recorded
  program, as in R4 it reaches it as text handed over by a typed command. The review holds it the same way: the
  saved file is material of the person, and the row of such a route is met.
- Noted: the text does not say this in so many words, and S8.2-23 read alone makes the saved file
  code. Under that reading no system in which a person can record a program of his or her own can have P4: a
  recorded program may treat any input as instructions, the system cannot tell that from reading values, and the
  plan makes recording one's own script and building one's own program part of the ordinary work. If the author of the papers
  overturns this entry, that argument is, together with R4, the argument for outcome 0 of P4 and goes to a separate
  review.

Applied: not counted against P4; listed with the places of the text to state more exactly. No case of `CASES.md`
performs this route; the evidence is the builder's probe.

## A departure from Section 9.5, repaired before complete run 3 (2026-11-25)

Section 9.5: “Each success becomes a new case, committed before the next complete run.” The 14 routes and 3 attempts
that ran on 0.32 after complete run 1 were not added to `CASES.md` before complete run 2 was committed (an omission of
the party that directed the work). On the release of run 2 they were performed by the catalogue outside the run and all were refused.
Complete run 2 is reported with this departure. They become cases in the sixth freeze, before complete run 3
(order 4 of the party that directed the work), together with one way of running saved code that the builder found by
itself (saved Basic macro libraries, builder's entry 80).

## Not decided by the review

D1–D6 of `cases/QUESTIONS-derive.md` (what the derivation of the Understanding row may read and use). Table 9 lets
the derivation read only the packages that the lines name; S8.2-16 records a dependency by the line of the package
that brought it. Rows of Understanding are evaluated under both and are `undecided` when met only with the
dependencies read. Under the plan this stands until the implementation requires a declaration to name every package;
the outcome by the text of S8.2-16 and Section 8.4 is reported next to it.
