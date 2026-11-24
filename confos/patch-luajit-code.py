#!/usr/bin/python3
"""Guard LuaJIT's native file/bytecode loader, preserving explicit data APIs."""
from pathlib import Path
import sys
root = Path(sys.argv[1])
here = Path(__file__).resolve().parent
(root/'src/confos-code-policy.h').write_bytes((here/'code-file-policy.h').read_bytes())
path = root/'src/lj_load.c'
text = path.read_text()
old = '  status = lua_loadx(L, reader_file, &ctx, chunkname, mode);'
if text.count(old) != 1: raise ValueError('LuaJIT loader anchor mismatch')
if 'confos_code_fd_allowed' not in text:
    text = text.replace('#include <stdio.h>', '#include <stdio.h>\n#include "confos-code-policy.h"')
    text = text.replace(old, '''  if (!confos_code_fd_allowed(fileno(ctx.fp))) {
    if (filename) { lua_pop(L, 1); fclose(ctx.fp); }
    lua_pushfstring(L, "Permission denied for saved code input");
    return LUA_ERRFILE;
  }
'''+old)
if not text.startswith('#ifndef _GNU_SOURCE'):
    text = '#ifndef _GNU_SOURCE\n#define _GNU_SOURCE 1\n#endif\n'+text
path.write_text(text)
