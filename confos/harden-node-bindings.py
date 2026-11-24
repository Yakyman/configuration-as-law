#!/usr/bin/python3
"""Do not expose writable enforcement function properties to JavaScript."""
from pathlib import Path
import sys
path = Path(sys.argv[1])/'src/node_file.cc'
text = path.read_text()
for name, callback in [('readCodeFileUtf8', 'ReadCodeFileUtf8'),
                       ('readCodeFile', 'ReadCodeFile'), ('checkCodeFd', 'CheckCodeFd')]:
    old = f'  SetMethod(isolate, target, "{name}", {callback});'
    if text.count(old) != 1: raise ValueError(old)
    new = f'''  target->Set(FIXED_ONE_BYTE_STRING(isolate, "{name}"),
              NewFunctionTemplate(isolate, {callback}, Local<v8::Signature>(),
                                  v8::ConstructorBehavior::kThrow),
              static_cast<v8::PropertyAttribute>(v8::ReadOnly | v8::DontDelete));'''
    text = text.replace(old, new)
path.write_text(text)
