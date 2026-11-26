"""Portable case plans. All platform-dependent operations go through adapter.py.

A request is an action/capture, never a verdict. Checks are executed by engine.py.
Tokens are release bindings (ASSUMPTIONS A11), never host-shell substitutions.
"""
import json
from pathlib import Path

CASES=[]

def ck(field,op,value): return {'field':field,'op':op,'value':value}
def ref(name): return {'ref':name}
def step(op,name,checks=(),**args):
    return {'name':name,'request':dict(op=op,**args),'checks':list(checks)}
def cmd(name,command,role='user',required=True,stdout=None):
    checks=[ck('returncode','eq',0)] if required else []
    if stdout is not None: checks.append(ck('stdout','match',stdout))
    return step('command',name,checks,role=role,command=command)
def query(name,subject,field='value',op='eq',value=True,**args):
    return step('query',name,[ck(field,op,value)],subject=subject,**args)
def edit(name,action,line): return step('edit',name,[ck('returncode','eq',0)],action=action,line=line)
def apply(name):
    return [step('read-law',name+'-candidate',scope='candidate'),
            step('apply',name,[ck('status','eq',ref(name+'-candidate.expected_status'))]),
            step('read-law',name+'-law',[ck('sha256','eq',ref(name+'-candidate.sha256'))],scope='committed')]
def fresh(): return [step('fresh','fresh',[ck('returncode','eq',0)],declaration='D-test')]
def checkpoint(name,after_apply=False):
    return [step('read-law',name+'-law',scope='committed'),
            dict(step('inventory',name,scope='all-stored-and-live'),compare_to=ref(name+'-law.declaration'),
                 companion_parts=['P1','UND']+(['P2'] if after_apply else []))]
def case(cid,labels,purpose,steps,kind='system',**meta):
    CASES.append(dict(id=cid,statements=labels.split(),purpose=purpose,kind=kind,steps=steps,**meta))
def attempt_case(cid,labels,purpose,command,variants=(),role='user',setup=None,subject='marker'):
    steps=fresh()+(setup or [])
    steps += [query('control', 'positive-control', value=True, program=cid),
              query('tool-present','command-present',value=True,command=command),
              query('before',subject,value=False),cmd('attempt',command,role,False),
              query('after',subject,value=False)]
    steps+=checkpoint('final')
    case(cid,labels,purpose,steps,variants=list(variants))

case('P1-0','C0 D K1 K2 W2a W2b W3e','Inventory the complete clean machine, including base and all stored generations.',fresh()+checkpoint('clean'))
case('UND-0','K2 W3a W3b W3c','Derive without a disk or guest transport; only declared source/package inputs.',
     [step('derive-inputs','derive',[ck('machine_reads','eq',[]),ck('errors','eq',[])],declaration='D-test')])
case('G-SHELL','Q4','Typed ordinary shell command works.',fresh()+[cmd('shell',"@SH@ -c 'printf shell-ok'",stdout='^shell-ok$')]+checkpoint('final'))

attempt_case('G-INSTALL','K1 K4 W2a Q2','User/root tool installation, direct package import, extraction, removal, purge, hold and hooks.',
             '@PKG_INSTALL@ case-small-2.confpkg', ['user install','root install','direct native executable path','file import','remove recorded package','forced purge','extract then run','hold recorded version','installer hook'],subject='unrecorded-installation')
attempt_case('G-BRING','K1 W2a W4b Q2 Q3','Bring an absent installer/runtime as data, then try direct and extracted launch.',
             '@FETCH@ @PAYLOAD_URL@ @HOME@/brought && chmod +x @HOME@/brought && @HOME@/brought',
             ['plain executable','archive extract','self-extracting wrapper','interpreter','container engine','user/root'])
attempt_case('G-DOWNLOAD','K1 W2c Q3','Downloaded executable is data until an allowed line; test each storage route.',
             '@FETCH@ @PAYLOAD_URL@ @TARGET@/brought && chmod +x @TARGET@/brought && @TARGET@/brought',
             ['home','/tmp','/dev/shm','/var/tmp','archive extraction'],subject='payload-executed')
attempt_case('G-BUILD','K1 W2c W3b Q3','Compilation may create material; direct execution outside an opening is refused.',
             '@CC@ @HOME@/case-small.c -o @TARGET@/case-small && @TARGET@/case-small',
             ['home','/tmp','/dev/shm','recipe file','command expansion','make install'],
             setup=[step('put-material','source',source='payloads/case-small.c',target='@HOME@/case-small.c')])
attempt_case('G-SCRIPT','K1 W4b Q3','Every shipped interpreter and loader refuses an unrecorded file.',
             '@READER@ @TARGET@/case-input',
             ['shell filename','shell redirected file','shell source','shebang direct','every shipped interpreter','loader non-executable ELF','debugger rc','runtime nested reader','explicit plugin','temporary nested reader'],
             setup=[step('put-material','script',source='payloads/unrecorded.sh',target='@TARGET@/case-input')])
case('G-STDIN','W2c Q4','Typed pipeline reads material; no unrecorded persistent installation or setting may result.',
     fresh()+[step('put-material','script',source='payloads/typed-input.sh',target='@HOME@/case-input'),
              cmd('pipe','cat @HOME@/case-input | @SH@',stdout='typed-ok'),
              step('restart','restart',[ck('boot_id','ne',ref('fresh.boot_id'))])]+checkpoint('final'),
     variants=['cat file | shell','typed command substitution','saved stdin file is a direct route: G-SCRIPT'])
attempt_case('G-STARTUP','K1 W2b W4b Q3 Q7','Saved startup, hook, alias, automatic macro and login access do not take effect past the law.',
             '@STARTUP_ATTEMPT@', ['shell rc','login profile','logout','executable alias','hook directory','autostart','SSH rc','authorized key login','installer pre-invoke','editor rc','plugin directory','plugin setting','saved macro home','saved macro tmp','SSH ProxyCommand','SSH Match exec'],subject='startup-effect')
case('G-READER','K1 W2c Q3 Q4','Recorded personal file reader versus unrecorded reader; input execution follows Q4/R10, installation/configuration still forbidden.',
     fresh()+[edit('record','add',{'kind':'package','name':'case-probe','binding':'probe'} )]+apply('record-apply')+
     [step('put-material','script',source='payloads/typed-input.sh',target='@HOME@/case-input'),
      cmd('reader','case-probe read @HOME@/case-input',stdout='typed-ok'),
      step('put-material','persistent-script',source='payloads/persistent.sh',target='@HOME@/persistent-input'),
      cmd('reader-persistent','case-probe read @HOME@/persistent-input',required=False),
      step('restart','restart',[ck('boot_id','ne',ref('fresh.boot_id'))]),
      query('persistence','persistent-unrecorded-effect',value=False)]+checkpoint('final'))
case('G-UPDATER','K1 K4 W1c W2a Q2','Recorded downloader/installer fetches and attempts a child and a self-update; then explicit lines allow the intended child.',
     fresh()+[edit('record','add',{'kind':'package','name':'case-probe','binding':'probe'})]+apply('record-apply')+
     [cmd('attempt','case-probe fetch-install @PAYLOAD_URL@ @HOME@/.local/bin/case-child',required=False),
      query('unrecorded','unrecorded-installation',value=False),
      cmd('self-update','case-probe fetch-install @PROBE_V2_URL@ @PROBE_PATH@',required=False),
      query('old-version','package-version',value='1',package='case-probe')]+checkpoint('before-child')+
     [edit('child','add',{'kind':'package','name':'case-small','binding':'small-v2'})]+apply('child-apply')+
     [cmd('child-run','case-small',stdout='case-small 2')]+checkpoint('final',True),
     variants=['user local prefix','root global prefix','project directory','download cache then install','fetch-and-execute','self-update'])

SETTINGS={
 'ACCOUNT':('useradd -m case-user','account:case-user',['useradd','usermod groups','passwd','chpasswd','groupadd']),
 'RIGHTS':('@RIGHTS_TOOL@ @RIGHTS_INPUT@','access:case-rule',['rights editor','login key','direct root write is W5-BREAK']),
 'SERVICE':('@SERVICE_TOOL@ enable case-unrecorded','service:case-unrecorded',['user persistent','user transient','delayed timer','user crontab','root crontab','root service link','disable/mask recorded service','linger','at','service parameter','root crontab for another user']),
 'FIREWALL':('@FIREWALL_TOOL@ @RULE_INPUT@','firewall:case-rule',['add rule','remove recorded rule']),
 'NETWORK':('@NETWORK_TOOL@ @NETWORK_INPUT@','network:case-address',['temporary address','route']),
 'SAVED-NETWORK':('@SAVED_NETWORK_TOOL@ @NETWORK_INPUT@','saved-network:case-network',['create saved network']),
 'HOST':('hostname case-host','hostname:case-host',['set name']),
 'TIME':('@TIME_TOOL@ @TIME_INPUT@','time:case-timezone',['timezone']),
 'LOCALE':('@LOCALE_TOOL@ @LOCALE_INPUT@','locale:case-locale',['system locale']),
 'MODULE':('modprobe @TEST_MODULE@','module:case-module',['load module']),
 'SYSCTL':('sysctl -w net.ipv4.ip_forward=1','sysctl:forward',['kernel setting']),
 'MOUNT':('mount -t tmpfs case-tmp /mnt','mount:/mnt',['mount filesystem'])}
for name,(command,subject,variants) in SETTINGS.items():
    attempt_case('G-'+name,'K1 W2b W5a Q2','Built-in '+name.lower()+' mutation through actual tool, including root and absolute tool paths.',command,variants,role='root',subject=subject)

case('G-PIPE','K1 W2b Q4','Download/execute typed input; preserve before-reboot evidence and judge persistence after reboot.',
     fresh()+[cmd('pipeline','@FETCH_STDOUT@ @PERSISTENT_URL@ | @SH@',required=False),
              step('inventory','before-reboot',scope='all-stored-and-live'),
              step('restart','restart',[ck('boot_id','ne',ref('fresh.boot_id'))]),
              query('persistent','persistent-unrecorded-effect',value=False)]+checkpoint('final'),
     variants=['pipeline','process substitution if supported','typed string substitution'])
case('G-CONTAINER','K1 W2a Q5','An actual namespace/container child is inventoried as a host process; unrecorded image/child refuses, recorded child works.',
     fresh()+[query('runtime','capability',value=True,capability='container'),
              step('container','attempt',action='unrecorded-child',role='user'),query('absent','container-child',value=False),
              edit('record','add',{'kind':'container','binding':'case-child'})]+apply('record-apply')+
     [step('container','launch',action='recorded-child'),query('host-process','process-identity',value=True,scope='host-and-namespace')]+checkpoint('final'),question='Q-PRODUCT')

# Required folder line: three separate cases, plus boundary/removal checks.
OPEN={'kind':'open-folder','path':'@HOME@/opened','scope':'execute'}
for cid,inside,purpose in [('OPEN-IN',True,'Own saved script runs inside the opened folder.'),('OPEN-OUT',False,'Same script is refused outside the opened folder.')]:
    target='@HOME@/opened/script' if inside else '@HOME@/closed/script'
    steps=fresh()+[edit('open','add',OPEN)]+apply('open-apply')+[
        step('put-material','script',source='payloads/unrecorded.sh',target=target),
        query('positive-script','positive-control',value=True,program='same-script-inside-opened-folder',reset_marker=True),
        query('before-script','marker',value=False),
        cmd('script-attempt','@SH@ '+target,required=False),
        query('marker','marker',value=inside)]+checkpoint('final')
    case(cid,'K1 W4a Q1 Q3',purpose,steps)
case('OPEN-VISIBLE','K2 W1c W4a Q1','Candidate opening is not law until apply; committed externally read declaration visibly names exactly the folder.',
     fresh()+[step('read-law','old',scope='committed'),edit('open','add',OPEN),
              step('read-law','still-old',[ck('sha256','eq',ref('old.sha256'))],scope='committed')]+apply('open-apply')+
     [query('visible','opening-line',value=OPEN,scope='external-committed-declaration')]+checkpoint('final'))
case('OPEN-BOUNDARY','K1 K4 W4a Q1','No prefix-sibling or symlink-out escape; removal closes the opening after application.',
     fresh()+[edit('open','add',OPEN)]+apply('open-apply')+
     [step('put-material','links',source='boundary-fixture',target='@HOME@'),
      cmd('symlink-out','@SH@ @HOME@/opened/link-out',required=False),query('out','marker',value=False),
      cmd('prefix','@SH@ @HOME@/opened-sibling/script',required=False),query('prefix-refused','marker',value=False),
      edit('close','remove',OPEN)]+apply('close-apply')+[
      cmd('closed','@SH@ @HOME@/opened/script',required=False),query('closed-refused','marker',value=False)]+checkpoint('final'),question='Q-OPEN-BOUNDARY')

# All eight previously untested statement labels have an explicit case.
case('N-VERDICT','N','No percentage/degree substitutes for verdict 1/0/?; test report aggregation with controlled evidence.',[],kind='logic',fixture_rule='aggregate')
case('W4c-DEFAULT','W4c W4b','A permissive default is a failure even if a later prohibition closes it; preserve both observations.',
     fresh()+[step('put-material','script',source='payloads/unrecorded.sh',target='@HOME@/case-input'),
              cmd('default-attempt','@SH@ @HOME@/case-input',required=False),query('default','marker',value=False),
              step('edit','prohibition',action='add',line={'kind':'prohibition','binding':'optional-no-exec'}),
              step('apply','prohibit'),cmd('again','@SH@ @HOME@/case-input',required=False),query('closed','marker',value=False)]+checkpoint('final'),question='Q-LOGIC')
case('W1d-MULTI','W1d W1c','Split designated description across two files; change included file; compare joined law and unapplied candidate.',
     fresh()+[step('split-declaration','split',[ck('file_count','eq',2)],files=['main','programs'])]+apply('split-apply')+
     [query('equivalence','description-equivalent',value=True),
      step('edit','included-edit',file='programs',action='add',line={'kind':'package','name':'case-small','binding':'small-v2'}),
      query('not-yet','package-version',value='1',package='case-small')]+apply('include-apply')+checkpoint('final'),question='Q-OPTIONAL')
case('W3d-OPEN','K3 W3d W3e','Omitted UID/GID may differ; every explicitly named account field must match across order-reversed installations.',
     [step('two-clean-builds','builds',declaration='D-accounts-open',orders=[['a','b'],['b','a']]),
      query('explicit','named-account-fields-equal',value=True),query('source','same-declaration',value=True)],question='Q-OPTIONAL')
case('W3d-LATEST','W3d W3e','Mutable selector resolves two source versions; compare only named constraints, record both resolutions.',
     [step('two-clean-builds','builds',declaration='D-latest',source_states=['catalogue-v1','catalogue-v2']),
      query('named','named-fields-satisfied',value=True),query('resolutions','resolved-versions',value=['1','2'])],question='Q-OPTIONAL')
case('W5-BREAK','W5a W5b Q2','Separate disposable-guest raw root mutation from built-in installer use; retain event for independent review.',
     fresh()+[step('clone-disposable','clone',[ck('scope','eq','owned-guest')]),
              step('raw-root-write','breaking-candidate',path='/usr/local/bin/case-forced',source='payloads/unrecorded.sh'),
              query('event','forced-effect',value=True),step('review-event','review',[ck('decision','eq','breaking')],event=ref('breaking-candidate'))],question='Q-BREAK')
case('Q9-SOURCE','Q9 W3c W3e','Actual accounts follow a named external server; change server list, reproduce, and remove source line.',
     fresh()+[step('external-server','server',state='accounts-a'),edit('source','add',{'kind':'external-accounts','source':'@ACCOUNT_SOURCE@'})]+apply('source-apply')+
     [query('lookup-a','account-lookup',value='account-a'),step('external-server','change',state='accounts-b'),
      query('lookup-b','account-lookup',value='account-b'),step('fresh-from-law','reproduce'),
      query('again','account-lookup',value='account-b'),edit('remove','remove',{'kind':'external-accounts','source':'@ACCOUNT_SOURCE@'})]+apply('remove-apply')+
     [query('gone','external-accounts-active',value=False)]+checkpoint('final'),question='Q-OPTIONAL')
case('Q6-GUEST','Q6','Recorded VM program contains an unrecorded guest system without changing host installation/settings; outer test VM is not this case.',
     fresh()+[query('vm','capability',value=True,capability='in-guest-vm'),step('guest-system','guest',action='run-contained-system'),
              query('contained','guest-output',value='guest-ok'),query('host-change','unrecorded-host-effect',value=False)]+checkpoint('final'),question='Q-PRODUCT')
case('Q7-VALUES','W2c Q3 Q7','Ordinary theme/user-agent value is program data; executable/access value is a computer setting.',
     fresh()+[step('put-material','values',source='payloads/values.txt',target='@HOME@/case-values'),
              cmd('read-values','case-probe values @HOME@/case-values',stdout='theme=plain'),
              step('put-material','exec-value',source='payloads/unrecorded.sh',target='@HOME@/startup-value'),
              cmd('execute-value','@STARTUP_VALUE_ATTEMPT@',required=False),query('marker','marker',value=False)]+checkpoint('final'))
case('Q8-PORT','Q8','Process and listener attributable to recorded executable bytes, with no separate process/port lines.',
     fresh()+[cmd('listen','case-probe listen @TEST_PORT@ > @HOME@/listener.out 2>&1 &'),
              query('port','listening-owner',value='case-probe'),query('identity','namespace-executable-hash',value=True)]+checkpoint('final'))

# Terminal ordinary work. Updates bind to actual whole-system source locks.
case('OW-1','K1 W1b W2a','Install a source-built program by adding its line.',fresh()+[edit('install','add',{'kind':'package','name':'case-small','binding':'small-v2'})]+apply('install-apply')+[cmd('program','case-small',stdout='case-small 2')]+checkpoint('final',True))
for n in (2,3):
    case('OW-'+str(n),'K2 W1b W1c W2a W3b','System update '+str(n-1)+' followed by a restart.',
         (fresh()+[step('select-update-start','start',state='T0')] if n==2 else [step('resume-sequence','resume',[ck('previous_case','eq','OW-2')],sequence='system-updates')])+[step('read-boot','old'),
                  edit('update','replace',{'kind':'base','binding':'T'+str(n-1)})]+apply('update-apply')+
         [step('restart','restart',[ck('boot_id','ne',ref('old.boot_id'))]),query('sources','system-source-state',value='T'+str(n-1)),
          query('changed','system-components-changed',value=True)]+checkpoint('final',True),sequence='OW-2 then OW-3 on the same installation',question='Q-UPDATE')
case('OW-4','W2c','Fetch a plain document with the terminal source-fetch tool.',fresh()+[cmd('fetch','@FETCH@ @DOCUMENT_URL@ @HOME@/document'),cmd('read','cat @HOME@/document',stdout='case document')]+checkpoint('final'))
case('OW-5','W2c','Create, edit and read a plain text file.',fresh()+[cmd('edit',"printf 'first\\n' > @HOME@/document && sed 's/first/second/' @HOME@/document > @HOME@/new && mv @HOME@/new @HOME@/document"),cmd('read','cat @HOME@/document',stdout='^second\n$')]+checkpoint('final'))
case('OW-6','W2c Q4','Ordinary commands and the recorded own script.',fresh()+[cmd('commands','ls @HOME@ && cp /etc/hostname @HOME@/name && grep . @HOME@/name && sort @HOME@/name'),cmd('script','@HOME@/bin/cases-report.sh',stdout='cases-report ok')]+checkpoint('final'))
case('OW-7','W2c W3b Q1 Q4','Fetch, build, change and rebuild in the opened folder; run all three changed versions.',
     fresh()+[edit('open','add',OPEN)]+apply('open-apply')+[cmd('fetch','@FETCH@ @SOURCE_URL@ @HOME@/opened/case-small.c')]+
     sum(([cmd('build-'+str(i),'@CC@ -DCASE_VERSION='+str(i)+' @HOME@/opened/case-small.c -o @HOME@/opened/case-small'),
           cmd('run-'+str(i),'@HOME@/opened/case-small',stdout='case-small '+str(i)),
           cmd('edit-'+str(i),"printf '\\n/* edit "+str(i)+" */\\n' >> @HOME@/opened/case-small.c")] for i in (1,2,3)),[])+checkpoint('final'))
case('OW-8','K1 K4 W3b Q2','Recorded updater and child replace launcher/game; apply install/update/remove through lines.',
     fresh()+[edit('child','add',{'kind':'package','name':'case-small','binding':'small-v1'})]+apply('install')+
     [cmd('run','case-small',stdout='case-small 1'),edit('update-line','replace',{'kind':'package','name':'case-small','binding':'small-v2'})]+apply('update')+
     [cmd('updated','case-small',stdout='case-small 2')]+checkpoint('final'))
for cid in ('OW-9','P2-NET-1'):
    case(cid,'K2 W1c','Interrupt an installation after observed transfer starts; old law survives failure; restore and retry.',
         fresh()+[step('read-law','old',scope='committed'),edit('install','add',{'kind':'package','name':'case-small','binding':'slow-package'}),
                  step('start-apply','begin'),query('progress','download-bytes',op='gt',value=0),
                  step('network','down',state='down'),step('finish-apply','failed',[ck('returncode','ne',0)]),
                  step('read-law','unchanged',[ck('sha256','eq',ref('old.sha256'))],scope='committed')]+checkpoint('failed-state')+
         [step('network','up',state='up')]+apply('retry')+[cmd('program','case-small',stdout='case-small')]+checkpoint('final',True))
for cid,radio,physical in [('OW-10','wifi',True),('OW-11','bluetooth',True),('X-WIFI','wifi',False),('X-BT','bluetooth',False)]:
    case(cid,'K3 K4 W2b','Connect/pair, independently inspect stored/effective state, reproduce and remove; '+('physical laptop' if physical else 'simulated radio only')+'.',
         fresh()+[query('hardware','radio-kind',value='physical' if physical else 'simulated',radio=radio),
                  step('radio-request','request',radio=radio,action='connect' if radio=='wifi' else 'pair'),
                  step('record-radio-if-needed','line',radio=radio)]+apply('connect-apply')+
         [query('connected','radio-effective',value=True,radio=radio),query('stored','radio-stored',value=True,radio=radio)]+checkpoint('connected-state',True)+
         [step('fresh-from-law','reproduce'),query('reproduced','radio-effective',value=True,radio=radio),
          edit('remove','remove',{'kind':'radio','name':radio})]+apply('remove-apply')+
         [query('gone-live','radio-effective',value=False,radio=radio),query('gone-stored','radio-stored',value=False,radio=radio)]+checkpoint('removed',True),hardware=physical)

for change in ('ADD','CHG','REM'):
    for i in (1,2,3):
        cid=f'P2-{change}-{i}'
        case(cid,'K2 W1a W1b W1c W1e W3a','Power cut immediately after reported success: '+change.lower()+', repetition '+str(i)+'.',
             fresh()+[step('prepare-change','prepare',change=change,index=i,target={'ADD':['case-extra-a','case-extra-b','case-extra-service'],'CHG':['hostname','firewall-port','account-shell'],'REM':['case-small','test-firewall','test-user-timer']}[change][i-1]),
                      step('read-law','candidate',scope='candidate'),
                      step('apply-cut','cut',[ck('success','eq',ref('candidate.expected_status')),ck('cut_after_success','eq',True)],trigger='exact-success-status'),
                      step('boot','boot',[ck('boot_id','ne',ref('fresh.boot_id'))]),
                      step('read-law','durable',[ck('sha256','eq',ref('candidate.sha256'))],scope='committed')]+checkpoint('final',True))
for cid,thing in [('REM-1','program-and-process'),('REM-2','service-and-process'),('REM-3a','firewall-rule'),('REM-3b','rights-rule')]:
    case(cid,'K4 W3b W3e','Remove '+thing+' and every contribution not supplied by another line.',
         fresh()+[step('prepare-removal','prepare',thing=thing),query('present','removal-target-present',value=True),
                  step('inventory','before',scope='all-stored-and-live'),edit('remove','remove',{'kind':'test-target','name':thing})]+apply('remove-apply')+
         [query('absent','removal-target-present',value=False),query('contributions','remaining-unowned-contributions',value=[])]+checkpoint('final',True))
case('REM-4','K4 W3b W3e','Shared dependency remains with one owner; disappears after removing last owner.',
     fresh()+[step('prepare-shared','owners',owners=['case-owner-a','case-owner-b'],dependency='case-shared'),
              edit('remove-a','remove',{'kind':'package','name':'case-owner-a'})]+apply('remove-a-apply')+
     [query('shared-stays','package-present',value=True,package='case-shared')]+checkpoint('one-owner',True)+
     [edit('remove-b','remove',{'kind':'package','name':'case-owner-b'})]+apply('remove-b-apply')+
     [query('shared-gone','package-present',value=False,package='case-shared')]+checkpoint('final',True))
for cid,decl in [('REPRO-1','D-test'),('REPRO-2a','D-accounts-fixed'),('REPRO-2b','D-accounts-open')]:
    case(cid,'K3 W3c W3d','Two independent clean builds; compare named source/recipe and setting values, not compiled byte identity.',
         [step('two-clean-builds','builds',declaration=decl,orders=[['a','b'],['b','a']]),
          query('independent','independent-build-evidence',value=True),query('equal','named-state-equal',value=True)],
         question='Q-OPTIONAL' if cid.endswith('b') else None)

# Additional recorder cycles retain the v5 refusal branch and positive manual application.
for suffix,target in [('APT','package'),('APT2','package-file'),('HOST','hostname'),('TIME','timezone'),('SYSCTL','sysctl'),('ENABLE','service'),('UENABLE','user-service'),('USER','account'),('USERMOD','account-change'),('NFT','firewall'),('LOCALE','locale'),('GROUP','group'),('SUDO','rights'),('MODULE','module'),('LINGER','linger')]:
    case('X-REC-'+suffix,'K1 K4 W1a W1b W1c W2a W2b Q2','Request '+target+'; refusal or exact record is allowed; manual line supplies positive install/apply/remove cycle.',
         fresh()+[step('read-law','old',scope='committed'),step('tool-request','request',target=target,action='add',role='root'),
                  step('read-law','still-old',[ck('sha256','eq',ref('old.sha256'))],scope='committed'),
                  query('candidate-delta','request-delta-valid',value=True,target=target),query('no-effect','request-in-force',value=False,target=target),
                  step('record-if-refused','record',target=target)]+apply('requested-apply')+
         [query('effect','request-in-force',value=True,target=target)]+checkpoint('applied',True)+
         [step('tool-request','remove-request',target=target,action='remove',role='root'),
          query('still-effect','request-in-force',value=True,target=target),step('record-removal-if-refused','remove',target=target)]+apply('removed-apply')+
         [query('gone','request-in-force',value=False,target=target)]+checkpoint('final',True))

# Migration origins are preserved alongside executable targets.
PORT=json.loads((Path(__file__).parent/'port.json').read_text())
BY_ID={c['id']:c for c in CASES}
for row in PORT:
    BY_ID[row['target']].setdefault('origins',[]).append(row['old'])
IDS=list(BY_ID)
assert len(IDS)==len(CASES)
