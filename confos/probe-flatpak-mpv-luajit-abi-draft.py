#!/usr/bin/python3
"""Original-runtime ABI controls for a private library candidate, no guest."""
from pathlib import Path
import subprocess
import hashlib

root = Path.cwd()
base = root/'interpreter-inputs/flatpak-analysis/root/usr/lib/confos/flatpak'
app = base/'app/io.mpv.Mpv/x86_64/stable/13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc/files'
runtime = base/'runtime/org.freedesktop.Platform/x86_64/26.08/df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c/files'
target = 'lib/libluajit-5.1.so.2.1.1781966178'
candidate = root/'interpreter-inputs/flatpak-mpv-lua-candidate/candidate'/Path(target).name
def symbols(path):
    output = subprocess.check_output(['readelf', '--dyn-syms', '--wide', str(path)], text=True)
    return {fields[7] for line in output.splitlines() if len(fields := line.split()) >= 8
            and fields[4] in ('GLOBAL', 'WEAK') and fields[6] != 'UND'}
original_symbols, new_symbols = symbols(app/target), symbols(candidate)
missing = original_symbols-new_symbols
print('MISSING_EXPORTED_SYMBOLS', sorted(missing), flush=True)
print('ADDED_EXPORTED_SYMBOLS', sorted(new_symbols-original_symbols), flush=True)
assert not missing
print('CANDIDATE_SHA256', hashlib.sha256(candidate.read_bytes()).hexdigest(), flush=True)
command = ['bwrap', '--unshare-all', '--die-with-parent', '--clearenv',
           '--ro-bind', str(runtime), '/usr', '--ro-bind', str(app), '/app',
           '--symlink', 'usr/bin', '/bin', '--symlink', 'usr/lib', '/lib',
           '--symlink', 'usr/lib64', '/lib64', '--proc', '/proc', '--dev', '/dev',
           '--tmpfs', '/tmp', '--setenv', 'PATH', '/app/bin:/usr/bin',
           '--setenv', 'HOME', '/tmp', '--setenv', 'LC_ALL', 'C',
           '--setenv', 'LD_LIBRARY_PATH', '/app/lib:/usr/lib/x86_64-linux-gnu']
for patched in (False, True):
    prefix = command+(['--ro-bind', str(candidate), '/app/'+target] if patched else [])
    for label, args, data in [
        ('version', ['/app/bin/mpv', '--version'], None),
        ('typed-pipe-lua', ['--symlink', '/proc/self/fd/0', '/tmp/typed.lua', '/app/bin/mpv',
          '--no-config', '--load-scripts=no', '--vo=null', '--ao=null', '--idle=yes', '--script=/tmp/typed.lua'],
         'print("LUA_NATIVE_CONTROL",jit.version); '
         'local f=assert(io.open("/tmp/nested.lua","w")); f:write("return 47\\n"); f:close(); '
         'assert(assert(loadfile("/tmp/nested.lua"))()==47); '
         'assert(dofile("/tmp/nested.lua")==47); package.path="/tmp/?.lua"; '
         'assert(require("nested")==47); '
         'local d=assert(io.open("/tmp/nested.lua","r")); assert(d:read("*a")=="return 47\\n"); d:close(); '
         'print("UNCONFINED_LOADFILE_DOFILE_REQUIRE_DATA_CONTROL"); mp.commandv("quit")\n')]:
        result = subprocess.run(prefix+args, input=data, text=True, capture_output=True, timeout=30)
        print('PATCHED', patched, label, 'RC', result.returncode, flush=True)
        print(result.stdout, result.stderr, flush=True)
        assert result.returncode == 0
        if data:
            assert 'LUA_NATIVE_CONTROL' in result.stdout+result.stderr
            assert 'UNCONFINED_LOADFILE_DOFILE_REQUIRE_DATA_CONTROL' in result.stdout+result.stderr
print('ORIGINAL_RUNTIME_LUAJIT_ABI_AND_TYPED_PIPE_CONTROLS_PASS', flush=True)
