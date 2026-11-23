# Gaming repair plan

Before FX1: historical round4 statuses/counts were synchronized from the host; no content outputs were opened. Historical store client exit81 and anonymous download exit87 are retained. The current private virtual display/session bus is kept for both clients. SteamCMD now sets an explicit destination before anonymous login, following its maintainer's documentation, then verifies the same publisher-specified ServerHelper.sh. Expected: no path mismatch; remaining failures will be diagnosed from action stderr only. This is the same application download action.

No new store-client replacement has been chosen before its permitted diagnostic reveals the failure. The distribution wrapper source was consulted from the official Ubuntu source archive; its own checksum, extraction and first-run dialog remain unmodified.

Before FX1, independent source review identified premature Steam wrapper-exit failure and incomplete descendant cleanup. `actions/gui_guard.py` now preserves the action session, supervises a separate GUI group through wrapper handoff, and treats controller-pipe EOF as a cleanup request. TERM, bounded KILL and no-live-member verification cover all group members; the controller also verifies cleanup. Lutris scope follows the supervised group. Only the instrument process group is inspected; no collected object output is read. Sources: https://docs.python.org/3/library/subprocess.html and https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html.

Expected before one host-only synthetic fixture: a wrapper that forks a TERM-ignoring child then exits must leave the guardian live; killing its controller must close the pipe and stop all live group members within 22 seconds. The fixture uses only newly created processes and emits booleans/statuses; it does not start a machine or inventory the host. Shell and embedded Python syntax are valid.

The single synthetic process-group fixture passed all three booleans: guardian survives wrapper handoff, controller receives SIGKILL, and EOF cleanup leaves no live group members. Evidence: `rehearsal/mint/gui-guard-verification.json`; reproducible source: `rehearsal/verify-gui-guard.py`. Its output is instrument-only and reveals no machine inventory.

FX1 live diagnostic read at2026-11-23 09:50 UTC: `diagnostics/fx1/live-gaming_prerequisites.stderr` was empty while the prerequisite action was still running; it revealed no machine fact. The separate retained transport stderr file was empty (byte count only). No action stdout was read.

FX1 live diagnostic read at2026-11-23 09:53 UTC: `diagnostics/fx1/live-0954-gaming_prerequisites.stderr` was empty while prerequisites had not yet returned and revealed no machine fact. Only the action stderr was read; stdout remained unread. The separate transport stderr is retained.

Before any second round, the documented repair candidate for a timed-out package acquisition is command-scoped `Acquire::http::Timeout=30`, `Acquire::https::Timeout=30`, and `Acquire::Retries=2`; no repository, package or frozen installation choice would change. The primary APT manual says the timeout covers both connection and data waits and Retries repeats failed acquisitions: https://manpages.debian.org/trixie/apt/apt-transport-http.1.en.html and https://manpages.debian.org/trixie/apt/apt.conf.5.en.html. This is a conditional repair plan, not a diagnosis of the running first round. No first-round action is replayed or changed in place.

During FX1 actions, before its collector launched, the shared collector discovery was expanded to detect Homebrew and emit an explicit unsupported-adapter gap with a numeric counter. This change supplies no invented package, reason, ownership or integrity facts. It is included in the final collector sources; previously completed rounds are not relabelled as executions of this later source.

Primary-source passages for the conditional APT repair: [HTTP transport](https://manpages.debian.org/trixie/apt/apt-transport-http.1.en.html) says the timeout “applies to the connection as well as the data timeout.” [APT configuration](https://manpages.debian.org/trixie/apt/apt.conf.5.en.html) says “If this is non-zero APT will retry failed files the given number of times.” Reviewed before any fresh second round.

Immediately before the preset FX1 batch timeout, `diagnostics/fx1/live-before-timeout-prerequisites.stderr` was retained and read; it was empty and revealed no machine fact. The old harness fetched stderr only for actions with a completed status row. The subsequent harness revision fetches stderr for every fixed expected action label, preserving partial-action diagnostics after timeout; it does not invent a completed status.

FX1 actions reached the preset batch timeout: status124 after1501.058 seconds; `stop-action-batch` returned0 after3.249 seconds, certifying termination before collection. No action had emitted a completed status row. The retained live prerequisite stderr was empty; its underlying stall cause is not established. stdout was not read. Exact initially staged action source is `lived-gaming-fx1-staged.sh`; `fx1-runner.py` reproduces the captured initial runner SHA256 by reversing only the later stderr-retention patch, and its hash was checked against `fx1-local.sha256`. The reviewed APT repair will be applied only to a fresh FX2 clone after FX1 cleanup.

FX1 completed and destroyed its clone with status0; whole-run1697.787 seconds. The reviewed APT timeout/stage-marker candidate was then applied as `actions/lived-gaming.sh`, captured in `lived-gaming-fx2-staged.sh`, and deployed with matching source hashes. Fresh FX2 started2026-11-23 10:17 UTC. Expected: bounded acquisition waits and retained static phase diagnostics, all nine activities unchanged.

FX1 permitted diagnostic reads after cleanup: `diagnostics/fx1/collector.stderr`
reported permission denial at `/run/user/113/gvfs`; it revealed an inaccessible
GVFS virtual mount, not its contents. `diagnostics/fx1/coverage.tsv` and each
nonzero query stderr were read and individually listed in AUTO-DIAGNOSTIC-READS.md.
The two retained Flatpak assertion stderr files reveal crashes while listing
some user scopes; their user identities and query stdout were not read. Other
nonzero queries report missing optional commands or an unavailable user bus.
The probe correction adds only the exact documented GVFS virtual boundary.
Default-user Flatpak preflight prevents queries from creating absent scopes;
custom scopes remain explicitly uncollected. New numeric per-file type counters
will distinguish integrity-denominator causes without reading file inventories.
Expected before the next collector run: no GVFS traversal error, explicit
unavailable default-scope statuses instead of those assertion crashes, and
numerical type totals only. Earlier counts remain untouched.

FX2 live diagnostic `diagnostics/fx2/live-prerequisites.stderr` was read at2026-11-23 10:20 UTC. Its three static phase markers establish that architecture setup and repository-index update completed and package installation began. It contains no package inventory or error at that point; the separate transport stderr is retained.

FX2 `diagnostics/fx2/live-second-prerequisites.stderr` was read after the collector repair deployment; it still contained only the same three static phase markers, with no package-level content or error. Collector build5 and Python source hashes match in `fx2-collector-local.sha256` and `fx2-collector-deployed.sha256`; these supersede only the collector entries in the launch-time FX2 hash files. The collector had not yet launched when this reviewed deployment completed.

Before a bounded live action-self diagnostic in FX2: the package-install phase remained incomplete despite bounded APT connection/data waits. The diagnostic will inspect only the action job session named by its own job.sid, emitting process command names, states, elapsed seconds and wait-channel names to stderr; no command arguments, environment, package inventory, filesystem contents or unrelated processes will be read. Expected: distinguish a waiting acquisition process from an active unpack/configuration subprocess. The exact retained stderr and any machine fact it reveals will be disclosed. This diagnoses the instrument itself under the lead's diagnostic exception.

The bounded own-session stderr shows that the action is in APT acquisition: apt-get and its HTTP worker wait in select; no unpack/configuration subprocess appears in that session. `diagnostics/fx2/live-own-session.stderr` is retained. The next single two-sample diagnostic reads only numeric I/O counters of that same fixed HTTP worker, 30 seconds apart, to distinguish ongoing download from no progress; no file descriptors, request URLs, arguments or package contents are read.

The two numeric HTTP-worker samples at10:23:38 and10:24:08 UTC advanced wchar by1549352 bytes in30 seconds, about51.6 kB/s. Thus acquisition was progressing slowly, not idle; the underlying network cause is not established. The first25-minute failure plus this repeated slow attempt exceeded30 minutes of repair work. FX2 is being explicitly interrupted to try the same native package action through HTTPS for the same official repository coordinates. The operator stop reuses the reviewed session-termination/absence check; only after certified absence does it write an explicitly operator-supplied143 batch marker. This is not a returned per-action result, and no completed action is invented. The driver will retain that interruption and collect with the reviewed collector before destroying the clone.

Official HTTPS endpoint HEAD checks returned200 for archive.ubuntu.com/ubuntu/ and security.ubuntu.com/ubuntu/; packages.linuxmint.com returned a URL retrieval error (not interpreted as guest failure). Therefore the final transport helper rewrites only ubuntu.com and its subdomains; Linux Mint source URLs remain unchanged. Exact status-only retrieval record: `https-endpoints.tsv`. It copies sources to the temporary instrument directory and leaves /etc inputs, suites, components, keys and repository identity unchanged.

FX2 completed after the explicit operator interruption: batch143/560.511 seconds, no completed action row, collector0/171.665 seconds, whole750.287 seconds, destroy0/2.144 seconds and20/20 transport. `diagnostics/fx2/collector.stderr` was read and empty. Coverage and nonzero query stderr are individually disclosed in AUTO-DIAGNOSTIC-READS.md. The GVFS boundary and default Flatpak preflight removed the previous failures. Numeric type counters show161084 unknown symlink ownership records,67 unknown regular-file records and4128 unknown unresolved records. The installed dpkg `.list` and `.md5sums` interfaces provide no expected symlink targets; presence does not establish equality, so these facts remain unknown. No file/member contents were read.

After FX2 destruction, FX3 launched at2026-11-23 10:31:55 UTC with the reviewed Ubuntu-only HTTPS source helper. Source and deployed hashes match in fx3-local.sha256 and fx3-deployed.sha256; exact action snapshot is lived-gaming-fx3-staged.sh. The same nine activities and packages are retained. Expected: the alternative transport improves acquisition while preserving repository identity and authentication.

FX3 live read saved at2026-11-23 10:32:54 UTC: `diagnostics/fx3/live-prerequisites.stderr` contains only phase markers and the numeric count of four official URL occurrences switched to HTTPS. Architecture setup and index update completed; package installation began. It reveals no package identity. The separate transport stderr is retained.

FX3 prerequisite action completed0/122 seconds. At2026-11-23 10:35:38 UTC, `diagnostics/fx3/live-store-runtime.stderr` was read: it contained only the static distribution-client installation marker, without an error or package identity. Transport stderr was retained. This establishes successful prerequisite acquisition through the reviewed HTTPS form, not successful Steam bootstrap yet.

FX3 numeric live action status then recorded `gaming_store_runtime`0/134seconds. The private display, supervised bootstrap and bounded cleanup completed successfully on this fresh clone. No client stdout or installed members were read.

FX3 anonymous-download action completed0/105seconds. At2026-11-23 10:38:16 UTC, `diagnostics/fx3/live-anonymous-download.stderr` was read: it shows numeric curl transfer progress for the bootstrap and SteamCMD starting/restarting under the fixed action directory. This reveals only the instrument bootstrap activity and expected action path; application members and query stdout were not read. The separate transport stderr is retained.

A later live status fetch raced the harness removal of action outputs. `diagnostics/fx3/live-status-after-removal.stderr` retains the cat missing-file error (transport merged the command stderr into its returned stream). This reveals only that the instrument status file had already been removed; no action result is inferred from it. The definitive host status.tsv is used instead.

FX3 all nine action statuses are0; total batch408.305seconds. Individual durations are122,134,105,31,8,8,0,0,0seconds in fixed action order. The collector then started. The remaining installed-record limitation cannot be repaired by claiming symlink equality from presence; a final fourth fresh clone, if required after the collector result, will verify these same repaired actions and preserve unknown facts.

FX3 completed: collector0/200.697seconds, second-level36454rows, package reasons2202/2303, integrity283328/449205,20/20transport, whole628.085seconds and destroy0/3.037seconds. `diagnostics/fx3/collector.stderr` was read and empty. Coverage and each nonzero query stderr are individually disclosed in AUTO-DIAGNOSTIC-READS.md; all FX3 nonzero queries have named limitations. Unknown file records comprise161672symlink,79regular and4126unresolved entries. The remaining expected symlink targets are not supplied by the installed dpkg interface; no equality is inferred from presence.

Before FX4: all repaired actions now pass and source review confirms the conservative integrity denominator. The fourth fresh clone will repeat the final instrument and the same nine actions to complete the binding four-round allowance. It is expected to preserve the documented integrity limitation, rather than synthesize target facts or remove symlinks from the denominator. No action or collector source is changed between FX3 and FX4.

FX4 source and deployment digests match in fx4-local.sha256 and fx4-deployed.sha256. Exact staged action source is lived-gaming-fx4-staged.sh; it is byte-identical to FX3. The fourth run started on a new disposable clone after FX3 destruction.

FX4 prerequisite action completed0/127seconds. At2026-11-23 10:48:36 UTC, `diagnostics/fx4/live-store-runtime.stderr` was read to check the ongoing bootstrap. It contained only the static client-installation marker, without an error or package identity; no action stdout or inventory was opened. The separate transport stderr is retained.

FX4 numeric live status subsequently confirmed store-runtime0/191seconds, in addition to prerequisite0/127seconds. These are completed action returns; the final host status.tsv remains authoritative.

FX4 completed all nine actions with status0. The observed durations in fixed action order were127,191,109,31,8,11,0,0,0seconds. The definitive host reduction and collector results follow after completion; no successful action is inferred from only its launch.

FX4 final result: all9actions0, batch481.897seconds; collector0/194.159seconds; second-level36446rows; package reasons2202/2303; integrity283328/449205;20/20transport; whole695.253seconds; destroy0/3.034seconds. `diagnostics/fx4/collector.stderr` was read and empty. Coverage and nonzero query stderr are individually disclosed in AUTO-DIAGNOSTIC-READS.md, with all FX4 nonzero queries covered by documented limitations. Unknown file records remain161672symlink,79regular and4126unresolved entries. The four-round allowance is exhausted; no fifth clone or replay was run. Mint remains not ready solely because packaged-file integrity is below90%.

The host final cleanup certificate `rehearsal/cleanup-final.tsv` records zero remaining rehearsal clones, transient unread inventories, active preparation units, temporary probe build directories and uncompressed build outputs. Source-build caches and local temporary bytecode were removed; fixed bases, necessary access inputs and the compressed collector artifact remain.
