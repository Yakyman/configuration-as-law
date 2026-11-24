#!/usr/bin/python3
"""Guard mpv Lua source reads on the same open descriptor; draft, not integrated."""
from pathlib import Path
import sys

root = Path(sys.argv[1])
here = Path(__file__).resolve().parent

def replace(relative, old, new):
    path = root/relative
    source = path.read_text()
    if source.count(old) != 1:
        raise ValueError('mpv original source anchor mismatch: '+relative)
    path.write_text(source.replace(old, new))

(root/'stream/confos-code-policy.h').write_bytes((here/'code-file-policy.h').read_bytes())
replace('stream/stream.h', '#define STREAM_ALLOW_PARTIAL_READ (1 << 7)',
        '#define STREAM_CODE_INPUT         (1 << 8) // require opened code descriptor policy\n'
        '#define STREAM_ALLOW_PARTIAL_READ (1 << 7)')
replace('player/lua.c',
        'struct bstr s = stream_read_file(fname, tmp, ctx->mpctx->global, 100000000);',
        'struct bstr s = stream_read_file2(fname, tmp,\n'
        '        STREAM_READ_FILE_FLAGS_DEFAULT | STREAM_CODE_INPUT,\n'
        '        ctx->mpctx->global, 100000000);')
replace('stream/stream.c', '    *ret = NULL;\n\n    const char *path = url;',
        '    *ret = NULL;\n\n'
        '    // Only these backends enforce code policy on the descriptor they read.\n'
        '    if ((flags & STREAM_CODE_INPUT) &&\n'
        '        sinfo != &stream_info_file && sinfo != &stream_info_fd)\n'
        '        return STREAM_NO_MATCH;\n\n'
        '    const char *path = url;')
replace('stream/stream_file.c', '#include "config.h"',
        '#include "config.h"\n#include "confos-code-policy.h"')
replace('stream/stream_file.c', '#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION',
        '    if ((args->flags & STREAM_CODE_INPUT) &&\n'
        '        !confos_code_fd_allowed(p->fd)) {\n'
        '        s_close(stream);\n'
        '        return STREAM_ERROR;\n'
        '    }\n\n#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION')
print('MPV LUA SAME-DESCRIPTOR PATCH PREPARED')
