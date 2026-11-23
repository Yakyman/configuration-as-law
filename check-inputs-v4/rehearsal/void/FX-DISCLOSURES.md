# Void diagnostic disclosure, continued rehearsals

No collected object, raw query stdout, package-file content or member list has
been read. Numerical status/count reductions are retained separately. Permitted
diagnostic files read below are relative to `rehearsal/void/diagnostics/`.

The symlink-target adapter repair follows published XBPS source, not exposed
machine contents. The initial host service-launch error revealed only an invalid
working-directory argument, and no guest process started from that command.

- `fx1/action-language_program.stderr`: Node could not start because the installed
  C++ runtime lacked `CXXABI_1.3.15`, required by libada.so.3 and libicui18n.so.78;
  XBPS also warned that tzdata-2025a_1 has an invalid py3 provides field.
- `fx1/action-network_connection.stderr`: only the same tzdata metadata warning;
  this action returned zero in continued round 1, so the prior failure's cause
  remains unknown.
- `fx1/collector.stderr`: empty; no machine information revealed.
- `fx1/coverage.tsv`: query exit statuses, durations and row/byte counts; all
  nonzero queries were status 127 for unavailable service/firewall/container
  tools, a limitation named in `COLLECT.md`. No collected row contents seen.
- `fx2/action-language_program.stderr`: the C++ ABI error was absent; Node now
  failed on undefined `sqlite3session_attach`; the same tzdata warning persisted.
- `fx2/collector.stderr`: empty; no machine information revealed.
- `fx2/coverage.tsv`: all nonzero queries remained 127 for unavailable tool
  interfaces; only query labels, statuses, durations and numerical sizes read.
- `fx3/action-language_program.stderr`: XBPS refused the transaction because
  liblastlog2-2.41.4_1 breaks installed util-linux-2.40.2_1; same tzdata warning.
- `fx3/collector.stderr`: empty; no machine information revealed.
- `fx3/coverage.tsv`: all nonzero queries were documented unavailable tool
  interfaces (127); only labels/statuses/durations/counts were read.

The final action form is repaired before continued round 4: XBPS first updates
its own package, then performs the documented full update, then installs tree.
The language action remains npm installing cowsay in the home directory; it now
uses `npm install --prefix "$HOME/.local" cowsay` and runs
`$HOME/.local/node_modules/.bin/cowsay`. Omitting `--global` retains npm's project
lock, which records direct requests and dependencies. This exact-form repair
was directed before the final run to preserve installation-reason evidence;
it is not a new workload or a different Section 9.2 action category.
- `fx4/collector.stderr`: empty; no machine information revealed.
- `fx4/coverage.tsv`: all nonzero queries were documented unavailable tool
  interfaces (127); only labels/statuses/durations/counts were read.

Final continued round 4: nine actions 0, transport 20/20, collector 0 in 27.682 s,
second-level 2068 rows, known reasons 530/546, known file integrity 37652/37931,
whole 365.953 s, destruction 0. These are numerical preparation facts only.

Independent-review correction: the separate Python/npm reason values inherited
from native parent packages were not justified and that shared collector logic
has been removed. Historical round 14's 530/546 known reasons is not accepted.
A conservative retained-count-only bound subtracts all 188 formerly known
Python/npm reasons, leaving 342/546 (62.64%); it is not a corrected inventory.
The >90 percent requirement is uncertified. Final Void is NOT READY after four
continued rounds, with no fifth permitted. Original count/status records remain
unchanged. No further diagnostic or collected content was read.
