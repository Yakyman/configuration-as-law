# Supplemental real-shell observations

Recorded before the supplemental guest is created. These are part of Round 1,
not additional hypothesis cases. The source review identified families whose
carried assertions still invoked the sealed launcher. The supplementary payloads
in `tools/v4-direct-selftest.py` and `tools/v4-extra-selftest.py` run those finite
representatives through actual ordinary Bash on a fresh overlay of the frozen,
fully rebuilt candidate. They do not change the installed mechanism or recipe.
Their hashes are saved before invocation. No observation is inferred from source.

The documented compiler pipeline and Python evaluation behavior are already
known; the unknown being tested is their integration with this image's generated
policy and concrete file provenance. Primary sources:

- [GCC output stages](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html):
  “Compilation can involve up to four stages: preprocessing, compilation proper, assembly and linking, always in that order.”
- [GCC plugins](https://gcc.gnu.org/onlinedocs/gccint/Plugins.html): loadable
  compiler modules; the test concerns whether the ordinary domain can load an
  unrecorded saved module.
- [Python built-ins](https://docs.python.org/3/library/functions.html#exec):
  evaluation of supplied code; the test concerns the saved input under the
  installed policy, not whether the language supports evaluation.
- The existing plan's Bash/AppArmor references and the extra suite's source
  ledger cover its respective language/kernel input mechanisms.

Expected: ordinary command/material/compiler work remains usable; recorded
objects/settings are the boundary. An unrecorded saved executable input must not
execute merely because a declared interpreter or helper reads it. Runtime-only
instructions are not assigned a mandatory new declaration line. For each test,
expected behavior is emitted before the command and exact effect/diagnostic,
file identity and declaration/report continuity are retained. Missing programs
or unsupported facilities are reported as unavailable, never successful denial.

Run each supplement once on the rebuilt image, preserve every failed property or
ordinary-work row, reboot and read back, then delete its disposable guest. The
supplemental observation controller's zero exit means completion, not universal
boundary success. The final report must count the failed rows separately.
