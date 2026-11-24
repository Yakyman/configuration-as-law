#!/usr/bin/python3
"""Future41 guest fixture; never build before the numbered transition."""
import hashlib
from pathlib import Path
import shutil
import subprocess

assert Path('VERSION').read_text() == '0.41\n'
work = Path('mpv-041-fixture'); work.mkdir(exist_ok=True)
shutil.copyfile('examples/recorded.sh', work/'recorded.sh')
text = Path('examples/development.conf').read_text()
text += ('package flatpak 1.16.6-1~deb13u3\npackage util-linux 2.41.5-0+deb13u1\n'
         'package gpg 2.4.7-21+deb13u1+b5\npackage gpg-agent 2.4.7-21+deb13u1+b5\n')
for name, ref, commit in (
    ('runtime', 'runtime/org.freedesktop.Platform/x86_64/26.08', 'df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c'),
    ('mpv', 'app/io.mpv.Mpv/x86_64/stable', '13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc')):
    source = Path('flatpak-inputs')/(name+'.flatpak')
    shutil.copyfile(source, work/source.name)
    text += f'flatpak {ref} {commit} {hashlib.sha256(source.read_bytes()).hexdigest()} {source.name}\n'

payloads = {
    'mpv41-app-probe.py': Path('mpv41-app-probe.py').read_bytes(),
    'recorded-flatpak-bash.sh': b'echo RECORDED-BASH-RAN\n',
    'recorded-flatpak-python.py': b'print("RECORDED-PYTHON-RAN")\n',
    'recorded_flatpak_module.py': b'print("RECORDED-PYTHON-RAN")\n',
    'mpv41-positive.lua': b'print("RECORDED-MPV41-LUA"); mp.commandv("quit", "0")\n',
    'mpv41-positive.js': b'print("RECORDED-MPV41-JS"); mp.commandv("quit", "0");\n',
    'mpv41-module.lua': b'print("RECORDED-MPV41-MODULE"); return {}\n',
    'mpv41-module.js': b'print("RECORDED-MPV41-MODULE"); module.exports = {};\n',
    'mpv41-api.lua': b'io.open("/home/user/.var/app/io.mpv.Mpv/mpv41-api-marker", "w"):close(); print("RECORDED-MPV41-API-LUA"); mp.commandv("quit", "0")\n',
    'mpv41-api.js': b'print("RECORDED-MPV41-API-JS"); mp.commandv("quit", "0");\n',
    'mpv41-watchdog.lua': b'mp.add_timeout(2, function() mp.commandv("quit", "0") end)\n',
}
for suffix, path in [('negative', '/home/user/.var/app/io.mpv.Mpv/mpv41-material'),
                     ('positive', '/home/user/bin/mpv41-module')]:
    for route in ('loadfile', 'dofile', 'require'):
        expression = (f'assert(loadfile("{path}.lua"))()' if route == 'loadfile' else
                      f'dofile("{path}.lua")' if route == 'dofile' else
                      f'package.path="{path.rsplit("/",1)[0]}/?.lua"; require("{path.rsplit("/",1)[1]}")')
        payloads[f'mpv41-{route}-{suffix}.lua'] = (
            'local ok, err = pcall(function() '+expression+' end); '
            'if not ok then print("NESTED-MPV41-BLOCKED", err) end; mp.commandv("quit", "0")\n').encode()
    payloads[f'mpv41-require-{suffix}.js'] = (
        'try { require("'+path+'"); } catch (e) { print("NESTED-MPV41-BLOCKED", String(e)); } '
        'mp.commandv("quit", "0");\n').encode()
payloads['mpv41-data.lua'] = (
    'local f=assert(io.open("/home/user/.var/app/io.mpv.Mpv/mpv41-data", "r")); '
    'assert(f:read("*a")=="MATERIAL"); f:close(); print("MPV41-DATA-PASS"); mp.commandv("quit","0")\n').encode()
payloads['mpv41-data.js'] = (
    'if(mp.utils.read_file("/home/user/.var/app/io.mpv.Mpv/mpv41-data") !== "MATERIAL") throw Error("data"); '
    'print("MPV41-DATA-PASS"); mp.commandv("quit","0");\n').encode()
payloads['mpv41-data-eval.js'] = (
    'var text = mp.utils.read_file("/home/user/.var/app/io.mpv.Mpv/mpv41-eval-data"); '
    'mp.utils.compile_js("explicit-data", text)(); mp.commandv("quit", "0");\n').encode()
payloads['mpv41-media.lua'] = b'''local loaded = false
local decoded = false
mp.register_event("file-loaded", function()
    loaded = true
    print("MPV41-MEDIA-FILE-LOADED")
end)
mp.observe_property("audio-params/samplerate", "number", function(name, value)
    if value == 8000 then decoded = true; print("MPV41-MEDIA-DECODED-8000") end
end)
mp.register_event("end-file", function(event)
    if loaded and decoded and event.reason == "eof" then
        print("MPV41-MEDIA-EOF-PASS"); mp.commandv("quit", "0")
    else
        mp.commandv("quit", "3")
    end
end)
mp.add_timeout(10, function() mp.commandv("quit", "3") end)
'''
for name, data in payloads.items():
    (work/name).write_bytes(data)
    text += f'file /home/user/bin/{name} 0644 0:0 {hashlib.sha256(data).hexdigest()} {name}\n'
data = payloads['recorded-flatpak-bash.sh']
text += f'file /home/user/bin/login/.bash_profile 0644 0:0 {hashlib.sha256(data).hexdigest()} recorded-flatpak-bash.sh\n'
(work/'declaration.conf').write_text(text)
subprocess.run(['bash', 'build.sh', str(work/'declaration.conf'), 'images/mpv-041.qcow2'], check=True)
print('MPV41 FIXTURE BUILT', flush=True)
