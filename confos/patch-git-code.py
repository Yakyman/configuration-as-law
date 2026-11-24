#!/usr/bin/python3
"""Check actual config descriptors before dispatching code-valued settings."""
from pathlib import Path
import sys
root = Path(sys.argv[1])
here = Path(__file__).resolve().parent
for source, target in [('code-file-policy.h', 'confos-code-policy.h'),
                       ('git-code-policy.h', 'confos-git-policy.h')]:
    (root/target).write_bytes((here/source).read_bytes())
path = root/'config.c'
text = path.read_text()
def change(old, new):
    global text
    if text.count(old) != 1: raise ValueError('missing/ambiguous anchor: '+old)
    text = text.replace(old, new)
change('#include "write-or-die.h"', '#include "write-or-die.h"\n#include "confos-git-policy.h"')
change('\tret = fn(name->buf, value, &ctx, data);',
       '\tif (confos_git_code_key(name->buf, value)) {\n'
       '\t\tint fd = cs->do_fgetc == config_file_fgetc ? fileno(cs->u.file) : -1;\n'
       '\t\tif (!confos_code_fd_allowed(fd)) return -1;\n'
       '\t}\n\tret = fn(name->buf, value, &ctx, data);')
change('\tvalidate_comment_string(comment);',
       '\t/* Built-in config writes cannot create executable settings off declaration. */\n'
       '\tif (value && confos_git_code_key(key, value) && !confos_code_fd_allowed(-1))\n'
       '\t\treturn CONFIG_INVALID_FILE;\n\n\tvalidate_comment_string(comment);')
path.write_text(text)
