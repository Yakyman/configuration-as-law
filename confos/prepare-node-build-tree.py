#!/usr/bin/python3
"""Debian's documented pre-build preparation, using pinned external sources."""
from pathlib import Path
import json
import re
root = Path('interpreter-inputs/node/tree')
external = Path('interpreter-inputs/node/dependencies/root/usr/share/nodejs')
(root/'deps/openssl').mkdir(parents=True, exist_ok=True)
(root/'deps/openssl/nodejs-openssl.cnf').touch()
for package, header in [('acorn', 'acorn'), ('cjs-module-lexer', 'cjs_module_lexer'), ('undici', 'undici')]:
    version = json.loads((external/package/'package.json').read_text())['version']
    path = root/'src'/(header+'_version.h')
    path.write_text(re.sub(r'\d+\.\d+\.\d+', version, path.read_text()))
