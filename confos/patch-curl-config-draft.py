#!/usr/bin/python3
"""Prepare a reviewable private curl config-reader patch; never compile."""
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

root = Path.cwd()
work = root/'interpreter-inputs/curl-config-draft'
source = work/'source/src/tool_parsecfg.c'
original = source.read_text()
assert hashlib.sha256(source.read_bytes()).hexdigest() == '5c8a2a3418c993229e7180c4f5c1e50fc891f016184135e1eeb4e1982b3dbf76'
header = root/'code-file-policy.h'
assert hashlib.sha256(header.read_bytes()).hexdigest() == '64e344ca44ea9859708b0f84fe3c8a41c6a56942eafc3e05a75a1f00434fbea2'
patched = original
for before, after in [
    ('#include "tool_util.h"\n', '#include "tool_util.h"\n#include "confos-curl-config-policy.h"\n'),
    ('  if(file) {\n    char *line;',
     '''  /* Configuration options are saved behavior inputs, not transfer data.
     Check the same descriptor that my_get_line will consume, including stdin. */
  if(file && !confos_code_fd_allowed(fileno(file))) {
    if(file != stdin)
      fclose(file);
    free(pathalloc);
    return 1;
  }

  if(file) {
    char *line;'''),
]:
    assert patched.count(before) == 1, before
    patched = patched.replace(before, after)
output = work/'patched/src'; output.mkdir(parents=True, exist_ok=True)
(output/'tool_parsecfg.c').write_text(patched)
shutil.copyfile(header, output/'confos-curl-config-policy.h')
(work/'curl-config-reader.patch').write_text(''.join(difflib.unified_diff(
    original.splitlines(keepends=True), patched.splitlines(keepends=True),
    fromfile='a/src/tool_parsecfg.c', tofile='b/src/tool_parsecfg.c')))
if not (work/'original-package').exists():
    subprocess.run(['dpkg-deb', '-x', str(work/'curl_8.14.1-2+deb13u7_amd64.deb'),
                    str(work/'original-package')], check=True)
paths = [source, header, output/'tool_parsecfg.c', output/'confos-curl-config-policy.h',
         work/'curl-config-reader.patch', work/'original-package/usr/bin/curl',
         *[work/'source/src'/name for name in ('tool_findfile.c','tool_operate.c','tool_getparam.c')]]
(work/'reader-provenance.json').write_text(json.dumps({str(path.relative_to(root)):
    hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}, indent=2)+'\n')
print('CURL_CONFIG_DESCRIPTOR_PATCH_PREPARED; not compiled or guest-tested')
