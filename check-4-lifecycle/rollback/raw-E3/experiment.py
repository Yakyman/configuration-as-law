#!/usr/bin/env python3
import contextlib, hashlib, http.server, json, os, pathlib, shutil, sqlite3, subprocess, tarfile, threading, time, urllib.request, urllib.error, xml.etree.ElementTree as ET
P=pathlib.Path('/root/E3'); R=P/'raw'; W=P/'work'; A=P/'apps'
R.mkdir(exist_ok=True); W.mkdir(exist_ok=True)
EVENTS=R/'events.jsonl'
def event(label, **kw):
    obj={'time':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'label':label,**kw}
    with EVENTS.open('a') as f: f.write(json.dumps(obj,sort_keys=True)+'\n')
    print(json.dumps(obj,sort_keys=True),flush=True)
def command(label,args,**kw):
    p=subprocess.run([str(x) for x in args],capture_output=True,text=True,**kw)
    event(label,argv=[str(x) for x in args],returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
    return p

def api(label, url, data=None, method=None, headers=None, timeout=20):
    body=None if data is None else json.dumps(data).encode()
    req=urllib.request.Request(url,body,{'Content-Type':'application/json',**(headers or {})},method=method)
    try:
        with urllib.request.urlopen(req,timeout=timeout) as res:
            status=res.status; raw=res.read().decode()
    except urllib.error.HTTPError as e: status=e.code; raw=e.read().decode()
    try: result=json.loads(raw)
    except ValueError: result=raw
    event(label,url=url,method=req.get_method(),request=data,status=status,response=result)
    return status,result

def manifest(folder):
    rows=[]
    for f in sorted(folder.rglob('*')):
        if f.is_file():
            rows.append({'path':str(f.relative_to(folder)),'size':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
    return rows

def inspect(label,folder,kind):
    out={'path':str(folder),'files':manifest(folder)}
    if kind=='firefox':
        out['compatibility.ini']=(folder/'compatibility.ini').read_text() if (folder/'compatibility.ini').exists() else None
        out['sqlite']={}
        for f in sorted(folder.rglob('*.sqlite')):
            try:
                con=sqlite3.connect('file:'+str(f)+'?mode=ro',uri=True)
                info={'user_version':con.execute('pragma user_version').fetchone()[0], 'integrity_check':con.execute('pragma integrity_check').fetchall(), 'schema':con.execute("select type,name,sql from sqlite_master order by type,name").fetchall()}
                if f.name=='cookies.sqlite': info['markers']=con.execute("select host,name,value from moz_cookies where host='127.0.0.1' order by name").fetchall()
                if f.name=='places.sqlite': info['markers']=con.execute("select url,title,visit_count from moz_places where url like 'http://127.0.0.1:%' order by url").fetchall()
                con.close(); out['sqlite'][str(f.relative_to(folder))]=info
            except Exception as e: out['sqlite'][str(f.relative_to(folder))]={'error':repr(e)}
    else:
        for f in folder.glob('config.xml*'):
            try: out[f.name]={'version':ET.parse(f).getroot().get('version'),'text':f.read_text()}
            except Exception as e: out[f.name]={'error':repr(e)}
    target=R/(label+'-inspection.json'); target.write_text(json.dumps(out,indent=2,sort_keys=True))
    event(label+'-inspection',file=target.name,file_count=len(out['files']),kind=kind)
    return out

def snapshot(label,folder,kind):
    inspect(label,folder,kind)
    snap=W/(label+'-snapshot'); shutil.copytree(folder,snap,symlinks=True)
    with tarfile.open(R/(label+'-state.tar.gz'),'w:gz') as tar: tar.add(folder,arcname=label)
    event(label+'-snapshot',source=str(folder),snapshot=str(snap),archive=label+'-state.tar.gz')
    return snap

def clone(source,label):
    dest=W/label; shutil.copytree(source,dest,symlinks=True); return dest

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        event('fixture-request',path=self.path)
        body=b'<!doctype html><title>E3 local state fixture</title><p>Local state fixture</p>'
        self.send_response(200);self.send_header('Content-Type','text/html');self.end_headers();self.wfile.write(body)
    def log_message(self,*args): pass

class Firefox:
    def __init__(self):
        self.log=(R/'geckodriver.log').open('w')
        self.proc=subprocess.Popen([str(A/'geckodriver'),'--port','4444','--log','debug'],stdout=self.log,stderr=subprocess.STDOUT)
        for _ in range(60):
            try:
                urllib.request.urlopen('http://127.0.0.1:4444/status',timeout=1).read();break
            except Exception: time.sleep(.2)
        self.session=None
    def call(self,label,path,data=None,method=None,timeout=30):
        return api(label,'http://127.0.0.1:4444'+path,data,method,timeout=timeout)
    def run(self,label,version,profile,add=None):
        status,res=self.call(label+'-start','/session',{'capabilities':{'alwaysMatch':{'browserName':'firefox','moz:firefoxOptions':{'binary':str(A/('firefox-'+version)/'firefox'),'args':['-headless','-profile',str(profile)]}}}},timeout=70)
        if status!=200:
            event(label+'-result',works=False,reason='session start refused or failed');return False
        self.session=res['value']['sessionId']; base='/session/'+self.session
        pid=res['value']['capabilities'].get('moz:processID')
        if pid:
            event(label+'-process',pid=pid,cmdline=pathlib.Path('/proc',str(pid),'cmdline').read_bytes().replace(b'\0',b' ').decode())
        self.call(label+'-navigate',base+'/url',{'url':'http://127.0.0.1:18080/'+label})
        script="return {cookie:document.cookie,storage:Object.fromEntries(Object.entries(localStorage))}"
        self.call(label+'-read-before',base+'/execute/sync',{'script':script,'args':[]})
        if add:
            key,value=add
            self.call(label+'-write',base+'/execute/sync',{'script':"localStorage.setItem(arguments[0],arguments[1]);document.cookie=arguments[0]+'='+arguments[1]+'; path=/; max-age=31536000';return true",'args':[key,value]})
        self.call(label+'-read-after',base+'/execute/sync',{'script':script,'args':[]})
        self.call(label+'-stop',base,method='DELETE')
        self.session=None
        event(label+'-result',works=True)
        return True
    def close(self):
        if self.session:
            with contextlib.suppress(Exception): self.call('firefox-final-stop','/session/'+self.session,method='DELETE')
        self.proc.terminate();self.proc.wait(timeout=10);self.log.close()

def firefox():
    profile=W/'firefox-active';profile.mkdir()
    prefs={'app.update.auto':False,'app.update.enabled':False,'datareporting.policy.dataSubmissionEnabled':False,'toolkit.telemetry.enabled':False,'browser.shell.checkDefaultBrowser':False,'browser.startup.homepage_override.mstone':'ignore','browser.aboutwelcome.enabled':False,'network.captive-portal-service.enabled':False,'network.connectivity-service.enabled':False}
    (profile/'user.js').write_text('\n'.join('user_pref('+json.dumps(k)+','+json.dumps(v)+');' for k,v in prefs.items()))
    httpd=http.server.ThreadingHTTPServer(('127.0.0.1',18080),Handler)
    threading.Thread(target=httpd.serve_forever,daemon=True).start()
    ff=Firefox()
    try:
        assert ff.run('ff-old','115.0esr',profile,('before','v115'))
        old=snapshot('ff-old',profile,'firefox')
        assert ff.run('ff-upgrade','128.0esr',profile,('after','v128'))
        new=snapshot('ff-new',profile,'firefox')
        # Direct launch excludes any WebDriver-specific suppression of downgrade protection.
        branch=clone(new,'ff-rollback-latest')
        binary=A/'firefox-115.0esr/firefox'
        args=[str(binary),'--headless','--no-remote','--profile',str(branch),'--screenshot',str(W/'ff-rollback.png'),'http://127.0.0.1:18080/ff-rollback-direct']
        start=time.monotonic()
        try:
            p=command('ff-rollback-latest',args,timeout=25)
            event('ff-rollback-latest-duration',seconds=round(time.monotonic()-start,3),screenshot_exists=(W/'ff-rollback.png').exists())
        except subprocess.TimeoutExpired as e:
            event('ff-rollback-latest',argv=args,timeout_seconds=25,stdout=(e.stdout or b'').decode(),stderr=(e.stderr or b'').decode())
        inspect('ff-after-refusal',branch,'firefox')
        assert ff.run('ff-new-after-refusal','128.0esr',branch)
        inspect('ff-recovery',branch,'firefox')
        restored=clone(old,'ff-rollback-snapshot')
        assert ff.run('ff-old-snapshot','115.0esr',restored)
        inspect('ff-restored',restored,'firefox')
    finally:
        ff.close();httpd.shutdown();httpd.server_close()

class Sync:
    def __init__(self): self.proc=None; self.log=None
    def start(self,label,version,state):
        self.label=label; self.log=(R/(label+'.log')).open('w')
        args=[str(A/('syncthing-'+version)/'syncthing'),'serve','--home='+str(state),'--no-browser','--no-restart','--no-upgrade','--gui-address=http://127.0.0.1:8384','--gui-apikey=e3-local-test-key']
        self.proc=subprocess.Popen(args,stdout=self.log,stderr=subprocess.STDOUT)
        event(label+'-start',argv=args,pid=self.proc.pid)
        for _ in range(100):
            if self.proc.poll() is not None:
                event(label+'-exit',returncode=self.proc.returncode);self.log.close();self.proc=None;return False
            try:
                req=urllib.request.Request('http://127.0.0.1:8384/rest/system/ping',headers={'X-API-Key':'e3-local-test-key'})
                urllib.request.urlopen(req,timeout=.5).read()
                self.request(label+'-version','/rest/system/version');return True
            except Exception: time.sleep(.2)
        event(label+'-timeout',seconds=20);self.stop();return False
    def request(self,label,path,data=None,method=None):
        return api(label,'http://127.0.0.1:8384'+path,data,method,{'X-API-Key':'e3-local-test-key'})
    def scan(self,label,count):
        self.request(label+'-scan','/rest/db/scan?folder=default',{},'POST')
        result=None
        for _ in range(100):
            req=urllib.request.Request('http://127.0.0.1:8384/rest/db/status?folder=default',headers={'X-API-Key':'e3-local-test-key'})
            result=json.loads(urllib.request.urlopen(req,timeout=2).read())
            if result.get('state')=='idle' and result.get('localFiles')==count:break
            time.sleep(.2)
        event(label+'-status',response=result,expected_files=count)
        assert result.get('state')=='idle' and result.get('localFiles')==count
        self.request(label+'-file-before','/rest/db/file?folder=default&file=before.txt')
        if count==2:self.request(label+'-file-after','/rest/db/file?folder=default&file=after.txt')
    def stop(self):
        if self.proc:
            with contextlib.suppress(Exception):self.request(self.label+'-shutdown','/rest/system/shutdown',{},'POST')
            try:self.proc.wait(timeout=15)
            except subprocess.TimeoutExpired:self.proc.terminate();self.proc.wait(timeout=5)
            event(self.label+'-exit',returncode=self.proc.returncode)
            self.proc=None;self.log.close()

def syncthing():
    state=W/'sync-active';files=W/'sync-files';files.mkdir()
    (files/'before.txt').write_text('Created before upgrade.\n')
    result=command('st-generate',[A/'syncthing-1.18.6/syncthing','generate','--home='+str(state)])
    assert result.returncode==0
    cfg=state/'config.xml'; tree=ET.parse(cfg);root=tree.getroot()
    folder=root.find('folder'); assert folder is not None
    folder.set('path',str(files));folder.set('rescanIntervalS','3600')
    opts=root.find('options')
    for key in ['globalAnnounceEnabled','localAnnounceEnabled','relaysEnabled','natEnabled','crashReportingEnabled']:
        e=opts.find(key)
        if e is not None:e.text='false'
    for key,value in [('listenAddress','tcp://127.0.0.1:22001'),('urAccepted','-1'),('autoUpgradeIntervalH','0')]:
        e=opts.find(key)
        if e is not None:e.text=value
    tree.write(cfg,encoding='utf-8',xml_declaration=True)
    shutil.copy2(cfg,R/'st-initial-config.xml')
    sync=Sync()
    try:
        assert sync.start('st-old','1.18.6',state);sync.scan('st-old',1);sync.stop()
        old=snapshot('st-old',state,'syncthing')
        assert sync.start('st-upgrade','1.27.0',state)
        sync.scan('st-upgrade-before-use',1)
        (files/'after.txt').write_text('Created after upgrade.\n')
        sync.scan('st-upgrade-after-use',2);sync.stop()
        new=snapshot('st-new',state,'syncthing')
        branch=clone(new,'st-rollback-latest')
        works=sync.start('st-rollback-latest','1.18.6',branch)
        if works: sync.scan('st-rollback-latest',2);sync.stop()
        event('st-rollback-latest-result',works=works)
        inspect('st-after-refusal',branch,'syncthing')
        assert sync.start('st-new-after-refusal','1.27.0',branch);sync.scan('st-new-after-refusal',2);sync.stop()
        inspect('st-recovery',branch,'syncthing')
        # Old state includes index/config only. User files remain current and should be re-scanned.
        restored=clone(old,'st-rollback-snapshot')
        assert sync.start('st-old-snapshot','1.18.6',restored);sync.scan('st-old-snapshot',2);sync.stop()
        inspect('st-restored',restored,'syncthing')
        # Test the exact archived pre-migration config supplied by Syncthing, with current index.
        archived=clone(new,'st-rollback-archived-config')
        saved=archived/'config.xml.v35'
        if saved.exists():
            shutil.copy2(saved,archived/'config.xml')
            works=sync.start('st-old-archived-config','1.18.6',archived)
            if works:sync.scan('st-old-archived-config',2);sync.stop()
            event('st-old-archived-config-result',works=works)
            inspect('st-archived-config-result',archived,'syncthing')
        event('st-source-files',files=manifest(files))
    finally:sync.stop()

if __name__=='__main__':
    import sys,traceback
    for name in sys.argv[1:] or ['firefox','syncthing']:
        event('begin',program=name)
        try:globals()[name]();event('complete',program=name)
        except Exception as e:event('harness-error',program=name,error=repr(e),traceback=traceback.format_exc());raise
