"""Ordered v4 rules over observed facts; no pathname or byte-signature inference."""

def classify(facts):
    def decided(category, required, question, **extra):
        return dict(category=category, required=required, question=question, missing=[], **extra)
    def unknown(*names):
        return dict(category='FACT_UNKNOWN', required=None, question=None, missing=list(names))
    if facts.get('runtime_only') is True:
        return decided('runtime', False, 'S8.2-5', creator=facts.get('creator'),
                       creator_status='known' if facts.get('creator') else 'FACT_UNKNOWN')
    # Three-valued conjunction: a known negative defeats an unknown operand.
    def both(a, b):
        if a is False or b is False: return False
        if a is True and b is True: return True
        return None
    package=facts.get('package_installed')
    member=both(facts.get('package_member'), facts.get('remains_as_received'))
    if package is True or member is True:
        return decided('installed object', True, 1)
    if package is not False or member is not False:
        return unknown('package_installed/package_member/remains_as_received')
    executable=facts.get('executable')
    if executable is True:
        if facts.get('own_process') is True:
            return decided('program', True, 2)
        # All conditions, including recorded host, must be facts for exemption.
        sandbox=('inside_recorded_program','cannot_launch_programs','cannot_change_installed','cannot_change_settings')
        if all(facts.get(k) is True for k in sandbox):
            return decided('contained code', False, 2, clarification='S8.2-21')
        if any(facts.get(k) is False for k in sandbox):
            return decided('program', True, 2)
        return unknown(*[k for k in sandbox if facts.get(k) is None])
    if executable is not False:return unknown('executable')
    setting=facts.get('setting')
    if setting is True:return decided('setting',True,3)
    if setting is None:
        chosen=facts.get('chosen_value')
        whole=both(chosen,facts.get('computer_obeys'))
        personal=both(facts.get('personal_program_value'),
                      True if facts.get('launches') is True or facts.get('grants_access') is True else
                      False if facts.get('launches') is False and facts.get('grants_access') is False else None)
        if whole is True or personal is True:return decided('setting',True,3)
        if whole is not False or personal is not False:
            return unknown('chosen_value/computer_obeys/personal_program_value/launches/grants_access')
    if facts.get('creator_kind')=='program':return decided('program record',False,4)
    if facts.get('creator_kind')=='person':return decided('material',False,4)
    return unknown('creator_kind')


def coverage(classification, observed, claims):
    """Claims are prevalidated provenance edges with an exact required state.

    Merely naming an interpreter/dependency/path is never such an edge. Caller
    must check each edge against independent installed-state provenance first.
    """
    if classification['category']=='FACT_UNKNOWN':
        return dict(status='FACT_UNKNOWN', lines=[], coverage=[])
    if classification['category']=='runtime':
        return dict(status='diagnostic',lines=[],coverage=[])
    matches=[]
    for claim in claims:
        relation=claim.get('relation')
        if relation not in ('own','package','derived'):continue
        if claim.get('provenance_verified') is not True:continue
        if classification['category']=='setting' and relation!='own':
            if relation!='package' or claim.get('package_default') is not True:continue
        if claim.get('required')!=observed:continue
        matches.append(dict(line=claim['line'],relation=relation,required=claim['required']))
    if matches:return dict(status='covered',lines=sorted(set(c['line'] for c in matches)),coverage=matches)
    if not classification['required']:return dict(status='not-required',lines=[],coverage=[])
    return dict(status='mismatch' if claims else 'unrecorded',lines=[],coverage=[])
