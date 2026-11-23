# External development controller; final acceptance reruns the complete installed suite.
import pathlib
text=pathlib.Path('/usr/local/lib/stand/round4-selftest.py').read_text()
exec(compile(text.split("session('USER-SERVICE-PROGRAM'",1)[0],'<installed ordinary suite prefix>','exec'))
document('ordinary-document.txt','First document\n')
session('DOCUMENT-EDIT','run','/usr/bin/red','ordinary-document.txt',data=b'1c\nEdited document\n.\nw\nq\n')
session('DOCUMENT-READ','run','/usr/bin/cat','/home/stand/ordinary-document.txt',contains='Edited document')
session('EDITOR-SHELL-REFUSED','run','/usr/bin/red','ordinary-document.txt',data=b'!id\nq\n',success=False)
session('EDITOR-COMMAND-READ-REFUSED','run','/usr/bin/red','ordinary-document.txt',data=b'r !id\nq\n',success=False)
command('FOCUSED-RESTORE-FACTORY',['/usr/local/bin/stand-apply','/etc/stand/factory'])
command('FOCUSED-VERIFY',['/usr/local/bin/stand-verify'])
record(phase='summary',passed=not failures,failures=failures)
sys.exit(bool(failures))
