#!/usr/bin/python3
"""Patch upstream Bash's code readers; do not intercept data-file reads."""
from pathlib import Path
import shutil
import sys

root = Path(sys.argv[1])
shutil.copyfile(Path(__file__).with_name('code-file-policy.h'), root/'confos-code-file-policy.h')

def change(name, old, new):
    p = root/name
    text = p.read_text()
    if text.count(old) != 1:
        raise ValueError(f'{name}: expected exactly one source anchor {old!r}')
    p.write_text(text.replace(old, new))

for name in ('shell.c', 'builtins/evalfile.c', 'input.c'):
    text = (root/name).read_text()
    anchor = '#include <config.h>' if '#include <config.h>' in text else '#include "config.h"'
    change(name, anchor, anchor+'\n#include "confos-code-file-policy.h"')
change('builtins/evalfile.c', 'if (fd < 0 || (fstat (fd, &finfo) == -1))',
       'if (fd < 0 || !confos_code_fd_allowed (fd) || (fstat (fd, &finfo) == -1))')
change('shell.c', '  free (dollar_vars[0]);\n  dollar_vars[0] = exec_argv0',
       '  if (!confos_code_fd_allowed (fd))\n'
       '    { file_error (filename); close (fd); sh_exit (EX_NOINPUT); }\n\n'
       '  free (dollar_vars[0]);\n  dollar_vars[0] = exec_argv0')
change('shell.c', 'set_bash_input ()\n{',
       'set_bash_input ()\n{\n'
       '#if defined (BUFFERED_INPUT)\n'
       '  int confos_fd = interactive ? fileno (stdin) : default_buffered_input;\n'
       '#else\n'
       '  int confos_fd = fileno (default_input);\n'
       '#endif\n'
       '  if (!confos_code_fd_allowed (confos_fd))\n'
       '    { file_error ("script input"); sh_exit (EX_NOINPUT); }\n')
change('input.c', '  ssize_t nr;\n  off_t o;\n\n  CHECK_TERMSIG;',
       '  ssize_t nr;\n  off_t o;\n\n'
       '  if (bash_input.type == st_bstream &&\n'
       '      bp->b_fd == bash_input.location.buffered_fd &&\n'
       '      !confos_code_fd_allowed (bp->b_fd))\n'
       '    { file_error ("script input"); sh_exit (EX_NOINPUT); }\n'
       '  CHECK_TERMSIG;')
