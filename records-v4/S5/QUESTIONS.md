# S5-O: questions for the author (second party, supplement 1 step 5)

Recorded 2026-11-23 UTC. None of these is decided here.

## Q1. Is a text the system writes from every saved byte a declaration in the sense of S8.1-2?

S8.1-2: “The computer is brought into conformity with this text, rather than the text being compiled from the computer.”

What the image does (facts, not readings):
- The five filesystem declarations designated in `/etc/stand/bc3-primary.json` (together with `machine.jsonl`) are written by the filesystem
  service, not by a person. Every create, write, truncate, rename, chmod or unlink by any program in `/home/stand`, `/tmp`,
  `/var/tmp`, `/dev/shm` or `/etc` makes the service write a new generation of that text with a success report, switch to it,
  and only then let readers see the new bytes (`B2/build/bc3_filesystem.py` lines 151–198, 343–366; single-threaded: fusepy maps
  `nothreads` to `-s`, `S5/raw/07-fusepy-options.txt`).
- The writers in the cases are a shell redirection (01), Python `open().write()` (05, 06), `base64 -d >` run by the ordinary
  account (all other way fixtures), the editor `ed` (13, its scratch file) and the native `useradd` (16, 90 generations of
  `/etc`, from which own account rows are derived).
- The first generation of each filesystem declaration was made by importing the directory as it already was (`--seed {mount}`,
  `B2/build/install-bc3.py` line 18; `import_tree`, `bc3_filesystem.py` line 110).
- A person designated the files once; no person wrote any of their lines in the cases.

Reading A. The text is written first and the computer follows it: the requested bytes are staged where nobody can read them,
written into the declaration, and only then exist on the computer. The computer is brought into conformity with the text; that
the text was produced at a program's request does not matter. S8.2-19 (“What need not be recorded may also be recorded in the
declaration.”) and S8.3-7 (“Its tools for installation and configuration record changes in the declaration …”) are cited in
support.

Reading B. A text produced automatically from whatever any program on the computer writes is a text compiled from the computer,
however short the time between the write and the record; it is what S8.1-2 excludes. S8.1-8 says general-purpose programs
(“an editor, file copying, link creation, the command shell”) are not built-in tools, and here their writes become lines.

Consequence for this record: under A, cases 01–16 meet the outcome rule of `SUP1/step-5.md` (what the way leaves is recorded) and
give 1, and the step gives 1. Under B, the only declaration is `machine.jsonl`, in which the saved sources and the account are not
recorded; each of those cases is a way not refused, not recorded, without an argument, and gives “?”; the step gives “?”.
This record therefore gives “?” for 01–16 until the author chooses.

## Q2. The same question for the account tool (case 16), with one difference

S8.3-7 says tools “record changes in the declaration even when they run with superuser privileges”. In this image `useradd` itself
does not record anything; the `/etc` filesystem derives own account rows from the database bytes `useradd` writes
(`B2/build/bc3_account_rows.py`). Reading A: that is the tool's change recorded in the declaration before it is in force, as
S8.3-7 asks. Reading B: rows derived from the account database after the tool computed it are compiled from the computer
(S8.1-2), and S8.3-7 is met only by a tool that writes the declaration as part of its own operation.

## Lines noticed, not checked (outside this task)

- Whether the ordinary account can save a file anywhere outside the five mediated roots on this image (for example a per-user
  runtime directory) is not established by the records; `B2/build/noexec.py` line 20 lists “other writable mounts” as open.
- S8.1-13/S8.1-14 with six separately reported successes, one per designated file, and one success per single write: which of these
  is “the last application that the system reported as successful”.
