# Executed by build.py with its in-memory fact rows.
# Separate independent requested facts and connect semantic statements to documentation.
unknown_parts={
 'producer_and_creation_time':['historical_producer','historical_creation_time'],
 'person_choice_and_time':['human_value_choice','human_chooser_role','human_choice_time'],
 'person_choice_and_producer':['human_value_choice','human_chooser_role','human_choice_time','historical_producer','historical_creation_time'],
 'historical_producer_inputs_choice':['historical_producer','historical_creation_time','derivation_input_set','human_value_choice','human_chooser_role','human_choice_time'],
 'member_content_execution_and_effects':['member_code_or_values','member_launch_behavior','member_access_effects'],
 'original_writer_and_time':['historical_producer','historical_creation_time'],
 'archive_contents_and_input_versions':['archive_member_inventory','archive_source_package_versions','archive_source_modifiedness'],
 'installed_version_and_permissions':['installed_addon_version','installed_addon_manifest_permissions'],
 'execution_rights_and_launch_access_capability':['effective_extension_rights','extension_external_program_launch','extension_host_changes'],
 'recorded_description_source':['primary_description_designation','successful_application_source'],
}
semantic_keys={'execution','execution_rights','effect_scope','launch_or_access','generation_mechanism','named_member_function','producer_mechanism','archive_execution_sequence'}
# General documentation supplement for metadata-based interpretations, scoped per object.
by_object=collections.defaultdict(list)
for z in out:by_object[z['object']].append(z)
for ident,rr in by_object.items():
 refs=[x['source'] for x in rr if x['fact'].startswith('documented_') or x['fact'] in ['archive_execution_sequence','producer_mechanism']]
 # Filesystem records alone support existence/content metadata, not API semantics.
 for z in rr:
  if z['fact'] in semantic_keys and not z['value'].startswith('UNKNOWN:'):
   z['source'] += '; '+ '; '.join(refs)
expanded=[]
for z in out:
 k=z['fact']
 if z['value'].startswith('UNKNOWN:') and k in unknown_parts:
  for kk in unknown_parts[k]:expanded.append(z|{'fact':kk})
 elif k.startswith('member_metadata:') or k in ['service_link','service_link_metadata']:
  d=json.loads(z['value']);path=k.split(':',1)[1] if ':'in k else d.get('path','link')
  for kk,v in d.items():
   if kk!='path':expanded.append(z|{'fact':'member_'+kk+':'+path,'value':str(v)})
 elif k.startswith('member_package_record:') and '; integrity=' in z['value']:
  a,b=z['value'].split('; integrity=',1);integrity,rule=b.split('; ',1)
  expanded.append(z|{'fact':'member_manifest_owner:'+k.split(':',1)[1]+':'+a,'value':a})
  value=integrity if integrity!='unknown' else 'UNKNOWN: Retained package-files collector could not establish integrity; '+rule
  expanded.append(z|{'fact':'member_integrity:'+k.split(':',1)[1]+':'+a,'value':value})
 else:expanded.append(z)
out=[];seen=set()
for z in expanded:
 key=tuple(z.items())
 if key not in seen:out.append(z);seen.add(key)
