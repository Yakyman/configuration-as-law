#!/usr/bin/python3
"""Guard package.json when it is obeyed by the module resolver, not read as data."""
from pathlib import Path
import sys
path = Path(sys.argv[1])/'src/node_file.cc'
text = path.read_text()
old = '  const size_t kBlockSize = 32 << 10;\n  std::vector<char> chars;'
if text.count(old) != 1: raise ValueError('missing package metadata reader anchor')
text = text.replace(old, '  if (!confos_code_fd_allowed(fd))\n'
    '    return env->ThrowUVException(UV_EACCES, "saved module configuration", nullptr);\n\n'+old)
path.write_text(text)
