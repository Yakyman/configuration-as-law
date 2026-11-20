#!/usr/bin/python3
"""VM-only real programs; explicitly assigned homes, installed owners removed."""
import hashlib,json,os,pwd,subprocess,runpy
from pathlib import Path
h=runpy.run_path('/root/q-main/check-lifecycle.py')
ctl,reset,emit,check=h['ctl'],h['reset'],h['emit'],h['check']
base=Path('/var/lib/cal')
def files(p):
    out={}
    if p.exists():
        for f in sorted(p.rglob('*')):
            if f.is_symlink():out[str(f.relative_to(p))]={'link':os.readlink(f)}
            elif f.is_file():out[str(f.relative_to(p))]={'size':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
    out.pop('version',None)
    return out
def user(label,cmd):
    argv=['runuser','-u','alice','--','/usr/local/bin/cal-login','-c',cmd]
    p=subprocess.run(argv,capture_output=True,text=True,timeout=90)
    emit('user-command',label=label,argv=argv,rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
    check(p.returncode==0,label)
    return p
def declared(mode,programs):
    doc=dict(archive=mode,programs={x:dict(version='1',scope='user',owners=['alice']) for x in programs},policies={},allow_channels={},shared={})
    Path('/etc/cal/root.json').write_text(json.dumps(doc));emit('declaration',document=doc)
    return ctl('apply')
browser='mkdir -p /var/lib/cal/active/browser/home; HOME=/var/lib/cal/active/browser/home XDG_CONFIG_HOME=/var/lib/cal/active/browser/home/.config XDG_CACHE_HOME=/var/lib/cal/active/browser/home/.cache /usr/lib/chromium/chromium --headless --no-sandbox --disable-dev-shm-usage --disable-gpu --no-first-run --no-default-browser-check --user-data-dir=/var/lib/cal/active/browser/home/profile --dump-dom http://127.0.0.1:8080/'
editor="mkdir -p /var/lib/cal/active/editor/home; HOME=/var/lib/cal/active/editor/home /usr/bin/vim.basic -N -n -es -i /var/lib/cal/active/editor/home/.viminfo /home/alice/day-document.txt -c 'normal GoEdited with Vim' -c 'w' -c 'wviminfo!' -c 'qa!'"
assert os.geteuid()==0 and Path('/run/cal.sock').exists()
for mode in ('keep','delete'):
    emit('case-start',archive=mode);reset()
    initial=declared(mode,['browser','editor']); generation=initial['generation']
    home_before=files(Path('/home/alice'))
    user('browser creates profile and crash state',browser)
    user('editor creates viminfo and saves user document',editor)
    initial_files={x:files(base/'active'/x) for x in ('browser','editor')}
    check(any('Crash Reports/settings.dat' in f for f in initial_files['browser']),'Chromium crash file is within assigned home')
    check('home/.viminfo' in initial_files['editor'],'Vim writes its own history')
    home_after=files(Path('/home/alice'))
    changes={x:v for x,v in home_after.items() if home_before.get(x)!=v}
    emit('home-changes',archive=mode,changes=changes,assigned=initial_files)
    check(set(changes)<= {'day-document.txt'},'no unassigned application state observed')
    declared(mode,['editor'])
    emit('package-owner-absence',output=subprocess.run(['dpkg-query','-W','-f=${Package} ${db:Status-Status}\n','chromium','vim'],capture_output=True,text=True).stdout)
    check(not Path('/usr/lib/chromium/chromium').exists(),'Chromium executable removed, no fixed-base owner')
    check(not Path('/usr/lib/chromium/chrome_crashpad_handler').exists(),'Chromium crash-handler owner removed too')
    check(files(base/'archive'/'browser')==initial_files['browser'],'all assigned browser state archived intact')
    check(files(base/'active'/'editor')==initial_files['editor'],'remaining editor state stays active')
    ctl('rollback',generation)
    check(Path('/usr/lib/chromium/chromium').exists(),'rollback restores actual browser executable')
    for ident in ('browser','editor'):
        check(files(base/'active'/ident)==initial_files[ident],'rollback restores exact assigned state',ident=ident)
    user('browser works after rollback',browser)
    user('editor works after rollback',editor)
    latest={x:files(base/'active'/x) for x in ('browser','editor')}
    document=Path('/home/alice/day-document.txt').read_bytes()
    declared(mode,[])
    check(not Path('/usr/lib/chromium/chromium').exists() and not Path('/usr/bin/vim.basic').exists(),'both owner executables removed')
    for package in ('chromium','chromium-common','vim','vim-runtime','vim-common'):
        p=subprocess.run(['dpkg-query','-W','-f=${db:Status-Status}',package],capture_output=True,text=True)
        emit('package-status',package=package,rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
        check(p.stdout!='installed','complete application package group absent',package=package)
    for ident in latest:
        check(not (base/'active'/ident).exists() and files(base/'archive'/ident)==latest[ident],'saved generations retain all assigned derivatives in archive',ident=ident)
    h['gc_saved']()
    for ident in latest:
        check((base/'archive'/ident).exists()==(mode=='keep'),'archive policy honored after last generation removed',ident=ident,archive=mode)
        if mode=='keep':check(files(base/'archive'/ident)==latest[ident],'keep preserves exact bytes',ident=ident)
    check(Path('/home/alice/day-document.txt').read_bytes()==document,'user document survives program removal and GC')
    emit('case-result',archive=mode,outcome='1',scope='assigned Chromium and Vim homes; no inferred arbitrary ownership')
emit('SUMMARY',outcome='1',qualification='finite procedure; O1/O2/O7 general cases remain unresolved')
