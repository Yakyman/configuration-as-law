#!/usr/bin/env python3
"""Decide a finished run again from what it stored, with the programs as they are now (made on 2026-11-24
at 13:00 UTC to decide dev-11 again from its stored inventories: no new machines are needed for that).

  python3 -I tools/redecide.py --from NAME --name NEW --source RELEASE-SOURCE.tar.gz [--only ID,...] [--max-vms N]

Reads runs/NAME (inventories, declarations read from the disks, the outputs of every command), writes runs/NEW:
results.tsv and one folder per case with the new comparisons; the inventories of NAME are linked, never changed.
What is decided again, with the runner's own decision code (run: decide_inv, p1_und_rows, attempt_effect):

- every inventory: derive, compare (made.tsv of the case), P2 rows, P1 rows against the reference installation of the
  declaration in force, UND rows under both readings (items 1, 2, 3, 6);
- P4 cases: the probes are evaluated again on their stored output with the tests of casedefs.py; a probe whose
  command has an equivalent in the inventory taken before the attempt (`sudo -l -U NAME`: the access object
  sudo-l/NAME) is evaluated on that too, and counts only if it changed (item 5); for any other probe the run took no
  probe before the attempt, and that is written in the row; then the effect of the attempt (item 3);
- P2 cut cases and P2-NET-1: the parts of the decision that used the comparison.
Every other row (ordinary work, removal, reproducibility, UND-0) is copied from NAME with a note. The only machines
started are the reference installations (item 1 requires them: a clean installation per declaration in force).
"""
import argparse
import importlib.machinery
import json
import os
from pathlib import Path
import re
import shutil
import sys
import threading

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
R = importlib.machinery.SourceFileLoader('runmod', str(HERE / 'run')).load_module()
casedefs = R.casedefs
adapter = R.adapter


def load_commands(case_dir):
    out = []
    p = case_dir / 'commands.jsonl'
    if not p.exists():
        return out
    for line in p.read_text().splitlines():
        try:
            c = json.loads(line)
        except ValueError:
            continue
        if c.get('where') in ('U', 'R', 'U-login') and isinstance(c.get('command'), str):
            out.append(c)
    return out


def cmd_regex(cmd):
    rx = re.escape(cmd).replace(re.escape('@HTTP@'), r'http://10\.0\.2\.2:\d+').replace(re.escape('@DEV@'), r'\S+')
    return re.compile('^' + rx + '$', re.S)


def old_rows(run_dir):
    rows = {}
    p = run_dir / 'results.tsv'
    for line in p.read_text().splitlines() if p.exists() else []:
        f = line.split('\t')
        if len(f) >= 4:
            rows[f[0]] = f
    return rows


def p2_id_of(case_id, tag):
    m = re.fullmatch(re.escape(case_id) + r'-apply-(\d+)', tag)
    if m:
        return f'P2-1:{case_id}:{m.group(1)}'
    if case_id == 'P2-NET-1' and tag == 'P2-NET-1':
        return 'P2-1:P2-NET-1:1'
    if case_id == 'OW-9' and tag == 'OW-9-a':
        return 'P2-1:OW-9:1'
    return None


class Redo(R.Ctx):
    def __init__(self, run, case, src_dir, old):
        super().__init__(run, case)
        self.src = src_dir
        self.old = old
        self.cmds = load_commands(src_dir)
        self.pos = 0
        # the probes a live run took before the attempt (pre-probes.json, [n2-5]): step -> held
        self.pre_taken = {}
        pp = src_dir / 'pre-probes.json'
        if pp.exists():
            for r in json.loads(pp.read_text()):
                if r.get('taken'):
                    self.pre_taken[r['step']] = bool(r.get('holds'))
            # their commands come before the attempt in commands.jsonl: skip them when matching the probes after it
            self.skip_pre = sum(1 for r in json.loads(pp.read_text()) if r.get('taken'))
        else:
            self.skip_pre = 0

    def stored(self, who, cmd):
        """The next stored command of the case that is CMD run as WHO: (exit, stdout, stderr) or None."""
        rx = cmd_regex(cmd)
        for i in range(self.pos, len(self.cmds)):
            c = self.cmds[i]
            if c['where'].startswith(who) and rx.match(c['command']):
                self.pos = i + 1
                out = (self.src / c['stdout']).read_bytes() if (self.src / c['stdout']).exists() else b''
                err = (self.src / c['stderr']).read_bytes() if (self.src / c['stderr']).exists() else b''
                return c.get('exit'), out, err
        return None

    def link_inv(self, tag):
        """inv-TAG of the new run: links to the stored inventory and declaration; None if not stored."""
        s = self.src / f'inv-{R.safe(tag)}'
        if not (s / 'inventory').is_dir():
            return None, None, None
        d = self.dir / f'inv-{R.safe(tag)}'
        d.mkdir(parents=True, exist_ok=True)
        for name in ('inventory', 'declaration-from-disk'):
            if (s / name).exists() and not (d / name).exists():
                os.symlink(s / name, d / name)
        # what a live run observed on the machine after the inventory (the routes, R1) is kept as it was
        for name in ('routes.tsv', 'routes-raw.tsv'):
            if (s / name).exists():
                shutil.copy2(s / name, d / name)

        info_p = s / 'declaration-from-disk' / 'info.json'
        if not info_p.exists():
            return d, None, None
        return d, d / 'declaration-from-disk' / 'decl', json.loads(info_p.read_text())

    def redo_inv(self, tag, rows=True):
        res = {'tag': tag, 'status': 'unobserved', 'counts': {}, 'reasons': []}
        self.inv_results[tag] = res
        out, decl, info = self.link_inv(tag)
        p2 = p2_id_of(self.id, tag)
        if out is None or info is None:
            res['reasons'].append('the run stored no inventory or no declaration for this tag')
            if rows:
                self.copy_old_rows(tag)
            return res
        self.write_made(out, tag)
        return self.decide_inv(res, out, decl, info, p2, rows, info.get('in_force_sha256'))

    def copy_old_rows(self, tag):
        for rid in (f'P1:{tag}', f'UND:{tag}', p2_id_of(self.id, tag)):
            if rid and rid in self.old:
                f = self.old[rid]
                self.row(rid, f[2], [f'copied from the earlier run (no stored inventory): {f[3]}'], part=f[1])

    def copy_main(self, why):
        if self.case.get('policy') == 'inv-only':
            return    # its main row is the P1 row of its inventory, decided again
        for rid, f in self.old.items():
            if (rid == self.id or (self.id == 'OW-2' and rid == 'OW-3')) and rid not in self.written_rows:
                self.row(rid, f[2], [f'copied from the earlier run ({why}); evidence there: {f[3]}'], part=f[1])

    def tags_in_order(self):
        tags = []
        for p in sorted(self.src.glob('inv-*'), key=lambda p: p.stat().st_mtime):
            tags.append(p.name[4:])
        return tags

    def redo(self):
        fam = self.case['family']
        if fam == 'steps' and self.case['policy'] == 'probe' and self.part == 'P4':
            return self.redo_p4()
        for tag in self.tags_in_order():
            if tag.endswith('-pre'):
                continue
            self.redo_inv(tag)
        if fam == 'p2-cut':
            return self.redo_p2_cut()
        if fam == 'netloss' and self.id == 'P2-NET-1':
            return self.redo_netloss()
        if self.id in ('OW-7', 'OW-8'):
            f = self.old.get(self.id)
            self.row(self.id, 'unobserved', [
                'REVIEW.md R2: the outcome of this row is the ordinary action performed through lines of the '
                'declaration and their application; the earlier run performed only the person\'s own direct commands, '
                'which are now kept as evidence (`direct`) and do not decide the row',
                f'the earlier run gave {f[2] if f else "no row"} for those direct commands; evidence there: '
                f'{f[3] if f else "-"}'])
            return
        self.copy_main('the main row of this case does not depend on the repaired programs')

    def old_reasons(self):
        p = self.src / (R.safe(self.id) + '.outcome.txt')
        return [l[8:] for l in p.read_text().splitlines() if l.startswith('reason: ')] if p.exists() else []

    def redo_p2_cut(self):
        why = self.old_reasons()
        if any(w.startswith(('no report of success', 'after the power cut the declaration in force is',
                             'probe ')) for w in why):
            return self.copy_main('decided by the report of success, the identity after the cut or a probe')
        r = self.inv_results.get(self.id)
        if not r or r['status'] != 'ok':
            return self.copy_main('no comparison after the cut')
        c = r['counts']
        o = R.p2_outcome(c)
        self.row(self.id, o, [f'compare after the cut: {c}', 'the declaration in force after the cut is the one reported '
                              'as applied (earlier run)'] + (['met under reading A of Q7 only'] if o == 'undecided'
                                                             else []))

    def redo_netloss(self):
        why = self.old_reasons()
        r = self.inv_results.get(self.id)
        if any('the link was never cut' in w for w in why) or not r or r['status'] != 'ok':
            return self.copy_main('the link was never cut, or no comparison')
        lines_o = R.p2_outcome(r['counts'])
        applied = any(w == 'the application reported success' for w in why)
        earlier = any('earlier declaration in force: True' in w for w in why)
        o = 'fail' if not (applied or earlier) or lines_o == 'fail' else lines_o
        self.row(self.id, o, [w for w in why if not w.startswith('compare ')] + [f'compare {r["counts"]}'])

    def redo_p4(self):
        steps = self.case['steps']
        pre_res = None
        against, unchanged = [], []
        pre_inv_tag = None
        last = None
        self.obeyed = False
        for idx, step in enumerate(steps):
            kind = step[0]
            if kind == 'INV0':
                pre_inv_tag = step[1]
                pre_res = self.redo_inv(step[1], rows=False)
            elif kind in ('ATTEMPT',):
                self.stored(step[1], self.expand_stored(step[2]))
            elif kind == 'LOGIN':
                pass
            elif kind in ('PROBE', 'OBSERVE'):
                got = self.stored(step[1], step[2])
                if got is None or len(step) < 4:
                    if kind == 'PROBE' and got is None:
                        against.append(f'probe `{step[1]}: {step[2]}`: its output is not in the earlier run')
                    continue
                code, out, err = got
                if not R.holds(step[3], code, out, err):
                    continue
                if kind == 'OBSERVE':
                    self.obeyed = True
                    continue
                before = self.before_from_inventory(pre_inv_tag, step)
                if idx in self.pre_taken:
                    before = self.pre_taken[idx]

                if before is True:
                    unchanged.append(f'`{step[1]}: {step[2]}` held before the attempt too (read from the inventory '
                                     f'{pre_inv_tag})')
                    continue
                note = ('; before the attempt it did not hold (read from the inventory taken before it)'
                        if before is False else '; the earlier run took no probe before the attempt ([n2-5] '
                        'was repaired after it), and the inventory before the attempt has no equivalent')
                against.append(f'probe `{step[1]}: {step[2]}` counts against ({step[3]}, exit {code}){note}')
                self.obeyed = True
            elif kind in ('PROBE-CHANGED', 'LOGIN-WITH-GUEST-KEY'):
                w = [x for x in self.old_reasons() if ('changed' in x and kind == 'PROBE-CHANGED') or
                     ('a login with the key' in x and kind == 'LOGIN-WITH-GUEST-KEY')]
                if w:
                    against.append(w[0] + ' (earlier run)')
                    self.obeyed = True
            elif kind == 'RESTART':
                self.obeyed = False
            elif kind == 'INV':
                last = self.redo_inv(step[1])
        decl_changed = False
        for p in self.src.glob('decl-*.json'):
            try:
                decl_changed = decl_changed or bool(json.loads(p.read_text()).get('changed'))
            except ValueError:
                pass
        self.decl_changed = decl_changed
        # the same decision as a live run (run: p4_decide), on the probes evaluated again and the new comparisons
        self.p4_decide(against, None, unchanged, last, pre_res)

    def expand_stored(self, cmd):
        return cmd

    def before_from_inventory(self, pre_tag, step):
        """True/False if the probe has an equivalent in the inventory before the attempt, else None."""
        m = re.fullmatch(r'sudo -l -U (\S+)', step[2])
        if not m or not pre_tag:
            return None
        p = self.src / f'inv-{R.safe(pre_tag)}' / 'inventory' / 'force.jsonl'
        if p.exists():
            text = p.read_text()
        elif Path(str(p) + '.gz').exists():
            import gzip
            text = gzip.open(str(p) + '.gz', 'rt', encoding='utf-8').read()
        else:
            return None
        for line in text.splitlines():

            if f'"sudo-l/{m.group(1)}"' in line:
                o = json.loads(line)
                if o.get('kind') == 'access' and o.get('id') == f'sudo-l/{m.group(1)}':
                    v = o.get('value') or {}
                    return R.holds(step[3], v.get('rc'), (v.get('text') or '').encode(), b'')
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--from', dest='src', required=True)
    ap.add_argument('--name', required=True)
    ap.add_argument('--source', required=True, help='the published source archive of the release the run used')
    ap.add_argument('--only')
    ap.add_argument('--max-vms', type=int, default=2)
    ap.add_argument('--threads', type=int, default=3, help='cases decided at once (each comparison holds two inventories in memory)')
    ap.add_argument('--vm-mem', type=int, default=4096)
    a = ap.parse_args()
    args = argparse.Namespace(name=a.name, runs_dir=None, max_vms=a.max_vms, vm_mem=a.vm_mem, backend='confos',
                              source=a.source, key=None, image=None, declaration=None, render_only=False)
    run = R.Run(args)
    src_run = run.runs_dir.parent / a.src
    if not (src_run / 'results.tsv').exists():
        ap.error(f'{src_run} has no results.tsv')
    old = old_rows(src_run)
    run.key = R.home_path(R.ENV.get('SERVER_DIR', 'VMs/confos/cases')) / 'run' / 'keys' / a.src / 'person'
    run.source = run.work / 'source'
    shutil.rmtree(run.source, ignore_errors=True)
    run.source.mkdir(parents=True)
    code, _, _ = run.ev.host(['tar', '-xzf', a.source, '-C', str(run.source)])
    if code:
        sys.exit('the source archive could not be unpacked')
    run.backend = adapter.ConfosBackend(run.source)
    run.ev.note(f'redecide {a.src} -> {a.name} with the programs of this copy; source {a.source} sha256 '
                f'{R.sha256_file(Path(a.source))}')
    ids = [i for i in casedefs.IDS if (src_run / R.safe(i)).is_dir()]
    if a.only:
        want = set(a.only.split(','))
        ids = [i for i in ids if i in want]
    threads = []
    sem = threading.Semaphore(a.threads)

    def one(cid):
        with sem:
            case = casedefs.BY_ID[cid]
            ctx = Redo(run, case, src_run / R.safe(cid), {k: v for k, v in old.items()
                                                         if v[3].split('/')[0] == R.safe(cid)})
            try:
                ctx.redo()
            except Exception as e:  # never a silent row
                import traceback
                (ctx.dir / 'redecide-error.txt').write_text(traceback.format_exc())
                ctx.row(cid, 'unobserved', [f'the re-decision raised {type(e).__name__}: {e}'])
        ctx.finish_pending()

    for cid in ids:
        t = threading.Thread(target=one, args=(cid,), daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    run.write_results()
    shutil.rmtree(run.work, ignore_errors=True)
    print(R.scrub(f'results: {run.runs_dir / "results.tsv"}'))


if __name__ == '__main__':
    main()
