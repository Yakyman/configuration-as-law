#!/usr/bin/python3
"""Guard Vimscript, saved key input, Lua stdin and the bundled LuaJIT reader."""
from pathlib import Path
import sys
root = Path(sys.argv[1])
here = Path(__file__).resolve().parent
(root/'src/nvim/confos-code-policy.h').write_bytes((here/'code-file-policy.h').read_bytes())
(root/'confos').mkdir()
for name in ('patch-luajit-code.py', 'code-file-policy.h'):
    (root/'confos'/name).write_bytes((here/name).read_bytes())
def change(name, old, new):
    path = root/name
    text = path.read_text()
    if text.count(old) != 1: raise ValueError((name, old, text.count(old)))
    path.write_text(text.replace(old, new))
for name in ('runtime.c', 'getchar.c', 'ex_getln.c', 'lua/executor.c', 'main.c'):
    change('src/nvim/'+name, '#include <stdio.h>',
           '#include <stdio.h>\n#include "nvim/confos-code-policy.h"')
change('src/nvim/runtime.c', '  os_set_cloexec(fd_tmp);\n\n  return fdopen(fd_tmp, READBIN);',
       '  os_set_cloexec(fd_tmp);\n'
       '  if (!confos_code_fd_allowed(fd_tmp)) { close(fd_tmp); return NULL; }\n\n'
       '  return fdopen(fd_tmp, READBIN);')
change('src/nvim/getchar.c',
       '  int error = file_open(&scriptin[curscript], NameBuff, kFileReadOnly, 0);',
       '  int error = file_open(&scriptin[curscript], NameBuff, kFileReadOnly, 0);\n'
       '  if (!error && !confos_code_fd_allowed(file_fd(&scriptin[curscript]))) {\n'
       '    file_close(&scriptin[curscript], false); error = UV_EACCES;\n  }')
change('src/nvim/getchar.c', '  if (error) {\n    fprintf(stderr, _("Cannot open for reading:',
       '  if (!error && !confos_code_fd_allowed(file_fd(&scriptin[0]))) {\n'
       '    file_close(&scriptin[0], false); error = UV_EACCES;\n  }\n'
       '  if (error) {\n    fprintf(stderr, _("Cannot open for reading:')
change('src/nvim/ex_getln.c', 'char *getexline(int c, void *cookie, int indent, bool do_concat)\n{',
       'char *getexline(int c, void *cookie, int indent, bool do_concat)\n{\n'
       '  if (exmode_active && !confos_code_fd_allowed(STDIN_FILENO)) return NULL;')
change('src/nvim/main.c',
       '  if (!stdin_isatty && !params.input_istext && silent_mode && exmode_active) {\n    input_start();',
       '  if (!stdin_isatty && !params.input_istext && silent_mode && exmode_active) {\n'
       '    if (!confos_code_fd_allowed(STDIN_FILENO)) return 2;\n    input_start();')
change('src/nvim/lua/executor.c', '    StringBuilder sb = KV_INITIAL_VALUE;\n    kv_resize(sb, 64);',
       '    if (!confos_code_fd_allowed(file_fd(&stdin_dup))) {\n'
       '      file_close(&stdin_dup, false); return false;\n    }\n'
       '    StringBuilder sb = KV_INITIAL_VALUE;\n    kv_resize(sb, 64);')
# Cached bytecode is itself code. Keep the loader API/module lookup but always use
# the checked original file loader; mutable disk caches are neither read nor written.
path = root/'runtime/lua/vim/loader.lua'
text = path.read_text()
start = text.index('function Loader.load(modpath, opts)')
end = text.index('--- Finds Lua modules', start)
text = text[:start]+'''function Loader.load(modpath, opts)
  opts = opts or {}
  return Loader._loadfile(modpath, opts.mode, opts.env)
end

'''+text[end:]
path.write_text(text)
change('cmake.deps/cmake/BuildLuajit.cmake', '    DOWNLOAD_DIR ${DEPS_DOWNLOAD_DIR}/luajit',
       '    DOWNLOAD_DIR ${DEPS_DOWNLOAD_DIR}/luajit\n'
       '    PATCH_COMMAND /usr/bin/python3 "${CMAKE_CURRENT_SOURCE_DIR}/../confos/patch-luajit-code.py" <SOURCE_DIR>')
change('cmake.deps/cmake/BuildLuajit.cmake', '${MAKE_PRG} -j CFLAGS=-fPIC',
       '${MAKE_PRG} -j2 CFLAGS=-fPIC')
change('cmake.deps/cmake/BuildLuajit.cmake',
       'CC=${DEPS_C_COMPILER} PREFIX=${DEPS_INSTALL_DIR}\n    ${DEPLOYMENT_TARGET} install)',
       'CC=${DEPS_C_COMPILER} PREFIX=/usr DESTDIR=${CMAKE_BINARY_DIR}\n    ${DEPLOYMENT_TARGET} install)')
