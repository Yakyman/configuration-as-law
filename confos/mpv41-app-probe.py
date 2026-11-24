#!/usr/bin/python3
"""Recorded native-app controls; all claims require observed markers."""
import ctypes
import math
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import time
import wave

assert Path('/proc/self/attr/current').read_text().strip() == 'confos-flatpak (enforce)'
assert Path('/.flatpak-info').is_file()
assert os.geteuid() != 0
home = Path('/home/user/.var/app/io.mpv.Mpv'); home.mkdir(parents=True, exist_ok=True)
lua = 'print("UNRECORDED-MPV41-RAN"); mp.commandv("quit", "0")\n'
js = 'print("UNRECORDED-MPV41-RAN"); mp.commandv("quit", "0");\n'
base = ['/app/bin/mpv', '--no-config', '--vo=null', '--ao=null', '--idle=yes', '--load-scripts=no',
        '--script=/home/user/bin/mpv41-watchdog.lua']

def run(arguments, marker=None, blocked=False, input_text=None, pass_fds=()):
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=20,
                            input=input_text, pass_fds=pass_fds)
    output = result.stdout+result.stderr
    print('COMMAND', arguments, 'EXIT', result.returncode, '\n'+output, flush=True)
    if blocked:
        assert 'UNRECORDED-MPV41-RAN' not in output, output
        assert 'ConfOS: Permission denied for saved code input' in output, output
    else:
        assert result.returncode == 0, output
        if marker: assert marker in output, output
    return output

run(['/app/bin/mpv', '--version'], 'mpv ')
for directory in (home, Path('/tmp'), Path('/dev/shm')):
    for extension, content in [('lua', lua), ('js', js)]:
        path = directory/('mpv41-material.'+extension); path.write_text(content)
        run(base+['--script='+str(path)], blocked=True)
for extension, marker in [('lua', 'RECORDED-MPV41-LUA'), ('js', 'RECORDED-MPV41-JS')]:
    run(base+['--script=/home/user/bin/mpv41-positive.'+extension], marker)
    alias = Path('/tmp')/('mpv41-typed.'+extension)
    alias.unlink(missing_ok=True); alias.symlink_to('/proc/self/fd/0')
    typed = ('print("MPV41-TYPED-PIPE-PASS"); mp.commandv("quit", "0")'+(';' if extension == 'js' else '')+'\n')
    run(base+['--script='+str(alias)], 'MPV41-TYPED-PIPE-PASS', input_text=typed)
    alias.unlink(); alias.symlink_to(home/('mpv41-material.'+extension))
    run(base+['--script='+str(alias)], blocked=True)
    for descriptor_root in ('/proc/self/fd', '/dev/fd'):
        for path, blocked in [(home/('mpv41-material.'+extension), True),
                              (Path('/home/user/bin/mpv41-positive.'+extension), False)]:
            with path.open('rb') as opened:
                alias.unlink(); alias.symlink_to(descriptor_root+'/'+str(opened.fileno()))
                run(base+['--script='+str(alias)], marker if not blocked else None,
                    blocked=blocked, pass_fds=(opened.fileno(),))
for route, extension in [('loadfile', 'lua'), ('dofile', 'lua'), ('require', 'lua'), ('require', 'js')]:
    run(base+[f'--script=/home/user/bin/mpv41-{route}-negative.{extension}'], blocked=True)
    run(base+[f'--script=/home/user/bin/mpv41-{route}-positive.{extension}'], 'RECORDED-MPV41-MODULE')
(home/'mpv41-data').write_text('MATERIAL')
for extension in ('lua', 'js'):
    run(base+['--script=/home/user/bin/mpv41-data.'+extension], 'MPV41-DATA-PASS')
(home/'mpv41-eval-data').write_text('print("MPV41-DATA-EVAL-PASS");')
run(base+['--script=/home/user/bin/mpv41-data-eval.js'], 'MPV41-DATA-EVAL-PASS')
# The same automatic config script entry reported in search entry1.
config = home/'mpv41-mpv.conf'
for extension, content in [('lua', lua), ('js', js)]:
    path = home/('mpv41-material.'+extension)
    config.write_text('script='+str(path)+'\n')
    run(base+['--include='+str(config)], blocked=True)
# Native scripting.c discovers config/scripts entries, including directories
# whose entry point is main.lua or main.js. Exercise both languages separately.
for extension, content in [('lua', lua), ('js', js)]:
    for directory_entry in (False, True):
        with tempfile.TemporaryDirectory(prefix='mpv41-auto-', dir=home) as temporary:
            configdir = Path(temporary)
            scripts = configdir/'scripts'; scripts.mkdir()
            if directory_entry:
                entry = scripts/'module'; entry.mkdir()
                source = entry/('main.'+extension)
            else:
                source = scripts/('automatic.'+extension)
            automatic = [value for value in base if value not in ('--no-config', '--load-scripts=no')]
            automatic += ['--config-dir='+str(configdir), '--load-scripts=yes']
            source.write_text(content)
            run(automatic, blocked=True)
            source.unlink()
            source.symlink_to('/home/user/bin/mpv41-positive.'+extension)
            run(automatic, 'RECORDED-MPV41-'+extension.upper())
            print('MPV41 AUTOMATIC DISCOVERY PASS', extension, directory_entry, flush=True)
# Ordinary saved media remains readable as data.
audio = home/'mpv41-tone.wav'
with wave.open(str(audio), 'wb') as stream:
    stream.setnchannels(1); stream.setsampwidth(2); stream.setframerate(8000)
    stream.writeframes(b''.join(struct.pack('<h', int(4000*math.sin(2*math.pi*440*i/8000))) for i in range(800)))
media = [value for value in base if value != '--script=/home/user/bin/mpv41-watchdog.lua']
run(media+['--script=/home/user/bin/mpv41-media.lua', str(audio)], 'MPV41-MEDIA-EOF-PASS')
print('MPV41 ORDINARY MEDIA PASS', flush=True)
# Native library startup must use the same guarded Lua reader as the executable.
library = ctypes.CDLL('/app/lib/libmpv.so.2')
library.mpv_create.restype = ctypes.c_void_p
library.mpv_set_option_string.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
library.mpv_initialize.argtypes = [ctypes.c_void_p]
library.mpv_terminate_destroy.argtypes = [ctypes.c_void_p]
library.mpv_request_log_messages.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
class LogMessage(ctypes.Structure):
    _fields_ = [('prefix', ctypes.c_char_p), ('level', ctypes.c_char_p),
                ('text', ctypes.c_char_p), ('log_level', ctypes.c_int)]
class Event(ctypes.Structure):
    _fields_ = [('event_id', ctypes.c_int), ('error', ctypes.c_int),
                ('reply_userdata', ctypes.c_ulonglong), ('data', ctypes.c_void_p)]
library.mpv_wait_event.argtypes = [ctypes.c_void_p, ctypes.c_double]
library.mpv_wait_event.restype = ctypes.POINTER(Event)
marker = home/'mpv41-api-marker'
material = home/'mpv41-api.lua'
material.write_text('io.open("'+str(marker)+'", "w"):close(); mp.commandv("quit", "0")\n')
(home/'mpv41-api.js').write_text(js)
for source, expected in [(material, False), (Path('/home/user/bin/mpv41-api.lua'), True),
                         (home/'mpv41-api.js', False), (Path('/home/user/bin/mpv41-api.js'), True)]:
    marker.unlink(missing_ok=True)
    handle = library.mpv_create(); assert handle
    # The descriptor-policy helper writes directly to fd 2, outside mpv's log
    # event API. Capture it as well as API logs, restoring stderr on every path.
    captured = tempfile.TemporaryFile(mode='w+b', dir=home)
    saved_stderr = os.dup(2)
    log_messages = []
    try:
        os.dup2(captured.fileno(), 2)
        assert library.mpv_request_log_messages(handle, b'info') >= 0
        for key, value in {'config':'no', 'idle':'yes', 'vo':'null', 'ao':'null', 'terminal':'yes', 'load-scripts':'no', 'scripts':str(source)}.items():
            assert library.mpv_set_option_string(handle, key.encode(), value.encode()) >= 0, key
        assert library.mpv_initialize(handle) >= 0
        deadline = time.monotonic()+3
        shutdown = False
        while time.monotonic() < deadline:
            event = library.mpv_wait_event(handle, .05).contents
            if event.event_id == 2:
                message = ctypes.cast(event.data, ctypes.POINTER(LogMessage)).contents
                log_messages.append(message.text.decode(errors='replace'))
            if event.event_id == 1:
                shutdown = True
                break
        assert shutdown == expected, (source, expected)
        if source.suffix == '.lua': assert marker.exists() == expected, (source, expected)
    finally:
        try:
            library.mpv_terminate_destroy(handle)
        finally:
            os.dup2(saved_stderr, 2); os.close(saved_stderr)
            captured.seek(0)
            output = captured.read().decode(errors='replace')+''.join(log_messages)
            captured.close()
    print(output, flush=True)
    if expected:
        assert 'RECORDED-MPV41-API-'+source.suffix[1:].upper() in output, output
    else:
        assert 'ConfOS: Permission denied for saved code input' in output, output
        assert 'UNRECORDED-MPV41-RAN' not in output, output
    print('MPV41 LIBMPV INPUT PASS', source, expected, flush=True)
print('MPV41 APP INPUT CONTROLS PASS', flush=True)
