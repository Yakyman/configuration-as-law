exec(open('A1/c1/part-4.2-classify.py').read().split('for i,x in enumerate(rows):')[0])
base='doc:https://raw.githubusercontent.com/Millak/guix/master/'
for i,x in enumerate(rows):
 n=x['name'].split('-',1)[1]
 if x['id'] in finished:continue
 if n.startswith('shepherd-') and n.endswith('.scm'):
  emit(x,'MUST','S2.2-10,S2.2-13','Defines executable service lifecycle and registration code.','doc:https://codeberg.org/guix/guix/raw/commit/d58da8a56b75af73a7b5466f7ef8a81679713aa3/gnu/services/shepherd.scm','Service definitions are Scheme code executed with interpreter rights, including when they contain configuration.','S')
 elif n=='shepherd.conf':
  emit(x,'MUST','S2.2-10,S2.2-13','Loads service definitions and starts configured services.','raw:guix/system-boot.scm','Boot explicitly passes this file as the service manager configuration; that configuration is executed Scheme.','individual')
 elif n in {'module-import','module-import-compiled'}:
  # Raw activation supplies particular path-to-loader link; others have only names.
  raw=open('A1/in/raw/guix/configuration/run/current-system/activate').read()
  if x['name'] in raw:
   emit(x,'MUST','S2.2-10','Supplies Scheme activation modules to the interpreter.','raw:guix/configuration/run/current-system/activate','Activation adds this object to its module loading paths before importing system activation procedures.','individual')
 elif n in {'emacs-subdirs'}:
  emit(x,'MUST','S2.2-10,S2.2-13','Adds installed editor package directories to the editor code search path.',base+'guix/profiles.scm','Generated subdirs.el is editor Lisp executed with editor rights; executable configuration is expressly recorded.','individual')
 elif n in {'set-up-network','tear-down-network','validate-guix-ownership'}:
  what={'set-up-network':'Configures network addresses, links and routes.','tear-down-network':'Removes configured network addresses and routes.','validate-guix-ownership':'Validates and adjusts ownership of the package store and associated files.'}[n]
  emit(x,'MUST','S2.2-9,S2.2-10',what,base+'gnu/services/base.scm','The generator creates an executable program, providing a capability lost on removal.','individual')
 elif n=='elogind-dbus-shepherd-sync':
  emit(x,'MUST','S2.2-9,S2.2-10','Coordinates session management startup between the message bus and service manager.',base+'gnu/services/desktop.scm','This program executes service management procedures with interpreter rights.','individual')
 elif n=='startx':
  emit(x,'MUST','S2.2-9,S2.2-10','Starts the graphical display server using configured modules and fonts.',base+'gnu/services/xorg.scm','The generator creates an executable launch program; removal prevents this launch operation.','individual')
 elif n=='usb_modeswitch-sh':
  emit(x,'MUST','S2.2-9,S2.2-10','Dispatches mode switching when suitable USB devices are detected.',base+'gnu/services/networking.scm','This executable wrapper performs USB device mode switching with interpreter rights.','individual')
f.close();json.dump(log,open(root/'part-4.2-rules.json','w'));print('Written',len(finished))
