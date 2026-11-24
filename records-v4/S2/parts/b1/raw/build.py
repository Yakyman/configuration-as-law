from pathlib import Path
import csv,json
root=Path('S2/parts/b1')
# All source references are restricted to factual channel descriptions and documentation.
D={
'gcc':('https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html','linking combines all the object files','Compilation and assembly produce object files; linking produces an executable. -o selects the output name; the default executable name is a.out. An object file is linker input, not the linked executable.'),
'gcc-purpose':('https://gcc.gnu.org/onlinedocs/gcc/G_002b_002b-and-GCC.html','GCC is an integrated distribution of compilers for several major programming languages.','The documented purpose is compilation; back ends generate machine code.'),
'plugin':('https://gcc.gnu.org/onlinedocs/gccint/Plugins.html','GCC plugins are loadable modules that provide extra features to the compiler.','Plugins extend the compiler using its API, including transformations and analysis.'),
'plugin-load':('https://gcc.gnu.org/onlinedocs/gccint/Plugins-loading.html','They are loaded by the compiler using `dlopen` or equivalent','The plugin option names a shared-library file loaded into GCC. This documents an in-process extension rather than a separate plugin process.'),
'cmake':('https://cmake.org/cmake/help/latest/manual/cmake.1.html','cross-platform buildsystem generator CMake','CMake reads a project starting at CMakeLists.txt, generates a build tree, and writes CMakeCache.txt with persistent build information. It provides --build, --install and -P script interfaces.'),
'install':('https://cmake.org/cmake/help/latest/command/install.html','This command generates installation rules for a project.','Install rules select destinations relative to a prefix and copy outputs. CMake generates cmake_install.cmake in the build directory; the install target, CPack, or cmake -P can execute it.'),
'run':('https://cmake.org/cmake/help/latest/command/try_run.html','Try compiling and then running some code.','try_run builds an executable and, on success, runs it. Compile and run results are cached unless NO_CACHE; a configure-log event is written unless NO_LOG. COPY_FILE requests a retained copy. Cross compilation may require an emulator.'),
'log':('https://cmake.org/cmake/help/latest/manual/cmake-configure-log.7.html','The log file is a YAML document stream','CMake writes selected configure events for build debugging. The documented location is <build>/CMakeFiles/CMakeConfigureLog.yaml; the path can change between versions.'),
'child':('https://cmake.org/cmake/help/latest/command/execute_process.html','Execute one or more child processes.','CMake scripts have a documented facility for starting child processes; this does not establish which commands an unspecified project actually invokes.'),
'theme':('https://support.mozilla.org/en-US/kb/use-themes-change-look-of-firefox','A browser theme changes the appearance of Firefox','The selected theme controls browser appearance; this value is distinct from an installed theme bundle.'),
'pref':('https://support.mozilla.org/en-US/kb/firefox-support-troubleshooting-guide?mobile=0','This file stores all user preferences','The prefs.js entry explicitly includes the home page and activated theme. These two selected values, rather than the entire preference file, are the objects here.'),
'home':('https://support.mozilla.org/en-US/kb/how-to-set-the-home-page','The Firefox homepage is the first page you see when you open Firefox','The selected page opens on browser opening, Home button, or a new window; session restore can instead restore previous tabs. The documented UI lets the user choose the URL.'),
'python':('https://docs.python.org/3/tutorial/interactive.html','The history will be available again during the next interactive interpreter session.','The default interactive configuration saves history in ~/.python_history. Input editing and history substitution allow recall; this does not assert that an arbitrary whole history file is a valid script.'),
'readline':('https://docs.python.org/3/library/readline.html','reading/writing of history files','The interpreter has history reading/writing functions. The module is optional, and different back ends may use different file formats.'),
'bash':('https://tiswww.case.edu/php/chet/bash/bashref.html','Read the history file and append its contents to the history list.','HISTFILE selects a saved file (default ~/.bash_history). Startup reads entries into history; exit saves entries if enabled and writable. history -r reads without replay; fc and history substitution can re-execute entries. Bash executes startup files and uses PATH for command search.'),
'symlink':('https://man7.org/linux/man-pages/man7/symlink.7.html','A symbolic link is a special type of file','A symbolic link contains a pathname used to resolve access to another file.'),
'exec':('https://man7.org/linux/man-pages/man2/execve.2.html','execve() executes the program referred to by path.','Execution replaces the calling process image. Effective IDs can change for set-ID executables and capabilities; exact rights require instance evidence, not just an output filename.'),
}
with (root/'SOURCES.md').open('w') as f:
 f.write('# Primary documentation checked 2026-11-23 UTC\n\nDocumentation behavior is not a claim that a machine was observed. The pages describe their published versions; no tool version is assigned to a B1 template.\n')
 for key,(url,q,note) in D.items():f.write(f'\n## {key}\n\n[{key}]({url})\n\n> {q}\n\n{note}\n')
def src(k):return 'S2/parts/b1/SOURCES.md#'+k+' ('+D[k][0]+')'
objs=[]
def obj(fam,ch,name,form,producer,derive,execution,consumer,keys,origin='Generated locally in the described operation; not described as package-delivered bytes.',choice='No person-chosen value is specified; a person invokes the operation.',human='The described operation is initiated by a person; the named producer writes the output.'):
 objs.append(dict(family=fam,object='s2-'+str(len(objs)+1),machine='unspecified',name=name,channel=ch,form=form,producer=producer,derive=derive,execution=execution,consumer=consumer,keys=keys,origin=origin,choice=choice,human=human))
obj(13,'C8.08 a','<Firefox-profile>/prefs.js: activated theme preference','A selected preference value retained in the profile file','Firefox preference storage','User selection of a theme','The selected value is read by Firefox, not supplied as executable statements.','Firefox for the user of this profile',['pref','theme'],origin='The object is a user-chosen value stored in a profile; no package-supplied value is identified.',choice='A person chooses the theme in the described channel.',human='A person chooses the value; Firefox stores it.')
obj(13,'C8.08 b','<Firefox-profile>/prefs.js: home-page URL preference','A selected URL retained in the profile file','Firefox preference storage','User selection of a home page','The URL is read as a navigation value; this object is not the fetched page or its scripts.','Firefox for the user of this profile',['pref','home'],origin='The object is a user-chosen value stored in a profile; no package-supplied value is identified.',choice='A person chooses the home-page URL in the described channel.',human='A person chooses the value; Firefox stores it.')
obj(14,'C5.1 a','./a.out or <-o-path>','Native linked executable','GCC compilation/linking','C source and linker inputs','The channel specifies native output then execution as a process.','Operating-system execution of the built file',['gcc','exec'])
obj(14,'C5.1 b','./<name>.c','C source file','UNKNOWN: The writing program or creator of the source is not identified.','C source input; earlier origin not given','Compilation is needed before the native execution described; source is compiler input.','GCC reads source',['gcc'],origin='UNKNOWN: B1 names a C source input but gives no package-delivery provenance.',human='UNKNOWN: B1 names the source input but does not identify its creator or whether the operator brought it.')
obj(14,'C5.1 d','./<name>.o','Unlinked object file','GCC compilation/assembly','C source and compilation inputs','The described intermediate needs linking before execution; the linker consumes it.','Linker',['gcc'])
obj(14,'C5.2 a recipe','CMakeLists.txt','Project file with CMake-language commands','Project author','Project build instructions','CMake evaluates this project file; its command language can start child processes.','CMake configuring this project',['cmake','child'],origin='Project input; no package provenance is stated.',human='UNKNOWN: B1 names the project recipe without stating whether the invoking person wrote it or brought it.')
obj(14,'C5.2 a executable','<try_run COPY_FILE destination>','Copied configure-test executable','CMake try_run and invoked compiler/linker','Source files passed to try_run','try_run builds and runs a test executable; COPY_FILE retains it when requested.','CMake test execution and operating-system loader',['run','exec'])
obj(14,'C5.2 b cache','build/CMakeCache.txt: compile/run result entries','Cached result values','CMake try_run','Build success/failure and test exit result','CMake reads cached results as values.','CMake configuring this project',['run','cmake'],choice='These result values are calculated from compilation/run outcomes, rather than chosen by a person.')
obj(14,'C5.2 b log','<build>/CMakeFiles/CMakeConfigureLog.yaml: try_run event','YAML event in the configure log','CMake during configuration','Compile/run event details','The event is written/read as log data.','People or tools inspecting the configure log',['run','log'],choice='Event values are obtained from execution, rather than selected by a person.')
obj(14,'C5.3 a executable','<prefix>/bin/<program>','Executable copied by install rules','CMake-generated install operation','Built executable selected by project install rules','The copied target is an executable; launch uses the operating-system loader.','Programs/users invoking the installed path',['install','exec'])
obj(14,'C5.3 a library','<prefix>/lib/<library>.so','Shared library copied by install rules','CMake-generated install operation','Built library selected by project install rules','Shared-library machine code is loaded into a consuming process.','Program loading the library',['install'])
obj(14,'C5.3 b','build/cmake_install.cmake','Generated CMake script','CMake install() processing','Project install rules','Executed by generated install target, CPack, or cmake -P.','CMake install operation',['install','cmake','child'])
obj(14,'C5.3 c','<shell-startup-file>: PATH assignment','Persisted shell assignment','Person editing a shell startup file','Person-selected command-search path','Bash reads and executes startup-file statements; PATH changes command lookup.','Shell reading that file and processes receiving exported PATH',['bash'],origin='Person-written startup assignment; no package-delivered bytes identified.',choice='A person chooses the PATH assignment in the described channel.',human='Person writes the assignment.')
obj(14,'C5.3 d','<prefix>/bin/<alias>','Symbolic link to an executable','Person creating a link','Chosen target executable path','A link resolves to its target; invocation via the alias executes the target.','Command lookup/path resolution and target process',['symlink','exec'],origin='Person-created link; no package delivery is stated.',choice='A person chooses a launch alias and its target.',human='The person creates the link in the described channel.')
obj(14,'C5.4 a executable','./<program> (replacement)','Executable bytes replacing previous contents at the same path','Compiler/build operation','New source/build inputs replacing earlier output','Native executable can be started as a process in the described channel.','Programs/users invoking that path',['gcc','exec'])
obj(14,'C5.4 a library','./<library>.so (replacement)','Shared-library bytes replacing previous contents at the same path','Compiler/build operation','New source/build inputs replacing earlier output','Library code can execute within a process that loads it.','Program loading the replaced library',['gcc'])
obj(14,'C5.5 a','./<plugin>.so','Locally built compiler plugin shared library','Local compiler/linker build','Plugin source and build inputs','GCC loads the plugin into its own process; plugin extends compiler behavior.','GCC loading the plugin',['plugin','plugin-load','gcc'])
obj(14,'C5.5 b','<packaged-plugin-path>','Unchanged plugin obtained in an installed package','Package installation in the described channel','Installed package containing the plugin','GCC plugin module loaded into compiler process.','GCC loading the plugin',['plugin','plugin-load'],origin='The channel explicitly specifies an unchanged plugin obtained in an installed package.',human='A person using the channel selects a plugin; the package supplies its bytes.')
obj(14,'C5.5 c','./a.out or <-o-path> (plugin-enabled build)','Generated executable','Compiler/linker with plugin loaded','Source, linker inputs and compilation affected by the plugin','Linked output can execute as its own process in the described channel.','Operating-system loader',['gcc','plugin','exec'])
obj(15,'C7.06 b','~/.python_history','Saved interactive Python history entries','Interactive Python history facility','Retained user input from interactive sessions','History is loaded for recall/editing. Retained statements can be submitted to Python.','User-run interactive Python session',['python','readline'],choice='A person types input; the history facility chooses what to save under its configuration.',human='A person supplies input; the interpreter records the file.')
obj(15,'C7.17 c','<HISTFILE> (default ~/.bash_history)','Saved shell command text','Bash history facility','Retained shell history list entries','History reading populates a list; recalled commands can be executed through fc or history substitution.','User-run shell and its history facility',['bash'],choice='A person types commands; configured history filters affect which entries are retained.',human='A person supplies commands; Bash writes the file.')
rows=[]
def add(o,k,v,s): rows.append({**{x:o[x] for x in ['family','object','machine','name']},'fact':k,'value':v,'source':s})
for o in objs:
 scope='B1/fix-b1-1/CHANNELS-V4.tsv: '+o['channel']+' leaves column only'
 doc='; '.join(src(k) for k in o['keys'])
 add(o,'channel_object',o['channel'],scope)
 add(o,'evidence_scope','Documentation-defined disk object; no inventory instance is identified by B1.', 'B1/raw/root-sources.md: opening scope; B1/part-install/sources.md: opening scope; B1/fix-b1-1/raw/procedure.md: documentation-only procedure')
 add(o,'disk_form',o['form'],scope+'; '+doc)
 add(o,'package_origin',o['origin'],scope)
 add(o,'execution_behavior',o['execution'],scope+'; '+doc)
 add(o,'consumer',o['consumer'],scope+'; '+doc)
 add(o,'producer',o['producer'],scope+'; '+doc)
 add(o,'derivation',o['derive'],scope+'; '+doc)
 add(o,'person_choice',o['choice'],scope+'; '+doc)
 add(o,'human_creation_or_bringing',o['human'],scope)
 common={
 'observed_presence':'B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.',
 'exact_bytes_or_selected_value':'B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.',
 'package_name':'No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.',
 'package_version':'No delivering package version is given for an identified instance.',
 'producer_version':'No observed version of the writing/building program is given for an instance.',
 'actor_identity':'Only the generic role of a user is described; no person identity is recorded.',
 'choice_time':'No UTC choice time is recorded for an identified instance.',
 'production_time':'The documented producing operation has no observed run or UTC timestamp in B1.',
 'effective_rights':'B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.',
 'primary_description':'No person-designated primary description for this object is supplied by B1.',
 'source_build_line':'No exact source/build line for this object is supplied by B1.',
 'persistent_backing':'The channel specifies a saved file but names no observed filesystem backing or restart survival.',
 }
 for k,v in common.items():add(o,k,'UNKNOWN: '+v,scope+'; B1/raw/root-sources.md: generic parameter paths; D1/in/FACTS.md; A3/in/FACTS.md')
 if o['object']=='s2-18':add(o,'remains_as_received','Yes, stipulated by the channel description; not an observed digest comparison.',scope)
 elif o['object'] in ['s2-15','s2-16']:add(o,'remains_as_received','The channel specifies replacement by different bytes at the same path.',scope)
 else:add(o,'remains_as_received','UNKNOWN: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.',scope)
 add(o,'persistence','The channel names a saved disk file/value/link, not only a process.',scope)
 if o['family']==14:
  if o['object'] in ['s2-3','s2-4','s2-5','s2-15','s2-16','s2-17','s2-18','s2-19']:add(o,'channel_tool_purpose','GCC: compilation, including machine-code generation and plugin loading; this describes the compiler, not an unidentified package manager or source editor.',src('gcc-purpose')+'; '+src('plugin'))
  elif o['object']=='s2-13':add(o,'channel_tool_purpose','Bash: shell command execution and startup-file processing.',src('bash'))
  elif o['object']=='s2-14':add(o,'channel_tool_purpose','UNKNOWN: The channel does not identify the program used to create the link.',scope)
  else:add(o,'channel_tool_purpose','CMake: buildsystem generation, build operations and project installation from generated rules.',src('cmake')+'; '+src('install'))
 if o['object']=='s2-1':effect='The selected theme value selects Firefox appearance; no program invocation or login/access permission is specified for that value.'
 elif o['object']=='s2-2':effect='The selected URL causes Firefox to open a page on the documented triggers.'
 elif o['object']=='s2-14':effect='Invocation via the stored alias reaches the target executable; the link does not by itself record a login permission.'
 elif o['object']=='s2-13':effect='The assignment changes shell command lookup; an assignment alone does not start a command.'
 elif o['object']=='s2-6':effect='CMake commands in the recipe can invoke child processes; actual effects depend on its commands and caller permissions.'
 elif o['object']=='s2-12':effect='The generated CMake installation script executes installation rules that write destinations; actual effects depend on rules and caller permissions.'
 elif o['object'] in ['s2-8','s2-9']:effect='The named result/event values report compilation and execution; they are not commands in the documented file reader.'
 else:effect='UNKNOWN: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.'
 add(o,'launch_change_access_behavior',effect,scope+'; '+doc)
 if o['object'] in ['s2-11','s2-16']:add(o,'specific_consumer','UNKNOWN: B1 identifies a shared library but no named process or program that loads it.',scope)
 if o['object']=='s2-2':add(o,'additional_launch_or_access','UNKNOWN: No selected URL, protocol handler or target contents are recorded; behavior beyond page navigation cannot be established.',scope)
 if o['object'] in ['s2-20','s2-21']:add(o,'whole_file_executability','UNKNOWN: Actual retained bytes and interpreter state are absent; the validity of the entire file as a script cannot be established.',scope)
 if o['object'] in ['s2-6','s2-13','s2-14']:add(o,'writing_program','UNKNOWN: The editor or link-creation program is not named in the channel.',scope)
 if o['object'] in ['s2-17','s2-18']:add(o,'process_boundary','Loaded into the GCC process using dlopen or equivalent; no separate plugin process is specified.',src('plugin')+'; '+src('plugin-load'))
(root/'objects.json').write_text(json.dumps(objs,indent=2)+'\n')
with (root/'facts.tsv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['family','object','machine','name','fact','value','source'],delimiter='\t');w.writeheader();w.writerows(rows)
titles={13:'a browser\'s home page and “launches something”',14:'a compiler or a build tool as a built-in tool or as general-purpose work',15:'saved history as values read or as executable statements'}
with (root/'FACTS.md').open('w') as f:
 f.write('# Facts for families 13–15\n\n21 disk-object examples are retained from the eight named channels. Where a channel lists an executable or a shared library, each receives a separate ID. Typed commands and runtime-only processes are not added. Family 15 retains only the two history objects named by its card.\n\nB1 describes documented channels, not measured instances. `unspecified` is not a machine. Path templates are preserved and do not assert existence. No inventory ID or operator run is linked in B1, so an unrelated inventory object is not substituted. Historical bytes, identities and times cannot be recovered by a fresh probe. Documented semantics were checked in primary sources before considering probes; no fresh machine was needed for those semantics.\n\nThe precise facts and their sources are in `facts.tsv`. `SOURCES.md` contains short checked quotations and primary URLs. No classification columns are included. UNKNOWN counts here count rows, not different people or hypotheses.\n')
 for fam in titles:
  f.write(f'\n## {fam}. {titles[fam]}\n\n')
  for o in objs:
   if o['family']!=fam:continue
   f.write(f'### {o["object"]} — {o["name"]}\n\nChannel: {o["channel"]}. {o["form"]}. Producer: {o["producer"]}. Derived from: {o["derive"]}. {o["execution"]}\n\nUnknown facts:\n\n')
   for r in rows:
    if r['object']==o['object'] and r['value'].startswith('UNKNOWN:'):f.write(f'- `{r["fact"]}`: {r["value"][9:]}\n')
 print('objects',len(objs),'rows',len(rows),'unknown',sum(r['value'].startswith('UNKNOWN:') for r in rows))
