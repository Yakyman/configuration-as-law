#!/usr/bin/env python3
"""Prepare revised sources from preserved S4-P inputs; no guest operations."""
import ast
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

# Record descriptions, not answers to the classification questions.
how = {
'A01': 'npm-archive-sources.tsv records cache references and reference type; no per-object acquisition event record is emitted',
'A02': 'alma-facts.tsv current-content and installer-directives; saved-network credentials excluded',
'A03': 'alma-facts.tsv retains installer directives, bounded journal/audit extracts and scriptlets; no complete per-object choice/change event table is emitted',
'A04': 'alma-facts.tsv retains current unit/preset and bounded operation extracts; no original disablement-event record is emitted',
'A05': 'store-members.tsv and store-coverage.tsv; bounded inner traversal, nested boundaries explicit',
'A06': 'Inner metadata and prefix signatures recorded; no complete payload receipt or per-member creation-event table is emitted',
'A07': 'alma-facts.tsv records RPM key metadata and DNF history; no per-key import-reason field is emitted',
'A08': 'alma-facts.tsv current-content',
'A09': 'alma-facts.tsv current contents and bounded history extracts; no per-value creation-event record is emitted',
'A10': 'alma-facts.tsv s4-persistent-selinux-values, native read-only semanage query',
'A11': 'alma-facts.tsv values, scriptlets and bounded history extracts; no per-value chooser-event record is emitted',
'A12': 'alma-facts.tsv compiled-values; isolated dconf profile reads each existing system database',
'A13': 'Schemas, profiles and bounded current mapped-reader snapshot; no complete consumer history is emitted',
'A14': 'font-cache-sources.tsv fc-cat decoding and font-source-packages.tsv package-file joins; 2 RESULT-only IDs, 0 IDs in fixed matching inputs',
'A15': 'npm-member-integrity.tsv complete byte/target comparisons against verified cache-reference archives; reference type retained separately',
'V01': 'npm-archive-sources.tsv and npm-member-integrity.tsv retain lock references, verified cached archives and complete member comparisons',
'V02': 'old-package-receipt-sources.tsv and old-package-member-integrity.tsv query installed, residual and cached manifests; missing references carry no-surviving-receipt',
'V03': 'Current account/group/sudo sources and package records; no per-object installation/choice event table is emitted',
'V04': 'store-members.tsv and store-coverage.tsv; parent joins to child store path',
'V05': 'Bounded inner metadata and prefixes; no complete payload receipt or per-member creation-event table is emitted',
'V06': 'void-configuration-facts.tsv selected file bytes and full-digests.tsv whole-file hashes',
'V07': 'Current configuration, key and mount records; historical_creator has an unknown marker, no creation event is emitted',
'V08': 'font-cache-sources.tsv, font-source-packages.tsv and package-files.tsv; 1 RESULT-only ID, 0 IDs in fixed matching inputs',
'M01': 'Sysusers source files and RPM scriptlets; no per-account/group creation-event table is emitted',
'M02': 's4-microos-unit-selected.tsv, s4-microos-unit-links.tsv, s4-microos-sources.tsv and active /etc traversal',
'M03': 'Current links and package script text; no per-link enablement-event table is emitted',
'M04': 's4-microos-sources.tsv source bytes plus package-files.tsv; 8 dependent IDs, 7 duplicate-key IDs, at most 1 structurally matchable ID',
'M05': 'Current source bytes and package-file comparisons; no per-rule choice-event table; 7 dependent IDs, 6 duplicate-key IDs, at most 1 structurally matchable ID',
'M06': 'objects/member tables traverse /etc while retaining expanded snapshot marker; full-digests.tsv and source sidecars',
'M07': 's4-microos-snapshot-files.tsv snapshot RPM manifests and full hashes; absent manifest rows and unknown comparisons remain explicit',
'M08': 'full-digests.tsv and s4-microos-snapshot-current.tsv complete SHA256 pairs',
'M09': 'semodule format/checksum listings and full snapshot/current comparisons; no original per-copy receipt or derivation-event record is emitted',
'M10': 's4-microos-sources.tsv bounded complete bytes of grubenv',
'M11': 'Current grubenv bytes; no per-value creation/choice event table is emitted',
'M12': 'Snapshot-root RPM query, s4-microos-snapshot-files.tsv and full snapshot/current SHA256 pairs; 1 RESULT-only ID, 0 IDs in fixed matching inputs',
'M13': 's4-microos-solver-cache.tsv bounded dumpsolv decoding, cookie/source bytes and full SHA256; 1 RESULT-only ID, 0 IDs in fixed matching inputs',
'T01': 'talos-image-sources.tsv current StaticPod image references; no historical pull-actor record is emitted',
'T02': 'talos-expanded-members.tsv and talos-listing-coverage.tsv bounded API listings; proc/sys/dev component boundaries explicit',
'T03': 'Current listing, hashes and mount tables; no original installed-image member manifest or receipt comparison is emitted',
'T04': 'talos-mountinfo.tsv exact bounded API-daemon mount namespace; no per-object historical overlay-layer record is emitted',
'T05': 'Current listing, content hashes and source references; no per-member creation/derivation-event record is emitted',
'T06': 'talos-content.tsv and talos-content-attempts.tsv bounded Read, Copy and fresh-metadata Read hashes/signatures; per-file failures explicit',
'G01': 'Fresh four-slot boot and two inventory levels recorded; browser_extension and container_run each exited 1, so the full prescribed action sequence did not succeed; 0 first-night IDs',
}

renames = {
'npm original acquisition and receipt provenance':'npm original acquisition event and receipt records',
'No creation event for seven alias/enablement settings':'No creation event for seven alias/enablement links',
'Generated SELinux CIL/HLL derivation and original receipt':'SELinux CIL/HLL copy derivation and original receipt records',
'Generated representation lacked a full original package/derivation record':'SELinux CIL/HLL copies lacked original package/derivation records',
'No causal creation record distinguishes original image, generated or later-written members':'No per-member creation or derivation event was retained',
'Current values do not establish installer default versus later choice':'No installation-default or later-choice event was recorded',
'No causal creation/change record established the chooser':'No chooser-linked creation/change event was recorded',
'No event establishes who chose the values':'No chooser-linked event was recorded',
'No causal event established default versus later choice':'No default-selection or later-choice event was recorded',
'Current-root ownership and 4096-byte prefix equality did not establish snapshot-specific receipt':'No snapshot-root manifest or complete snapshot-file comparison was recorded',
}

class MissingRevision(ast.NodeTransformer):
    def visit_Constant(self, node):
        if isinstance(node.value, str) and node.value in renames:
            return ast.copy_location(ast.Constant(renames[node.value]), node)
        return node
    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id == 'add':
            key = ast.literal_eval(node.args[1])
            node.args[5] = ast.Constant(how[key])
        return node

source = (ROOT/'S4/build-missing.py').read_text()
source = source.replace('ROOT=pathlib.Path(__file__).resolve().parent.parent', '''import argparse
ROOT=pathlib.Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('output',type=pathlib.Path,help='New output directory; must not exist')
OUT=parser.parse_args().output
OUT.mkdir(parents=True,exist_ok=False)''')
source = source.replace("ROOT/'S4/MISSING.tsv'", "OUT/'MISSING.tsv'").replace("ROOT/'S4/missing-row-map.tsv'", "OUT/'missing-row-map.tsv'")
source = source.replace("for ident,machine,name in extra:", """extra += [('void-f2e5d5edfa5902c8aee7bace','void','/etc/ssl/certs'),
          ('microos-dcce813055fa256ed012c87a','microos','/var/lib/ca-certificates/openssl')]
for ident,machine,name in extra:""")
# No certificate kind is guessed. These rows enter only their ID-specific fact group.
source = source.replace("kind='L2:stored-outside-packages' if machine=='microos' else 'L2:stored-ownership-unresolved'", "kind='' if ident in {x[0] for x in extra[5:]} else ('L2:stored-outside-packages' if machine=='microos' else 'L2:stored-ownership-unresolved')")
tree = MissingRevision().visit(ast.parse(source))
source = ast.unparse(ast.fix_missing_locations(tree)) + '\n'
new_groups = '''
add('void','V09','Trust-value choice events and actual consumer/use records',lambda r:r['id']==extra[5][0],
    'D1/RESULT.md Card 2 explicitly leaves the trust-value facts unrecorded',
    'No per-value historical choice or complete consumer/use record is emitted; current metadata/digests may be present, but those named records have no collection route; 1 RESULT-only ID, 0 IDs in fixed matching inputs')
add('microos','M14','Trust-value choice events and actual consumer/use records',lambda r:r['id']==extra[6][0],
    'D1/RESULT.md Card 2 explicitly leaves the trust-value facts unrecorded',
    'No per-value historical choice or complete consumer/use record is emitted; current metadata/digests may be present, but those named records have no collection route; 1 RESULT-only ID, 0 IDs in fixed matching inputs')
'''
source = source.replace('covered = ', new_groups + '\ncovered = ', 1)
source = source.replace("result_only_rows=5", "result_only_rows=7")
(HERE/'build-missing.py').write_text('#!/usr/bin/env python3\n' + source)

notes = {
'A01':'41 cache-reference records; no per-object acquisition-event record is emitted by extra_alma.py/extra_void.py.',
'A02':'Current file content and sanitized installer/network directives recorded.',
'A03':'Recipe, bounded retained-history extracts and scriptlets recorded; no complete per-object choice/change event table is emitted.',
'A04':'Current unit/preset and bounded operation extracts recorded; no original per-unit disablement-event record is emitted.',
'A05':'Three inner-store metadata scans completed; zero nested atomic boundaries in the scan counters.',
'A06':'Inner metadata and prefixes recorded; no complete per-member payload receipt or creation-event table is emitted.',
'A07':'Current key metadata and DNF history recorded; no per-key import-reason field is emitted.',
'A08':'Selected ALSA file contents recorded in alma-facts.tsv.',
'A09':'Stored values and bounded history extracts recorded; no per-value creation-event record is emitted.',
'A10':'Native semanage query records persistent boolean values.',
'A11':'Values, script and bounded history extracts recorded; no per-value chooser-event record is emitted.',
'A12':'Five isolated dconf database reads succeeded.',
'A13':'Schemas/profiles and bounded current mapped-reader snapshot recorded; no complete consumer history is emitted.',
'A14':'24 cache queries decoded with native package-file joins; 2 dependent IDs are outside the fixed matching inputs.',
'A15':'41 verified cache-reference archives and 459 equal complete member comparisons recorded; reference type is retained.',
'V01':'41 lock-addressed verified archives and 459 equal complete member comparisons recorded; directory entries are separately labeled.',
'V02':'Installed/residual/cache manifest routes yield zero unowned members with a reference; 6859 paths have no-surviving-receipt; 22282 equal comparisons belong to already-owned paths.',
'V03':'Current sources and package records retained; no per-account/group/sudo installation-choice event table is emitted.',
'V04':'Three inner-store scans completed with zero nested atomic boundaries; parent association documented.',
'V05':'Metadata and prefixes recorded; no complete per-member payload receipt or creation-event table is emitted.',
'V06':'Selected configuration bytes and whole-file hashes recorded.',
'V07':'Current text/key/mount records retained; historical_creator remains an unknown marker, no creation-event record emitted.',
'V08':'Font-cache source paths and native package-file joins recorded; 1 dependent ID is outside the fixed matching inputs.',
'M01':'Sysusers files and RPM scriptlets recorded; no per-account/group creation-event table is emitted.',
'M02':'263 of 263 unit selections recorded with source files and enablement links.',
'M03':'Current links and script text recorded; no per-link enablement-event table is emitted.',
'M04':'Sudo source bytes and native package-file comparisons recorded; 8 dependent IDs, 7 duplicate old-key IDs, at most 1 structural match.',
'M05':'Source bytes and comparisons recorded; no per-rule choice-event table is emitted; 7 dependent IDs, 6 duplicate old-key IDs, at most 1 structural match.',
'M06':'2219 active /etc descendants traversed; snapshot marker retained.',
'M07':'Two snapshot-root manifests and 15837 complete comparisons recorded; no reference for every snapshot member is emitted.',
'M08':'16177 of 16177 snapshot/current file pairs have complete SHA256 comparisons.',
'M09':'Two SELinux store listings/checksums and snapshot/current comparisons recorded; no original per-copy receipt or derivation-event record is emitted.',
'M10':'Complete bounded grubenv bytes recorded.',
'M11':'Current boot values recorded; no per-value creation/choice event table is emitted.',
'M12':'Snapshot-root package set and database-file comparisons recorded; 1 dependent ID is outside the fixed matching inputs.',
'M13':'One solver-cache decode and three cache/source files recorded; 1 dependent ID is outside the fixed matching inputs.',
'T01':'Three current StaticPod image references recorded; no historical pull-actor table is emitted.',
'T02':'Six opaque roots expanded; 18 component boundaries remain after three listing methods.',
'T03':'Current listing/hash/mount queries emit no original complete installed-image member manifest or receipt comparison.',
'T04':'API-daemon mountinfo recorded; no per-object historical overlay-layer record is emitted.',
'T05':'Current listing/content/source references recorded; no per-member creation/derivation-event table is emitted.',
'T06':'5940 of 5963 initial regular files have complete hashes; 23 remain not-found after Read, Copy and fresh-metadata Read (9 containerd, 14 kubelet).',
'G01':'Fresh four-slot boot and two-level inventory recorded; browser_extension and container_run each exit 1; full prescribed action sequence did not succeed.',
'V09':'No per-trust-value historical choice or complete consumer/use record is emitted by the existing collector; 0 matching-input IDs. No new probe attempted.',
'M14':'No per-trust-value historical choice or complete consumer/use record is emitted by the existing collector; 0 matching-input IDs. No new probe attempted.',
}
status = ast.parse((ROOT/'S4/build-status.py').read_text())
for node in status.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        name = node.targets[0].id
        if name == 'notes': node.value = ast.parse(repr(notes), mode='eval').body
        elif name in ('recorded','partial'):
            values = ast.literal_eval(node.value)
            if name == 'recorded': values.remove('G01')
            else: values.add('G01')
            node.value = ast.parse(repr(sorted(values)), mode='eval').body
status_source = ast.unparse(ast.fix_missing_locations(status)) + '\n'
status_source = status_source.replace('R = Path(__file__).resolve().parent', '''import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('tables',type=Path)
parser.add_argument('output',type=Path,help='New status TSV; must not exist')
args=parser.parse_args()
R=args.tables''')
status_source = status_source.replace("(R / 'fact-status.tsv').open('w', newline='')", "args.output.open('x', newline='')")
status_source = status_source.replace("'rehearsal/", "'S4/rehearsal/")
status_source = status_source.replace("key, status, evidence[r['machine']], notes[key]", "key, status, evidence[r['machine']] + ';S4/collector/extra_' + r['machine'] + '.py' if r['machine'] != 'gentoo' else evidence[r['machine']], notes[key]")
(HERE/'build-status.py').write_text('#!/usr/bin/env python3\n' + status_source)

# Revised neutral instrument documentation. Older documents remain preserved.
doc = (ROOT/'S4/COLLECT.md').read_text()
replacements = {
'five source/content extent candidates explicitly named in D1/RESULT.md add five IDs':'five source/content candidates and two trust-value candidates explicitly named in D1/RESULT.md add seven IDs, outside the fixed matching inputs',
'Snapshot-generated CIL/HLL copies can have known complete equality without a surviving original generation receipt. Current sysusers/default files and enablement links do not establish a historical chooser.':'SELinux CIL/HLL copies have separate manifest and snapshot/current comparison tables. Current sysusers/default files and enablement links are retained as sources; no per-object chooser-event table is emitted.',
'A package script text is not proof that its branch executed. A present installer recipe does not establish every later event.':'The scriptlets and installer directives are stored as source text; the adapter emits no complete per-object execution history.',
'No receipt equality is inferred without a reference.':'Reference comparisons, when available, are in separate tables.',
'Prefix signatures do not verify image/package receipt.':'This table stores metadata and prefix signatures, without a reference-image comparison column.',
'These are supporting facts for opaque objects, not invented ownership receipts.':'The table stores metadata without per-member receipt or acquisition-event records.',
'A verified archive is distinct from an installation receipt.':'The record identifies its reference source (lock, installed metadata or cache index).',
'Only full archive-member comparison establishes byte equality to that recorded reference; locally added members remain unproved.':'Complete member bytes or targets are compared with that reference; members absent from it carry not-compared-to-archive.',
'Generated module lists/initramfs are not assumed shipped.':'Only entries in the queried manifests have reference fields.',
"A registry/reference match does not prove the file's past installation event.":'The table contains a reference comparison, with no per-file installation-event field.',
'Cache-only reference status explicitly says it is not an installation receipt.':'The existing cache-only reference status literal is documented below.',
'complete installed member hashes/targets are compared, and local extra members remain unproved.':'complete installed member hashes/targets are compared, and members absent from the reference are labeled not-compared-to-archive.',
'`parts/void.md` records the three old-receipt routes and their limits.':'The three routes are installed manifests, residual metadata and cached archive manifests.',
'complete SHA256 equality only; no original receipt inferred.':'complete SHA256 comparison of the two named paths.',
'Original image receipt, historical acquisition and unambiguous historical overlay attribution remain unknown.':'The added tables emit no original image-member manifest, pull-event history or per-object historical layer record.',
'Does not establish the historical pull actor.':'No pull-actor field is emitted.',
'no image integrity inference.':'no original-image comparison field.',
'Backing/receipt remain unknown where not certified.':'The existing backing and image_integrity fields retain their source references or explicit unknown markers.',
'A successful listing or batch exit does not prove per-file content success or original-image equality.':'Batch/listing exits and per-file content statuses are separate fields; no original-image comparison is performed.',
'Current mount options/source support backing analysis but do not identify a historical writer, image receipt, or unchanged lower-layer contents. `parts/talos.md` cites the API implementation and mountinfo documentation.':'The table contains current mount options/source and no historical writer or lower-layer comparison fields. Format reference: https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html .',
'The complete fresh-run reports, distinct attempted methods, remaining facts and cleanup evidence are in `READY.md` and the per-system parts. Rehearsals do not observe the hypothesis and make no object decisions. The independent acceptance is RV-S4-P; source/aggregate checks by the builder are not that acceptance.':'Rehearsal reports and diagnostics are records only, excluded from the instrument and classification handoff lists. The deciding parties receive no rehearsal output, readiness report, fact-status summary or part report. Independent acceptance remains separate from preparation.',
}
for old,new in replacements.items():
    assert old in doc, old
    doc = doc.replace(old,new)
doc += '''
## Revision scope and unchanged status literals

This revision's documents and tables live in `S4/fix-s4-p-1/`; runtime code and the matching script remain in `S4/collector/`, with `S4/collect.sh` as entry point. `PUBLISH.list` is the revised instrument set; `CLASSIFICATION-INPUTS.list` is the document subset for deciding parties, supplied alongside the new observation and matching output. `RECORDS.list` is a separate publication set, not a classification input.

Existing collector status literals such as `cache-identity-reference-not-install-receipt`, `recorded-not-history-proof`, and `unknown:no-original-image-manifest` are preserved for byte/schema compatibility. They identify reference source types or absent collector fields; this document makes no ruling on which facts answer a question in the published text. Per-file query failures and explicit unknown fields remain available in observation output. Deciding parties assess the recorded evidence themselves.

V09/M14 list the choice events and consumer/use records missing for the two trust-value groups named by D1/RESULT.md. The current collector emits no per-value choice history or complete consumer/use table. File metadata, prefix signatures and eligible whole-file digests retain their usual path joins; they are not relabeled as those missing records. A past choice with no retained event record has no retrospective query route in this instrument. No additional machine, action, case, or matching input is introduced. Whether the text decides these objects remains for the deciding parties within the authorized scope.

`objects` in MISSING.tsv remains an integer count of dependent first-night IDs, as required by the original task. Matching limits appear in `how_recorded_now` and `match-scope.tsv`: RESULT-only IDs have zero fixed-input matching routes; M04/M05 each have at most one structurally eligible ID. Eligibility does not promise a match in a new inventory.
'''
doc = doc.replace('`MISSING.tsv`', '`tables/MISSING.tsv`').replace('`missing-row-map.tsv`', '`tables/missing-row-map.tsv`').replace('`match-scope.tsv`', '`checks/match-scope.tsv`')
(HERE/'COLLECT.md').write_text(doc)
match = (ROOT/'S4/MATCH.md').read_text().replace('the five additional extent candidates', 'the seven additional source/content and trust-value candidates')
match += '\nThe runtime rule and its two input tables are unchanged. `match-scope.tsv` records dependency counts and structural eligibility only. M04 has seven duplicate-key IDs of eight; M05 has six of seven. Each has at most one structurally eligible ID. The seven RESULT-only IDs have no route in these matching inputs; their inclusion in a later decision scope remains an author question.\n'
match = match.replace('MISSING.tsv', 'tables/MISSING.tsv').replace('`match-scope.tsv`','`checks/match-scope.tsv`')
(HERE/'MATCH.md').write_text(match)
commands = (ROOT/'S4/COMMANDS.md').read_text().replace('`S4/PUBLISH.list`','`S4/fix-s4-p-1/PUBLISH.list`').replace('`S4/input-files.sha256.tsv`','`S4/fix-s4-p-1/input-files.sha256.tsv`').replace('python3 S4/verify-inputs.py','python3 S4/fix-s4-p-1/verify-inputs.py').replace('follows `MATCH.md`','follows `S4/fix-s4-p-1/MATCH.md`')
commands += '\nInstrument commit scope is the revised PUBLISH.list. S4_INPUTS still points to the S4 runtime directory containing collect.sh and collector/. Documents/tables are taken from fix-s4-p-1/, not the superseded top-level copies. RECORDS.list is published separately and withheld from deciding parties; use CLASSIFICATION-INPUTS.list for their document handoff.\n'
(HERE/'COMMANDS.md').write_text(commands)
void = (ROOT/'S4/parts/void.md').read_text().replace('default settings (1), module settings (1), sudo rules (1)', '`/etc/default` (1), `/etc/modules-load.d` (1), `/etc/sudoers.d` (1)')
(HERE/'records/void.md').write_text('Correction copy, 2026-11-23 UTC. Replaces the cited wording of S4/parts/void.md; earlier evidence paths are relative to S4/. Records only; not supplied to deciding parties.\n\n'+void)
print('Prepared revised table generators and documentation; runtime unchanged.')
