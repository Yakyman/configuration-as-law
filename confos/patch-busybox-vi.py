#!/usr/bin/python3
"""Guard BusyBox vi's saved automatic startup command reader."""
from pathlib import Path
import sys
root = Path(sys.argv[1])
path = root/'editors/vi.c'
text = path.read_text()
anchor = '#include "libbb.h"'
assert text.count(anchor) == 1
text = text.replace(anchor, anchor+'\n#include "confos-code-file-policy.h"')
anchor = '\t\t\t\t\t\tcmds = xmalloc_open_read_close(exrc, NULL);'
assert text.count(anchor) == 1
text = text.replace(anchor, '''\t\t\t\t\t\tint fd = xopen(exrc, O_RDONLY);
\t\t\t\t\t\tif (!confos_code_fd_allowed(fd))
\t\t\t\t\t\t\tbb_perror_msg_and_die("saved startup commands");
\t\t\t\t\t\tcmds = xmalloc_read(fd, NULL);
\t\t\t\t\t\tclose(fd);''')
path.write_text(text)
