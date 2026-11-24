#!/usr/bin/python3
"""Guard JS code-file streams while keeping explicit data reads separate."""
from pathlib import Path
import sys
root=Path(sys.argv[1])
def replace(relative,old,new):
    path=root/relative;text=path.read_text()
    assert text.count(old)==1, 'exact JS source anchor mismatch: '+old
    path.write_text(text.replace(old,new))
file='player/javascript.c'
replace(file,'static void af_push_file(js_State *J, const char *fname, int limit, void *af)',
             'static void af_push_file(js_State *J, const char *fname, int limit, int code_flags, void *af)')
replace(file,'                STREAM_SILENT;','                STREAM_SILENT | code_flags;')
replace(file,'static int s_push_file(js_State *J, const char *fname, int limit, void **af)',
             'static int s_push_file(js_State *J, const char *fname, int limit, int code_flags, void **af)')
replace(file,'    af_push_file(J, fname, limit, *af);','    af_push_file(J, fname, limit, code_flags, *af);')
replace(file,'static void push_file_content(js_State *J, const char *fname, int limit)',
             'static void push_file_content(js_State *J, const char *fname, int limit, int code_flags)')
replace(file,'    int r = s_push_file(J, fname, limit, &af);','    int r = s_push_file(J, fname, limit, code_flags, &af);')
replace(file,'    push_file_content(J, js_tostring(J, 1), limit);',
             '    push_file_content(J, js_tostring(J, 1), limit, 0);')
replace(file,'    push_file_content(J, fname, -1);','    push_file_content(J, fname, -1, STREAM_CODE_INPUT);')
replace(file,'// Runs a file with the caller\'s this, leaves the stack as is.',
'''// Internal code reader for module loading; ordinary read_file remains a data API.
static void script__read_code_file(js_State *J)
{
    int limit = js_isundefined(J, 2) ? -1 : jsL_checkint(J, 2);
    push_file_content(J, js_tostring(J, 1), limit, STREAM_CODE_INPUT);
}

// Runs a file with the caller's this, leaves the stack as is.''')
replace(file,'    FN_ENTRY(read_file, 2),','    FN_ENTRY(read_file, 2),\n    FN_ENTRY(_read_code_file, 2),')
defaults='player/javascript/defaults.js'
replace(defaults,'                mp.utils.read_file(f, 1);  // throws on any error',
                 '                mp.utils._read_code_file(f, 1);  // code-file policy, throws on any error')
replace(defaults,'                          mp.utils.read_file(filename) +',
                 '                          mp.utils._read_code_file(filename) +')
print('JS_INITIAL_AND_REQUIRE_DESCRIPTOR_POLICY_PATCHED; ordinary data reader unchanged')
