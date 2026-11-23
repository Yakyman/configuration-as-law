import csv,re,json
rs=[r for r in csv.DictReader(open('A1/in/part-4.tsv'),delimiter='\t') if r['kind']=='system-closure-store-object'][:431]
p='A1/c1/part-4.1.tsv';old={r['id'] for r in csv.DictReader(open(p),delimiter='\t')};f=open(p,'a');w=csv.writer(f,delimiter='\t',lineterminator='\n')
def add(i,d,s,what,b,reason):
 r=rs[i]
 if r['id'] not in old:w.writerow([r['id'],d,s,what,b,reason]);f.flush();old.add(r['id'])
def must(i,what,b):add(i,'MUST','S2.2-1,S2.2-2,S2.2-9,S2.2-10',what,b,'This executable program or library provides the stated capability; removing it removes that functionality.')
url='https://codeberg.org/guix/guix/raw/commit/d58da8a56b75af73a7b5466f7ef8a81679713aa3/gnu/services/shepherd.scm'
for i,r in enumerate(rs):
 n=r['name'][44:]
 if n.startswith('shepherd-') and n.endswith('.go'):
  add(i,'MUST','S2.2-10,S2.2-13','Executes compiled service definition code in the system service manager.','doc:'+url,'The service manager directly loads compiled service code with its own rights; generated code remains code, not merely internal settings.')
 elif n.startswith('shepherd-') and n.endswith('.scm'):
  add(i,'UNKNOWN','S3-1,S3-2','Supplies Scheme source for a service; actual source execution remains unestablished.','raw:guix/service-provenance.tsv','Only a service expression and source path survive; documentation loads compiled counterparts. Whether this source itself executes or contributes additional behavior is unestablished.')
for i,desc,u in [(2,'Provides vector, matrix and graphics mathematics routines.','https://imath.readthedocs.io/en/latest/'),(8,'Executes SPARQL queries and manages RDF data.','https://tracker.api.gnome.org/'),(35,'Provides local and network printing services.','https://www.cups.org/'),(158,'Discovers and publishes local network services.','https://github.com/avahi/avahi'),(415,'Interprets Python programs and supplies the runtime library.','https://www.python.org/doc/essays/blurb/'),(430,'Edits text files through line-oriented commands.','https://www.gnu.org/software/ed/')]:must(i,desc,'doc:'+u)
for i in [144,407]:add(i,'MUST','S2.2-10,S2.2-13','Executes shell startup commands with the shell’s rights.','doc:https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files','Shell startup files are expressly included as code executed with interpreter rights; their settings content does not exempt them.')
add(3,'MUST','S2.2-1,S2.2-2','Selects account and hostname lookup sources across programs.','raw:guix/nsswitch.txt','System account and hostname resolution depend on these rules; the settings are shared across programs.')
add(81,'MUST','S2.2-10,S2.2-13','Runs activation, creates runtime directories, and starts the system service manager.','raw:guix/system-boot.scm','The boot script is interpreter code performing system actions with its interpreter’s rights.')
add(281,'MUST','S2.2-10','Executes system activation from the boot script.','raw:guix/system-boot.scm','The observed boot script primitive-loads this exact object as code with its own rights.')
add(231,'MUST','S2.2-1,S2.2-2','Supplies the initial RAM filesystem selected for system boot.','raw:guix/configuration/run/current-system/parameters','The boot parameters select this exact initrd; removing it removes the configured boot input.')
add(134,'MUST','S2.2-1,S2.2-2','Specifies boot kernel, initrd, root device and kernel arguments.','raw:guix/configuration/run/current-system/parameters','These values determine system boot and device selection, rather than behavior confined to one application.')
meta=json.load(open('A1/c1/part-4.1-metadata.json'))
for i in [54,87,169,179,211,214,255,275,313,364,401,429]:
 r=rs[i];pkg=re.split(r'-(?=\d)',r['name'][44:])[0];m=next(x for x in meta if pkg in x[:2]);b='doc:'+m[3]
 if i in [211,275]:add(i,'NOT','S2.2-4,S2.2-7','Supplies visual theme assets.','doc:'+m[3],'These visual assets supply appearance content; removing them removes their appearance, not the underlying application.')
 elif i in [364,429]:add(i,'NOT','S2.2-4','Supplies font glyph outlines or bitmaps.',b,'The font is visual content; removal makes these glyph designs unavailable while text rendering programs remain.')
 elif i==87:add(i,'MUST','S2.2-1,S2.2-2','Provides audio plugin development interfaces and support tools.',b,'Removing the development interfaces prevents building software against this installed plugin specification.')
 elif i==255:add(i,'MUST','S2.2-1,S2.2-2','Assembles the desktop environment’s executable components.',b,'The package exposes desktop programs; removal removes that assembled executable environment.')
 elif i==401:add(i,'MUST','S2.2-1,S2.2-2','Defines desktop settings schemas consumed by multiple desktop components.',b,'These shared settings schemas serve multiple programs; their removal removes settings interfaces used across the desktop.')
 elif i in [54,179,214,313]:add(i,'MUST','S2.2-1,S2.2-2','Supplies operational lookup tables used by system software.',b,'These tables implement timezone conversion, radio restrictions, network naming, or text decoding; removal loses functionality rather than only user content.')
 elif i==169:add(i,'UNKNOWN','S3-2','Specific audio topology configuration behavior is unestablished.',b,'Package documentation inherits a library synopsis; it does not establish the behavior or scope of this configuration-only output.')
add(414,'MUST','S2.2-1,S2.2-2','Registers image loader modules for image decoding.','doc:https://gnome.pages.gitlab.gnome.org/gtk/gdk-pixbuf/type_func.Pixbuf.init_modules.html','The documented loader initialization uses this registry; its cache name does not establish removal merely slows decoding.')
add(419,'HOLE','S2.2-1,S2.2-4','Provides operating-system identity values to applications.','doc:https://www.freedesktop.org/software/systemd/man/251/os-release.html','Identity information can be content or a behavioral input for application branches; the text does not delimit these readings for this object.')
f.close()
print('rows now',len(old))
