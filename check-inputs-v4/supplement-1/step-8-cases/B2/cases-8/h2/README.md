# History 2: committed development inputs

Prepared 2026-11-23 UTC. Preparation only; no history attempt or outcome is reported.

The project is the public `docker-library/hello-world` native C executable,
`hello.c` at commit `522bcd2faf422c60b9d20e64d7cd6d56600aec97`.
Source and SHA-256 are fixed in `inputs.json`; the exact downloaded file is
`hello.c`. Only its single source file is needed for the native executable;
the project's container packaging is not part of this development action.
Its printed references to a container are fixed text, not an observation of
a container being used. The small project needs only the compiler and C library
already present in the image.

On one fresh copy of the final step-6 image, run the exact bytes of `history.sh`
through the ordinary shell:

```sh
python3 lab.py run second-h2 < cases-8/h2/history.sh > raw/step-8/second-h2/actions.stdout 2> raw/step-8/second-h2/actions.stderr
```

The surrounding controller must save the command's exit status without stopping
before the final three observation queries from `OBSERVE-8.md`. It must use the
normal fresh-copy, lock and cleanup procedure committed in `CASES-8.md`.
No root flag is used. Do not stage or execute this script by bypassing the
ordinary shell. No prerequisite installation is necessary: Python 3, GCC,
the static C library, `stand-import` and `stand-build` are recipe components.

The loop commits three consecutive complete rounds on the same copy. Each round
fetches the same pinned original source from its public URL; imports that source
through the built-in tool; builds using the image's fixed GCC tool; imports the
result through the built-in tool; runs the actual admitted native executable;
changes exactly the greeting source line; and repeats source import, build,
result import and run. The third round's edited source and executable remain.
There are three fetches, three one-line edits, six builds and six launches.
The built-in import is a required normal admission step, not an image change.

For each action retain exact command/stdin, UTC, stdout, stderr and exit status.
`ACTION_BEGIN` without `ACTION_DONE` names an unfinished action; actions after
the failed `set -e` command are not done, with prerequisite-failure reason.
The complete runner status must not be treated as a hypothesis outcome.
Success requires checksum-verified fetched bytes, successful source admission,
compiler and binary admission, zero exit of each native launch and exact output
SHA-256, and a verified single changed source line. Expected output bytes and
all source/output hashes are alongside this document. They are calculated from
the public source, not copied from a trial's observed output. No restart occurs
in this history. All three observations occur at its end, including after an
early failure; if a restart is needed unexpectedly, record its reason and make
the mandatory observations immediately after it without rerunning actions.

The preparation assessment is performable from documented tools and pinned
input construction. Actual completion, declaration correspondence and outcome
are determined only by the second party's single attempt and separate review.

## Source evidence

- Public source: <https://github.com/docker-library/hello-world/blob/522bcd2faf422c60b9d20e64d7cd6d56600aec97/hello.c>.
  It defines `const char message[]` and invokes
  `syscall(SYS_write, STDOUT_FILENO, message, sizeof(message) - 1);`.
- `build/bootstrap.sh` installs `gcc libc6-dev` and Python before final capture.
- `build/import_channels.py:prepare` supports `source` admission with exact
  bytes/hash and source metadata; `build:35` requires one recorded C source and
  invokes the recorded compiler with `-x c -O2 -fno-lto -static`.
- `build/import_channels.py:65` generates the result specification and writes
  the inert binary to the ordinary user's mediated directory.
- `build/stand.py:526` dispatches `stand-import`; `:529` dispatches `stand-build`.
- `build/round4-selftest.py:36–43` documents the existing source admission,
  compilation, result import and launch sequence. It is cited as interface
  evidence, not as a new trial or the outcome of this history.

The precise single-file compiler interface answers the tool-availability and
build-method questions. No disposable VM, compilation or history trial was
performed during this preparation; therefore none needs cleanup.
