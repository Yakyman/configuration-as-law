#!/usr/bin/python3
"""Prototype BusyBox ash, awk and sed program-file checks; data reads unchanged."""
from pathlib import Path
import shutil
import sys

root = Path(sys.argv[1])
shutil.copyfile(Path(__file__).with_name('code-file-policy.h'), root/'include/confos-code-file-policy.h')

def change(name, old, new):
    p = root/name
    text = p.read_text()
    if text.count(old) != 1:
        raise ValueError(f'{name}: expected exactly one source anchor {old!r}')
    p.write_text(text.replace(old, new))

for name, anchor in [('shell/ash.c', '#include "shell_common.h"'),
                     ('editors/awk.c', '#include "libbb.h"'),
                     ('editors/sed.c', '#include "libbb.h"')]:
    change(name, anchor, anchor+'\n#include "confos-code-file-policy.h"')
for signature, fd in [('setinputfd(int fd, int push)', 'fd'),
                      ('preadfd(void)', 'g_parsefile->pf_fd')]:
    change('shell/ash.c', signature+'\n{', signature+'\n{\n'
           '\tif (!confos_code_fd_allowed('+fd+'))\n'
           '\t\tbb_perror_msg_and_die("saved code input");\n')
change('editors/awk.c', '\t\t\tfd = xopen_stdin(g_progname);',
       '\t\t\tfd = xopen_stdin(g_progname);\n'
       '\t\t\tif (!confos_code_fd_allowed(fd))\n'
       '\t\t\t\tbb_perror_msg_and_die("saved code input");')
change('editors/sed.c', '\t\tcmdfile = xfopen_stdin(llist_pop(&opt_f));',
       '\t\tcmdfile = xfopen_stdin(llist_pop(&opt_f));\n'
       '\t\tif (!confos_code_fd_allowed(fileno(cmdfile)))\n'
       '\t\t\tbb_perror_msg_and_die("saved code input");')
