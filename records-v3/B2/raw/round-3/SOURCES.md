# Round 3 mechanism sources and unanswered integration questions

Recorded 2026-11-22 UTC, before the first round-3 VM run.

- https://man7.org/linux/man-pages/man2/fsync.2.html: “an explicit fsync() on a file descriptor for the directory is also needed.” File and containing-directory flushes are used for generation selection and the local success report.
- https://www.freedesktop.org/software/systemd/man/257/systemd.unit.html: “this unit will not be started.” `Requires=` with `After=` blocks dependent session services when replay fails. Ordering alone is insufficient.
- https://www.freedesktop.org/software/systemd/man/257/systemd.kill.html: “all remaining processes in the control group of this unit will be killed”. Managed services require control-group termination; socket/timer activation is stopped first.
- https://man7.org/linux/man-pages/man8/pam_exec.8.html: “PAM module that can be used to run an external command.” An account-phase requisite test checks the volatile ready marker before a login session is created. The ordinary launcher independently checks the same marker.
- B1/raw/mechanics-sources.md supplies the earlier fsync, cgroup, unlink, mapping and native backend evidence. No primitive behavior already answered by those documents is reprobed here.

Unanswered integration questions: whether this recipe boots with admission gated until complete replay; whether the supervised worker restores the previous supported declaration at every injected phase and at shortened silence timeout; whether supported activation edges and shared contributions are withdrawn/preserved correctly; whether the independent census surfaces all planted kinds; whether nine immediate reported-success cuts recover the exact reported generation; whether two executions of the final recipe produce equal observations for one identical declaration. Expectations and fixture details are in HARNESS-PLAN.md and the checked-in round3 drivers before execution.

Initial build expectation: a fresh pinned source image plus verified package cache builds the new transaction, inventory and socket implementation. No system change is made on the laptop or host. A build failure is an implementation defect; its log is retained before a corrected recipe is tested. The integration image is separate from the required final rebuild. Full arbitrary-device restoration and semantic P1 completeness are not inferred from finite positive tests.

Preflight: server KVM and user systemd are present, approximately 52 GiB memory is available, and the retained package cache is 70 MiB. Implementation and review were independent.

Socket integration correction, 2026-11-22 UTC: https://www.freedesktop.org/software/systemd/man/257/systemd.socket.html states, “Socket units automatically gain a `Before=` dependency on the service units they activate.” The application had submitted independent sequential service/timer/socket start calls, allowing the service to start first. The corrected application submits all required active jobs in one native systemd transaction so its dependency engine orders them. The unanswered check is the corrected whole service/timer/socket fixture, not the documented primitive.

- The [versioned systemctl implementation](https://raw.githubusercontent.com/systemd/systemd/v257/src/systemctl/systemctl-start-unit.c), lines 359–362, loops over requested names and calls `start_unit_one` for each; line 125 calls the native manager for that one name. Thus a multi-name CLI invocation is not one atomic dependency transaction. Socket, timer and service activation must be ordered across those calls.
