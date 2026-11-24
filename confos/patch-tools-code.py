#!/usr/bin/python3
"""Code input checks for dash, mawk, gawk and GNU sed; ordinary data unchanged."""
from pathlib import Path
import shutil
import sys

root = Path(sys.argv[1])
header = Path(__file__).with_name('code-file-policy.h')
for name, directory in [('dash', 'src'), ('mawk', ''), ('gawk', ''), ('sed', 'sed')]:
    shutil.copyfile(header, root/name/directory/'confos-code-file-policy.h')

def change(name, old, new):
    path = root/name
    text = path.read_text()
    if text.count(old) != 1:
        raise ValueError(f'{name}: expected one anchor: {old!r}')
    path.write_text(text.replace(old, new))

change('dash/src/input.c', '#include "input.h"', '#include "input.h"\n#include "confos-code-file-policy.h"')
for signature, fd in [('setinputfd(int fd, int push)', 'fd'), ('preadfd(void)', 'parsefile->fd')]:
    change('dash/src/input.c', signature+'\n{', signature+'\n{\n'
           '\tif (!confos_code_fd_allowed('+fd+'))\n'
           '\t\tsh_error("saved code input: Permission denied");\n')
change('mawk/scan.c', '#include <scan.h>', '#include <scan.h>\n#include "confos-code-file-policy.h"')
change('mawk/scan.c', '\tmawk_exit(2);\n    }\n}\n\nvoid\nscan_cleanup',
       '\tmawk_exit(2);\n    }\n'
       '    if (!confos_code_fd_allowed(program_fd)) mawk_exit(2);\n}\n\nvoid\nscan_cleanup')
# The distribution carries both grammar and generated parser. Keep both in step
# so rebuilding does not depend on an unpinned host bison version.
for name in ('gawk/awkgram.y', 'gawk/awkgram.c'):
    change(name, '#include "awk.h"', '#include "awk.h"\n#include "confos-code-file-policy.h"')
    change(name, '\t\tsourcefile->fd = fd;',
           '\t\tif (!confos_code_fd_allowed(fd))\n'
           '\t\t\tfatal("saved code input: Permission denied");\n\t\tsourcefile->fd = fd;')
change('sed/sed/compile.c', '#include "sed.h"', '#include "sed.h"\n#include "confos-code-file-policy.h"')
change('sed/sed/compile.c', '  cur_input.name = cmdfile;',
       '  if (!confos_code_fd_allowed(fileno(prog.file)))\n'
       '    panic("saved code input: Permission denied");\n  cur_input.name = cmdfile;')
