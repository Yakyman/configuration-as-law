#!/usr/bin/env python3
"""Compare two copies of the published set: for Python files, the token streams without comments and line breaks
must be equal except for string tokens, and every differing string token is printed; for other files every changed
line must be a comment line (starting with #) or a file of documentation (.md). Usage: tokcmp.py OLD_DIR NEW_DIR"""
import difflib
import io
import sys
import tokenize
from pathlib import Path

old_root, new_root = Path(sys.argv[1]), Path(sys.argv[2])
SKIP = {tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING}
bad = 0


def is_python(p):
    if p.suffix == '.py':
        return True
    head = p.read_bytes()[:100]
    return head.startswith(b'#!') and b'python' in head.split(b'\n')[0]


def toks(p):
    return [(t.type, t.string) for t in tokenize.tokenize(io.BytesIO(p.read_bytes()).readline) if t.type not in SKIP]


for new in sorted(new_root.rglob('*')):
    if not new.is_file():
        continue
    rel = new.relative_to(new_root)
    old = old_root / rel
    if not old.exists():
        print(f'{rel}: NEW FILE' + ('' if rel.suffix == '.md' else ' (not documentation)'))
        bad += rel.suffix != '.md'
        continue
    if old.read_bytes() == new.read_bytes():
        continue
    if is_python(new):
        a, b = toks(old), toks(new)
        sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == 'equal':
                continue
            olds, news = a[i1:i2], b[j1:j2]
            if op == 'replace' and len(olds) == len(news) and all(
                    x[0] == tokenize.STRING and y[0] == tokenize.STRING for x, y in zip(olds, news)):
                for x, y in zip(olds, news):
                    print(f'{rel}: STRING {x[1][:140]!r}\n{"":>{len(str(rel)) + 2}}-> {y[1][:140]!r}')
            else:
                bad += 1
                print(f'{rel}: NON-STRING TOKEN CHANGE {op} {olds} -> {news}')
        print(f'{rel}: python, code tokens equal apart from the strings above' if not bad else f'{rel}: CODE CHANGED')
    else:
        ol, nl = old.read_text().splitlines(), new.read_text().splitlines()
        changed = [l for l in difflib.unified_diff(ol, nl, lineterm='', n=0)
                   if l[:1] in '+-' and not l.startswith(('+++', '---'))]
        if rel.suffix == '.md':
            print(f'{rel}: documentation, {len(changed)} changed lines')
            continue
        non_comment = [l for l in changed if not l[1:].lstrip().startswith('#')]
        if non_comment:
            bad += 1
            print(f'{rel}: NON-COMMENT LINES CHANGED: {non_comment}')
        else:
            print(f'{rel}: only comment lines changed ({len(changed)})')
print('RESULT:', 'only comments, documentation and strings differ' if not bad else f'{bad} code changes')
sys.exit(1 if bad else 0)
