"""Independent checking and evidence rules. No guest transport or OS commands here."""
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

OUTCOMES = ('pass', 'fail', 'undecided', 'unobserved')
COVERAGE = ('stored', 'process', 'port', 'account', 'group', 'access', 'service',
            'network', 'saved-network', 'mount', 'module', 'sysctl', 'locale',
            'time', 'hostname', 'wifi', 'bluetooth')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()


def read_json(path):
    return json.loads(Path(path).read_text())


def index(objects):
    result = {}
    for obj in objects:
        key = (obj['kind'], obj['id'])
        if key in result:
            raise ValueError('duplicate object: ' + repr(key))
        result[key] = obj
    return result


def within(path, folder):
    """Requires normalized resolved paths from the collector, not lexical '..'."""
    p, f = PurePosixPath(path), PurePosixPath(folder)
    if not p.is_absolute() or not f.is_absolute() or '..' in p.parts or '..' in f.parts:
        return False
    return p == f or f in p.parents


def derive(declaration, package_reader=None):
    """Only explicit lines and hash-bound package inputs. Never reads a machine."""
    expected, errors, openings = {}, [], []
    seen = set()
    def add(obj, owner):
        key = (obj['kind'], obj['id'])
        value = obj.get('value', {})
        if key in expected and expected[key]['value'] != value:
            raise ValueError('conflicting declared values: ' + repr(key))
        if key not in expected:
            expected[key] = dict(obj, owners=[])
        expected[key]['owners'].append(owner)
    for line in declaration['lines']:
        lid, kind = line['id'], line['kind']
        if lid in seen:
            raise ValueError('duplicate declaration line: '+lid)
        seen.add(lid)
        if kind == 'binding':
            errors.append({'line': lid, 'reason': 'release binding unresolved: '+line['name']})
        elif kind == 'package':
            if package_reader is None:
                errors.append({'line':lid, 'reason':'package reader unavailable'})
                continue
            try:
                objects = package_reader(line)
            except (OSError, ValueError) as exc:
                errors.append({'line':lid, 'reason':str(exc)})
                continue
            add({'kind':'package','id':line['name'], 'value':{
                'version':line['version'], 'source_sha256':line['source_sha256'],
                'recipe_sha256':line['recipe_sha256']}}, lid)
            for obj in objects:
                add(obj, lid)
        elif kind == 'open-folder':
            folder = line['path']
            if not within(folder, folder):
                raise ValueError('invalid open folder')
            openings.append(folder)
            add({'kind':'open-folder','id':folder,'value':{'scope':line.get('scope','execute')}},lid)
        elif kind == 'external-accounts':
            # It names the source, not an invented list of accounts.
            add({'kind':'external-source','id':lid,'value':{'source':line['source']}},lid)
        elif kind == 'object':
            add(line['object'],lid)
        elif kind == 'file':
            content=line['text'].encode()
            add({'kind':'file','id':line['path'],'value':{'sha256':digest(content),
                'mode':line['mode'],'uid':line['uid'],'gid':line['gid']}},lid)
        else:
            errors.append({'line':lid,'reason':'unimplemented semantic kind '+kind})
    return {'objects':list(expected.values()), 'errors':errors, 'openings':openings,
            'declaration_sha256':digest(canonical(declaration))}


def compare(expected, observed):
    """Partial evidence never yields an empty, successful comparison."""
    issues=[]
    def issue(status, key, reason):
        issues.append({'status':status,'object':list(key),'reason':reason})
    try:
        want, got=index(expected['objects']),index(observed['objects'])
    except (KeyError, ValueError) as exc:
        return [{'status':'UNVERIFIED','object':['schema','inventory'],'reason':str(exc)}]
    for error in expected.get('errors',[]):
        issue('UNDERIVED', ('line',error.get('line','?')),error['reason'])
    for error in observed.get('errors',[]):
        issue('UNVERIFIED', ('capture',error.get('kind','?')),error['reason'])
    coverage=observed.get('coverage',{})
    for kind in COVERAGE:
        c=coverage.get(kind,{})
        # not-applicable needs a documented absence AND a concrete independent probe.
        if not (c.get('status')=='complete' and c.get('evidence')) and not (
            c.get('status')=='not-applicable' and c.get('evidence') and c.get('reason')):
            issue('UNVERIFIED',('coverage',kind),'missing complete independent capture')
    for key,w in want.items():
        if key not in got:
            cover_kind='stored' if key[0] in ('file','dir','symlink','package') else key[0]
            status='MISSING' if coverage.get(cover_kind,{}).get('status')=='complete' else 'UNVERIFIED'
            issue(status,key,'required by '+','.join(w['owners']))
            continue
        g=got[key]
        for field,value in w.get('value',{}).items():
            if field not in g.get('value',{}):
                issue('UNVERIFIED',key,'unobserved field '+field)
            elif g['value'][field]!=value:
                issue('DIFFERS',key,field)
    known_hashes={o['value']['sha256'] for o in want.values()
                  if o['kind']=='file' and o.get('value',{}).get('sha256')}
    for key,g in got.items():
        if key in want:
            continue
        v=g.get('value',{})
        if g['kind'] in ('process','port'):
            # R9: namespace path equality alone is never attribution.
            if v.get('exe_sha256') in known_hashes and v.get('exe_evidence'):
                continue
            issue('UNRECORDED' if v.get('exe_sha256') and v.get('exe_evidence') else 'UNVERIFIED',
                  key,'running executable not attributable by observed bytes')
            continue
        if g['kind']=='account' and v.get('external_source'):
            sources={o.get('value',{}).get('source') for o in want.values()
                     if o['kind']=='external-source'}
            if v['external_source'] in sources and v.get('source_evidence'):
                continue
        # Opening affects execution within its precise documented scope, not arbitrary settings.
        if g['kind'] in ('file','dir','symlink') and v.get('resolved_path') and any(
            within(v['resolved_path'],f) for f in expected.get('openings',[])):
            if g.get('classification')=='opened-material' and g.get('route_evidence'):
                continue
        if g.get('classification') in ('material','program-record'):
            routes=g.get('routes',[])
            if any(r.get('observed') is True and (r.get('installed') or r.get('configured')
                   or (r.get('kind')=='direct' and r.get('executed') is True)) for r in routes):
                issue('UNRECORDED',key,'observed direct execution or installation/configuration')
                continue
            if g.get('origin_evidence') and g.get('route_evidence') and routes and all(
                r.get('kind') in ('direct','data','values') and r.get('observed') is True
                and (r['kind']!='direct' or r.get('executed') is False)
                for r in routes):
                if not any(r.get('installed') or r.get('configured') for r in routes):
                    continue
            issue('UNVERIFIED',key,'material/record classification lacks route or origin evidence')
            continue
        if g.get('classification')=='inactive-generation' and g.get('review_evidence'):
            continue
        issue('UNDERIVED' if expected.get('errors') else 'UNRECORDED',key,'no derived attribution or independently evidenced data classification')
    return issues


def outcome(issues):
    if any(i['status'] in ('UNRECORDED','MISSING','DIFFERS') for i in issues):
        return 'fail'
    if any(i['status'] in ('UNDERIVED','UNVERIFIED') for i in issues):
        return 'unobserved'
    return 'pass'


def aggregate(rows):
    values={r['outcome'] for r in rows}
    if not rows or 'unobserved' in values or 'undecided' in values:
        return '?' if 'fail' not in values else '0'
    return '0' if 'fail' in values else '1'


def field(obj, path):
    for part in path.split('.') if path else []:
        obj=obj[int(part)] if isinstance(obj,list) else obj[part]
    return obj


def resolve(value, captures):
    if isinstance(value,dict) and set(value)=={'ref'}:
        name,_,path=value['ref'].partition('.')
        return field(captures[name],path)
    if isinstance(value,dict):
        return {k:resolve(v,captures) for k,v in value.items()}
    if isinstance(value,list):
        return [resolve(v,captures) for v in value]
    return value


def check(actual, condition, captures):
    """Returns raw check outcome; no arbitrary expression evaluation."""
    try:
        value=field(actual,condition['field'])
        target=resolve(condition.get('value'),captures)
        op=condition['op']
        if op=='eq': ok=value==target
        elif op=='ne': ok=value!=target
        elif op=='match': ok=isinstance(value,str) and re.search(target,value) is not None
        elif op=='not-match': ok=isinstance(value,str) and re.search(target,value) is None
        elif op=='contains': ok=target in value
        elif op=='gt': ok=value>target
        elif op=='in': ok=value in target
        else: raise ValueError('unknown check operator '+op)
        if not ok and condition.get('alternative') is not None:
            alt=condition['alternative']
            alt_result, _=check(actual,alt,captures)
            if alt_result=='pass':
                if not condition.get('question'): raise ValueError('alternative reading lacks question')
                return 'undecided', {'actual':value,'question':condition['question'],'expected':target}
        return ('pass' if ok else 'fail', {'actual':value,'expected':target,'operator':op})
    except (KeyError, IndexError, TypeError) as exc:
        return ('unobserved',{'reason':'missing evidence: '+str(exc)})


def evaluate_query(subject, reply):
    """Compute comparisons from raw operands; ignore adapter-supplied verdicts.

    Scalar queries (e.g. a marker or kernel parameter) are native parser outputs.
    Relational queries must never be satisfied by a bare True from an adapter.
    """
    equality={'description-equivalent','same-declaration','named-account-fields-equal',
              'named-state-equal','namespace-executable-hash'}
    result=dict(reply)
    if subject in equality:
        left,right=reply['left'],reply['right']
        if left is None or right is None:
            raise ValueError('comparison operands missing')
        if not reply.get('evidence'):
            raise ValueError('comparison lacks raw operand evidence')
        result['value']=left==right
    elif subject=='request-delta-valid':
        before=set(reply['before_lines']);after=set(reply['after_lines'])
        added=set(reply['expected_added']);removed=set(reply['expected_removed'])
        if not reply.get('binding_evidence'):
            raise ValueError('request delta has no frozen expectation binding')
        # Either exact requested record, or unchanged refusal. No arbitrary extra lines.
        result['value']=(after==before or (after-before==added and before-after==removed))
    elif subject=='system-components-changed':
        old,new=reply['before_components'],reply['after_components']
        required=set(reply['system_components'])
        if not required or not reply.get('binding_evidence'):
            raise ValueError('system component set not bound')
        result['value']=any(k in old and k in new and old[k]!=new[k] for k in required)
    elif subject=='independent-build-evidence':
        a,b=reply['builds']
        result['value']=(a['work_id']!=b['work_id'] and a['log_sha256']!=b['log_sha256']
                         and a['source_sha256']==b['source_sha256']
                         and a['clean'] is True and b['clean'] is True
                         and not a['cloned'] and not b['cloned'])
    return result
