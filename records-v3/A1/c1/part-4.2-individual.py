exec(open('A1/c1/part-4.2-classify.py').read().split('for i,x in enumerate(rows):')[0])
base='https://raw.githubusercontent.com/Millak/guix/master/'
# Entries were examined individually against the generators and observations.
E={
17:('MUST','Bundles certificate authorities used to verify remote endpoints.','S2.2-1,S2.2-2','guix/profiles.scm','Removing trust anchors prevents certificate verification for programs requiring this bundle.'),
28:('NOT','Indexes installed documentation in the Info directory.','S2.2-4','guix/profiles.scm','The index is documentation content; its removal loses those navigation entries, not the reader capability.'),
29:('MUST','Unites kernel modules and records their loading dependencies.','S2.2-1,S2.2-2','guix/profiles.scm','This object exposes loadable kernel code and its dependency relationships; removal prevents module loading through it.'),
32:('MUST','Defines administrative authorization for the wheel group.','S2.2-10,S2.2-15','gnu/services/desktop.scm','Executable authorization rules determine administrative rights, explicitly within required recording.'),
41:('UNKNOWN','Exact profile composition is unestablished.','S3-2','none','The generic store name does not identify this profile’s linked contents or runtime role.'),
43:('UNKNOWN','The client configuration’s consumer and values are unestablished.','S3-2','none','The name is shared by unrelated clients; inventory provides neither contents nor a consumer link.'),
52:('UNKNOWN','Exact policy directory contents are unestablished.','S3-2','none','The store basename alone does not enumerate policies or establish their effects.'),
65:('UNKNOWN','Exact stored firmware collection and loading role are unestablished.','S3-2','none','No inventory member list or device loading evidence identifies what this generated object supplies.'),
71:('MUST','Directs device management to the system device rules directory.','S2.2-1,S2.2-2','gnu/services/base.scm','The generated setting selects system device rules; these determine device access and initialization outside a single interface.'),
76:('HOLE','Supplies protocol headers used to build X Window software.','S2.2-1,S2.2-2,S2.2-4','gnu/packages/xorg.scm','Headers enable compilation but also constitute source content; the text does not distinguish capability loss from unavailable development content.'),
81:('MUST','Selects the system time zone for programs reading that setting.','S2.2-1,S2.2-2','gnu/system.scm','The system setting determines local time interpretation across programs, rather than only one program’s interface.'),
87:('MUST','Defines authentication rules for graphical login.','S2.2-15','gnu/services/xorg.scm','Login authentication controls which access is permitted; the password-login rule is explicitly recordable.'),
110:('HOLE','Configures power monitoring and low-battery actions.','S2.2-1,S2.2-7','gnu/services/desktop.scm','One daemon reads the settings, but they govern machine power actions; the text does not define where settings are in force.'),
112:('UNKNOWN','Exact generated device-management directory contents are unestablished.','S3-2','none','The observed link identifies a directory, but its inventory does not enumerate all rules or executable helpers.'),
117:('MUST','Defines authentication rules for changing account information.','S2.2-1,S2.2-2,S2.2-15','gnu/system/pam.scm','The generated PAM policy controls account-changing access, rather than being the similarly named executable.'),
129:('MUST','Makes locale definitions available to multiple runtime library versions.','S2.2-1,S2.2-2','gnu/system.scm','Removing system locale definitions prevents configured locale selection and associated character handling.'),
136:('HOLE','Configures audio library device and routing behavior.','S2.2-1,S2.2-7','none','The text does not distinguish settings inside a shared audio library from settings governing every application using it.'),
143:('HOLE','Configures name-service cache behavior.','S2.2-1,S2.2-5,S2.2-7','gnu/services/base.scm','Daemon settings affect many clients; the text does not say whether their force remains inside the daemon or extends to clients.'),
159:('UNKNOWN','Exact authentication policy or executable role is unestablished.','S3-2','none','The unversioned name can identify a screen-locker program or its PAM policy; the object contents are unavailable.'),
160:('UNKNOWN','Exact compiled module contents and consumers are unestablished.','S3-2','none','The generic compiled-import directory lacks a saved member list or matching loader reference.'),
177:('MUST','Sets group ownership and permissions for the virtualization device.','S2.2-1,S2.2-2','gnu/services/base.scm','The rule decides access to the virtualization device, affecting what users can do on the computer.'),
179:('MUST','Denies authentication for applications lacking a specific PAM policy.','S2.2-15','gnu/system/pam.scm','The generated fallback authentication policy denies access and therefore determines login permission.'),
181:('HOLE','Supplies display-server configuration fragments from installed modules.','S2.2-1,S2.2-7','gnu/services/xorg.scm','One server reads the fragments but controls display behavior for many clients; the text leaves the scope of internal settings undefined.'),
186:('NOT','Supplies the package manager’s user manual.','S2.2-4','guix/self.scm','Manuals are documentation content; removing them removes that content rather than the documented commands.'),
189:('MUST','Configures graphical login launch commands and authentication integration.','S2.2-1,S2.2-2,S2.2-15','gnu/services/xorg.scm','The login manager configuration controls login and launched sessions, which extend beyond its own interface.'),
191:('MUST','Provides the running system kernel and associated kernel functionality.','S2.2-1,S2.2-2','raw:guix/guix-system-description.txt','The system description identifies this kernel; removing it prevents booting and executing the operating system.'),
194:('UNKNOWN','Exact kernel parameter assignments are unavailable.','S3-2','none','No saved contents identify which kernel parameters this particular generated configuration changes.'),
203:('NOT','Provides decorative package-manager icons.','S2.2-4','gnu/system.scm','Icons are image content; their removal removes those images while leaving programs’ operations available.'),
204:('MUST','Provides UTF-8 locale definitions to runtime libraries.','S2.2-1,S2.2-2','gnu/packages/base.scm','Runtime locale availability determines character handling and locale selection; this is operational input rather than merely displayed content.'),
208:('MUST','Maps host names to network addresses.','S2.2-1,S2.2-2','gnu/services/base.scm','System name mappings determine destinations reachable by configured names across programs.'),
224:('HOLE','Provides shared desktop widget styling.','S2.2-1,S2.2-4,S2.2-7','gnu/packages/xfce.scm','Theme content is exempt within one program; the text does not specify whether a theme shared across applications remains exempt.'),
228:('MUST','Provides compiled locale definitions for runtime formatting and character handling.','S2.2-1,S2.2-2','gnu/system.scm','Without the selected definitions the runtime cannot select those system locales or perform their locale-dependent operations.'),
233:('NOT','Provides graphical glyph content for a typeface.','S2.2-4','gnu/packages/fonts.scm','Removing the typeface removes its glyph content; text rendering software remains capable of rendering available content.'),
245:('MUST','Supplies shared rules identifying file content types.','S2.2-1,S2.2-2','gnu/packages/freedesktop.scm','Applications depend on these operational classification rules to recognize formats; removal loses recognition rather than only database contents for viewing.'),
252:('UNKNOWN','Exact display configuration contents are unavailable.','S3-2','none','The basename does not establish whether the file contains executable setup or only display-server values.'),
259:('MUST','Defines authentication permission for account creation.','S2.2-1,S2.2-2,S2.2-15','gnu/system/pam.scm','The generator emits a root-permission PAM policy for account creation, controlling administrative access.'),
260:('UNKNOWN','Exact imported module contents and consumers are unestablished.','S3-2','none','The generic module-import directory lacks a saved member list or matching loader reference.'),
263:('MUST','Defines audio hardware use-case setup.','S2.2-1,S2.2-2','gnu/packages/linux.scm','Device use-case definitions permit usable audio configurations; removal loses device setup capabilities across audio applications.'),
270:('MUST','Directs message-bus activation through the session-service synchronization wrapper.','S2.2-1,S2.2-2','gnu/services/desktop.scm','The generated service entry changes which executable starts the system session manager; removal prevents that activation route.'),
274:('HOLE','Configures system login-session and power-management policy.','S2.2-1,S2.2-7','gnu/services/desktop.scm','A single daemon consumes these settings but their effects govern system sessions; the text leaves the boundary of internal settings undefined.'),
279:('NOT','Provides bitmap glyph content for display fonts.','S2.2-4','gnu/packages/xorg.scm','Font glyphs are display content; removing these glyphs leaves rendering programs and other content available.'),
281:('UNKNOWN','The exact package-cache representation and regeneration behavior are unestablished.','S3-2','none','The basename says cache, but no contents or consumer evidence establishes whether removal only slows operation.'),
299:('UNKNOWN','Exact profile composition is unestablished.','S3-2','none','The generic store name does not identify this profile’s linked contents or runtime role.'),
305:('NOT','Supplies decorative desktop icon images.','S2.2-4','gnu/packages/xfce.scm','Removing the icon collection removes image content rather than the applications’ ability to operate.'),
306:('UNKNOWN','The wrapper’s executable contents are unavailable.','S3-2','none','The name suggests a power-service wrapper, but neither saved contents nor an exact generator match establishes its operations.'),
313:('MUST','Sets environment variables inherited by login sessions.','S2.2-1,S2.2-2','gnu/system/pam.scm','Session environment values influence subsequently launched programs, extending beyond the authentication module that reads them.'),
323:('UNKNOWN','Exact shell startup directory contents are unavailable.','S3-2','none','The directory link is observed, but members and whether any executable startup file exists are not enumerated.'),
331:('MUST','Configures which applications may request location information.','S2.2-1,S2.2-2','gnu/services/desktop.scm','The generated whitelist controls cross-application access to location information, affecting what those applications can obtain.'),
338:('MUST','Defines keyboard layouts used by the display input stack.','S2.2-1,S2.2-2','gnu/packages/xorg.scm','Removing layout definitions loses selectable input mappings across applications, rather than only displayed content.'),
349:('NOT','Indexes installed documentation in the Info directory.','S2.2-4','guix/profiles.scm','The index is documentation content; its removal loses those navigation entries, not the reader capability.'),
350:('MUST','Provides system authentication policies for services.','S2.2-15','gnu/system/pam.scm','The aggregate supplies login and administrative authentication rules, whose permission settings must be recorded.'),
351:('UNKNOWN','Exact compiled module contents and consumers are unestablished.','S3-2','none','The generic compiled-import directory lacks a saved member list or matching loader reference.'),
354:('UNKNOWN','Exact service-discovery settings are unavailable.','S3-2','none','No saved contents identify whether the particular file changes publication, access, networking, or only internal service preferences.'),
357:('NOT','Provides desktop background pictures.','S2.2-4','gnu/packages/gnome.scm','Pictures are expressly exempt content; their removal removes those pictures rather than display capability.'),
364:('MUST','Provides the selected operating-system generation and its boot configuration.','S2.2-1,S2.2-2','raw:guix/guix-system-description.txt','The current generation contains the selected kernel and boot setup; removing it prevents booting that configured system.'),
368:('MUST','Maps display font names to available font resources.','S2.2-1,S2.2-2','gnu/packages/xorg.scm','Alias rules determine whether named font requests resolve; they are operational mappings rather than glyph content.'),
375:('MUST','Defines package source channels as executable Scheme expressions.','S2.2-10,S2.2-13','gnu/services/base.scm','Channel specifications are evaluated Scheme code; settings expressed as executed code must be recorded.'),
380:('HOLE','Indexes installed manual pages for lookup.','S2.2-1,S2.2-4,S2.2-5','guix/profiles.scm','The text does not distinguish documentation index content from lost lookup functionality when an index is removed.'),
385:('NOT','Supplies translated package-manager message text.','S2.2-4','guix/self.scm','Message translations are text content; removing them removes those translations while commands still operate.'),
388:('HOLE','Supplies protocol specifications used for generating display-client code.','S2.2-1,S2.2-2,S2.2-4','gnu/packages/freedesktop.scm','Protocol descriptions are content but enable code generation; the text does not distinguish lost development inputs from lost capabilities.'),
397:('UNKNOWN','Indexes input-method modules; removal behavior is unestablished.','S3-2','guix/profiles.scm','The generator calls this a cache, but available evidence does not establish whether GTK regenerates it or loses input methods.'),
402:('MUST','Defines authentication rules for privilege escalation.','S2.2-15','gnu/system/pam.scm','The generated PAM policy determines permission to become superuser, explicitly required to be recorded.'),
403:('UNKNOWN','Exact unversioned daemon-named object function is unestablished.','S3-2','none','The basename may identify configuration, a wrapper, or another generated artifact; contents are absent.'),
405:('MUST','Provides compiled locale definitions for runtime formatting and character handling.','S2.2-1,S2.2-2','gnu/system.scm','Without the selected definitions the runtime cannot select those system locales or perform their locale-dependent operations.'),
415:('NOT','Provides recorded sound samples for desktop events.','S2.2-4','gnu/packages/freedesktop.scm','Sound samples are media content; their removal removes those recordings rather than the playback capability.'),
417:('MUST','Defines the operating system as evaluated Scheme configuration.','S2.2-10,S2.2-13','raw:guix/configuration/run/current-system/configuration.scm','This is executable Scheme configuration evaluated by the system builder with its interpreter’s rights.')
}
for i,(decision,what,sentences,source,reason) in E.items():
 x=rows[i]
 if x['id'] in finished:continue
 basis=source if source.startswith('raw:') or source=='none' else 'doc:'+base+source
 if i==136:basis='raw:guix/files.tsv'
 emit(x,decision,sentences,what,basis,reason,'individual')
# Named build nodes explicitly generated as executable Scheme modules.
for i in [78,88,92,100,108,133,146,209,294,355,404]:
 x=rows[i]
 emit(x,'MUST','S2.2-2,S2.2-10','Provides executable package-management Scheme modules.','doc:'+base+'guix/self.scm','These generated module nodes supply interpreter-executed package management operations; removal prevents using their procedures.','M')
f.close();json.dump(log,open(root/'part-4.2-rules.json','w'));print('Written',len(finished))
for i,x in enumerate(rows):
 if x['id'] not in finished:print(i,x['name'].split('-',1)[1])
