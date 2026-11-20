import experiment as e
import json,os,threading,time
# Same direct CLI and local-page fixture as the refusal, now with a closed old-state copy.
e.event('supplement-environment',MOZ_ALLOW_DOWNGRADE=os.environ.get('MOZ_ALLOW_DOWNGRADE'),MOZ_HEADLESS=os.environ.get('MOZ_HEADLESS'))
server=e.http.server.ThreadingHTTPServer(('127.0.0.1',18080),e.Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
profile=e.clone(e.W/'ff-old-snapshot','ff-direct-positive')
args=[str(e.A/'firefox-115.0esr/firefox'),'--headless','--no-remote','--profile',str(profile),'--screenshot',str(e.W/'ff-positive.png'),'http://127.0.0.1:18080/ff-direct-positive']
try:
    p=e.command('ff-direct-positive',args,timeout=30)
    e.event('ff-direct-positive-result',returncode=p.returncode,screenshot_exists=(e.W/'ff-positive.png').exists(),screenshot_bytes=(e.W/'ff-positive.png').stat().st_size if (e.W/'ff-positive.png').exists() else 0)
    e.shutil.copy2(e.W/'ff-positive.png',e.R/'ff-direct-positive.png')
finally:server.shutdown();server.server_close()
# The config-only remedy has run the old binary on the newer index. Check it with the new binary too.
s=e.Sync()
try:
    assert s.start('st-new-after-config-remedy','1.27.0',e.W/'st-rollback-archived-config')
    s.scan('st-new-after-config-remedy',2)
finally:s.stop()
e.inspect('st-after-config-remedy-recovery',e.W/'st-rollback-archived-config','syncthing')
# Preserve the source-file data and the post-remedy states for independent reinspection.
with e.tarfile.open(e.R/'st-source-files.tar.gz','w:gz') as tar:tar.add(e.W/'sync-files',arcname='sync-files')
for name in ['ff-rollback-latest','ff-rollback-snapshot','st-rollback-latest','st-rollback-snapshot','st-rollback-archived-config']:
    with e.tarfile.open(e.R/(name+'-final.tar.gz'),'w:gz') as tar:tar.add(e.W/name,arcname=name)
e.event('supplement-complete')
