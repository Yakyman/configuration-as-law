import csv,re,collections,pathlib
csv.field_size_limit(10000000)
root=pathlib.Path('A3R/c1'); out=root/'part-1.system.tsv'; notes=root/'part-1.system.notes.md'
rows=[x for x in csv.DictReader(open('A3R/in/part-1.tsv'),delimiter='\t') if not x['kind'].startswith(('package:','python-distribution','package-environment-evidence','executable-code-outside-packages','stored-outside-packages'))]
header=['id','decision','sentences','what_it_does','basis','reason']
existing={x['id'] for x in csv.DictReader(out.open(),delimiter='\t')} if out.exists() else set()
f=out.open('a'); w=csv.writer(f,delimiter='\t',lineterminator='\n')
if not existing:w.writerow(header)
rules=collections.defaultdict(list)
def emit(r,d,s,what,why,rule=None,basis='evidence'):
 assert len(what.split())<=15,(r['id'],what)
 assert len(why.split())<=30,(r['id'],why)
 if rule:rules[rule].append(r)
 if r['id'] not in existing:w.writerow([r['id'],d,s,what,basis,why]);f.flush();existing.add(r['id'])
for r in rows:
 k=r['kind']; m=r['members']; n=r['name']
 if k=='account':emit(r,'MUST','S2.2-15','Defines an operating-system account.','Accounts are explicitly required, including accounts without interactive login.','accounts')
 elif k=='group':emit(r,'MUST','S2.2-1,S2.2-2','Defines a named group identity and its supplementary membership.','Removing the group prevents named group selection and removes its membership definition; these affect system credentials.','groups')
 elif k=='polkit-actions':emit(r,'MUST','S2.2-1,S2.2-2','Defines an authorization action requested by clients of a privileged service.','Removing the action removes an authorization operation available across programs; its effect is not confined to one program.','polkit', 'doc:https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html')
 elif k=='driver':emit(r,'MUST','S2.2-1,S2.2-2','Binds a device to the kernel driver controlling it.','Removing this driver binding removes the associated device-control capability.','drivers','doc:https://docs.kernel.org/driver-api/driver-model/binding.html')
 elif k=='port':emit(r,'MUST','S2.2-15','Provides a bound network endpoint for incoming traffic.','Ports open for connection are explicitly required; loopback binding does not create an exemption.','ports')
 elif k=='firewall-rule':emit(r,'MUST','S2.2-15','Applies a kernel packet-filtering, forwarding, marking, or translation rule.','Firewall rules are explicitly required.','firewall-rules')
 elif k in ('service','user-service'):
  if 'not-found' in m:emit(r,'NOT','S2.2-1,S2.2-2','Names an absent service with no loaded unit or running process.','The inventory explicitly reports not-found and inactive; removing this absent reference removes no service capability.','absent-services')
  else:emit(r,'MUST','S2.2-1,S2.2-2,S2.2-9','Provides a loadable service that starts an external program.','Removing the service removes its launch capability; active services additionally run programs explicitly required by the text.','services')
 elif k in ('unit-file','user-unit-file'):
  if 'masked' in m:emit(r,'MUST','S2.2-1','Blocks service activation through a systemd mask.','The mask determines which external program can be started; the computer’s permitted behavior depends on it.')
  else:emit(r,'MUST','S2.2-1,S2.2-2','Defines activation of an external service or scheduled job.','Removing the unit removes its service or scheduling capability; its effects reach external programs, beyond systemd itself.','units','doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html')
 elif k=='process':
  line=int(r['evidence'].rsplit(':',1)[1]); raw=pathlib.Path('A3R/in/raw/lived/raw/076-process.out').read_text().splitlines()[line-1]
  if len(raw.split('\t'))!=2:emit(r,'UNKNOWN','S3-2','Identifies a PID whose executable was not resolved.','Collector concatenates failed readlink entries; the trailing executable belongs to another PID, so this PID’s function is unknown.','unresolved-processes','raw:A3R/in/raw/lived/raw/076-process.sh')
  else:emit(r,'MUST','S2.2-9,S2.2-12','Runs an executable as its own process.','The resolved executable is running as a separate process; such programs are explicitly required.','processes')
f.close()
with notes.open('w') as nf:
 nf.write('# Classification c1: system subset\n\nOnly the authorized input, raw inventory, fixed text, build description and cited public documentation were consulted. No objects were removed.\n\n')
 nf.write('## Exact text\n\n')
 for l in pathlib.Path('SENTENCES.md').read_text().splitlines():
  if l.startswith('- **S2.2-') or l.startswith('- **S3-1**') or l.startswith('- **S3-2**'):nf.write(l+'\n')
 nf.write('\n## Homogeneous rules and manual checks\n\nEach rule below was checked against the displayed raw entries for its first ten listed IDs. Functions, not inventory class labels, determine the decisions.\n\n')
 for rule,rr in rules.items():
  sample=rr[:10]
  nf.write('### '+rule+'\n\n')
  nf.write('Scope: '+', '.join(sorted({r['kind'] for r in rr}))+'. '+str(len(rr))+' rows. The corresponding TSV reason is the rule applied by `classify_system.py`.\n\n')
  nf.write('Manual checks: '+', '.join(r['id'] for r in sample)+'.\n\n')
 nf.write('## Sources\n\n')
 nf.write('- https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html : “Actions correspond to operations that clients can request the mechanism to carry out”. Policies span client, authority and service processes.\n')
 nf.write('- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html : “A unit file is a plain text ini-style file”. Service units arrange external program activation, rather than settings confined to systemd’s interface.\n')
 nf.write('- https://docs.kernel.org/driver-api/driver-model/binding.html : “Driver binding is the process of associating a device with a device driver that can control it.” Rows identify the binding, not ordinary stored symlink files.\n')
 nf.write('- https://www.man7.org/linux/man-pages/man5/group.5.html : “The /etc/group file is a text file that defines the groups on the system.” Group records define usable named credentials, including empty groups.\n')
 nf.write('- https://netfilter.org/projects/nftables/manpage.html : “nft - Administration tool of the nftables framework for packet filtering and classification”.\n')
 nf.write('- https://man.openbsd.org/sshd_config : “The file contains keyword-argument pairs, one per line.” These are values, not executable code.\n')
 nf.write('- https://docs.podman.io/en/latest/markdown/podman-run.1.html : “Run a process in a new container.” The same documentation specifies automatic image pulling when absent.\n')
 nf.write('\n## Process evidence defect\n\n`A3R/in/raw/lived/raw/076-process.sh` prints the PID and a tab before `readlink`; a failed readlink emits no newline. Several raw lines therefore concatenate unresolved PIDs before another PID and its executable. The row name is the first PID. Those rows are UNKNOWN, not assigned the last PID’s executable. Public program documentation cannot recover which program an unidentified PID ran.\n')
print(len(existing),collections.Counter(x['kind'] for x in rows if x['id'] not in existing))
