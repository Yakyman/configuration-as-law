# Round 2 pre-run plan

Recorded 2026-11-22 UTC. These are development integration checks, not Check 2.
The existing recipe and saved evidence answer the old-policy question: five-tree noexec cannot restrict interpreter inputs. That experiment is not repeated.

Before implementation testing, read installed kernel/package capability state on one clean integration VM. This is prerequisite inventory, not a bypass experiment. Expect the pinned Linux cloud image to support existing mandatory access controls and syscall filtering; unavailable features require a different implementation, not a hypothesis verdict.

Implementation tests will attempt each C7.01–C7.17 and C8.01–C8.06 input literally, including direct interpreter argv, shebang, command argument, pipe/FIFO/socket/heredoc/process substitution, redirect/fd, REPL, source/eval/import, embedded tools, helpers/hooks/loader/preload, memfd, anonymous memory and typed input. Expect refusal by the selected mandatory boundary, plus successful declared native and recorded-script runs, browsing and editing. Additional tests cover mount location, environment, startup/project code, process injection, foreign handlers and removed-code reuse. Exact commands and expected results are recorded in the test recipe before each implementation run. Fresh final-image VMs repeat the complete suite as required by the build task.
