#!/usr/bin/python3
"""Prototype checks at Perl lexer creation and code-input refills."""
from pathlib import Path
import shutil
import sys

root = Path(sys.argv[1])
shutil.copyfile(Path(__file__).with_name('code-file-policy.h'), root/'confos-code-file-policy.h')
p = root/'toke.c'
text = p.read_text()
def change(old, new):
    global text
    if text.count(old) != 1:
        raise ValueError(f'expected exactly one source anchor {old!r}')
    text = text.replace(old, new)
change('#include "perl.h"', '#include "perl.h"\n#include "confos-code-file-policy.h"')
for signature, stream in (
    ('Perl_lex_start(pTHX_ SV *line, PerlIO *rsfp, U32 flags)', 'rsfp'),
    ('Perl_filter_read(pTHX_ int idx, SV *buf_sv, int maxlen)', 'PL_parser ? PL_rsfp : NULL'),
    ('S_filter_gets(pTHX_ SV *sv, STRLEN append)', 'PL_rsfp'),
):
    change(signature+'\n{', signature+'\n{\n'
           '    PerlIO *confos_input = '+stream+';\n'
           '    if (confos_input && !confos_code_fd_allowed(PerlIO_fileno(confos_input)))\n'
           '        Perl_croak(aTHX_ "Permission denied for saved code input");\n')
p.chmod(p.stat().st_mode | 0o200)
p.write_text(text)
