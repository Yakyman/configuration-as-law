#!/usr/bin/python3
"""Descriptor guards for manifest-pinned CPython 3.14.9's code readers."""
from pathlib import Path
import shutil
import sys

root = Path(sys.argv[1])
shutil.copyfile(Path(__file__).with_name('code-file-policy.h'), root/'Include/confos-code-file-policy.h')

def change(name, old, new):
    p = root/name
    text = p.read_text()
    if text.count(old) != 1:
        raise ValueError(f'{name}: expected exactly one source anchor {old!r}')
    p.write_text(text.replace(old, new))

change('Lib/importlib/_bootstrap_external.py',
       '        data = self.get_data(path)\n        # Call _classify_pyc',
       '        with _io.open_code(path) as code_file:\n            data = code_file.read()\n        # Call _classify_pyc')

for name in ('Objects/fileobject.c', 'Python/pythonrun.c'):
    change(name, '#include "Python.h"', '#include "Python.h"\n#include "confos-code-file-policy.h"')

change('Objects/fileobject.c', '    return f;\n}\n\nPyObject *\nPyFile_OpenCode(',
       '''    if (f) {
        int fd = PyObject_AsFileDescriptor(f);
        if (fd < 0 || !confos_code_fd_allowed(fd)) {
            Py_DECREF(f);
            errno = EACCES;
            return PyErr_SetFromErrnoWithFilenameObject(PyExc_PermissionError, path);
        }
    }
    return f;
}

PyObject *
PyFile_OpenCode(''')

for signature in (
    '_PyRun_AnyFile(FILE *fp, PyObject *filename, int closeit,\n               PyCompilerFlags *flags)',
    '_PyRun_SimpleFile(FILE *fp, PyObject *filename, int closeit,\n                  PyCompilerFlags *flags)',
):
    change('Python/pythonrun.c', signature+'\n{', signature+'''\n{
    if (!confos_code_fd_allowed(fileno(fp))) {
        PyErr_SetFromErrnoWithFilenameObject(PyExc_PermissionError, filename);
        if (closeit) fclose(fp);
        return NULL;
    }
''')
signature = '_PyRun_File(FILE *fp, PyObject *filename, int start, PyObject *globals,\n            PyObject *locals, int closeit, PyCompilerFlags *flags)'
change('Python/pythonrun.c', signature+'\n{', signature+'''\n{
    if (!confos_code_fd_allowed(fileno(fp))) {
        PyErr_SetFromErrnoWithFilenameObject(PyExc_PermissionError, filename);
        if (closeit) fclose(fp);
        return NULL;
    }
''')
signature = 'run_pyc_file(FILE *fp, PyObject *globals, PyObject *locals,\n             PyCompilerFlags *flags)'
change('Python/pythonrun.c', signature+'\n{', signature+'''\n{
    if (!confos_code_fd_allowed(fileno(fp))) {
        PyErr_SetFromErrno(PyExc_PermissionError);
        fclose(fp);
        return NULL;
    }
''')
signature = '_PyRun_InteractiveOne(FILE *fp, PyObject *filename, PyCompilerFlags *flags)'
change('Python/pythonrun.c', signature+'\n{', signature+'''\n{
    if (!confos_code_fd_allowed(fileno(fp))) {
        PyErr_SetFromErrnoWithFilenameObject(PyExc_PermissionError, filename);
        return -1;
    }
''')
