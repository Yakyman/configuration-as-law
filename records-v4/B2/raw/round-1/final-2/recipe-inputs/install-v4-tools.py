#!/usr/bin/python3 -I
"""Install the document editor; typed tools use the existing broker frontends.

Canonical native backend paths stay available to the laboratory operator.
Their direct privileged mutation remains an explicit unclosed channel.
"""
import pathlib
editor = pathlib.Path('/usr/local/bin/v4-editor')
editor.unlink(missing_ok=True)
editor.symlink_to('/usr/local/lib/stand/v4-editor.py')
print('Document editor with declaration-writing installer installed')
