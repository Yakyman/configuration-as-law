#!/usr/bin/python3
"""Run only in disposable VM as root. Attempts retain full stdout/stderr per row."""
import hashlib,json,os,pathlib,shlex,subprocess,sys,time
OUT=pathlib.Path(sys.argv[1]);OUT.mkdir(parents=True,exist_ok=True)
rows=[]
def run(ident,channel,command,expected,user='alice',timeout=40,contains=None):
    argv=['runuser','-u',user,'--','/usr/local/bin/cal-login','-c',command] if user!='root' else ['/bin/bash','-c',command]
    before=pathlib.Path('/var/lib/cal/current.json').read_bytes()
    try:
        p=subprocess.run(argv,capture_output=True,text=True,timeout=timeout)
        rc,stdout,stderr=p.returncode,p.stdout,p.stderr
    except subprocess.TimeoutExpired as e:
        rc=124;stdout=(e.stdout or b'').decode() if isinstance(e.stdout,bytes) else (e.stdout or '');stderr=str(e)
    after=pathlib.Path('/var/lib/cal/current.json').read_bytes()
    met=(rc!=0) if expected=='blocked' else (rc==0 and (contains is None or contains in stdout)) if expected=='works' else None
    row=dict(id=ident,channel=channel,command=command,user=user,expected=expected,observed=('blocked' if rc else 'executed'),returncode=rc,met=met,stdout=stdout,stderr=stderr,declaration_before=hashlib.sha256(before).hexdigest(),declaration_after=hashlib.sha256(after).hexdigest(),utc=time.strftime('%FT%TZ',time.gmtime()))
    (OUT/(ident+'.json')).write_text(json.dumps(row,indent=2)+'\n');rows.append(row)
    print(json.dumps({k:row[k] for k in ('id','returncode','expected','met')}),flush=True)
    return row
def rootdoc(doc,label):
    pathlib.Path('/etc/cal/root.json').write_text(json.dumps(doc))
    return run(label,'declaration apply','calctl apply','works','root',180)
base=dict(archive='keep',programs={},policies={},allow_channels={},shared={})
for user in ('alice','bob'):
    path=pathlib.Path('/home')/user/'declaration.json';path.write_text('{"programs":{}}\n')
rootdoc(base,'00-reset')
run('01-identity','identity','id; cat /proc/self/attr/current','works',contains='cal-alice (enforce)')
run('02-system-package','system package manager','apt-get install -y hello','blocked')
run('03-pip-global','pip global','pip3 install --break-system-packages /srv/cal-web/python-package','blocked')
run('04-pip-user','pip user','pip3 install --user --break-system-packages /srv/cal-web/python-package','blocked')
run('05-npm-global','npm global','npm install --global /srv/cal-web/node-package','blocked')
run('06-npm-user','npm user','npm install --prefix "$HOME/local-node" /srv/cal-web/node-package','blocked')
run('07-flatpak-system','Flatpak system','flatpak install --system --noninteractive /srv/cal-web/probe.flatpak','blocked')
run('08-flatpak-user','Flatpak user','flatpak install --user --noninteractive /srv/cal-web/probe.flatpak','blocked')
run('09-appimage','AppImage','curl -fsS http://127.0.0.1:8080/probe.AppImage -o "$HOME/probe.AppImage" && chmod +x "$HOME/probe.AppImage" && "$HOME/probe.AppImage" --appimage-extract-and-run','blocked')
run('10-download-home','download into home','curl -fsS http://127.0.0.1:8080/downloaded -o "$HOME/downloaded" && chmod +x "$HOME/downloaded" && "$HOME/downloaded"','blocked')
run('11-download-tmp','download into tmp','curl -fsS http://127.0.0.1:8080/downloaded -o /tmp/downloaded && chmod +x /tmp/downloaded && /tmp/downloaded','blocked')
run('12-archive','archive download/extract','mkdir -p "$HOME/unpacked" && curl -fsS http://127.0.0.1:8080/program.tar.gz -o "$HOME/program.tar.gz" && tar -xzf "$HOME/program.tar.gz" -C "$HOME/unpacked" && "$HOME/unpacked/downloaded"','blocked')
run('13-build','build in home',"printf '#include <stdio.h>\\nint main(){puts(\"source program\");}\\n' >\"$HOME/probe.c\"; gcc \"$HOME/probe.c\" -o \"$HOME/built\" && \"$HOME/built\"",'blocked')
run('14-user-service','systemd user unit',"mkdir -p \"$HOME/.config/systemd/user\"; printf '[Service]\\nExecStart=/home/alice/downloaded\\n' >\"$HOME/.config/systemd/user/probe.service\"; systemctl --user daemon-reload && systemctl --user start probe.service",'blocked')
run('15-user-timer','systemd user timer','systemd-run --user --on-active=1 /home/alice/downloaded','blocked')
run('16-cron','cron',"printf '* * * * * /home/alice/downloaded\\n' | crontab -",'blocked')
run('17-python-script','interpreter Python',"printf 'print(\"USER_SCRIPT\")\\n' >\"$HOME/probe.py\"; python3 \"$HOME/probe.py\"",'O5 unresolved')
run('18-shell-script','interpreter shell',"printf 'echo USER_SCRIPT\\n' >\"$HOME/probe.sh\"; bash \"$HOME/probe.sh\"",'O5 unresolved')
run('19-system-write','system tree','printf forbidden >/usr/local/forbidden','blocked')
run('20-loader','direct dynamic loader','/lib64/ld-linux-x86-64.so.2 "$HOME/downloaded"','blocked')
allow={**base,'allow_channels':{'alice':['download']}}
rootdoc(allow,'21-allow-apply')
run('22-allow-home','explicit allow line home','"$HOME/downloaded"','works',contains='Hello, world!')
run('23-allow-tmp','explicit allow line tmp','/tmp/downloaded','works',contains='Hello, world!')
rootdoc(base,'24-revoke-apply')
run('25-revoked','allow line revoked','"$HOME/downloaded"','blocked')
run('26-install','ordinary declaration install',"printf '%s\\n' '{\"programs\":{\"hello\":{\"version\":\"1\"}}}' >\"$HOME/declaration.json\" && calctl apply && /usr/bin/hello",'works',timeout=180,contains='Hello, world!')
run('27-network','ordinary network','curl -fsS http://127.0.0.1:8080/; curl -I -sS --max-time 20 https://www.debian.org/','works')
update={**base,'system_update':'apt-upgrade-request-1'}
rootdoc(update,'28-update')
run('29-update-packages','ordinary update evidence','dpkg-query -W -f=\'${Package} ${Version}\\n\' | sort','works','root')
run('30-browser-declare','ordinary browser declare',"printf '%s\\n' '{\"programs\":{\"hello\":{\"version\":\"1\"},\"browser\":{\"version\":\"1\"}}}' >\"$HOME/declaration.json\" && calctl apply",'works',timeout=180)
browser='/usr/lib/chromium/chromium --headless --no-sandbox --disable-dev-shm-usage --disable-gpu --no-first-run --no-default-browser-check --user-data-dir=/var/lib/cal/active/browser --dump-dom http://127.0.0.1:8080/'
run('31-browser','ordinary browser',browser,'works',timeout=60,contains='CAL browser fixture')
run('32-extension-prepare','browser extension derivative',"mkdir -p \"$HOME/extension\"; printf '%s' '{\"manifest_version\":3,\"name\":\"CAL extension fixture\",\"version\":\"1.0\",\"content_scripts\":[{\"matches\":[\"http://127.0.0.1/*\"],\"js\":[\"content.js\"]}]}' >\"$HOME/extension/manifest.json\"; printf '%s' 'document.body.append(\"EXTENSION_EXECUTED\");' >\"$HOME/extension/content.js\"",'works')
run('33-extension','extension within declared browser',browser.replace('--dump-dom','--load-extension=/home/alice/extension --disable-extensions-except=/home/alice/extension --virtual-time-budget=3000 --dump-dom'),'works',timeout=60,contains='EXTENSION_EXECUTED')
run('34-root-managed','managed root program write','/usr/local/lib/cal/worker --probe','blocked','root')
run('35-root-unconfined','unmanaged root program write',"/bin/sh -c 'printf ROOT_PROGRAM_UNCONFINED >/usr/local/root-program-probe'; cat /usr/local/root-program-probe",'coverage defect','root')
for ident,channel in [('36-wifi','Wi-Fi'),('37-bluetooth','Bluetooth')]:
    run(ident,channel,'ls -l /sys/class/ieee80211 /sys/class/bluetooth','hardware absent','root')
run('38-audit','AppArmor audit','journalctl -k --no-pager | grep -E \'apparmor=|DENIED\'','evidence','root')
(OUT/'rows.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'summary':len(rows),'unexpected':[r['id'] for r in rows if r['met'] is False]}))
