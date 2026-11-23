# P01 — Current distribution Python and locked execution securebits

Prerecorded 2026-11-22 UTC, before VM creation or the probe. One question, one invocation; no retry of the interpreter probe.

Question: On current Debian 13.8 with a kernel exposing AT_EXECVE_CHECK and the execution securebits, does the distribution's fresh Python interpreter refuse `-c` when both EXEC_RESTRICT_FILE and EXEC_DENY_INTERACTIVE and their lock bits are set?

Source gap: kernel documentation specifies cooperative behavior, while the selected upstream CPython files in `c7-pinned-source-checks.json` do not establish the current distribution binary's behavior. PEP 578 documents existing hook limits, not this downstream build. A runtime question about this one build is narrower than universal interpreter adoption and is eligible for one probe. Sources: https://docs.kernel.org/7.3/userspace-api/check_exec.html ; https://peps.python.org/pep-0578/ ; https://packages.debian.org/trixie-backports/linux-image-amd64 .

Expected result: setting and rereading mask 0xf00 (bits 8–11: file restriction, its lock, interactive denial, its lock) succeeds; a fresh stock Python invoked with `-I -S -c` nevertheless prints PYTHON_CODE_RAN and exits 0. That would establish non-cooperation of this binary for this input route, not universal unclosability or the behavior of all script/import/eval routes. If the kernel rejects the bits, the interpreter question is not reached; record prerequisite failure and do not substitute a different kernel during the probe. If Python refuses, record that bounded positive behavior without inferring every code path is covered.

Guest target: Debian 13.8 amd64, kernel image linux-image-7.3.4+deb13-amd64, package 7.3.4-1~bpo13+1 from trixie-backports. Record actual `/etc/os-release`, `uname -r`, package versions, mask-setting return, mask readback, marker and exit status. Verify guest versions and prerequisites before the single probe; those checks must not execute the test invocation.

Resources: one server VM, 2 vCPU, at most 4 GiB RAM, one flock slot. No system changes to the server. Disposable image and task-generated SSH key removed on completion. No adapter/power-cut/whole-system test.

Prerun refinement at 2026-11-22 04:51 UTC, while guest packages are still being prepared and before any test invocation: the root wrapper drops supplementary groups and changes gid/uid to 65534 after setting the locked bits; the fresh interpreter payload prints its own effective uid and PR_GET_SECUREBITS before the marker. Expected child euid=65534 and bits=0xf00. This avoids treating privileged-interpreter behavior as evidence about an ordinary user and directly verifies inheritance across exec. Still one invocation of the same question.
