# Independent final-2 supplement review

Review time: 2026-11-23T09:43:53Z

Scope: frozen final-2 supplemental inputs and exported records only. This review does not accept the overall result, close any variant, or substitute for the pending gate, main-tool, and carried-suite evidence.

## Input identity

The frozen input bytes match both recorded hash manifests:

- `v4-direct-selftest.py`: `82bd871f23561397ff510a3c28b81294a045dfd97d6f120ccc3fb5380c5f0399`
- `v4-extra-selftest.py`: `5e4dc0dc59711c80a46e547d254400c350726cf499c615a4eaeae3a2b88c757a`

The controller's stdin hashes cover its wrapper payloads and therefore need not equal the source-file hashes. The source identities are separately and consistently recorded.

## Direct-shell observations

The direct summary identifies exactly five property failures. Each returned exit zero, emitted the exact effect below on stdout, set `marker_observed=true`, and retained identical declaration/report readback:

- `DIRECT-REDIRECT-STDIN`: `SAVED_DIRECT_RAN`
- `DIRECT-PROC-FD`: `SAVED_DIRECT_RAN`
- `DIRECT-READ-EXEC`: `READ_EXEC_RAN`
- `DIRECT-AWK-FILE`: `AWK_FILE_RAN`
- `DIRECT-SCRIPT-HELPER`: `SAVED_DIRECT_RAN`

The positive fixture steps establish the intended preconditions before their separate launch attempts: HTTP download hash, nested extraction, compiled executable, prefix copy and symlink, and compiler plugin output. The associated unrecorded executable or mapping attempts show permission or mapping-specific refusal. The runtime alias positive also succeeds. The summary contains no unavailable row and preserves all five failures despite controller completion.

## Extra mechanism observations

Four extra rows are genuine property failures with exact standalone stdout effects and unchanged declaration/report readback:

- `RC-STARTUP`: `SAVED_RC_EXECUTED`
- `EDITOR-SAVED-COMMANDS`: `SAVED_EDITOR_COMMAND_EXECUTED`
- `JIT-SAVED-INPUT`: `JIT_SAVED_INPUT_EXECUTED 42`
- `DISPATCHER-SAVED`: `DISPATCHER_SAVED_EXECUTED`

`SAVED-FFI` is correctly a denial, not a failure. Its stdout is empty, `effect_marker_observed=false`, and the loader exits one with `failed to map segment from shared object`. The marker text occurs only inside a traceback echo of the supplied source line. The frozen detector requires an exact output line or a marker followed by a value, so it does not misclassify that echo.

The records also support the narrower denial observations for saved `LD_PRELOAD`, `LD_AUDIT`, anonymous-file execution, and binfmt registration. Runtime-only observations remain separately labelled and do not prove saved-input mediation. Git, Make, foreign-interpreter, editor-plugin/modeline, and browser-extension shapes remain explicitly untested.

## Readback, reboot, and cleanup

The before- and after-reboot verification files are byte-identical, each contains 553 checks, and every check has status `OK`. Their SHA-256 is `310e45e22d3485a91b16154be45f77eec237b61c50ad78454593822a89d808cc`.

The before- and after-reboot reports are also byte-identical, with SHA-256 `9c94126d0114f81434ea21c7c584c3eca2cd461579dfe6da52b31b38f028b303`. They report declaration `2bbb7700f168debb3154368ae4856f6fa7529e7d26b2227ed0c56473a3e4efec`, status `SUCCESS`, and no terminated processes. The reboot record explicitly confirms equal last-success bytes.

All controller steps completed with their expected exit status, including destruction. The final summary records no remaining owned virtual machine. Its exit-zero semantics mean observation completion only; it does not erase property failures.

## Disposition

The supplement independently supports nine concrete saved-input counterexamples, the corrected FFI mapping denial, stable declaration/report readback across the tests, and identical full verification after reboot. Its honest hypothesis outcome is `?`. It supplies bounded evidence for later row-level assessment but cannot close a variant or support overall acceptance by itself.
