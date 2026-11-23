#!/usr/bin/env python3
"""Build on the server only, with a task-local runtime source overlay."""
import gzip,hashlib,json,os,pathlib,subprocess
root=pathlib.Path(__file__).resolve().parent
stage=root/'build';stage.mkdir(exist_ok=True)
goroot=pathlib.Path(subprocess.check_output(['go','env','GOROOT'],text=True).strip())
source=goroot/'src/runtime/os_linux.go';text=source.read_text()
# Go startup ordinarily reads a sysfs huge-page setting before main. This
# inventory helper does not need huge-page optimisation. Disable that read and
# the exceptional auxv/random device fallbacks without changing the toolchain.
for old,new in [
 ('physHugePageSize = getHugePageSize()','physHugePageSize = 0'),
 ('fd := open(&procAuxv[0], 0 /* O_RDONLY */, 0)','fd := int32(-1)'),
 ('fd := open(&urandom_dev[0], 0 /* O_RDONLY */, 0)','fd := int32(-1)')]:
 if old not in text:raise SystemExit('Unsupported Go runtime source; review startup reads before building')
 text=text.replace(old,new)
patched=stage/'os_linux.go';patched.write_text(text)
overlay=stage/'overlay.json';overlay.write_text(json.dumps({'Replace':{str(source):str(patched)}}))
env={**os.environ,'CGO_ENABLED':'0','GOOS':'linux','GOARCH':'amd64','GOMAXPROCS':'2','GOCACHE':str(stage/'cache'),'TMPDIR':str(stage)}
subprocess.run(['go','build','-overlay',str(overlay),'-trimpath','-ldflags=-s -w','-o',str(root/'probe-linux-amd64'),str(root/'probe.go'),str(root/'btrfs_linux.go')],check=True,env=env)
binary=(root/'probe-linux-amd64').read_bytes();(root/'probe-linux-amd64.gz').write_bytes(gzip.compress(binary,mtime=0))
(root/'probe-build.json').write_text(json.dumps({'go':subprocess.check_output(['go','version'],text=True).strip(),'binary_sha256':hashlib.sha256(binary).hexdigest(),'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'probe.go',root/'btrfs_linux.go']},'runtime_original_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'runtime_overlay_sha256':hashlib.sha256(patched.read_bytes()).hexdigest(),'runtime_changes':['disable hugepage sysfs read','disable auxv proc fallback','disable random device fallback']},indent=2)+'\n')
