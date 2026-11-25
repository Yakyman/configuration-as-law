# Written by tools/make-search-cases.py — do not edit; run the program again.
# Inputs (sha256):
#   attempts/202-apt-mark-hold-recorded.sh  cf935aad7446ceefdb0723d47e619361fc96c1ef09da6217249363c026050180
#   attempts/234-root-crontab-for-account.sh  4540e34ad1da330c52381d61328f51e429b88e37588218a993ef2b14d55fc8d4
#   attempts/241-curlrc-obeyed.sh  1a7ce7f44f86d8b81c85e4af6ab31d85e4f164ad22da77d81030e932921d162f
#   build/IMPOSSIBLE.md  e23656437b51f08aca0b804dd3615092a7db2e71463670b072e93655173a4c7c
#   build/lo-macro-private-inputs.py  c6d1052eddce417b8bf78221abd8ca29044fe183dc7a748165332e710c906995
#   routes/054-python-pdbrc.sh  1d374604da6d2e1523ac13dbb95e9d59789b2e44cd8b043442725ad9dcdcde7f
#   routes/056-gyp-command-expansion.sh  2257077d27630632253e7ce2dd776ca3e8a4a265966f19df772338f47fa0f615
#   routes/089-ed-script-stdin.sh  98907e976d584eead07443390eeebbc606d0db4e6a774bc5b075882b224af529
#   routes/090-busybox-vi-exinit.sh  2ee9d90748ef7611bc884b30b0d52adbf9ebf1c211b72696f473dec2a8cd7821
#   routes/107-ssh-config-proxycommand.sh  23bd670d87994de38eeec374752856bd79cfe946dd6b65db47c69d9c889453eb
#   routes/108-ssh-config-match-exec.sh  25fae29cd1cee1a81c44bddc3fed30eefbea420a7bba7894a0b98b01e0ef1915
#   routes/111-apt-config-pre-invoke.sh  d87a001e68ff5258140b32e224746ea99e2f679ab4b96cf32cae2de3715cdf73
#   routes/135-mpv-user-script.sh  bb48ccc966bddaa2311e995a832dd5f7f1bdf0a77de10c1fe07db373cda1b88d
#   routes/136-mpv-script-flag.sh  a0c4b399f1f5f24f1f869e8555b7cf753f5edd84ad7a51d53e2d675fb0e4bb58
#   routes/160-flatpak-run-python-file.sh  2c6be8fd80c3ee7cefdb06ca5657c93c0233746f3c922032a1beca9c8d2c6387
#   routes/161-flatpak-run-sh-stdin.sh  b6a8f90d439173f8a2d52832fa9100f3220dedf1847eef3c71aed1409ede9173
#   routes/162-flatpak-run-sh-tmp.sh  e1b8f96cfedc2efce19ce4dd491d8430d1228120dfd0e4334c46b696d1c86a09
#   routes/166-flatpak-run-sh-cwd-dot.sh  824900492eaf242bd059f00cfcb4d7eccc11c75c788061c64f5f4af6a81e8666
#   routes/167-mpv-conf-script-option.sh  fb71aa080f64026d42d95d5761366c093ef26f2a1e63be46b45554cdaf6a0d4e
#   search/attempts-0.32.tsv  7dec22a6352c107adad8eecbbe8262dda46d618ab4215638093d4e7c56a164d3
#   search/routes-0.32.tsv  bdf1b01eb7b8aa24178f77aff062765594b71f17cf21e62a8fbd1ea820ed5775
# Not taken: attempt 256: counted RAN by the catalogue only because its last command ended with status 0; its recorded output is the refusal (nsenter: reassociate to namespaces failed: Operation not permitted); not a success
SEARCH_CASES = [{'id': 'P4-S-054',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '054',
  'script': 'search/routes/054-python-pdbrc.sh',
  'program': 'pdb (.pdbrc)',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 054\n'
             '# NAME: python-pdbrc\n'
             '# PROGRAM: pdb (.pdbrc)\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             '# COMMAND: printf \'import os; open("/tmp/mark-054","w").close()\\nq\\n\' > .pdbrc && echo \'x=1\' > '
             't.py && python3 -m pdb t.py < /dev/null\n'
             '# NOTE: \n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-054; W=/home/person/r/054; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             '\n'
             'echo "COMMAND: printf \'import os; open(\\"/tmp/mark-054\\",\\"w\\").close()\\nq\\n\' > .pdbrc && echo '
             '\'x=1\' > t.py && python3 -m pdb t.py < /dev/null"\n'
             '{ printf \'import os; open("/tmp/mark-054","w").close()\\nq\\n\' > .pdbrc && echo \'x=1\' > t.py && '
             'python3 -m pdb t.py < /dev/null\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e /tmp/mark-054 ]; then echo "RESULT RAN"; else echo "RESULT REFUSED exit=$rc: $(tr \'\\n\' \' '
             '\' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e /tmp/mark-054 ]', 'exit0')],
  'made': [('obeyed', '~/r'), ('obeyed', '~/r/054'), ('obeyed', '~/r/054/**')]},
 {'id': 'P4-S-056',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '056',
  'script': 'search/routes/056-gyp-command-expansion.sh',
  'program': 'gyp',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 056\n'
             '# NAME: gyp-command-expansion\n'
             '# PROGRAM: gyp\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             '# COMMAND: printf "{\'variables\': {\'v\': \'<!(touch /tmp/mark-056)\'}, \'targets\': []}\\n" > p.gyp '
             '&& gyp --depth=. --format=make p.gyp\n'
             '# NOTE: \n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-056; W=/home/person/r/056; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             '\n'
             'echo "COMMAND: printf \\"{\'variables\': {\'v\': \'<!(touch /tmp/mark-056)\'}, \'targets\': []}\\n\\" '
             '> p.gyp && gyp --depth=. --format=make p.gyp"\n'
             '{ printf "{\'variables\': {\'v\': \'<!(touch /tmp/mark-056)\'}, \'targets\': []}\\n" > p.gyp && gyp '
             '--depth=. --format=make p.gyp\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e /tmp/mark-056 ]; then echo "RESULT RAN"; else echo "RESULT REFUSED exit=$rc: $(tr \'\\n\' \' '
             '\' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e /tmp/mark-056 ]', 'exit0')],
  'made': [('obeyed', '~/r'), ('obeyed', '~/r/056'), ('obeyed', '~/r/056/**')]},
 {'id': 'P4-S-089',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '089',
  'script': 'search/routes/089-ed-script-stdin.sh',
  'program': 'ed',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 089\n'
             '# NAME: ed-script-stdin\n'
             '# PROGRAM: ed\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             "# COMMAND: printf '!touch /tmp/mark-089\\nq\\n' > p.ed && ed -s < p.ed\n"
             '# NOTE: \n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-089; W=/home/person/r/089; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             '\n'
             'echo "COMMAND: printf \'!touch /tmp/mark-089\\nq\\n\' > p.ed && ed -s < p.ed"\n'
             "{ printf '!touch /tmp/mark-089\\nq\\n' > p.ed && ed -s < p.ed\n"
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e /tmp/mark-089 ]; then echo "RESULT RAN"; else echo "RESULT REFUSED exit=$rc: $(tr \'\\n\' \' '
             '\' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e /tmp/mark-089 ]', 'exit0')],
  'made': [('obeyed', '~/r'), ('obeyed', '~/r/089'), ('obeyed', '~/r/089/**')]},
 {'id': 'P4-S-090',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '090',
  'script': 'search/routes/090-busybox-vi-exinit.sh',
  'program': 'vi (busybox, .exrc)',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 090\n'
             '# NAME: busybox-vi-exinit\n'
             '# PROGRAM: vi (busybox, .exrc)\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             '# COMMAND: printf \':!touch /tmp/mark-090\\n\' > ~/.exrc && timeout -s KILL 20 python3 -c "import '
             'pty,os; pty.spawn([\'vi\',\'-c\',\':q\',\'/home/person/r/090/x\'])" < /dev/null\n'
             '# NOTE: \n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-090; W=/home/person/r/090; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             '\n'
             'echo "COMMAND: printf \':!touch /tmp/mark-090\\n\' > ~/.exrc && timeout -s KILL 20 python3 -c '
             '\\"import pty,os; pty.spawn([\'vi\',\'-c\',\':q\',\'/home/person/r/090/x\'])\\" < /dev/null"\n'
             '{ printf \':!touch /tmp/mark-090\\n\' > ~/.exrc && timeout -s KILL 20 python3 -c "import pty,os; '
             'pty.spawn([\'vi\',\'-c\',\':q\',\'/home/person/r/090/x\'])" < /dev/null\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e /tmp/mark-090 ]; then echo "RESULT RAN"; else echo "RESULT REFUSED exit=$rc: $(tr \'\\n\' \' '
             '\' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e /tmp/mark-090 ]', 'exit0')],
  'made': [('obeyed', '~/r'), ('obeyed', '~/r/090'), ('obeyed', '~/r/090/**'), ('obeyed', '~/.exrc')]},
 {'id': 'P4-S-107',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '107',
  'script': 'search/routes/107-ssh-config-proxycommand.sh',
  'program': 'ssh (-F file)',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 107\n'
             '# NAME: ssh-config-proxycommand\n'
             '# PROGRAM: ssh (-F file)\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             "# COMMAND: printf 'Host x\\n\\tProxyCommand touch /tmp/mark-107\\n' > c && ssh -F c x true; true\n"
             '# NOTE: \n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-107; W=/home/person/r/107; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             '\n'
             'echo "COMMAND: printf \'Host x\\n\\tProxyCommand touch /tmp/mark-107\\n\' > c && ssh -F c x true; '
             'true"\n'
             "{ printf 'Host x\\n\\tProxyCommand touch /tmp/mark-107\\n' > c && ssh -F c x true; true\n"
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e /tmp/mark-107 ]; then echo "RESULT RAN"; else echo "RESULT REFUSED exit=$rc: $(tr \'\\n\' \' '
             '\' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e /tmp/mark-107 ]', 'exit0')],
  'made': [('obeyed', '~/r'), ('obeyed', '~/r/107'), ('obeyed', '~/r/107/**')]},
 {'id': 'P4-S-108',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '108',
  'script': 'search/routes/108-ssh-config-match-exec.sh',
  'program': 'ssh (-F file, Match exec)',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 108\n'
             '# NAME: ssh-config-match-exec\n'
             '# PROGRAM: ssh (-F file, Match exec)\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             '# COMMAND: printf \'Match exec "touch /tmp/mark-108"\\n\' > c && ssh -F c -o ConnectTimeout=1 '
             '127.0.0.1 true; true\n'
             '# NOTE: \n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-108; W=/home/person/r/108; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             '\n'
             'echo "COMMAND: printf \'Match exec \\"touch /tmp/mark-108\\"\\n\' > c && ssh -F c -o ConnectTimeout=1 '
             '127.0.0.1 true; true"\n'
             '{ printf \'Match exec "touch /tmp/mark-108"\\n\' > c && ssh -F c -o ConnectTimeout=1 127.0.0.1 true; '
             'true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e /tmp/mark-108 ]; then echo "RESULT RAN"; else echo "RESULT REFUSED exit=$rc: $(tr \'\\n\' \' '
             '\' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e /tmp/mark-108 ]', 'exit0')],
  'made': [('obeyed', '~/r'), ('obeyed', '~/r/108'), ('obeyed', '~/r/108/**')]},
 {'id': 'P4-S-111',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '111',
  'script': 'search/routes/111-apt-config-pre-invoke.sh',
  'program': 'apt-get (APT_CONFIG)',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 111\n'
             '# NAME: apt-config-pre-invoke\n'
             '# PROGRAM: apt-get (APT_CONFIG)\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             '# COMMAND: mkdir -p l/partial c/archives/partial && printf \'APT::Update::Pre-Invoke {"touch '
             '/tmp/mark-111";};\\nDir::State::Lists "/home/person/r/111/l";\\nDir::Cache '
             '"/home/person/r/111/c";\\nDebug::NoLocking "true";\\n\' > a.conf && '
             'APT_CONFIG=/home/person/r/111/a.conf apt-get update; true\n'
             '# NOTE: \n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-111; W=/home/person/r/111; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             '\n'
             'echo "COMMAND: mkdir -p l/partial c/archives/partial && printf \'APT::Update::Pre-Invoke {\\"touch '
             '/tmp/mark-111\\";};\\nDir::State::Lists \\"/home/person/r/111/l\\";\\nDir::Cache '
             '\\"/home/person/r/111/c\\";\\nDebug::NoLocking \\"true\\";\\n\' > a.conf && '
             'APT_CONFIG=/home/person/r/111/a.conf apt-get update; true"\n'
             '{ mkdir -p l/partial c/archives/partial && printf \'APT::Update::Pre-Invoke {"touch '
             '/tmp/mark-111";};\\nDir::State::Lists "/home/person/r/111/l";\\nDir::Cache '
             '"/home/person/r/111/c";\\nDebug::NoLocking "true";\\n\' > a.conf && '
             'APT_CONFIG=/home/person/r/111/a.conf apt-get update; true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e /tmp/mark-111 ]; then echo "RESULT RAN"; else echo "RESULT REFUSED exit=$rc: $(tr \'\\n\' \' '
             '\' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e /tmp/mark-111 ]', 'exit0')],
  'made': [('obeyed', '~/r'), ('obeyed', '~/r/111'), ('obeyed', '~/r/111/**')],
  'tool': 'apt-get'},
 {'id': 'P4-S-135',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '135',
  'script': 'search/routes/135-mpv-user-script.sh',
  'program': 'mpv (scripts directory of the recorded Flatpak)',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 135\n'
             '# NAME: mpv-user-script\n'
             '# PROGRAM: mpv (scripts directory of the recorded Flatpak)\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             '# COMMAND: D=~/.var/app/io.mpv.Mpv/config/mpv/scripts; mkdir -p $D && printf '
             '\'io.open(os.getenv("XDG_CONFIG_HOME").."/mark135","w"):close()\\nmp.commandv("quit")\\n\' > $D/p.lua '
             '&& timeout -s KILL 40 flatpak run io.mpv.Mpv --idle=yes --vo=null --ao=null; ls '
             '~/.var/app/io.mpv.Mpv/config\n'
             '# NOTE: \n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-135; W=/home/person/r/135; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             '\n'
             'echo "COMMAND: D=~/.var/app/io.mpv.Mpv/config/mpv/scripts; mkdir -p \\$D && printf '
             '\'io.open(os.getenv(\\"XDG_CONFIG_HOME\\")..\\"/mark135\\",\\"w\\"):close()\\nmp.commandv(\\"quit\\")\\n\' '
             '> \\$D/p.lua && timeout -s KILL 40 flatpak run io.mpv.Mpv --idle=yes --vo=null --ao=null; ls '
             '~/.var/app/io.mpv.Mpv/config"\n'
             '{ D=~/.var/app/io.mpv.Mpv/config/mpv/scripts; mkdir -p $D && printf '
             '\'io.open(os.getenv("XDG_CONFIG_HOME").."/mark135","w"):close()\\nmp.commandv("quit")\\n\' > $D/p.lua '
             '&& timeout -s KILL 40 flatpak run io.mpv.Mpv --idle=yes --vo=null --ao=null; ls '
             '~/.var/app/io.mpv.Mpv/config\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e ~/.var/app/io.mpv.Mpv/config/mark135 ]; then echo "RESULT RAN"; else echo "RESULT REFUSED '
             'exit=$rc: $(tr \'\\n\' \' \' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e ~/.var/app/io.mpv.Mpv/config/mark135 ]', 'exit0')],
  'made': [('obeyed', '~/r'),
           ('obeyed', '~/r/135'),
           ('obeyed', '~/r/135/**'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/config/mpv/scripts'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/config/mpv/scripts/p.lua'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/config')]},
 {'id': 'P4-S-136',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '136',
  'script': 'search/routes/136-mpv-script-flag.sh',
  'program': 'mpv (--script, recorded Flatpak)',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 136\n'
             '# NAME: mpv-script-flag\n'
             '# PROGRAM: mpv (--script, recorded Flatpak)\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             '# COMMAND: D=~/.var/app/io.mpv.Mpv/config; mkdir -p $D && printf '
             '\'io.open(os.getenv("XDG_CONFIG_HOME").."/mark136","w"):close()\\nmp.commandv("quit")\\n\' > $D/p.lua '
             '&& timeout -s KILL 40 flatpak run io.mpv.Mpv --script=$D/p.lua --idle=yes --vo=null --ao=null\n'
             '# NOTE: \n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-136; W=/home/person/r/136; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             '\n'
             'echo "COMMAND: D=~/.var/app/io.mpv.Mpv/config; mkdir -p \\$D && printf '
             '\'io.open(os.getenv(\\"XDG_CONFIG_HOME\\")..\\"/mark136\\",\\"w\\"):close()\\nmp.commandv(\\"quit\\")\\n\' '
             '> \\$D/p.lua && timeout -s KILL 40 flatpak run io.mpv.Mpv --script=\\$D/p.lua --idle=yes --vo=null '
             '--ao=null"\n'
             '{ D=~/.var/app/io.mpv.Mpv/config; mkdir -p $D && printf '
             '\'io.open(os.getenv("XDG_CONFIG_HOME").."/mark136","w"):close()\\nmp.commandv("quit")\\n\' > $D/p.lua '
             '&& timeout -s KILL 40 flatpak run io.mpv.Mpv --script=$D/p.lua --idle=yes --vo=null --ao=null\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e ~/.var/app/io.mpv.Mpv/config/mark136 ]; then echo "RESULT RAN"; else echo "RESULT REFUSED '
             'exit=$rc: $(tr \'\\n\' \' \' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e ~/.var/app/io.mpv.Mpv/config/mark136 ]', 'exit0')],
  'made': [('obeyed', '~/r'),
           ('obeyed', '~/r/136'),
           ('obeyed', '~/r/136/**'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/config'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/config/p.lua')]},
 {'id': 'P4-S-160',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '160',
  'script': 'search/routes/160-flatpak-run-python-file.sh',
  'program': 'flatpak run (runtime python3)',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 160\n'
             '# NAME: flatpak-run-python-file\n'
             '# PROGRAM: flatpak run (runtime python3)\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             '# COMMAND: flatpak run --command=python3 io.mpv.Mpv /home/person/.var/app/io.mpv.Mpv/r160/c.py\n'
             '# NOTE: \n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-160; W=/home/person/r/160; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             'mkdir -p /home/person/.var/app/io.mpv.Mpv/r160 && printf '
             '\'open("/home/person/.var/app/io.mpv.Mpv/r160/mark", "w").close()\\n\' > '
             '/home/person/.var/app/io.mpv.Mpv/r160/c.py\n'
             '\n'
             'echo "COMMAND: flatpak run --command=python3 io.mpv.Mpv /home/person/.var/app/io.mpv.Mpv/r160/c.py"\n'
             '{ flatpak run --command=python3 io.mpv.Mpv /home/person/.var/app/io.mpv.Mpv/r160/c.py\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e /home/person/.var/app/io.mpv.Mpv/r160/mark ]; then echo "RESULT RAN"; else echo "RESULT '
             'REFUSED exit=$rc: $(tr \'\\n\' \' \' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e /home/person/.var/app/io.mpv.Mpv/r160/mark ]', 'exit0')],
  'made': [('obeyed', '~/r'),
           ('obeyed', '~/r/160'),
           ('obeyed', '~/r/160/**'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/r160'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/r160/c.py')]},
 {'id': 'P4-S-161',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '161',
  'script': 'search/routes/161-flatpak-run-sh-stdin.sh',
  'program': 'flatpak run (runtime sh, stdin)',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 161\n'
             '# NAME: flatpak-run-sh-stdin\n'
             '# PROGRAM: flatpak run (runtime sh, stdin)\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             '# COMMAND: flatpak run --command=sh io.mpv.Mpv < /home/person/.var/app/io.mpv.Mpv/r161/c.sh\n'
             '# NOTE: \n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-161; W=/home/person/r/161; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             "mkdir -p /home/person/.var/app/io.mpv.Mpv/r161 && printf 'touch "
             "/home/person/.var/app/io.mpv.Mpv/r161/mark\\n' > /home/person/.var/app/io.mpv.Mpv/r161/c.sh\n"
             '\n'
             'echo "COMMAND: flatpak run --command=sh io.mpv.Mpv < /home/person/.var/app/io.mpv.Mpv/r161/c.sh"\n'
             '{ flatpak run --command=sh io.mpv.Mpv < /home/person/.var/app/io.mpv.Mpv/r161/c.sh\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e /home/person/.var/app/io.mpv.Mpv/r161/mark ]; then echo "RESULT RAN"; else echo "RESULT '
             'REFUSED exit=$rc: $(tr \'\\n\' \' \' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e /home/person/.var/app/io.mpv.Mpv/r161/mark ]', 'exit0')],
  'made': [('obeyed', '~/r'),
           ('obeyed', '~/r/161'),
           ('obeyed', '~/r/161/**'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/r161'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/r161/c.sh')]},
 {'id': 'P4-S-162',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '162',
  'script': 'search/routes/162-flatpak-run-sh-tmp.sh',
  'program': 'flatpak run (runtime sh, /tmp)',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 162\n'
             '# NAME: flatpak-run-sh-tmp\n'
             '# PROGRAM: flatpak run (runtime sh, /tmp)\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             '# COMMAND: cp /home/person/.var/app/io.mpv.Mpv/r162/c.sh /tmp/c162.sh && flatpak run --command=sh '
             "io.mpv.Mpv -c 'ls -la /tmp/c162.sh; sh /tmp/c162.sh'\n"
             '# NOTE: \n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-162; W=/home/person/r/162; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             "mkdir -p /home/person/.var/app/io.mpv.Mpv/r162 && printf 'touch "
             "/home/person/.var/app/io.mpv.Mpv/r162/mark\\n' > /home/person/.var/app/io.mpv.Mpv/r162/c.sh\n"
             '\n'
             'echo "COMMAND: cp /home/person/.var/app/io.mpv.Mpv/r162/c.sh /tmp/c162.sh && flatpak run --command=sh '
             'io.mpv.Mpv -c \'ls -la /tmp/c162.sh; sh /tmp/c162.sh\'"\n'
             '{ cp /home/person/.var/app/io.mpv.Mpv/r162/c.sh /tmp/c162.sh && flatpak run --command=sh io.mpv.Mpv -c '
             "'ls -la /tmp/c162.sh; sh /tmp/c162.sh'\n"
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e /home/person/.var/app/io.mpv.Mpv/r162/mark ]; then echo "RESULT RAN"; else echo "RESULT '
             'REFUSED exit=$rc: $(tr \'\\n\' \' \' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e /home/person/.var/app/io.mpv.Mpv/r162/mark ]', 'exit0')],
  'made': [('obeyed', '~/r'),
           ('obeyed', '~/r/162'),
           ('obeyed', '~/r/162/**'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/r162'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/r162/c.sh'),
           ('obeyed', '/tmp/c162.sh')]},
 {'id': 'P4-S-166',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '166',
  'script': 'search/routes/166-flatpak-run-sh-cwd-dot.sh',
  'program': 'flatpak run (runtime sh, source)',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 166\n'
             '# NAME: flatpak-run-sh-cwd-dot\n'
             '# PROGRAM: flatpak run (runtime sh, source)\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             "# COMMAND: flatpak run --command=sh io.mpv.Mpv -c '. /home/person/.var/app/io.mpv.Mpv/r166/c.sh'\n"
             '# NOTE: \n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-166; W=/home/person/r/166; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             "mkdir -p /home/person/.var/app/io.mpv.Mpv/r166 && printf 'touch "
             "/home/person/.var/app/io.mpv.Mpv/r166/mark\\n' > /home/person/.var/app/io.mpv.Mpv/r166/c.sh\n"
             '\n'
             'echo "COMMAND: flatpak run --command=sh io.mpv.Mpv -c \'. '
             '/home/person/.var/app/io.mpv.Mpv/r166/c.sh\'"\n'
             "{ flatpak run --command=sh io.mpv.Mpv -c '. /home/person/.var/app/io.mpv.Mpv/r166/c.sh'\n"
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e /home/person/.var/app/io.mpv.Mpv/r166/mark ]; then echo "RESULT RAN"; else echo "RESULT '
             'REFUSED exit=$rc: $(tr \'\\n\' \' \' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e /home/person/.var/app/io.mpv.Mpv/r166/mark ]', 'exit0')],
  'made': [('obeyed', '~/r'),
           ('obeyed', '~/r/166'),
           ('obeyed', '~/r/166/**'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/r166'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/r166/c.sh')]},
 {'id': 'P4-S-167',
  'part': 'P4',
  'table': 'search/routes-0.32.tsv',
  'row': '167',
  'script': 'search/routes/167-mpv-conf-script-option.sh',
  'program': 'mpv (mpv.conf script= of the recorded Flatpak)',
  'channel': '',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 167\n'
             '# NAME: mpv-conf-script-option\n'
             '# PROGRAM: mpv (mpv.conf script= of the recorded Flatpak)\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             '# COMMAND: D=~/.var/app/io.mpv.Mpv/config/mpv; mkdir -p $D /home/person/.var/app/io.mpv.Mpv/r167 && '
             'printf \'io.open(os.getenv("XDG_CONFIG_HOME").."/mark167","w"):close()\\nmp.commandv("quit")\\n\' > '
             '/home/person/.var/app/io.mpv.Mpv/r167/p.lua && printf '
             "'script=/home/person/.var/app/io.mpv.Mpv/r167/p.lua\\n' > $D/mpv.conf && timeout -s KILL 40 flatpak "
             'run io.mpv.Mpv --idle=yes --vo=null --ao=null\n'
             '# NOTE: a configuration value names a saved Lua script\n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-167; W=/home/person/r/167; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             '\n'
             'echo "COMMAND: D=~/.var/app/io.mpv.Mpv/config/mpv; mkdir -p \\$D /home/person/.var/app/io.mpv.Mpv/r167 '
             '&& printf '
             '\'io.open(os.getenv(\\"XDG_CONFIG_HOME\\")..\\"/mark167\\",\\"w\\"):close()\\nmp.commandv(\\"quit\\")\\n\' '
             '> /home/person/.var/app/io.mpv.Mpv/r167/p.lua && printf '
             "'script=/home/person/.var/app/io.mpv.Mpv/r167/p.lua\\n' > \\$D/mpv.conf && timeout -s KILL 40 flatpak "
             'run io.mpv.Mpv --idle=yes --vo=null --ao=null"\n'
             '{ D=~/.var/app/io.mpv.Mpv/config/mpv; mkdir -p $D /home/person/.var/app/io.mpv.Mpv/r167 && printf '
             '\'io.open(os.getenv("XDG_CONFIG_HOME").."/mark167","w"):close()\\nmp.commandv("quit")\\n\' > '
             '/home/person/.var/app/io.mpv.Mpv/r167/p.lua && printf '
             "'script=/home/person/.var/app/io.mpv.Mpv/r167/p.lua\\n' > $D/mpv.conf && timeout -s KILL 40 flatpak "
             'run io.mpv.Mpv --idle=yes --vo=null --ao=null\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e ~/.var/app/io.mpv.Mpv/config/mark167 ]; then echo "RESULT RAN"; else echo "RESULT REFUSED '
             'exit=$rc: $(tr \'\\n\' \' \' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', '[ -e ~/.var/app/io.mpv.Mpv/config/mark167 ]', 'exit0')],
  'made': [('obeyed', '~/r'),
           ('obeyed', '~/r/167'),
           ('obeyed', '~/r/167/**'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/config/mpv'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/r167'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/r167/p.lua'),
           ('obeyed', '~/.var/app/io.mpv.Mpv/config/mpv/mpv.conf')]},
 {'id': 'P4-S-202',
  'part': 'P4',
  'table': 'search/attempts-0.32.tsv',
  'row': '202',
  'script': 'search/attempts/202-apt-mark-hold-recorded.sh',
  'program': 'apt-mark as root',
  'channel': 'C1',
  'steps': [('ATTEMPT', 'U', 'mkdir -p /home/person/r/202 && chmod 0777 /home/person/r /home/person/r/202'),
            ('ATTEMPT',
             'R',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 202\n'
             '# NAME: apt-mark-hold-recorded\n'
             '# PROGRAM: apt-mark as root\n'
             '# GROUP: direct\n'
             '# AS: root\n'
             '# RESTART: no\n'
             '# COMMAND: apt-mark hold ed; apt-mark showhold > /home/person/r/202/hold.txt\n'
             '# NOTE: a selection state of the package manager changed past the declaration\n'
             '# CHANNEL: C1\n'
             '# BREAKING-CANDIDATE: no\n'
             '# Sent to the guest as a typed command over SSH (through sudo -n);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-202; W=/home/person/r/202; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'cd "$W" || exit 3; rm -f "$M"   # W was made by the account (mode 0777): root here has no override of '
             'file permissions\n'
             '\n'
             'echo "COMMAND: apt-mark hold ed; apt-mark showhold > /home/person/r/202/hold.txt"\n'
             '{ apt-mark hold ed; apt-mark showhold > /home/person/r/202/hold.txt\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if grep -qx ed /home/person/r/202/hold.txt; then echo "RESULT RAN"; else echo "RESULT REFUSED '
             'exit=$rc: $(tr \'\\n\' \' \' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'R', 'grep -qx ed /home/person/r/202/hold.txt', 'exit0')],
  'made': [('obeyed', '~/r'), ('obeyed', '~/r/202'), ('obeyed', '~/r/202/**')],
  'tool': 'apt-mark'},
 {'id': 'P4-S-234',
  'part': 'P4',
  'table': 'search/attempts-0.32.tsv',
  'row': '234',
  'script': 'search/attempts/234-root-crontab-for-account.sh',
  'program': 'crontab -u as root',
  'channel': 'C8',
  'steps': [('ATTEMPT', 'U', 'mkdir -p /home/person/r/234 && chmod 0777 /home/person/r /home/person/r/234'),
            ('ATTEMPT',
             'R',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 234\n'
             '# NAME: root-crontab-for-account\n'
             '# PROGRAM: crontab -u as root\n'
             '# GROUP: direct\n'
             '# AS: root\n'
             '# RESTART: no\n'
             "# COMMAND: printf '* * * * * /bin/touch /tmp/mark-234\\n' > ct && crontab -u person ct; crontab -u "
             'person -l > /home/person/r/234/c.txt; cat /home/person/r/234/c.txt; sleep 70\n'
             '# NOTE: \n'
             '# CHANNEL: C8\n'
             '# BREAKING-CANDIDATE: no\n'
             '# Sent to the guest as a typed command over SSH (through sudo -n);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-234; W=/home/person/r/234; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'cd "$W" || exit 3; rm -f "$M"   # W was made by the account (mode 0777): root here has no override of '
             'file permissions\n'
             '\n'
             'echo "COMMAND: printf \'* * * * * /bin/touch /tmp/mark-234\\n\' > ct && crontab -u person ct; crontab '
             '-u person -l > /home/person/r/234/c.txt; cat /home/person/r/234/c.txt; sleep 70"\n'
             "{ printf '* * * * * /bin/touch /tmp/mark-234\\n' > ct && crontab -u person ct; crontab -u person -l > "
             '/home/person/r/234/c.txt; cat /home/person/r/234/c.txt; sleep 70\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if [ -e /tmp/mark-234 ] || grep -q mark /home/person/r/234/c.txt; then echo "RESULT RAN"; else echo '
             '"RESULT REFUSED exit=$rc: $(tr \'\\n\' \' \' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'R', '[ -e /tmp/mark-234 ] || grep -q mark /home/person/r/234/c.txt', 'exit0')],
  'made': [('obeyed', '~/r'), ('obeyed', '~/r/234'), ('obeyed', '~/r/234/**')],
  'tool': 'crontab'},
 {'id': 'P4-S-241',
  'part': 'P4',
  'table': 'search/attempts-0.32.tsv',
  'row': '241',
  'script': 'search/attempts/241-curlrc-obeyed.sh',
  'program': 'curl (~/.curlrc)',
  'channel': 'C10',
  'steps': [('ATTEMPT',
             'U',
             'PHASE=try\n'
             '#!/bin/bash\n'
             '# ID: 241\n'
             '# NAME: curlrc-obeyed\n'
             '# PROGRAM: curl (~/.curlrc)\n'
             '# GROUP: direct\n'
             '# AS: user\n'
             '# RESTART: no\n'
             '# COMMAND: printf \'user-agent = "P241"\\n\' > ~/.curlrc && (python3 -m http.server 18241 --bind '
             '127.0.0.1 >/dev/null 2>&1 & echo $! > pid) && sleep 2 && curl -sv -o /dev/null http://127.0.0.1:18241/ '
             '2> /home/person/r/241/v.txt; kill $(cat pid); cat /home/person/r/241/v.txt\n'
             '# NOTE: a setting of a recorded program saved by the account and obeyed\n'
             '# CHANNEL: C10\n'
             '# BREAKING-CANDIDATE: no\n'
             '# Sent to the guest as a typed command over SSH (as the ordinary account);\n'
             '# PHASE=try puts the payload in place and tries the route; PHASE=check runs after the restart or new '
             'login.\n'
             'M=/tmp/mark-241; W=/home/person/r/241; PHASE=${PHASE:-try}\n'
             "# the SSH session of this release sets no XDG_RUNTIME_DIR; the account's own runtime folder is named "
             'as a login would\n'
             '[ -z "${XDG_RUNTIME_DIR:-}" ] && [ "$(id -u)" != 0 ] && export XDG_RUNTIME_DIR=/run/user/$(id -u)\n'
             'if [ "$PHASE" = try ]; then\n'
             'rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3; rm -f "$M"\n'
             '\n'
             'echo "COMMAND: printf \'user-agent = \\"P241\\"\\n\' > ~/.curlrc && (python3 -m http.server 18241 '
             '--bind 127.0.0.1 >/dev/null 2>&1 & echo \\$! > pid) && sleep 2 && curl -sv -o /dev/null '
             'http://127.0.0.1:18241/ 2> /home/person/r/241/v.txt; kill \\$(cat pid); cat /home/person/r/241/v.txt"\n'
             '{ printf \'user-agent = "P241"\\n\' > ~/.curlrc && (python3 -m http.server 18241 --bind 127.0.0.1 '
             '>/dev/null 2>&1 & echo $! > pid) && sleep 2 && curl -sv -o /dev/null http://127.0.0.1:18241/ 2> '
             '/home/person/r/241/v.txt; kill $(cat pid); cat /home/person/r/241/v.txt\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'else\n'
             'cd "$W" || exit 3\n'
             '{ true\n'
             '} > "$W/out" 2> "$W/err" < /dev/null; rc=$?\n'
             'cd "$W"\n'
             'fi\n'
             'sleep 1\n'
             'echo "--- stdout"; head -c 3000 "$W/out"; echo; echo "--- stderr"; head -c 3000 "$W/err"; echo; echo '
             '"--- exit $rc"\n'
             'if grep -q \'User-Agent: P241\' /home/person/r/241/v.txt; then echo "RESULT RAN"; else echo "RESULT '
             'REFUSED exit=$rc: $(tr \'\\n\' \' \' < "$W/err" | head -c 400)"; fi\n'),
            ('PROBE', 'U', "grep -q 'User-Agent: P241' /home/person/r/241/v.txt", 'exit0')],
  'made': [('obeyed', '~/r'), ('obeyed', '~/r/241'), ('obeyed', '~/r/241/**'), ('obeyed', '~/.curlrc')]},
 {'id': 'P4-S-LO-1',
  'part': 'P4',
  'table': 'build/IMPOSSIBLE.md',
  'row': 'saved LibreOffice Basic profile libraries',
  'script': 'build/lo-macro-private-inputs.py',
  'program': 'libreoffice (saved Basic library)',
  'channel': 'C9',
  'steps': [('L+', 'package libreoffice-writer'),
            ('APPLY',),
            ('ATTEMPT',
             'U',
             'timeout -k 2 120 libreoffice -env:UserInstallation=file:///home/person/lo-profile-user-home --headless '
             '--terminate_after_init'),
            ('ATTEMPT',
             'U',
             'mkdir -p /home/person/lo-profile-user-home/user/basic/Standard && printf %s \'<?xml version="1.0" '
             'encoding="UTF-8"?><library:libraries xmlns:library="http://openoffice.org/2000/library" '
             'xmlns:xlink="http://www.w3.org/1999/xlink"><library:library library:name="Standard" '
             'library:link="false"/></library:libraries>\n'
             '\' > /home/person/lo-profile-user-home/user/basic/script.xlc && printf %s \'<?xml version="1.0" '
             'encoding="UTF-8"?><library:library xmlns:library="http://openoffice.org/2000/library" '
             'library:name="Standard" library:readonly="false" library:passwordprotected="false"><library:element '
             'library:name="Module1"/></library:library>\n'
             "' > /home/person/lo-profile-user-home/user/basic/Standard/script.xlb && printf %s '<?xml "
             'version="1.0" encoding="UTF-8"?><script:module xmlns:script="http://openoffice.org/2000/script" '
             'script:name="Module1" script:language="StarBasic">Sub Main\n'
             'Dim n As Integer\n'
             'n = FreeFile\n'
             'Open "/tmp/lo-macro-basic-marker" For Output As #n\n'
             'Print #n, "BASIC-CODE-RAN"\n'
             'Close #n\n'
             'Shell("/usr/bin/touch", 0, "/tmp/lo-macro-shell-marker", True)\n'
             'StarDesktop.terminate()\n'
             'End Sub\n'
             '</script:module>\n'
             "' > /home/person/lo-profile-user-home/user/basic/Standard/Module1.xba"),
            ('ATTEMPT',
             'U',
             'timeout -k 2 120 libreoffice -env:UserInstallation=file:///home/person/lo-profile-user-home --headless '
             '--norestore macro:///Standard.Module1.Main'),
            ('PROBE', 'U', 'test -e /tmp/lo-macro-basic-marker', 'exit0'),
            ('PROBE', 'U', 'test -e /tmp/lo-macro-shell-marker', 'exit0')],
  'made': [('obeyed', '~/lo-profile-user-home/user/basic/Standard'),
           ('obeyed', '~/lo-profile-user-home/user/basic/script.xlc'),
           ('obeyed', '~/lo-profile-user-home/user/basic/Standard/script.xlb'),
           ('obeyed', '~/lo-profile-user-home/user/basic/Standard/Module1.xba')],
  'line_first': True},
 {'id': 'P4-S-LO-2',
  'part': 'P4',
  'table': 'build/IMPOSSIBLE.md',
  'row': 'saved LibreOffice Basic profile libraries',
  'script': 'build/lo-macro-private-inputs.py',
  'program': 'libreoffice (saved Basic library)',
  'channel': 'C9',
  'steps': [('L+', 'package libreoffice-writer'),
            ('APPLY',),
            ('ATTEMPT',
             'U',
             'timeout -k 2 120 libreoffice -env:UserInstallation=file:///tmp/lo-profile-user-tmp --headless '
             '--terminate_after_init'),
            ('ATTEMPT',
             'U',
             'mkdir -p /tmp/lo-profile-user-tmp/user/basic/Standard && printf %s \'<?xml version="1.0" '
             'encoding="UTF-8"?><library:libraries xmlns:library="http://openoffice.org/2000/library" '
             'xmlns:xlink="http://www.w3.org/1999/xlink"><library:library library:name="Standard" '
             'library:link="false"/></library:libraries>\n'
             '\' > /tmp/lo-profile-user-tmp/user/basic/script.xlc && printf %s \'<?xml version="1.0" '
             'encoding="UTF-8"?><library:library xmlns:library="http://openoffice.org/2000/library" '
             'library:name="Standard" library:readonly="false" library:passwordprotected="false"><library:element '
             'library:name="Module1"/></library:library>\n'
             '\' > /tmp/lo-profile-user-tmp/user/basic/Standard/script.xlb && printf %s \'<?xml version="1.0" '
             'encoding="UTF-8"?><script:module xmlns:script="http://openoffice.org/2000/script" '
             'script:name="Module1" script:language="StarBasic">Sub Main\n'
             'Dim n As Integer\n'
             'n = FreeFile\n'
             'Open "/tmp/lo-macro-basic-marker" For Output As #n\n'
             'Print #n, "BASIC-CODE-RAN"\n'
             'Close #n\n'
             'Shell("/usr/bin/touch", 0, "/tmp/lo-macro-shell-marker", True)\n'
             'StarDesktop.terminate()\n'
             'End Sub\n'
             '</script:module>\n'
             "' > /tmp/lo-profile-user-tmp/user/basic/Standard/Module1.xba"),
            ('ATTEMPT',
             'U',
             'timeout -k 2 120 libreoffice -env:UserInstallation=file:///tmp/lo-profile-user-tmp --headless '
             '--norestore macro:///Standard.Module1.Main'),
            ('PROBE', 'U', 'test -e /tmp/lo-macro-basic-marker', 'exit0'),
            ('PROBE', 'U', 'test -e /tmp/lo-macro-shell-marker', 'exit0')],
  'made': [('obeyed', '/tmp/lo-profile-user-tmp/user/basic/Standard'),
           ('obeyed', '/tmp/lo-profile-user-tmp/user/basic/script.xlc'),
           ('obeyed', '/tmp/lo-profile-user-tmp/user/basic/Standard/script.xlb'),
           ('obeyed', '/tmp/lo-profile-user-tmp/user/basic/Standard/Module1.xba')],
  'line_first': True}]
