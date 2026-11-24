#!/usr/bin/python3
"""Native startup snapshot, SEA builder and environment configuration readers."""
from pathlib import Path
import sys
root = Path(sys.argv[1])
def change(name, old, new):
    path = root/name
    text = path.read_text()
    if text.count(old) != 1: raise ValueError((name, old, text.count(old)))
    path.write_text(text.replace(old, new))
change('src/util.h', 'int ReadFileSync(std::string* result, const char* path);',
       'int ReadFileSync(std::string* result, const char* path);\n'
       'int ReadCodeFileSync(std::string* result, const char* path);')
change('src/util.cc', '#include "util.h"',
       '#include "util.h"\n#include "confos-code-file-policy.h"')
change('src/util.cc', 'int ReadFileSync(std::string* result, const char* path) {',
       'static int ReadFileSyncImpl(std::string* result, const char* path, bool code) {')
change('src/util.cc', '  *result = std::string("");\n  char buffer[4096];',
       '  if (code && !confos_code_fd_allowed(file)) return UV_EACCES;\n\n'
       '  *result = std::string("");\n  char buffer[4096];')
change('src/util.cc', 'std::vector<char> ReadFileSync(FILE* fp) {',
       'int ReadFileSync(std::string* result, const char* path) {\n'
       '  return ReadFileSyncImpl(result, path, false);\n}\n\n'
       'int ReadCodeFileSync(std::string* result, const char* path) {\n'
       '  return ReadFileSyncImpl(result, path, true);\n}\n\n'
       'std::vector<char> ReadFileSync(FILE* fp) {')
change('src/node.cc', 'ReadFileSync(&builder_script_content, builder_script.c_str())',
       'ReadCodeFileSync(&builder_script_content, builder_script.c_str())')
change('src/node_snapshotable.cc', '#include "node_snapshotable.h"',
       '#include "node_snapshotable.h"\n#include "confos-code-file-policy.h"')
change('src/node_snapshotable.cc', 'bool SnapshotData::FromFile(SnapshotData* out, FILE* in) {',
       'bool SnapshotData::FromFile(SnapshotData* out, FILE* in) {\n'
       '  if (!confos_code_fd_allowed(fileno(in))) return false;')
for old in ['ReadFileSync(&config_content, config_path)',
            'ReadFileSync(&builder_script_content, builder_script_path.data())']:
    change('src/node_snapshotable.cc', old, old.replace('ReadFileSync', 'ReadCodeFileSync'))
for old in ['ReadFileSync(&config, config_path.c_str())',
            'ReadFileSync(&main_script, config.main_path.c_str())']:
    change('src/node_sea.cc', old, old.replace('ReadFileSync', 'ReadCodeFileSync'))
change('src/node_dotenv.cc', '#include "node_dotenv.h"',
       '#include "node_dotenv.h"\n#include "confos-code-file-policy.h"')
change('src/node_dotenv.cc', '  std::string result{};\n  char buffer[8192];',
       '  if (!confos_code_fd_allowed(file)) return ParseResult::FileError;\n\n'
       '  std::string result{};\n  char buffer[8192];')
change('lib/internal/process/pre_execution.js',
       "    const src = fs.readFileSync(manifestURL, 'utf8');",
       "    const src = internalBinding('fs').readCodeFileUtf8(\n"
       "      require('internal/url').fileURLToPath(manifestURL), 0);")
