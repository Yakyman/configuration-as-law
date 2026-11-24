#!/usr/bin/python3
"""Native code-file reads for Node CJS/ESM, stdin and REPL; data API unchanged."""
from pathlib import Path
import shutil
import subprocess
import sys
root = Path(sys.argv[1])
shutil.copyfile(Path(__file__).with_name('code-file-policy.h'), root/'src/confos-code-file-policy.h')
def change(name, old, new):
    path = root/name
    text = path.read_text()
    if text.count(old) != 1: raise ValueError((name, old, text.count(old)))
    path.write_text(text.replace(old, new))
native = 'src/node_file.cc'
change(native, '#include "node_buffer.h"', '#include "node_buffer.h"\n#include "confos-code-file-policy.h"')
change(native, 'static void ReadFileUtf8(const FunctionCallbackInfo<Value>& args) {',
       'static void ReadFileUtf8Impl(const FunctionCallbackInfo<Value>& args,\n'
       '                             bool code, bool as_buffer) {')
change(native, '  std::string result{};\n  char buffer[8192];',
       '  if (code && !confos_code_fd_allowed(file))\n'
       '    return env->ThrowUVException(UV_EACCES, "saved code input", nullptr);\n\n'
       '  std::string result{};\n  char buffer[8192];')
change(native, '  if (!ToV8Value(env->context(), result, isolate).ToLocal(&val)) {',
       '  if (as_buffer) {\n'
       '    Local<Object> bytes;\n'
       '    if (!Buffer::Copy(isolate, result.data(), result.size()).ToLocal(&bytes)) return;\n'
       '    args.GetReturnValue().Set(bytes);\n'
       '    return;\n'
       '  }\n'
       '  if (!ToV8Value(env->context(), result, isolate).ToLocal(&val)) {')
change(native, '// Wrapper for readv(2).',
       '''static void ReadFileUtf8(const FunctionCallbackInfo<Value>& args) {
  ReadFileUtf8Impl(args, false, false);
}
static void ReadCodeFileUtf8(const FunctionCallbackInfo<Value>& args) {
  ReadFileUtf8Impl(args, true, false);
}
static void ReadCodeFile(const FunctionCallbackInfo<Value>& args) {
  ReadFileUtf8Impl(args, true, true);
}
static void CheckCodeFd(const FunctionCallbackInfo<Value>& args) {
  Environment* env = Environment::GetCurrent(args);
  CHECK_GE(args.Length(), 1);
  CHECK(args[0]->IsInt32());
  if (!confos_code_fd_allowed(args[0].As<Int32>()->Value()))
    return env->ThrowUVException(UV_EACCES, "saved code input", nullptr);
}

// Wrapper for readv(2).''')
change(native, '  SetMethod(isolate, target, "readFileUtf8", ReadFileUtf8);',
       '  SetMethod(isolate, target, "readFileUtf8", ReadFileUtf8);\n'
       '  SetMethod(isolate, target, "readCodeFileUtf8", ReadCodeFileUtf8);\n'
       '  SetMethod(isolate, target, "readCodeFile", ReadCodeFile);\n'
       '  SetMethod(isolate, target, "checkCodeFd", CheckCodeFd);')
change(native, '  registry->Register(ReadFileUtf8);',
       '  registry->Register(ReadFileUtf8);\n'
       '  registry->Register(ReadCodeFileUtf8);\n'
       '  registry->Register(ReadCodeFile);\n'
       '  registry->Register(CheckCodeFd);')
cjs = 'lib/internal/modules/cjs/loader.js'
change(cjs, '    content = fs.readFileSync(filename, \'utf8\');',
       '    content = internalBinding(\'fs\').readCodeFileUtf8(filename, 0);')
esm = 'lib/internal/modules/esm/load.js'
change(esm, "const { URL } = require('internal/url');", "const { URL, fileURLToPath } = require('internal/url');")
change(esm, '    source = await readFileAsync(url);',
       "    source = context.format === 'json' ? await readFileAsync(url) :\n"
       "      internalBinding('fs').readCodeFile(fileURLToPath(url), 0);")
change(esm, '    source = readFileSync(url);',
       "    source = context.format === 'json' ? readFileSync(url) :\n"
       "      internalBinding('fs').readCodeFile(fileURLToPath(url), 0);")
translators = 'lib/internal/modules/esm/translators.js'
change(translators, "    source ??= readFileSync(new URL(url), 'utf8');",
       "    source ??= internalBinding('fs').readCodeFileUtf8(fileURLToPath(url), 0);")
change(translators, "        const source = readFileSync(resolved, 'utf-8');",
       "        const source = internalBinding('fs').readCodeFileUtf8(resolved, 0);")
change('lib/internal/process/execution.js', 'function readStdin(callback) {',
       "function readStdin(callback) {\n"
       "  if (!getOptionValue('--check')) internalBinding('fs').checkCodeFd(0);")
change('lib/repl.js', "  if (options.terminal === undefined) {",
       "  if (typeof options.input?.fd === 'number')\n"
       "    internalBinding('fs').checkCodeFd(options.input.fd);\n\n"
       "  if (options.terminal === undefined) {")
change('lib/repl.js', "          const data = fs.readFileSync(file, 'utf8');",
       "          const data = internalBinding('fs').readCodeFileUtf8(file, 0);")
subprocess.run([sys.executable, Path(__file__).with_name('harden-node-bindings.py'), root], check=True)
subprocess.run([sys.executable, Path(__file__).with_name('patch-node-metadata.py'), root], check=True)
subprocess.run([sys.executable, Path(__file__).with_name('patch-node-startup.py'), root], check=True)
