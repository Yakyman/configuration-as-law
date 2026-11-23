exec(open('D1/c1/part-flatcar.local.py').read().split('for x in src:')[0])
ssh={r['key'].lower():r for r in csv.DictReader(open('D1/c1/part-flatcar.ssh-map.tsv'),delimiter='\t')}
for x in src:
 k=x['kind'];n=x['name'];m=json.loads(x['members'])[0]
 if k=='L1:port':
  emit(x,'MUST','S2.2-15','Provides an open '+m.split()[0].upper()+' network endpoint.','Open connection ports must be recorded; loopback bindings are not exempt.')
 elif k=='L1:network-link':
  net=m.split()[1]
  emit(x,'MUST','S2.2-1,S2.2-2','Provides '+('local loopback' if net=='lo' else net+' Ethernet')+' networking.','Removing this network interface prevents communication through it; it is not an internal application preference.')
 elif k=='L1:login-key':emit(x,'MUST','S2.2-15','Authorizes public-key login to the account.','Keys used to log into an account must be recorded.')
 elif k=='L1:saved-network' or (k=='L1:access-rule' and '/.keep_' in n):
  emit(x,'NOT','S2.2-2,S2.2-4','Keeps an otherwise empty package directory represented.','An empty directory placeholder contains no effective network or access rule; removing the file removes only the placeholder.')
 elif k=='L1:package:system-image':
  emit(x,'MUST','S2.2-1,S2.2-2,S2.2-9','Supplies the running operating system and its system programs.','The mounted operating-system image supplies executable system functionality; removing it prevents running those programs.')
 elif k=='L1:access-rule':
  if n.startswith('ssh-access:'):
   opt=n.split(':',1)[1];r=ssh[opt.lower()];c=r['class']
   if c=='internal': d='NOT';s='S2.2-7,S2.2-13';reason='This value governs SSH protocol or presentation inside the program; the text exempts such settings.'
   elif c=='password':d='MUST';s='S2.2-15';reason='This is an account password-login or superuser-login rule, explicitly required to be recorded.'
   elif c=='port':d='MUST';s='S2.2-1,S2.2-15';reason='This rule determines listening endpoints or their accessibility, which the text requires recording.'
   elif c=='auth':d='MUST';s='S2.2-1,S2.2-2';reason='This rule determines access to system accounts and their sessions, extending beyond an internal SSH preference.'
   elif c=='launch':d='MUST';s='S2.2-1,S2.2-2';reason='This value controls program execution or its account; its effects extend beyond settings confined to the SSH interface.'
   elif c=='session':d='MUST';s='S2.2-1,S2.2-2';reason='This controls session processes, credentials, environment, or devices outside the SSH protocol interface.'
   elif c=='forward':d='HOLE';s='S2.2-1,S2.2-7,S2.2-13';reason='Forwarding changes machine connectivity but is implemented inside SSH; the text does not define whether such effects remain inside one program.'
   elif c=='integration':d='HOLE';s='S2.2-1,S2.2-7,S2.2-13';reason='The value belongs to SSH but exposes process identity to other programs; the text lacks a boundary for one-program settings.'
   emit(x,d,s,r['what'],reason)
  elif n.startswith(('sudo-access:','sudo-root:','sudo-user:')):
   emit(x,'MUST','S2.2-15','Permits command execution as any account, including superuser.','The right to become superuser must be recorded regardless of whether authentication requests a password.')
  elif n.endswith('.example'):
   emit(x,'NOT','S2.2-4','Provides an inactive example authorization script.','The example suffix is not loaded as a rule; removing this instructional content does not change authorization.')
  elif n.endswith('empower.rules'):
   emit(x,'MUST','S2.2-1,S2.2-10,S2.2-13,S2.2-15','Allows all privileged actions to members of the empower group.','Executed authorization code changes privileges across programs; it is not merely a value confined to one program.')
  elif n.endswith('systemd-networkd.rules'):
   emit(x,'MUST','S2.2-1,S2.2-10,S2.2-13','Allows the network service to change hostname and timezone and query hardware identity.','Executed authorization code changes permissions in other services, not merely values inside the authorization program.')
  elif n.endswith('sssd-realmd.rules'):
   emit(x,'MUST','S2.2-1,S2.2-10,S2.2-13','Allows SSSD to discover and renew authentication realms.','Executed authorization code grants cross-program realm operations; settings read only as values are different.')
  elif n.endswith('sssd-pcsc.rules'):
   emit(x,'MUST','S2.2-1,S2.2-10,S2.2-13','Allows SSSD access to smartcards and the smartcard service.','Executed authorization code grants access to another service and device; it is not confined program preference data.')
  elif n.endswith('50-default.rules'):
   emit(x,'MUST','S2.2-1,S2.2-10,S2.2-13','Selects the superuser account for administrative authentication.','Executed code determines administrative authorization identity across programs.')
  else:raise Exception(n)
f.close()
print(collections.Counter(r['decision'] for r in csv.DictReader(out.open(),delimiter='\t')))
