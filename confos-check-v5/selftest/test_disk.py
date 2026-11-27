#!/usr/bin/env python3
"""Tests of the external package and disk readers on packages and disks made in the test."""
import base64, hashlib, io, json, lzma, os, shutil, stat, subprocess, sys, tarfile, tempfile, unittest
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import adapter_disk as AD
from core import derive

TOOL_DIRS=('/usr/sbin','/sbin','/usr/bin','/bin')
def tool(name):
    return shutil.which(name) or shutil.which(name,path=os.pathsep.join(TOOL_DIRS))
def sha(b): return hashlib.sha256(b).hexdigest()
def run(*argv,**kw):
    return subprocess.run([str(a) for a in argv],check=True,capture_output=True,**kw)

# ---------------------------------------------------------------- hand-made packages
RECIPE=b'name: demo\nversion: 1.0\nbuild:\ntrue\n'
SOURCE=b'source bytes'
GOOD=[('dir','usr',0o755),('dir','usr/bin',0o755),('file','usr/bin/tool',0o4755,b'tool\n'),
      ('hardlink','usr/bin/tool2','usr/bin/tool'),('link','usr/bin/t','tool'),
      ('dir','usr/lib',0o755),('file','usr/lib/data',0o644,b'abc')]

def passport_for(entries,name='demo',version='1.0'):
    lines=['confpkg 1','name '+name,'version '+version,'source demo.tar sha256 '+sha(SOURCE),
           'recipe demo.recipe sha256 '+sha(RECIPE),'built-with base-files-0.60 bash-5.3']
    for e in entries:
        if e[0]=='dir': lines.append(f'dir {e[1]} {e[2]:04o} 0:0')
        elif e[0]=='file': lines.append(f'file {e[1]} {e[2]:04o} 0:0 {len(e[3])} {sha(e[3])}')
        elif e[0]=='link': lines.append(f'link {e[1]} -> {e[2]}')
        elif e[0]=='hardlink': lines.append(f'hardlink {e[1]} -> {e[2]}')
    return '\n'.join(lines)+'\n'

def member(e,prefix='root/'):
    ti=tarfile.TarInfo(prefix+e[1] if prefix is not None else e[1]); ti.mtime=1767225600; data=None
    if e[0]=='dir': ti.type,ti.mode=tarfile.DIRTYPE,e[2]
    elif e[0]=='file': ti.type,ti.mode,ti.size,data=tarfile.REGTYPE,e[2],len(e[3]),e[3]
    elif e[0]=='link': ti.type,ti.mode,ti.linkname=tarfile.SYMTYPE,0o777,e[2]
    elif e[0]=='hardlink': ti.type,ti.mode,ti.linkname=tarfile.LNKTYPE,0o755,'root/'+e[2]
    elif e[0]=='fifo': ti.type,ti.mode=tarfile.FIFOTYPE,e[2]
    return ti,data

def write_pkg(path,passport,members,passport_first=True):
    with lzma.open(path,'wb') as xf, tarfile.open(fileobj=xf,mode='w',format=tarfile.GNU_FORMAT) as tf:
        pt=tarfile.TarInfo('passport'); pt.mtime=1767225600; pt.mode=0o644; data=passport.encode(); pt.size=len(data)
        if passport_first: tf.addfile(pt,io.BytesIO(data))
        for ti,d in members: tf.addfile(ti,io.BytesIO(d) if d is not None else None)
        if not passport_first: tf.addfile(pt,io.BytesIO(data))

class Passports(unittest.TestCase):
    def test_good(self):
        p=AD.parse_passport(passport_for(GOOD))
        self.assertEqual((p['name'],p['version']),('demo','1.0'))
        self.assertEqual(p['sources'],[('demo.tar',sha(SOURCE))])
        self.assertEqual(p['recipe'],('demo.recipe',sha(RECIPE)))
        self.assertEqual(p['built_with'],['base-files-0.60','bash-5.3'])
        by={o['id']:o for o in p['entries']}
        self.assertEqual(by['/usr/bin/tool'],{'kind':'file','id':'/usr/bin/tool',
            'value':{'mode':'4755','uid':0,'gid':0,'sha256':sha(b'tool\n')}})
        self.assertEqual(by['/usr/bin/t']['value'],{'target':'tool'})
        self.assertEqual(by['/usr/bin/tool2'],{'kind':'hardlink','id':'/usr/bin/tool2','value':{'target':'/usr/bin/tool'}})
        self.assertEqual(p['sizes']['/usr/lib/data'],3)
    def test_link_target_with_spaces_and_declaration_recipe(self):
        t=passport_for([]).replace('recipe demo.recipe sha256 '+sha(RECIPE),'recipe - sha256 -')
        t=t.replace('built-with base-files-0.60 bash-5.3','built-with ')+'link etc/x -> a b -> c\n'
        p=AD.parse_passport(t)
        self.assertIsNone(p['recipe']); self.assertEqual(p['built_with'],[])
        self.assertEqual(p['entries'][0]['value']['target'],'a b -> c')
    def test_rejections(self):
        good=passport_for(GOOD)
        bad={'unknown kind':good+'device dev/x 0600 0:0\n',
             'duplicate path':good+'dir usr 0755 0:0\n',
             'bad mode':good.replace('dir usr 0755','dir usr 755'),
             'bad owner':good.replace('dir usr 0755 0:0','dir usr 0755 root:0'),
             'bad sha':good.replace(sha(b'abc'),'ABC'),
             'extra field':good.replace('dir usr 0755 0:0','dir usr 0755 0:0 x'),
             'absolute path':good.replace('dir usr/bin','dir /usr/bin'),
             'dotdot path':good.replace('dir usr/lib','dir usr/../lib'),
             'missing name':good.replace('name demo\n',''),
             'duplicate version':good.replace('version 1.0\n','version 1.0\nversion 2\n'),
             'wrong format':good.replace('confpkg 1','confpkg 2'),
             'hardlink to nothing':good.replace('hardlink usr/bin/tool2 -> usr/bin/tool','hardlink usr/bin/tool2 -> usr/bin/none'),
             'no newline':good[:-1],
             'blank line':good+'\n',
             'malformed source':good.replace('source demo.tar sha256','source demo.tar md5')}
        for why,text in bad.items():
            with self.subTest(why):
                with self.assertRaises(ValueError): AD.parse_passport(text)

class Packages(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.d=Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()
    def pkg(self,name,passport,members,**kw):
        p=self.d/name; write_pkg(p,passport,members,**kw); return p
    def good(self):
        return self.pkg('demo-1.0.confpkg',passport_for(GOOD),[member(e) for e in GOOD])
    def test_good_hand_made(self):
        p=self.good(); r=AD.read_confpkg(p)
        self.assertEqual(r['archive_sha256'],sha(p.read_bytes()))
        self.assertEqual(r['passport_sha256'],sha(passport_for(GOOD).encode()))
        self.assertEqual([o['id'] for o in r['objects']],['/'+e[1] for e in GOOD])
    def assertRejected(self,path,fragment):
        with self.assertRaises(ValueError) as cm: AD.read_confpkg(path)
        self.assertIn(fragment,str(cm.exception))
    def test_removed_member(self):
        self.assertRejected(self.pkg('x.confpkg',passport_for(GOOD),[member(e) for e in GOOD[:-1]]),'missing from archive')
    def test_added_member(self):
        ms=[member(e) for e in GOOD]+[member(('file','usr/lib/extra',0o644,b'x'))]
        self.assertRejected(self.pkg('x.confpkg',passport_for(GOOD),ms),'not in passport')
    def test_changed_byte(self):
        ms=[member(e) for e in GOOD[:-1]]+[member(('file','usr/lib/data',0o644,b'abd'))]
        self.assertRejected(self.pkg('x.confpkg',passport_for(GOOD),ms),'sha256 differs')
    def test_changed_mode_and_owner(self):
        ms=[member(e) for e in GOOD[:-1]]+[member(('file','usr/lib/data',0o755,b'abc'))]
        self.assertRejected(self.pkg('x.confpkg',passport_for(GOOD),ms),'mode')
        ti,d=member(GOOD[-1]); ti.uid=1000
        self.assertRejected(self.pkg('y.confpkg',passport_for(GOOD),[member(e) for e in GOOD[:-1]]+[(ti,d)]),'uid')
    def test_absolute_member(self):
        ms=[member(e) for e in GOOD]+[member(('file','/root/usr/lib/abs',0o644,b'x'),prefix=None)]
        self.assertRejected(self.pkg('x.confpkg',passport_for(GOOD),ms),'absolute')
    def test_dotdot_member(self):
        ms=[member(e) for e in GOOD]+[member(('file','usr/../../etc/evil',0o644,b'x'))]
        self.assertRejected(self.pkg('x.confpkg',passport_for(GOOD),ms),'unsafe member name')
    def test_link_then_child(self):
        ents=[('dir','usr',0o755),('link','usr/lib','/etc'),('file','usr/lib/evil',0o644,b'x')]
        self.assertRejected(self.pkg('x.confpkg',passport_for(ents),[member(e) for e in ents]),'below non-directory')
    def test_fifo_claimed_as_file(self):
        ms=[member(e) for e in GOOD[:-1]]+[member(('fifo','usr/lib/data',0o644))]
        self.assertRejected(self.pkg('x.confpkg',passport_for(GOOD),ms),'FIFO')
    def test_passport_not_first_and_duplicate(self):
        self.assertRejected(self.pkg('x.confpkg',passport_for(GOOD),[member(e) for e in GOOD],passport_first=False),'first member')
        ms=[member(e) for e in GOOD]+[member(GOOD[-1])]
        self.assertRejected(self.pkg('y.confpkg',passport_for(GOOD),ms),'duplicate member')
    def test_member_outside_root(self):
        ms=[member(e) for e in GOOD]+[member(('file','etc/x',0o644,b'x'),prefix='')]
        self.assertRejected(self.pkg('x.confpkg',passport_for(GOOD),ms),'outside root/')
    def test_hardlink_target_mismatch(self):
        ms=[member(e) for e in GOOD if e[0]!='hardlink']+[member(('hardlink','usr/bin/tool2','usr/lib/data'))]
        self.assertRejected(self.pkg('x.confpkg',passport_for(GOOD),ms),'link target')
        later=[member(e) for e in GOOD[:3]]+[member(('hardlink','usr/bin/tool2','usr/lib/data'))]+[member(e) for e in GOOD[4:]]
        ents=GOOD[:3]+[('hardlink','usr/bin/tool2','usr/lib/data')]+GOOD[4:]
        self.assertRejected(self.pkg('y.confpkg',passport_for(ents),later),'names no earlier regular file')
    def test_not_xz(self):
        p=self.d/'x.confpkg'; p.write_bytes(b'not an archive')
        self.assertRejected(p,'unreadable archive')
    def test_store_reader(self):
        p=self.good(); rec=self.d/'recipes'; rec.mkdir(); (rec/'demo.recipe').write_bytes(RECIPE)
        line={'id':'pkg','kind':'package','name':'demo','version':'1.0','archive':p.name,
              'archive_sha256':sha(p.read_bytes()),'recipe_sha256':sha(RECIPE),
              'source_sha256':[['demo.tar',sha(SOURCE)]]}
        read=AD.store_package_reader(self.d,rec)
        objs=read(line)
        self.assertEqual(objs[-1],{'kind':'file','id':'/usr/lib/confpkg/demo.passport',
            'value':{'mode':'0644','uid':0,'gid':0,'sha256':sha(passport_for(GOOD).encode())}})
        self.assertEqual(read(dict(line,source_sha256=sha(SOURCE)))[:-1],objs[:-1])
        d=derive({'lines':[line]},read)
        self.assertEqual(d['errors'],[])
        self.assertIn(('file','/usr/lib/confpkg/demo.passport'),{(o['kind'],o['id']) for o in d['objects']})
        for why,bad in {'archive hash':dict(line,archive_sha256='0'*64),'version':dict(line,version='2.0'),
                        'recipe':dict(line,recipe_sha256='0'*64),'source':dict(line,source_sha256=[['demo.tar','0'*64]]),
                        'traversal':dict(line,archive='../'+p.name)}.items():
            with self.subTest(why):
                with self.assertRaises(ValueError): read(bad)
                self.assertEqual(len(derive({'lines':[bad]},read)['errors']),1)
        (rec/'demo.recipe').write_bytes(RECIPE+b'#changed\n')
        with self.assertRaises(ValueError): read(line)

class RealBuilder(unittest.TestCase):
    BUILDER=Path(os.environ.get('CONFPKG_TOOL',ROOT.parent/'build'/'tools'/'confpkg'))
    def test_built_with_real_tool(self):
        if not self.BUILDER.is_file(): self.skipTest('builder tool not present: '+str(self.BUILDER))
        with tempfile.TemporaryDirectory() as t:
            t=Path(t)
            for d in ('src','out','work','emptyroot'): (t/d).mkdir()
            (t/'tiny.recipe').write_text('name: tiny\nversion: 1.0\nbuild:\n'
                'mkdir -p $DEST/usr/bin $DEST/usr/share/tiny\nprintf "hi\\n" > $DEST/usr/bin/hello\n'
                'chmod 4755 $DEST/usr/bin/hello\nln $DEST/usr/bin/hello $DEST/usr/bin/hello2\n'
                'ln -s hello $DEST/usr/bin/hi\nprintf data > $DEST/usr/share/tiny/data\n')
            run(sys.executable,'-I',self.BUILDER,'build',t/'tiny.recipe','--sources',t/'src','--out',t/'out',
                '--work',t/'work','--root',t/'emptyroot')
            pkg=t/'out'/'tiny-1.0.confpkg'
            run(sys.executable,'-I',self.BUILDER,'verify',pkg)
            r=AD.read_confpkg(pkg)
            by={o['id']:o for o in r['objects']}
            uid,gid=os.getuid(),os.getgid()
            self.assertEqual(by['/usr/bin/hello']['value'],{'mode':'4755','uid':uid,'gid':gid,'sha256':sha(b'hi\n')})
            self.assertEqual(by['/usr/bin/hello2'],{'kind':'hardlink','id':'/usr/bin/hello2','value':{'target':'/usr/bin/hello'}})
            self.assertEqual(by['/usr/bin/hi']['value'],{'target':'hello'})
            self.assertEqual(r['passport']['built_with'],[])
            self.assertEqual(set(by),{'/usr','/usr/bin','/usr/bin/hello','/usr/bin/hello2','/usr/bin/hi',
                                      '/usr/share','/usr/share/tiny','/usr/share/tiny/data'})

# ---------------------------------------------------------------- synthetic disks
GPT_TABLE=('label: gpt\n'
    'start=2048, size=262144, type=C12A7328-F81F-11D2-BA4B-00A0C93EC93B, name=EFI\n'
    'start=264192, size=12582912, type=0FC63DAF-8483-4772-8E79-3D69D8477DE4, name=CONFOS-SYSTEM\n'
    'start=12847104, type=0FC63DAF-8483-4772-8E79-3D69D8477DE4, name=CONFOS-DATA\n')
DATA_SECTORS=131072
G1=sha(b'generation one'); G0=sha(b'generation zero')
NEEDED=('sfdisk','mke2fs','debugfs','e2fsck','mksquashfs','unsquashfs')

def missing_tools():
    return [n for n in NEEDED if not tool(n)]

def mk(base,rel,data=None,mode=0o644,link=None):
    p=Path(base)/rel; p.parent.mkdir(parents=True,exist_ok=True)
    if link is not None: os.symlink(link,p); return
    if data is None: p.mkdir(exist_ok=True); os.chmod(p,mode); return
    p.write_bytes(data); os.chmod(p,mode)

def debugfs_w(dev,commands):
    subprocess.run([tool('debugfs'),'-w','-f','-',dev],input=''.join(c+'\n' for c in commands).encode(),
                   check=True,capture_output=True)

def make_disk(tmp, layout=GPT_TABLE, extra_sectors=DATA_SECTORS+2048):
    """A ConfOS-shaped raw disk in tmp; returns (disk path, facts used by the assertions)."""
    tmp=Path(tmp); tmp.mkdir(parents=True,exist_ok=True); disk=tmp/'disk.raw'
    with open(disk,'wb') as f: f.truncate((12847104+extra_sectors)*512)
    subprocess.run([tool('sfdisk'),'-q','--no-reread','--no-tell-kernel',disk],input=layout.encode(),check=True,capture_output=True)
    # generation roots
    roots={}
    for gid,host in ((G1,'one'),(G0,'zero')):
        r=tmp/('root-'+host)
        for d,m in (('',0o755),('usr',0o755),('usr/bin',0o755),('usr/lib',0o755),('usr/lib/confpkg',0o755),
                    ('etc',0o755),('etc/confos',0o755),('etc/sudoers.d',0o750),('etc/dropbear',0o755),
                    ('etc/dropbear/authorized_keys',0o755),('home',0o755),('root',0o700),('data',0o755),
                    ('system',0o755),('dev',0o755)):
            mk(r,d,mode=m)
        mk(r,'etc/passwd',b'root:x:0:0::/root:/bin/bash\nuser:x:1000:1000::/home/user:/bin/bash\n')
        mk(r,'etc/group',b'root:x:0:\nuser:x:1000:\n'); mk(r,'etc/shadow',b'root:!:1::::::\n',0o600)
        mk(r,'etc/hostname',(host+'\n').encode()); mk(r,'etc/confos/identity',(gid+'\n').encode())
        mk(r,'etc/sudoers',b'root ALL=(ALL) ALL\n',0o440); mk(r,'etc/sudoers.d/user',b'user ALL=(ALL) ALL\n',0o440)
        mk(r,'etc/dropbear/authorized_keys/user',b'ssh-ed25519 AAAA test\n')
        mk(r,'etc/localtime',link='../usr/share/zoneinfo/Etc/UTC'); mk(r,'etc/a -> b',link='c')
        mk(r,'usr/bin/su',b'su program\n',0o755); mk(r,'usr/bin/a',b'shared\n',0o755); os.link(r/'usr/bin/a',r/'usr/bin/b')
        mk(r,'usr/lib/confpkg/demo.passport',b'confpkg 1\nname demo\n')
        mk(r,'usr/lib/confpkg/declaration.passport',b'confpkg 1\nname declaration\n')
        mk(r,'home/user/stale',b'hidden by the bind mount\n')
        sq=tmp/(host+'.sqfs')
        run(tool('mksquashfs'),r,sq,'-noappend','-all-root','-pseudo-override','-no-progress','-quiet','-no-xattrs',
            '-p','usr/bin/su m 4755 0 0','-p','etc/shadow m 640 0 42','-p','dev/null c 666 0 0 1 3')
        roots[gid]=(r,sq)
    s=tmp/'system'; mk(s,'',mode=0o755)
    mk(s,'boot.cfg',(f'linux /generations/{G1}/vmlinuz console=ttyS0 confos.generation={G1}\n'
                     f'initrd /generations/{G1}/initramfs\nboot\n').encode())
    for gid,(r,sq) in roots.items():
        mk(s,f'generations/{gid}/root.sqfs',sq.read_bytes())
        mk(s,f'generations/{gid}/vmlinuz',b'kernel '+gid.encode()); mk(s,f'generations/{gid}/initramfs',b'initramfs '+gid.encode())
        mk(s,f'generations/{gid}/declaration/declaration.conf',b'setting hostname x\n'+gid.encode())
        mk(s,f'generations/{gid}/declaration/inputs/keys.conf',b'keys\n')
    mk(s,'state/applied',(G1+'\n').encode())
    write_pkg(tmp/'demo-1.0.confpkg',passport_for(GOOD),[member(e) for e in GOOD])
    mk(s,'packages/demo-1.0.confpkg',(tmp/'demo-1.0.confpkg').read_bytes()); mk(s,'packages/notes.txt',b'n')
    for sub in ('recipes','files','tools'): mk(s,'tree/'+sub,mode=0o755)
    mk(s,'tree/recipes/demo.recipe',b'name: demo\n'); mk(s,'tree/tools/confpkg',b'#!/bin/sh\n',0o755)
    mk(s,'tree/files/base-files/etc/os-release',b'VERSION_ID="9.9"\n'); mk(s,'tree/BASE.md',b'outside the parts\n')
    mk(s,'trees/9.8/recipes/demo.recipe',b'name: demo 9.8\n')
    mk(s,'sources/a.tar',b'a'); mk(s,'sources/b.tar',b'b')
    d=tmp/'data'; mk(d,'',mode=0o755)
    mk(d,'confos',mode=0o700); mk(d,'confos/declaration.conf',b'package demo 1.0\n')
    mk(d,'confos/inputs/x.conf',b'old input\n'); mk(d,'confos/work/tmp.txt',b'scratch\n')
    mk(d,'home',mode=0o755); mk(d,'home/user',mode=0o750); mk(d,'home/user/file',b'personal\n',0o600)
    mk(d,'home/user/link',link='/etc/passwd'); os.mkfifo(d/'home/user/fifo',0o600)
    mk(d,'home/user/h1',b'linked\n'); os.link(d/'home/user/h1',d/'home/user/h2')
    mk(d,'home/user/suid',b'#!/bin/sh\n',0o755); mk(d,'root',mode=0o700); mk(d,'root/.profile',b'PS1=#\n')
    env=dict(os.environ,E2FSPROGS_FAKE_TIME='1767225600')
    for label,src,start,size in (('CONFOS-SYSTEM',s,264192,12582912),('CONFOS-DATA',d,12847104,DATA_SECTORS)):
        run(tool('mke2fs'),'-q','-F','-t','ext4','-L',label,'-d',src,'-E',
            f'offset={start*512},root_owner=0:0,lazy_itable_init=1,lazy_journal_init=1',disk,f'{size//2}k',env=env)
    sysdev=f'{disk}?offset={264192*512}'; datadev=f'{disk}?offset={12847104*512}'
    # owners: everything root, then the person's home
    paths=[]
    for top,dev in ((s,sysdev),(d,datadev)):
        cmds=[]
        for dp,dns,fns in os.walk(top):
            for n in dns+fns:
                rel='/'+os.path.relpath(os.path.join(dp,n),top)
                cmds+= [f'sif "{rel}" uid 0',f'sif "{rel}" gid 0']
                if top==d: paths.append(rel)
        debugfs_w(dev,cmds)
    debugfs_w(datadev,[f'sif /home/user/{n} {f} 1000' for n in ('','file','h1') for f in ('uid','gid')]
              +['sif /home/user/suid mode 0104755'])
    # a change that exists only in the journal of the data partition (a running guest after sync)
    bs=AD.ext_superblock(disk,12847104*512)['block_size']
    out=subprocess.run([tool('debugfs'),'-c','-R','bmap /confos/inputs/x.conf 0',datadev],capture_output=True,check=True)
    block=int(out.stdout.split()[-1]); new=b'new input\n'
    (tmp/'blk').write_bytes(new.ljust(bs,b'\0'))
    debugfs_w(datadev,['jo',f'jw -b {block} {tmp/"blk"}','jc'])
    return disk,{'roots':roots,'data_paths':paths,'journal_content':new}

@unittest.skipIf(missing_tools(),'host tools missing: '+' '.join(missing_tools()))
class Disk(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(); cls.t=Path(cls.tmp.name)
        cls.disk,cls.facts=make_disk(cls.t/'build')
        os.chmod(cls.disk,0o444)
        cls.before=os.stat(cls.disk)
        cls.work=cls.t/'work'
        cls.info=AD.read_disk(str(cls.disk),str(cls.work))
        cls.after=os.stat(cls.disk)
    @classmethod
    def tearDownClass(cls):
        os.chmod(cls.disk,0o644); cls.tmp.cleanup()
    def test_gpt(self):
        parts=AD.gpt_partitions(self.disk)
        self.assertEqual([(p['number'],p['first_lba'],p['last_lba']) for p in parts][:2],
                         [(1,2048,264191),(2,264192,12847103)])
        self.assertEqual(parts[2]['first_lba'],12847104); self.assertEqual(parts[1]['name'],'CONFOS-SYSTEM')
        self.assertEqual(parts[0]['type_guid'],'C12A7328-F81F-11D2-BA4B-00A0C93EC93B')
        self.assertEqual(AD.check_layout(parts),[])
    def test_gpt_crc(self):
        bad=self.t/'bad.raw'
        with open(self.disk,'rb') as f: head=f.read(64*512)
        for off,why in ((512+40,'header CRC32'),(2*512+60,'entry array CRC32')):
            b=bytearray(head); b[off]^=1; bad.write_bytes(bytes(b))
            with self.assertRaises(ValueError) as cm: AD.gpt_partitions(bad)
            self.assertIn(why,str(cm.exception))
        b=bytearray(head); b[512:520]=b'NOT PART'; bad.write_bytes(bytes(b))
        with self.assertRaises(ValueError): AD.gpt_partitions(bad)
    def test_raw_disk_untouched_and_work_cleaned(self):
        self.assertEqual((self.before.st_size,self.before.st_mtime_ns),(self.after.st_size,self.after.st_mtime_ns))
        self.assertTrue(AD.ext_superblock(self.disk,12847104*512)['needs_recovery'])
        self.assertEqual(list(self.work.iterdir()),[])
    def test_no_errors(self):
        self.assertEqual(self.info['errors'],[])
        for g in self.info['generations'].values(): self.assertEqual(g['root']['errors'],[])
        self.assertEqual(self.info['data']['errors'],[])
    def test_system_partition(self):
        i=self.info
        self.assertEqual(i['selected'],G1); self.assertEqual(i['state_applied'],G1+'\n')
        self.assertEqual(set(i['generations']),{G1,G0})
        g=i['generations'][G1]
        self.assertEqual(g['declaration_files'],{'declaration.conf':sha(b'setting hostname x\n'+G1.encode()),'inputs/keys.conf':sha(b'keys\n')})
        self.assertEqual(g['declaration_text']['inputs/keys.conf'],'keys\n')
        self.assertEqual(g['kernel_sha256'],sha(b'kernel '+G1.encode())); self.assertEqual(g['initramfs_sha256'],sha(b'initramfs '+G1.encode()))
        self.assertEqual(g['root_sqfs_sha256'],sha(self.facts['roots'][G1][1].read_bytes()))
        st=i['system_store']
        self.assertEqual(st['packages'],{'demo-1.0.confpkg':sha((self.t/'build'/'demo-1.0.confpkg').read_bytes())})
        self.assertTrue(st['tree_present']); self.assertEqual(st['sources_count'],2)
        self.assertEqual(st['other_entries'],[{'path':'/packages/notes.txt'}])
    def test_root_objects(self):
        g=self.info['generations'][G1]; by={o['id']:o for o in g['root']['objects']}
        r=self.facts['roots'][G1][0]
        want=set()
        for dp,dns,fns in os.walk(r):
            for n in dns+fns: want.add('/'+os.path.relpath(os.path.join(dp,n),r))
        self.assertEqual(set(by),want|{'/dev/null'})
        self.assertEqual(by['/usr/bin/su']['value'],{'mode':'4755','uid':0,'gid':0,'sha256':sha(b'su program\n')})
        self.assertEqual(by['/etc/shadow']['value']['mode'],'0640'); self.assertEqual(by['/etc/shadow']['value']['gid'],42)
        self.assertEqual(by['/dev/null'],{'kind':'special','id':'/dev/null','value':{'mode':'0666','uid':0,'gid':0,'type':'char 1:3'}})
        self.assertEqual(by['/usr/bin/a']['kind'],'file')
        self.assertEqual((by['/usr/bin/b']['kind'],by['/usr/bin/b']['value']['target']),('hardlink','/usr/bin/a'))
        self.assertEqual(by['/etc/a -> b']['value']['target'],'c')
        self.assertEqual(by['/root']['value'],{'mode':'0700','uid':0,'gid':0})
        self.assertEqual(g['passports'],{'demo':'confpkg 1\nname demo\n','declaration':'confpkg 1\nname declaration\n'})
        self.assertEqual(g['texts']['/etc/hostname'],'one\n'); self.assertEqual(g['texts']['/etc/shadow'],'root:!:1::::::\n')
        self.assertEqual(set(g['texts']),{'/etc/passwd','/etc/group','/etc/shadow','/etc/hostname','/etc/confos/identity',
            '/etc/sudoers','/etc/sudoers.d/user','/etc/dropbear/authorized_keys/user'})
        self.assertEqual(g['links'],{'/etc/localtime':'../usr/share/zoneinfo/Etc/UTC'})
    def test_data_partition_and_journal(self):
        d=self.info['data']; by={o['id']:o for o in d['objects']}
        self.assertEqual(set(by),{'/data','/data/lost+found'}|{'/data'+p for p in self.facts['data_paths']})
        self.assertEqual(by['/data/home/user']['value'],{'mode':'0750','uid':1000,'gid':1000})
        self.assertEqual(by['/data/home/user/file']['value'],{'mode':'0600','uid':1000,'gid':1000,'sha256':sha(b'personal\n')})
        self.assertEqual(by['/data/home/user/suid']['value']['mode'],'4755')
        self.assertEqual(by['/data/home/user/link'],{'kind':'symlink','id':'/data/home/user/link','value':{'mode':'0777','uid':0,'gid':0,'target':'/etc/passwd'}})
        self.assertEqual(by['/data/home/user/fifo']['value'],{'mode':'0600','uid':0,'gid':0,'type':'fifo'})
        self.assertEqual((by['/data/home/user/h2']['kind'],by['/data/home/user/h2']['value']['target']),('hardlink','/data/home/user/h1'))
        new=self.facts['journal_content']
        self.assertEqual(by['/data/confos/inputs/x.conf']['value']['sha256'],sha(new))
        p3=self.info['evidence']['p3']
        self.assertTrue(p3['needs_recovery']); self.assertTrue(p3['journal_replayed']); self.assertEqual(p3['access'],'sparse copy')
        self.assertIn(p3['e2fsck_returncode'],(0,1))
        self.assertEqual(self.info['evidence']['p2']['access'],'offset')
        self.assertEqual(self.info['data']['candidate_encoding'],'base64')
        self.assertEqual({k:base64.b64decode(v) for k,v in d['candidate'].items()},
                         {'declaration.conf':b'package demo 1.0\n','inputs/x.conf':new})
    def test_copy_path_reads_identically(self):
        other=AD.read_disk(str(self.disk),str(self.t/'work2'),copy_system=True)
        self.assertEqual(other['evidence']['p2']['access'],'sparse copy')
        self.assertFalse(other['evidence']['p2']['needs_recovery'])
        for k in ('boot_cfg','selected','state_applied','generations','system_store','data','errors'):
            self.assertEqual(other[k],self.info[k],k)
    def test_inventory(self):
        inv=AD.inventory_from_disk(self.info); by={(o['kind'],o['id']):o for o in inv['objects']}
        self.assertEqual(inv['errors'],[]); self.assertEqual(inv['coverage']['stored']['status'],'complete')
        self.assertTrue(inv['coverage']['stored']['evidence'])
        # partition 3 keeps raw ids; the image keeps its own (the caller maps bind mounts)
        self.assertEqual(by[('file','/data/home/user/file')]['value']['uid'],1000)
        self.assertNotIn(('file','/home/user/file'),by)
        self.assertIn(('file','/data/root/.profile'),by); self.assertIn(('file','/data/confos/declaration.conf'),by)
        self.assertIn(('dir','/data/lost+found'),by)
        self.assertEqual(by[('hardlink','/data/home/user/h2')]['value']['target'],'/data/home/user/h1')
        self.assertEqual(by[('file','/home/user/stale')]['value']['sha256'],sha(b'hidden by the bind mount\n'))
        self.assertEqual(by[('dir','/home')]['value'],{'mode':'0755','uid':0,'gid':0})
        self.assertEqual(by[('dir','/data')]['value'],{'mode':'0755','uid':0,'gid':0})
        for mount in ('/data','/system'):
            self.assertEqual(by[('partition-root',mount)]['classification'],'mount-point')
        self.assertIn(('file','/usr/bin/su'),by)
        gen=by[('generation',G0)]
        self.assertEqual((gen['classification'],gen['question']),('inactive-generation','Q-GENERATION'))
        self.assertEqual(gen['value']['declaration_files'],self.info['generations'][G0]['declaration_files'])
        self.assertNotIn(('generation',G1),by)
        arc=by[('system-archive','/system/packages/demo-1.0.confpkg')]
        self.assertEqual((arc['classification'],arc['question']),('system-store','Q-GENERATION'))
        self.assertEqual((arc['value']['name'],arc['value']['version']),('demo','1.0'))
        self.assertEqual(arc['value']['sources'],[['demo.tar',sha(SOURCE)]])
        t=by[('release-tree','9.9')]['value']
        self.assertEqual((t['path'],t['files'],t['outside_parts']),('/system/tree',3,1))
        self.assertEqual(by[('release-tree','9.8')]['value']['path'],'/system/trees/9.8')
        self.assertEqual(by[('release-source','a.tar')]['value']['sha256'],sha(b'a'))
        self.assertEqual(by[('system-store','/system/state/applied')]['value']['identity'],G1)
        self.assertEqual(by[('system-store','/system/generations/'+G1)]['value']['identity'],G1)
        self.assertTrue(by[('system-store','/system/packages/notes.txt')]['value']['unexpected'])
        self.assertEqual(len(inv['objects']),len(by))
    def test_inventory_marks_problems(self):
        info=json.loads(json.dumps(self.info)); info['selected']='0'*64
        inv=AD.inventory_from_disk(info)
        self.assertEqual(inv['coverage']['stored']['status'],'incomplete')

@unittest.skipIf(missing_tools(),'host tools missing: '+' '.join(missing_tools()))
class OtherLayouts(unittest.TestCase):
    def test_layout_disagreement_is_an_error_not_an_exception(self):
        with tempfile.TemporaryDirectory() as t:
            disk=Path(t)/'small.raw'
            with open(disk,'wb') as f: f.truncate(16<<20)
            subprocess.run([tool('sfdisk'),'-q','--no-reread','--no-tell-kernel',disk],check=True,capture_output=True,
                input=b'label: gpt\nstart=2048, size=4096, name=A\nstart=6144, size=8192, name=B\nstart=14336, name=C\n')
            run(tool('mke2fs'),'-q','-F','-t','ext4','-L','WRONG','-E','offset=%d'%(6144*512),disk,'4096k')
            errs=AD.check_layout(AD.gpt_partitions(disk))
            self.assertTrue(any('partition 2 starts at sector 6144' in e for e in errs))
            info=AD.read_disk(str(disk),str(Path(t)/'work'))
            reasons=' | '.join(e['reason'] for e in info['errors'])
            self.assertIn('partition 1 ends at sector 6143',reasons)
            self.assertIn("label 'WRONG'",reasons); self.assertIn('partition 3: no ext4 superblock',reasons)
            self.assertIn('boot.cfg missing',reasons)
            self.assertEqual(AD.inventory_from_disk(info)['coverage']['stored']['status'],'incomplete')
            self.assertEqual(list((Path(t)/'work').iterdir()),[])
    def test_not_a_gpt(self):
        with tempfile.TemporaryDirectory() as t:
            disk=Path(t)/'zero.raw'; disk.write_bytes(bytes(8192))
            info=AD.read_disk(str(disk),str(Path(t)/'work'))
            self.assertIn('EFI PART',info['errors'][0]['reason'])

if __name__=='__main__': unittest.main(verbosity=2)
