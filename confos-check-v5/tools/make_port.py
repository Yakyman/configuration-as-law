#!/usr/bin/env python3
"""Regenerate the migration inventory from the immutable stand's case data."""
import argparse, json, re, runpy, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--records-root', type=Path, default=ROOT.parent,
                    help='repository root containing confos-check/ and confos-check-extra/')
STAND = parser.parse_args().records_root
sys.path.insert(0, str(STAND / 'confos-check'))
old = runpy.run_path(str(STAND / 'confos-check/casedefs.py'))['CASES']
extra = runpy.run_path(str(STAND / 'confos-check-extra/casedefs_extra.py'))['CASES']
# CASES is later extended with instrumentation self-tests; these are not complete-run cases.
old = [c for c in old if not c['id'].startswith('P4-T-') and not c['id'].startswith('T-')]
BT = ['ACCOUNT','ACCOUNT','ACCOUNT','ACCOUNT','RIGHTS','FIREWALL','NETWORK','SAVED-NETWORK','HOST','TIME','LOCALE','MODULE','SYSCTL','MOUNT','SERVICE']
SEARCH = {'054':'G-SCRIPT','056':'G-BUILD','089':'G-STDIN','090':'G-STARTUP','107':'G-STARTUP','108':'G-STARTUP','111':'G-STARTUP','135':'G-STARTUP','136':'G-SCRIPT','160':'G-SCRIPT','161':'G-STDIN','162':'G-SCRIPT','166':'G-SCRIPT','167':'G-STARTUP','202':'G-INSTALL','234':'G-SERVICE','241':'Q7-VALUES','LO-1':'G-READER','LO-2':'G-READER'}

def mapping(c):
    cid = c['id']; why = ''; action = 'changes'
    labels = ['K1','W4b','Q2']
    if cid.startswith('OW-'):
        n=int(cid.split('-')[1]); target=cid
        labels=['K1','W2c','W3b','Q4']
        why={1:'tree becomes source-built case-small',2:'first actual source/recipe system update, then restart',3:'second actual source/recipe system update, then restart',4:'browser leaves; terminal fetch replaces ordinary activity; Q6-GUEST retains the virtualization gap',5:'office document becomes a plain text file edited with base tools',6:'base commands and recorded report script',7:'local pinned C source replaces external hello.c; opened folder permits edit/build/rebuild',8:'game and launcher leave; recorded case-probe updater and child payload replace them',9:'small throttled source/package transfer replaces large font; loss at observed progress',10:'actual laptop Wi-Fi stack, connect/reproduce/remove',11:'actual laptop Bluetooth stack, pair/reproduce/remove'}[n]
        if n in (10,11): action='stays'; labels=['K3','K4','W2b']
    elif cid.startswith('P4-C'):
        ch=int(re.match(r'P4-C(\d+)',cid)[1]); targets={1:'G-INSTALL',2:'G-UPDATER',3:'G-UPDATER',4:'G-BRING',5:'G-BRING',6:'G-DOWNLOAD',7:'G-BUILD',8:'G-SERVICE',9:'G-SCRIPT',10:'G-STARTUP',11:'G-CONTAINER'}
        target=targets[ch]
        if ch in (2,3,4,5,11):
            action='leaves'; why='absent product channel; '+target+' retains its generic obligation; G-BRING tests bringing the absent consumer'
        else: why={1:'confpkg user/root installation, file import, removal/purge and extraction variants',6:'source-built payload in the same home/tmp/shm/var-tmp locations; root direct write separately',7:'base compiler and recipe runner, source and binary routes',8:'actual service/startup/scheduling interface, preserving persistent/transient/delayed/root variants',9:'all shipped interpreters and actual loader; additional readers enter via G-BRING',10:'actual startup/login/hook consumers and recorded private reader; absent consumers enter via G-BRING'}[ch]
        if ch in (5,6,7,9,10): labels=['K1','W2c','W4b','Q3','Q4']
        if ch==11: labels=['K1','W2a','Q5']; why+='; namespace observation is unobserved if unsupported'
        if cid=='P4-C6-5': target='W5-BREAK'; labels=['W5a','W5b']
    elif cid.startswith('P4-BT-'):
        target='G-'+BT[int(cid.rsplit('-',1)[1])-1]; why='actual base tool, same setting and root privilege; no missing executable counted as refusal'; labels=['K1','W2b','W5a','Q2']
    elif cid=='P4-SHELL': target='G-SHELL'; action='stays'; why='interactive base shell'; labels=['Q4']
    elif cid.startswith('P4-PIPE-'):
        target='G-PIPE'; why='base fetcher and shell; three input forms; inventory before reboot retained as evidence, after reboot decides'; labels=['K1','W2b','Q4']
    elif cid.startswith('P4-S-'):
        suffix=cid[5:]; target=SEARCH[suffix]; labels=['K1','W4b','Q3','Q4','Q7']; why='search route retained as variant: '+{'054':'debugger startup file','056':'build command expansion','089':'saved stdin instructions','090':'editor startup file','107':'SSH ProxyCommand','108':'SSH Match exec','111':'installer pre-invoke configuration','135':'automatic plugin directory','136':'explicit plugin file','160':'interpreter inside runtime','161':'stdin inside runtime','162':'temporary file inside runtime','166':'source command inside runtime','167':'configuration naming plugin','202':'package hold setting','234':'root schedules for another account','241':'ordinary user-agent value','LO-1':'saved profile macro in home','LO-2':'saved profile macro in temporary directory'}[suffix]
        if suffix not in ('089','241'): action='leaves'; why+='; absent original consumer replaced by base consumer or brought recorded reader, not a claimed retest of that product'
    elif cid.startswith('X-REC-'):
        t=cid[6:]; labels=['K1','K4','W1a','W1b','W1c','W2a','W2b','Q2']; target='X-REC-'+t
        if t in ('PIP','NPM','FLATPAK','PODMAN'): action='leaves'; target='G-UPDATER' if t!='PODMAN' else 'G-CONTAINER'; why='absent product; generic request/apply/remove and bringing consumer retained'
        else: why='actual base tool request, exact candidate delta, unchanged in-force state, apply, removal; refusal allowed by v5, positive manual-line route still required'
    elif cid.startswith('X-WIFI') or cid.startswith('X-BT'):
        target='X-WIFI' if cid.startswith('X-WIFI') else 'X-BT'; why='simulated radio lifecycle, separate from physical OW-10/11'; labels=['K3','K4','W2b']
    elif cid.startswith('P2-'):
        target=cid; why='same addition/change/removal and power-cut sequence, native package/setting/service'; labels=['C0','D','K2','W1a','W1b','W1c','W1e','W3a']
    elif cid.startswith('REM-'):
        target=cid; why='confpkg payload, actual service/access tool; two small owners of shared dependency in REM-4'; labels=['K4','W3b','W3e']
    elif cid.startswith('REPRO-'):
        target=cid; why='independent clean source builds, source/recipe identity; account order retained; omitted IDs tested separately'; labels=['K3','W3c','W3d']
    elif cid=='P1-0': target=cid; action='stays'; why='whole-machine independent stored and live inventory'; labels=['C0','K1','K2','W2a','W2b','W3e']
    elif cid=='UND-0': target=cid; action='stays'; why='derive before accessing machine; no implementation-produced reference inventory'; labels=['K2','W3a','W3b','W3c']
    else: raise ValueError(cid)
    return dict(old=cid, disposition=action, target=target, statements=labels, replacement=why)
rows=[mapping(c) for c in old+extra]
# First-form radio step IDs remain explicit even though final casedefs aggregate them.
for family in ('X-WIFI','X-BT'):
    for i in range(1,6): rows.append(mapping({'id':f'{family}-{i}'}))
assert len({r['old'] for r in rows})==len(rows)
(ROOT/'port.json').write_text(json.dumps(rows,indent=2)+'\n')
lines=['# Port of every stand case','', '2026-11-26 UTC. Source case IDs are extracted from both case-definition modules and the first-form radio steps in CASES-EXTRA.md. Search cases are included individually. Product removal does not assert that a missing command was tested. Replacement targets name cases in CASES.md; variants preserve locations, privilege and input form. See PROGRAMS.md for admission choices.', '',f'{len(rows)} explicit source case/step IDs. Labels are those of records-confos/TABLE.md. No system outcome is recorded here.','', '| Stand ID | Disposition | New case | Version 5 | Replacement / retained obligation |','|---|---|---|---|---|']
for r in rows: lines.append('| '+ ' | '.join([r['old'],r['disposition'],r['target'],', '.join(r['statements']),r['replacement']])+' |')
lines+=['','## Generated checks (every occurrence, not deleted)', '', '| Stand row family | Disposition | New check and statements |','|---|---|---|','| P1:&lt;TAG&gt; for every inventory | stays | P1 after each scenario checkpoint: C0, K1, K2, W2a, W2b, W3e. A ported scenario uses its new tag; no global inventory is replaced by just its marker probe. |','| P2-1:&lt;case&gt;:&lt;n&gt; after every application | stays | P2 for each application: D, K2, W1a–c, W1e, W3a. Expected state uses last reported success, not candidate text. |','| UND:&lt;TAG&gt; for every inventory | stays | UND strict derivation: K2, W3a–c; unknowns remain unobserved/undecided, never borrowed from a reference installation. |','| X-REC companion pre/recorded/applied/unrecorded/removed checks | changes | Same checkpoints for each retained X-REC; P1/P2/UND compare independently. Product-specific rows map to the generic target above. |','| X-WIFI and X-BT companion checks | stays | Each of five lifecycle checkpoints: saved settings included in stored and live inventory, K3/K4/W2b. |','| P4-PIPE before-restart P1/UND records | stays | Evidence only under review R6; after-restart checks decide. |','','These are universally quantified row-generation rules, including every one of the 458 complete-run-3 rows and the extra-set companion rows. A stopped or failed scenario still emits unobserved rows for missing checkpoints. Instrumentation-only P4-T-* and T-* are checker tests, not stand cases; their sensitivity obligations are retained by selftest.','']
(ROOT/'PORT.md').write_text('\n'.join(lines))
print(f'PORT: {len(rows)} source IDs')
