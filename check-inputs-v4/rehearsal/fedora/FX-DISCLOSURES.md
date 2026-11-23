# Fedora continued rehearsal disclosures

2026-11-23 UTC. Preparation has read only prior numerical status/count records,
the fixed action script and public primary documentation. No prior action stderr
exists in this system's retained rehearsal folder. The exact source of the old
Homebrew action's status 56 is therefore not asserted.

The action now downloads the same Homebrew installer into a temporary output
file with bounded retries before executing it, then removes that temporary
file. This is a transport repair of the same action, not a replacement. Full
commands are in `actions/lived-developer.sh`.

Diagnostic files read during continued rounds will be listed below, relative
to `rehearsal/fedora/diagnostics/`, with the machine information they revealed.

- `fx1/collector.stderr`: empty; no machine information revealed.
- `fx1/coverage.tsv`: query names/statuses/durations/counts; DNF selected-group
  history and OpenRC interfaces returned 127. Three user-service queries returned 1.
- `fx1/0300-user-service.err`: the queried user session had neither an available
  D-Bus session address nor XDG runtime directory; user-service scope uncollected.
- `fx1/0301-user-timer.err`: same unavailable user-session bus, timer scope uncollected.
- `fx1/0302-user-unit-file.err`: same unavailable user-session bus, unit-file scope uncollected.

Continued round 1: all 13 actions 0; transport 20/20; collector 0 in 144.971s;
L2=6870; known file integrity 164540/169962; known reasons 1679/2248; whole 308.750s;
destroy 0. Numerical reason classes:334 RPM group and 2 RPM unknown,77 RubyGems
unknown,78 npm unknown,78 Python unknown. Native parent reasons were not inherited.
The reason threshold failed. No action stderr content was read: every action
passed, including the same Homebrew/hello action after the bounded-download repair.
- `fx1/0016-package-selected-groups-dnf.err`: empty; coverage 127 establishes
  the selected-group helper's unavailable optional interface, not group contents.
- `fx1/0285-openrc-service.err`: rc-status is not installed/available to the query.
- `fx1/0286-openrc-runlevel.err`: rc-update is not installed/available to the query.

- `fx2/collector.stderr`: empty; no machine information.
- `fx2/coverage.tsv`: same optional-interface failure classes and numerical coverage as round 1.
- `fx2/0016-package-selected-groups-dnf.err`: Optional command or interpreter is unavailable; the corresponding interface is not collected.
- `fx2/0285-openrc-service.err`: Optional command or interpreter is unavailable; the corresponding interface is not collected.
- `fx2/0286-openrc-runlevel.err`: Optional command or interpreter is unavailable; the corresponding interface is not collected.
- `fx2/0300-user-service.err`: The user manager or session bus is unavailable; its interface is not collected.
- `fx2/0301-user-timer.err`: The user manager or session bus is unavailable; its interface is not collected.
- `fx2/0302-user-unit-file.err`: The user manager or session bus is unavailable; its interface is not collected.

- `fx3/collector.stderr`: empty; no machine information.
- `fx3/coverage.tsv`: same optional-interface classes as prior rounds; numerical query coverage only.
- `fx3/0016-package-selected-groups-dnf.err`: Optional command or interpreter is unavailable; the corresponding interface is not collected.
- `fx3/0285-openrc-service.err`: Optional command or interpreter is unavailable; the corresponding interface is not collected.
- `fx3/0286-openrc-runlevel.err`: Optional command or interpreter is unavailable; the corresponding interface is not collected.
- `fx3/0300-user-service.err`: The user manager or session bus is unavailable; its interface is not collected.
- `fx3/0301-user-timer.err`: The user manager or session bus is unavailable; its interface is not collected.
- `fx3/0302-user-unit-file.err`: The user manager or session bus is unavailable; its interface is not collected.

Continued round3 confirms one explicit unsupported Homebrew adapter gap, a numerical count emitted by the collector; no brew package or file content was read. Reason coverage remains1679/2248.

- `fx4/collector.stderr`: empty; no machine information.
- `fx4/coverage.tsv`: six optional-interface failures, matching the preceding rounds; numerical query coverage only.
- `fx4/0016-package-selected-groups-dnf.err`: The optional DNF4 history database is unavailable; its selected-group interface is not collected. Stderr is empty; the source guard explains status 127.
- `fx4/0285-openrc-service.err`: Optional command or interpreter is unavailable; the corresponding interface is not collected.
- `fx4/0286-openrc-runlevel.err`: Optional command or interpreter is unavailable; the corresponding interface is not collected.
- `fx4/0300-user-service.err`: The user manager or session bus is unavailable; its interface is not collected.
- `fx4/0301-user-timer.err`: The user manager or session bus is unavailable; its interface is not collected.
- `fx4/0302-user-unit-file.err`: The user manager or session bus is unavailable; its interface is not collected.

Correction for all four rounds: the empty DNF selected-group stderr does not establish a missing interpreter. The source guard establishes the unavailable optional DNF4 history database. The query limitation table now uses that precise class.

All four rounds are complete. Final reason coverage is 1679/2248; no unknown group or language reason was promoted. Final Homebrew unsupported-adapter count is 1; no brew package or file facts were inferred. Raw outputs and clones were deleted unread; `cleanup-status.tsv` records absence for all four rounds.
