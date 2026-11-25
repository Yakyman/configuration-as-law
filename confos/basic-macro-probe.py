#!/usr/bin/python3
"""Guest probe: is a saved Basic library of the office suite executed?

Usage (in the guest, as the ordinary account with sudo): basic-macro-probe.py ran|refused
The library (one module whose Main writes a file with Basic statements and starts an external
program) is saved, never recorded. Routes: the profile the suite uses by default and a profile
named by an option of the command; the library below the home folder and below /tmp (a profile
there, the profile's library folder linked there, a library linked from the profile's index);
the macro named by a macro address and by a script address; each as the ordinary account and
as root. Before each attempt the same profile converts a document, which shows that the suite
starts there. `ran` expects every attempt of the ordinary account to execute the library (a
system without the guard); `refused` expects that no attempt executes it.
"""
import json
import os
import shutil
import subprocess as sp
import sys
from pathlib import Path
from xml.sax.saxutils import escape

expect = sys.argv[1]
assert expect in ('ran', 'refused')
LIB = 'http://openoffice.org/2000/library'
CODE = '''Sub Main
Dim n As Integer
n = FreeFile
Open "/tmp/basic-macro-marker-basic" For Output As #n
Print #n, "BASIC-CODE-RAN"
Close #n
Shell("/usr/bin/touch", 0, "/tmp/basic-macro-marker-shell", True)
StarDesktop.terminate()
End Sub
'''
MODULE = ('<?xml version="1.0" encoding="UTF-8"?><script:module xmlns:script="http://openoffice.org/2000/script" '
          'script:name="Module1" script:language="StarBasic">'+escape(CODE)+'</script:module>\n')


def index(libraries):
    body = ''.join(f'<library:library library:name="{name}" '+(
        f'xlink:href="{link}" xlink:type="simple" library:link="true" library:readonly="false"/>' if link
        else 'library:link="false"/>') for name, link in libraries)
    return (f'<?xml version="1.0" encoding="UTF-8"?><library:libraries xmlns:library="{LIB}" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink">{body}</library:libraries>\n')


def library(name):
    return (f'<?xml version="1.0" encoding="UTF-8"?><library:library xmlns:library="{LIB}" library:name="{name}" '
            'library:readonly="false" library:passwordprotected="false"><library:element library:name="Module1"/>'
            '</library:library>\n')


MARKERS = [Path('/tmp/basic-macro-marker-basic'), Path('/tmp/basic-macro-marker-shell')]
declaration = Path('/state/declaration.conf').read_bytes()
results = []


def run(who, home, arguments, limit=25):
    command = ['timeout', '-k', '2', str(limit), 'libreoffice', *arguments]
    if who == 'root':
        command = ['sudo', '-n', 'env', 'HOME='+home, *command]
        environment = None
    else:
        environment = dict(os.environ, HOME=home)
    done = sp.run(command, capture_output=True, env=environment, timeout=limit+15)
    print('COMMAND', who, 'HOME='+home, ' '.join(arguments), 'EXIT', done.returncode,
          'OUT', repr(done.stdout[-300:]), 'ERR', repr(done.stderr[-300:]), flush=True)
    return done


def write(who, path, text):
    if who == 'root':
        sp.run(['sudo', '-n', 'mkdir', '-p', str(path.parent)], check=True)
        sp.run(['sudo', '-n', 'tee', str(path)], input=text.encode(), stdout=sp.DEVNULL, check=True)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)


def attempt(who, name, home, profile_option, basic, libraries, extra, address):
    """home: HOME of the command; profile_option: profile folder given by -env, or None for the default;
    basic: the folder that holds the library index; libraries: [(name, link)]; extra: {path: text}."""
    option = ['-env:UserInstallation='+Path(profile_option).as_uri()] if profile_option else []
    if who == 'root':
        sp.run(['sudo', '-n', 'mkdir', '-p', home], check=True)
    else:
        Path(home).mkdir(parents=True, exist_ok=True)
    document = Path('/tmp')/f'basic-macro-document-{who}-{name}.txt'
    write(who, document, 'DOCUMENT-CONTROL\n')
    # The first start creates the profile; it also shows that the suite works in this place.
    control = run(who, home, [*option, '--headless', '--convert-to', 'odt', '--outdir', '/tmp', str(document)], 60)
    converted = control.returncode == 0 and document.with_suffix('.odt').exists()
    if converted:
        # Ordinary work with the same profile: the converted document is read back.
        back = run(who, home, [*option, '--headless', '--cat', str(document.with_suffix('.odt'))], 60)
        converted = b'DOCUMENT-CONTROL' in back.stdout
    for path, text in extra.items():
        write(who, Path(path), text)
    write(who, Path(basic)/'script.xlc', index(libraries))
    for library_name, link in libraries:
        folder = Path(link.removeprefix('file://')).parent if link else Path(basic)/library_name
        write(who, folder/'script.xlb', library(library_name))
        write(who, folder/'Module1.xba', MODULE)
    sp.run(['sudo', '-n', 'rm', '-f', *map(str, MARKERS)], check=True)
    done = run(who, home, [*option, '--headless', '--norestore', address])
    observed = [marker.exists() for marker in MARKERS]
    sp.run(['sudo', '-n', 'pkill', '-x', 'soffice.bin'], capture_output=True)
    sp.run(['sudo', '-n', 'rm', '-f', *map(str, MARKERS)], check=True)
    row = {'account': who, 'route': name, 'suite_starts': converted, 'exit': done.returncode,
           'basic_ran': observed[0], 'external_program_ran': observed[1]}
    results.append(row)
    print('MACRO_RESULT', json.dumps(row, sort_keys=True), flush=True)


standard = [('Standard', None)]
for who in ('user', 'root'):
    base = '/home/user/basic-macro-'+who
    tmp = '/tmp/basic-macro-'+who
    default = '/.config/libreoffice/4/user/basic'
    # Root of a session has no right to pass the permissions of another account's folder
    # (`mkdir: cannot create directory '/home/user/basic-macro-root': Permission denied` on
    # 0.52), so the person opens one folder of the home to everyone for the attempts of root.
    Path(base).mkdir(exist_ok=True)
    Path(base).chmod(0o777 if who == 'root' else 0o755)
    # 1. the default profile, below the home folder
    attempt(who, 'default-profile-home', base+'/h1', None, base+'/h1'+default, standard, {}, 'macro:///Standard.Module1.Main')
    # 2. the default profile of a home below /tmp
    attempt(who, 'default-profile-tmp', tmp+'/h2', None, tmp+'/h2'+default, standard, {}, 'macro:///Standard.Module1.Main')
    # 3. the default profile below the home folder, a library below /tmp linked from its index
    attempt(who, 'default-profile-linked-tmp', base+'/h3', None, base+'/h3'+default,
            [('Standard', None), ('Saved', 'file://'+tmp+'/linked/Saved/script.xlb')], {}, 'macro:///Saved.Module1.Main')
    # 4. a profile below the home folder given by an option
    attempt(who, 'option-profile-home', base+'/h4', base+'/p4', base+'/p4/user/basic', standard, {}, 'macro:///Standard.Module1.Main')
    # 5. a profile below /tmp given by an option
    attempt(who, 'option-profile-tmp', base+'/h5', tmp+'/p5', tmp+'/p5/user/basic', standard, {}, 'macro:///Standard.Module1.Main')
    # 6. the script address instead of the macro address
    attempt(who, 'option-profile-home-script-address', base+'/h6', base+'/p6', base+'/p6/user/basic', standard, {},
            'vnd.sun.star.script:Standard.Module1.Main?language=Basic&location=application')
assert Path('/state/declaration.conf').read_bytes() == declaration
ran = [row for row in results if row['basic_ran'] or row['external_program_ran']]
started = [row for row in results if row['suite_starts']]
print('BASIC MACRO PROBE', len(results), 'attempts;', len(started), 'in a place where the suite converts a document;',
      len(ran), 'executed the saved library', flush=True)
if expect == 'ran':
    missing = [row for row in results if row['account'] == 'user' and not (row['basic_ran'] and row['external_program_ran'])]
    assert not missing, missing
    print('BASIC MACRO CONTROL PASS: every attempt of the ordinary account executed the saved library')
else:
    assert not ran, ran
    assert all(row['suite_starts'] for row in results), [row for row in results if not row['suite_starts']]
    print('BASIC MACRO REFUSED PASS: no attempt executed the saved library')
