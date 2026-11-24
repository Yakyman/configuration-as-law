"""Create revised evidence and gap files without modifying the original files."""
from pathlib import Path
import re

F = Path(__file__).resolve().parents[1]
B = F.parent
N = B.parent
sources = (B / 'SOURCES.md').read_text()
sources = sources.replace('Raw and part files preserve intermediate drafting evidence; CHANNELS-V4.tsv, GAPS.md, and RESULT.md are the final classification.',
    'The parent directory preserves the original drafting evidence and classification. This directory contains the FX-B1-1 revision; ../RESULT.md is the current summary. E100-E105 below supply the newly checked primary excerpts.')
sources = sources.replace('The history is reused by subsequent interactive sessions; this does not establish that every history file is a valid executable script.',
    'The history is reused by subsequent interactive sessions. FX-B1-1 applies S8.2-23 to this documented values-reading role and records its tension with the execution-capability reading of S8.2-9; syntax is not used to decide that textual dispute.')
sources = sources.replace('It does not establish the separate no-program-launch condition for every browser interface required by S8.2-21. C7.19 therefore leaves the saved-code exemption fact-unknown; renderer/helper executables still require recording.',
    'FX-B1-1 applies the express web-page example in S8.2-21 to the confined web code already specified by C7.19. It does not require a new capability fact for that example; separate renderer/helper executables still require recording.')
sources = sources.replace('The route decision applies S8.1-7 to that specialized purpose; it does not infer an installer/removal purpose.',
    'Applying S8.1-7 through the Q2 output definition is one reading, not an adopted resolution. The alternative is general-purpose build work under S8.1-8; see GAPS.md. No installer/removal purpose is inferred.')
sources = sources.replace('The Description identifies a dedicated build-system generator; the Install a Project section documents cmake --install. Generic shell/copy/link operations are separate operations under S8.1-8.',
    'The Description identifies a build-system generator and Install a Project documents cmake --install. This supports the built-in reading, especially for C5.3. The competing reading treats output copying/linking as the functionality expressly excluded by S8.1-8, whose exception requires an installer. No removal purpose is established. Both readings are retained in GAPS.md.')
sources += '''## FX-B1-1 evidence additions

Checked 2026-11-23 UTC. These are documentation checks, not runtime observations. Existing quoted excerpts above are preserved; the interpretation notes for E005, E013, E093 and E094 are corrected. The original notes remain in ../SOURCES.md.

## E100 — User transient-unit location

[systemd.unit, Unit File Load Path, user-mode table](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html#Unit%20File%20Load%20Path)

> $XDG_RUNTIME_DIR/systemd/transient

> Dynamic configuration for transient units

These are the path and description in the same user-mode table row. They directly support C6.3 object a, rather than relying on the generic unit-file description in E029.

## E101 — Container privilege, namespace and device options

[podman-run option reference](https://docs.podman.io/en/latest/markdown/podman-run.1.html)

The option headings and their relevant descriptions are:

> --privileged
>
> Give extended privileges to this container.

> --pid=mode
>
> host: use the host’s PID namespace for the container.

> --device=host-device[:container-device][:permissions]
>
> Add a host device to the container.

C9.5 object a names these selected values. Their existence and semantics are documented; no claim is made that running the command itself creates a new hook JSON file.

## E102 — Hook JSON and conditional directory default

[podman, --hooks-dir](https://docs.podman.io/en/latest/markdown/podman.1.html#hooks-dir-path)

> Each `*.json` file in the path configures a hook for Podman containers.

Relevant condition and directory fragments:

> If `--hooks-dir` is unset for root callers

> `/usr/share/containers/oci/hooks.d` and `/etc/containers/oci/hooks.d`

The documentation calls these defaults deprecated and recommends explicitly selecting the directory. C9.5 now states the root-caller/unset-option condition, with <hooks-dir>/*.json as the general template. This evidence establishes the configuration location, not the identity, provenance or effects of an unspecified hook executable; FACT_UNKNOWN therefore remains.

## E103 — System mount utility and filesystem configuration

[mount(8), Name, bind options, Availability](https://man7.org/linux/man-pages/man8/mount.8.html)

> mount - mount a filesystem

> The mount command is part of the util-linux package

> Since util-linux 2.27 mount permits changing the mount options

This documents the named utility's system-utility provenance and filesystem-configuration purpose for C3.5. S8.2-13 explicitly includes filesystems among settings; S8.1-7 applies to this functionality. It supplies no evidence about the AppImage updater's identity or status as a program of the system. E078 remains only a generic update-mode description, so the updater route is FACT_UNKNOWN in C3.5 and C4.3.

## E104 — Download purpose

[curl, Description](https://curl.se/docs/manpage.html#DESCRIPTION)

> curl is a tool for transferring data from or to a server using URLs.

Together with E079's output-file option, this establishes a transfer function. It does not establish the installation/configuration purpose in S8.1-7. C4.3 no longer claims S8.1-8 explicitly lists downloading. Copying is still one of that sentence's explicit examples.

## E105 — Shell history is read into a history list

[Bash reference manual, History Builtins, history -r](https://tiswww.case.edu/php/chet/bash/bashref.html#Bash-History-Builtins)

> Read the history file and append its contents to the history list.

The Bash Variables and Bash History Facilities sections identify HISTFILE and saving/reloading entries. This supports the values-reading role in C7.17. The same manual separately documents execution of command text. E005 supplies the corresponding saved-history fact for C7.06. GAPS.md records both textual readings rather than using missing syntax to choose between them.
'''
(F / 'SOURCES.md').write_text(sources)

gaps = (B / 'GAPS.md').read_text().replace(
    'The sole TWO_WAYS row is C8.08; there are no NOT_DECIDED rows.',
    'Eight rows are TWO_WAYS in three kinds of gap; there are no NOT_DECIDED rows. This is the FX-B1-1 revision.')
gaps += '''## Compiler and build-tool purpose versus general-purpose work

Variants: C5.1, C5.2, C5.3, C5.4, C5.5.

What the text lacks: S8.1-7 and S8.1-8 do not settle whether executable-producing build functionality is a built-in installation/configuration tool by way of S8.2-10, or general-purpose build/copy work.

The source facts are compilation/linking and executable output (SOURCES.md E083, E093), generated installation rules and a documented install command (E085, E094), and plugin loading (E084). No missing compiler output fact is used to resolve the route.

Reading A applies S8.1-7 because these documented operations create or replace programs, which S8.2-10 places among what is installed. Reading B understands the documented build purpose as general-purpose processing, with copying/link creation expressly excluded by S8.1-8. The generic route definition does not explicitly name compilation or choose between those readings. For C5.3, the documented install target is evidence for reading A, while reading B applies the copy/link exclusion to that output operation; no removing-programs purpose establishes the installer exception in S8.1-4 and S8.1-8. This is recorded as a dispute, not settled by adopting either interpretation. Separately invoked shell/editor/copy/link operations retain their explicit general-purpose classification. C5.4's separately privileged direct bypass remains the breaking branch when the conditions of S8.1-15 hold.

The output declaration requirement is the same under both readings: unchanged packaged objects stop at Q1; other executable output stops at Q2 and requires S8.2-16 coverage. The system behaviour differs: reading A requires the acting build tool itself to record its changes under S8.3-7; reading B does not establish that tool-specific duty. Under both, P4 still forbids an ordinary path changing an installed program past the declaration. This is not permission to leave a general-purpose tool's executable output unrecorded, and it prescribes no enforcement mechanism.

## Saved history: values read versus executable statements

Variants: C7.06 object b (.python_history), C7.17 object c (HISTFILE).

What the text lacks: S8.2-23 does not delimit a file read as history values from saved language statements that S8.2-9 treats as code executable at a person's command; S8.2-6 preserves the order but does not decide that boundary.

E005 and E105 in SOURCES.md document saving and reading the entries as history. Reading A applies the second clause of S8.2-23 to that history-file operation: Q1 no, Q2 no, Q3 no, Q4 program record under S8.2-15, requiring no line under S8.2-2. Reading B applies the capability wording of S8.2-9 to the retained language statements: Q1 no, Q2 yes, program under S8.2-10, without reaching Q4. It reads S8.2-23's values-only exclusion as inapplicable to code that can be executed at command. No observation of another invocation is added; no assertion is made that every possible history file is a valid complete script. The competing readings concern the described retained statements and the scope of the values-only exclusion, so requesting unspecified syntax did not resolve them.

The declarations differ by a required program line or actual derivation coverage under S8.2-16 versus no required history line. Under reading B, P1/P4 require the retained program to be recorded and disallow ordinary unrecorded program changes. Under reading A, writing that history record adds no such obligation. Personally typed commands remain actions under S8.2-4 in both readings, and runtime state follows S8.2-5. This records the two readings without selecting one or changing the questions' order.

## Additional exact text cited by the revised gap analysis

'''
sentences = {}
for line in (N / 'SENTENCES.md').read_text().splitlines():
    m = re.match(r'- \*\*(S\d\.\d-\d+)\*\* (.*)', line)
    if m:
        sentences[m[1]] = m[2].replace('**', '')
for sid in ['S8.1-4', 'S8.1-7', 'S8.1-8', 'S8.2-4', 'S8.2-9', 'S8.2-10',
            'S8.2-15', 'S8.2-16', 'S8.2-23', 'S8.3-4', 'S8.3-7']:
    gaps += f'{sid}: «{sentences[sid]}»\n\n'
(F / 'GAPS.md').write_text(gaps)
print('Created revised SOURCES.md and GAPS.md; originals preserved.')
