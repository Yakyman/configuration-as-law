#!/usr/bin/python3
"""VM-only randomized X6 measurement. Oracle frozen in X6-PROTOCOL.md.
Uses the unmodified B controller through calctl; never imports controller code.
"""
import argparse
import base64
import collections
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import random
import subprocess
import traceback

BASE = Path('/var/lib/cal')
ROOT = Path('/etc/cal/root.json')
PROGRAMS = ('alpha', 'beta')
KEYS = ('alpha', 'beta', 'shared-cache')
PERSONAL = {u: {'programs': {}} for u in ('alice', 'bob')}
SEEDS = (6, 42, 1119, 20261119)

def clone(x): return copy.deepcopy(x)
def b64(x): return base64.b64encode(x).decode()
def digest(x): return hashlib.sha256(x).hexdigest()
def save(path, obj): path.write_text(json.dumps(obj, indent=2, sort_keys=True)+'\n')
def decl(mode='keep', programs=None):
    return dict(archive=mode, programs={p:dict(version=str(v),scope='system',owners=[]) for p,v in (programs or {}).items()}, policies={},allow_channels={},shared={'cache':['alpha','beta']})

def active_keys(doc):
    # Independent known-owner fixture relation, not B statekeys implementation.
    p = set(doc['programs'])
    return p | ({'shared-cache'} if p else set())

def effective(doc, generation):
    return dict(root=clone(doc),personal=clone(PERSONAL),archive=doc['archive'],programs=clone(doc['programs']),shared=clone(doc['shared']),allow_channels={},generation=generation)

class Invalid(Exception): pass
class Failure(Exception):
    def __init__(self, signature, **details):
        self.signature=signature; self.details=details
        super().__init__(signature)

class Model:
    def __init__(self):
        self.saved={'reset':decl('delete')}; self.current='reset'
    @property
    def doc(self): return self.saved[self.current]
    def apply(self, op):
        kind=op['kind']
        if kind=='gc':
            if self.current in op['targets'] or any(x not in self.saved for x in op['targets']): raise Invalid('GC dependency')
            for x in op['targets']: del self.saved[x]
            return
        d=clone(self.doc)
        if kind=='set': d=clone(op['document'])
        elif kind=='rollback':
            if op['target'] not in self.saved or op['target']==self.current: raise Invalid('rollback dependency')
            d=clone(self.saved[op['target']])
        elif kind=='toggle': d['archive']='delete' if d['archive']=='keep' else 'keep'
        elif kind=='add':
            if op['program'] in d['programs']: raise Invalid('add precondition')
            d['programs'][op['program']]=dict(version=str(op['version']),scope='system',owners=[])
        elif kind=='remove':
            if op['program'] not in d['programs']: raise Invalid('remove precondition')
            del d['programs'][op['program']]
        elif kind=='upgrade':
            if op['program'] not in d['programs'] or int(op['version'])<=int(d['programs'][op['program']]['version']): raise Invalid('upgrade precondition')
            d['programs'][op['program']]['version']=str(op['version'])
        else: raise Invalid('unknown operation')
        if op['label'] in self.saved: raise Invalid('duplicate label')
        self.saved[op['label']]=d; self.current=op['label']

def plan(seed):
    rng=random.Random(seed); model=Model(); ops=[]
    def add(op): model.apply(op); ops.append(op)
    add(dict(kind='set',label='initial',phase='setup',document=decl('keep',dict(alpha=1,beta=1))))
    for i in range(128):
        present=sorted(model.doc['programs']); absent=sorted(set(PROGRAMS)-set(present))
        earlier=sorted(set(model.saved)-{model.current})
        kinds=['toggle']
        if absent: kinds.append('add')
        if present: kinds+=['remove','upgrade']
        if earlier: kinds.append('rollback')
        kind=rng.choice(kinds); op=dict(kind=kind,label=f'r{i:03}',phase='random',random_index=i)
        if kind=='add': op.update(program=rng.choice(absent),version='1')
        elif kind in ('remove','upgrade'):
            op['program']=rng.choice(present)
            if kind=='upgrade': op['version']=str(int(model.doc['programs'][op['program']]['version'])+1)
        elif kind=='rollback': op['target']=rng.choice(earlier)
        add(op)
        draw=rng.randrange(4); earlier=sorted(set(model.saved)-{model.current})
        if earlier and draw in (0,1):
            targets=earlier if draw==0 else sorted(rng.sample(earlier,rng.randint(1,len(earlier))))
            add(dict(kind='gc',phase='random-gc',label=f'g{i:03}',targets=targets))
    for index,mode in enumerate(('keep','delete')):
        prefix='tail-'+mode; first=PROGRAMS[(seed+index)%2]; second=next(p for p in PROGRAMS if p!=first)
        add(dict(kind='set',phase='tail',label=prefix+'-both',document=decl(mode,dict(alpha=1,beta=1))))
        add(dict(kind='remove',phase='tail',label=prefix+'-one',program=first))
        add(dict(kind='remove',phase='tail',label=prefix+'-zero',program=second))
        add(dict(kind='gc',phase='tail',label=prefix+'-gc',targets=sorted(set(model.saved)-{model.current})))
    return ops

class Run:
    def __init__(self, folder):
        self.folder=folder; folder.mkdir(parents=True,exist_ok=False)
        self.log=(folder/'events.jsonl').open('w'); self.seq=0
        self.model=Model(); self.ids={}; self.caches={}; self.counts=collections.Counter(); self.assertions=collections.Counter()
    def emit(self,event,**fields):
        self.seq+=1; self.log.write(json.dumps(dict(event=event,line=self.seq,**fields),sort_keys=True)+'\n'); self.log.flush()
    def check(self, ok, signature, category='P6', **fields):
        self.assertions[category]+=1
        if not ok:
            self.emit('failure',signature=signature,category=category,**fields)
            raise Failure(signature,category=category,**fields)
    def command(self, args, require=True):
        try:
            p=subprocess.run(args,capture_output=True,timeout=180)
        except Exception as exc:
            self.emit('command-error',argv=args,error=str(exc)); raise Failure('command-exception',error=str(exc))
        self.emit('command',argv=args,returncode=p.returncode,stdout_base64=b64(p.stdout),stderr=p.stderr.decode(errors='replace'))
        if require: self.check(p.returncode==0,'command-returncode','instrument',argv=args,returncode=p.returncode)
        return p
    def ctl(self,*args):
        p=self.command(['/usr/local/bin/calctl',*args])
        try: result=json.loads(p.stdout)
        except Exception as exc: raise Failure('command-json',error=str(exc))
        self.check(result.get('ok') is True,'controller-error','instrument',result=result)
        return result
    def reset(self):
        for user in PERSONAL:
            Path('/home',user,'declaration.json').write_text(json.dumps(PERSONAL[user]))
        ROOT.write_text(json.dumps(decl('delete')))
        applied=self.ctl('apply'); current=applied['generation']
        self.ids['reset']=current
        status=self.ctl('status'); old=[g for g in status['generations'] if g!=current]
        if old: self.ctl('gc',*old)
        status=self.ctl('status')
        self.check(not status['active'] and not status['archive'],'reset-not-empty','instrument',status=status)
        self.emit('reset-complete',current=current)
        self.verify(dict(kind='reset',label='reset',phase='setup'),{})
    def snapshot(self):
        entries=[]
        for area in ('active','archive'):
            for p in sorted((BASE/area).rglob('*')):
                st=p.lstat(); row=dict(path=str(p.relative_to(BASE)),inode=st.st_ino,mode=oct(st.st_mode),uid=st.st_uid,gid=st.st_gid)
                if p.is_symlink(): row['symlink']=os.readlink(p)
                elif p.is_file():
                    data=p.read_bytes(); row.update(size=len(data),sha256=digest(data),bytes_base64=b64(data))
                entries.append(row)
        return dict(entries=entries,current=json.loads((BASE/'current.json').read_text()),generations={p.stem:json.loads(p.read_text()) for p in sorted((BASE/'generations').glob('*.json'))},root=json.loads(ROOT.read_text()),personal={u:json.loads(Path('/home',u,'declaration.json').read_text()) for u in PERSONAL})
    def verify(self,op,previous):
        snap=self.snapshot(); d=self.model.doc; current=active_keys(d)
        referenced=set().union(*(active_keys(x) for x in self.model.saved.values()))
        self.emit('checkpoint',label=op['label'],operation=op,expected_current=d,logical_generations=self.model.saved,generation_handles=self.ids,expected_caches={k:b64(v) for k,v in self.caches.items()},snapshot=snap)
        expected_saved={self.ids[k]:effective(v,self.ids[k]) for k,v in self.model.saved.items()}
        self.check(snap['generations']==expected_saved,'saved-ledger','instrument')
        self.check(snap['current']==effective(d,self.ids[self.model.current]),'current-ledger','instrument')
        self.check(snap['root']==d and snap['personal']==PERSONAL,'declaration-restore','instrument')
        entries={e['path']:e for e in snap['entries']}
        locations={area:{p.name for p in (BASE/area).iterdir()} for area in ('active','archive')}
        self.check(not ((locations['active']|locations['archive'])-set(KEYS)),'unexpected-state-object','instrument',locations={k:sorted(v) for k,v in locations.items()})
        for k in KEYS:
            want='active' if k in current else ('archive' if k in self.caches else None)
            actual=[a for a in ('active','archive') if k in locations[a]]
            self.check(actual==([want] if want else []),'placement:'+k,expected=want,actual=actual,current_owners=sorted(set(d['programs'])&({k} if k in PROGRAMS else set(PROGRAMS))),saved_reference=k in referenced,archive=d['archive'])
            if want:
                path=f'{want}/{k}/cache'
                self.check(path in entries and 'bytes_base64' in entries[path],'cache-missing:'+k)
                data=base64.b64decode(entries[path]['bytes_base64'])
                if k in previous:
                    self.check(data.startswith(previous[k]),'retention-prefix:'+k)
                    if k=='shared-cache': self.check(data==previous[k],'shared-continuity:'+k)
                self.check(data==self.caches[k],'worker-contract:'+k,'instrument',expected_sha256=digest(self.caches[k]),actual_sha256=digest(data))
                if want=='active':
                    version='shared' if k=='shared-cache' else d['programs'][k]['version']
                    vpath=BASE/want/k/'version'
                    self.check(vpath.exists() and json.loads(vpath.read_text())==version,'version:'+k,'instrument')
                    consumers=sorted(d['programs']) if k=='shared-cache' else [k]
                    for p in consumers:
                        result=self.command(['/usr/local/lib/cal/'+p,'--read-shared',str(BASE/path)],require=False)
                        self.check(result.returncode==0 and result.stdout==self.caches[k],'readable:'+k+':'+p)
                        self.counts['shared_reads' if k=='shared-cache' else 'own_reads']+=1
            elif k in previous:
                self.check(k not in current and k not in referenced and d['archive']=='delete','unauthorized-deletion:'+k)
                self.counts['authorized_deletions']+=1
        if len(d['programs'])==1: self.counts['single_owner_checkpoints']+=1
        if not d['programs'] and not referenced:
            self.counts['ownerless_unreferenced_'+d['archive']]+=1
        if op['kind']=='rollback': self.counts['rollback_checkpoints']+=1
        self.emit('checkpoint-pass',label=op['label'],counts=dict(self.counts),assertions=dict(self.assertions))
    def step(self,op):
        before=self.snapshot(); previous=clone(self.caches); previous_doc=clone(self.model.doc)
        self.emit('before',operation=op,snapshot=before)
        self.model.apply(op)
        kind=op['kind']
        if kind=='gc': self.ctl('gc',*(self.ids[g] for g in op['targets']))
        elif kind=='rollback':
            result=self.ctl('rollback',self.ids[op['target']]); self.ids[op['label']]=result['generation']
            if previous_doc['archive']!=self.model.doc['archive']: self.counts['rollback_policy_changed']+=1
            for p in self.model.doc['programs']:
                if p not in previous_doc['programs']: self.counts['rollback_reactivated_programs']+=1
                elif int(self.model.doc['programs'][p]['version'])<int(previous_doc['programs'][p]['version']): self.counts['rollback_downgraded_programs']+=1
        else:
            ROOT.write_text(json.dumps(self.model.doc,sort_keys=True)); self.emit('declaration-write',document=self.model.doc)
            result=self.ctl('apply'); self.ids[op['label']]=result['generation']
        d=self.model.doc
        if kind!='gc':
            for p,item in d['programs'].items(): self.caches[p]=self.caches.get(p,b'')+f"{p} version={item['version']} uid=0\n".encode()
            if d['programs']: self.caches.setdefault('shared-cache',b'shared derivative\n')
        referenced=set().union(*(active_keys(x) for x in self.model.saved.values()))
        if d['archive']=='delete':
            self.caches={k:v for k,v in self.caches.items() if k in referenced}
        self.verify(op,previous)
        self.counts[op['phase']+':'+kind]+=1
        self.counts['mutations']+=1

def valid(ops):
    m=Model()
    try:
        for op in ops: m.apply(op)
    except Invalid: return False
    return True

def execute(folder,ops):
    run=Run(folder); result={'outcome':'1','failure':None,'completed':0,'planned':len(ops)}
    try:
        run.reset()
        for i,op in enumerate(ops):
            run.step(op); result['completed']=i+1
    except Failure as exc:
        result.update(outcome='?',failure=exc.signature,details=exc.details,traceback=traceback.format_exc())
    except Exception as exc:
        result.update(outcome='?',failure='harness-exception',details={'type':type(exc).__name__,'error':str(exc)},traceback=traceback.format_exc())
    result.update(counts=dict(run.counts),assertions=dict(run.assertions))
    run.emit('summary',**result); run.log.close(); save(folder/'summary.json',result)
    save(folder/'operations.json',ops)
    return result

def minimize(folder,ops,signature):
    folder.mkdir(); trials=[]; serial=0
    def reproduces(candidate):
        nonlocal serial
        serial+=1
        if not valid(candidate):
            trials.append(dict(trial=serial,length=len(candidate),valid=False)); return False
        result=execute(folder/f'trial-{serial:04}',candidate)
        same=result['failure']==signature
        trials.append(dict(trial=serial,length=len(candidate),valid=True,reproduced=same,failure=result['failure']))
        save(folder/'trials.json',trials)
        return same
    if not reproduces(ops):
        save(folder/'minimization.json',dict(status='not-reproduced',signature=signature)); return
    candidate=ops[:]; n=2
    while len(candidate)>=2:
        size=(len(candidate)+n-1)//n; reduced=False
        for start in range(0,len(candidate),size):
            trial=candidate[:start]+candidate[start+size:]
            if reproduces(trial): candidate=trial; n=max(2,n-1); reduced=True; break
        if not reduced:
            if n>=len(candidate): break
            n=min(len(candidate),n*2)
    changed=True
    while changed:
        changed=False
        for i in range(len(candidate)):
            if reproduces(candidate[:i]+candidate[i+1:]): candidate=candidate[:i]+candidate[i+1:]; changed=True; break
    save(folder/'minimal-operations.json',candidate)
    reruns=[execute(folder/f'rerun-{i}',candidate) for i in (1,2)]
    save(folder/'trials.json',trials)
    save(folder/'minimization.json',dict(status='1-minimal-under-valid-dependencies',signature=signature,length=len(candidate),reruns=[r['failure'] for r in reruns]))

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True); parser.add_argument('--plan-only',action='store_true'); parser.add_argument('--replay',type=Path)
    args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=False)
    if args.replay:
        if args.plan_only: raise ValueError('incompatible flags')
        execute(args.output/'replay',json.loads(args.replay.read_text())); return
    plans={s:plan(s) for s in SEEDS}
    for seed,ops in plans.items(): save(args.output/f'plan-{seed}.json',ops)
    if args.plan_only: return
    if os.geteuid()!=0 or not Path('/etc/cal').exists(): raise RuntimeError('root in disposable B VM required')
    results={}
    for seed,ops in plans.items():
        print(f"{datetime.datetime.now(datetime.timezone.utc).isoformat()} seed={seed} start",flush=True)
        r=execute(args.output/f'seed-{seed}',ops); results[str(seed)]=r
        print(f"seed={seed} complete={r['completed']} failure={r['failure']}",flush=True)
        if r['failure']:
            prefix=ops[:min(len(ops),r['completed']+1)]
            try:
                minimize(args.output/f'failure-{seed}',prefix,r['failure'])
            except Exception as exc:
                save(args.output/f'minimization-error-{seed}.json',dict(error=str(exc),traceback=traceback.format_exc(),signature=r['failure']))
        save(args.output/'summary.json',results)
    print('DONE',flush=True)

if __name__=='__main__': main()
