#!/usr/bin/python3
from pathlib import Path
import shutil
import sys
root = Path(sys.argv[1])
for name in ('code-file-policy.h', 'make-code-policy.h'):
    target = 'confos-code-file-policy.h' if name == 'code-file-policy.h' else name
    shutil.copyfile(Path(__file__).with_name(name), root/'src'/target)
def change(name, old, new):
    path = root/name
    text = path.read_text()
    if text.count(old) != 1: raise ValueError((name, old, text.count(old)))
    path.write_text(text.replace(old, new))
for name in ('src/main.c', 'src/read.c'):
    change(name, '#include "makeint.h"', '#include "makeint.h"\n#include "make-code-policy.h"')
change('src/read.c', '  /* Success; clear errno.  */',
       '  if (!confos_make_fd_allowed(fileno(ebuf.fp)))\n'
       '    O (fatal, reading_file, "saved code input: Permission denied");\n\n'
       '  /* Success; clear errno.  */')
change('src/main.c', '            outfile = get_tmpfile (&newnm);',
       '            outfile = confos_make_stdin_open (&newnm);')
change('src/main.c', '            fclose (outfile);',
       '            if (confos_make_stdin_finish(outfile) != 0)\n'
       '              O (fatal, NILF, "cannot seal stdin makefile");')
change('src/main.c', '''      const char *nm = makefiles->list[stdin_offset];
      int r = 0;

      stdin_offset = -1;
      EINTRLOOP(r, unlink (nm));
      if (r < 0 && errno != ENOENT && !handling_fatal_signal)
        perror_with_name (_("unlink (temporary file): "), nm);''',
       '''      /* Checked stdin has anonymous storage, reclaimed on exit.
         Never unlink a user-supplied --temp-stdin pathname. */
      stdin_offset = -1;''')
