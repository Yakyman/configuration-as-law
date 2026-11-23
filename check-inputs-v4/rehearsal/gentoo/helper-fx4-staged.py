#!/usr/bin/env python3
"""Called only by browser_extension inside the disposable guest."""
# https://firefox-source-docs.mozilla.org/python/marionette_driver.html
# https://addons-server.readthedocs.io/en/latest/topics/api/addons.html
# https://raw.githubusercontent.com/ClearURLs/Addon/master/manifest.json
# https://firefox-source-docs.mozilla.org/mozbase/mozprofile.html
# https://raw.githubusercontent.com/mozilla-firefox/firefox/main/testing/marionette/client/marionette_driver/geckoinstance.py
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time
import socket
import urllib.request
from mozprofile import Profile
from marionette_driver.marionette import Marionette
from marionette_driver.addons import Addons

home = Path.home()
addon_id = "{74145f27-f039-47ce-a470-a662b129930a}"
with urllib.request.urlopen("https://addons.mozilla.org/api/v5/addons/addon/clearurls/", timeout=60) as response:
    metadata = json.load(response)
assert metadata["guid"] == addon_id
release = metadata["current_version"]["file"]
with urllib.request.urlopen(release["url"], timeout=120) as response:
    payload = response.read()
algorithm, expected = release["hash"].split(":", 1)
assert hashlib.new(algorithm, payload).hexdigest() == expected
xpi = home / "Downloads/clearurls.xpi"
xpi.write_bytes(payload)
(home / "Downloads/clearurls-source.json").write_text(json.dumps({
    "id": addon_id, "version": metadata["current_version"]["version"],
    "url": release["url"], "hash": release["hash"]}, indent=2) + "\n")
# Passing a Profile object prevents GeckoInstance from cloning a path string.
# restore=False preserves the installed extension and the generated browser state.
profile = Profile(profile=str(home / ".mozilla/firefox/cal-check"), restore=False)
# Launch the self-contained application package directly. Connecting to its
# documented Marionette endpoint avoids assuming a native binary/application.ini
# directory layout for an AppImage.
profile.set_preferences({'marionette.port': 2828, 'browser.shell.checkDefaultBrowser': False,
                        'browser.startup.homepage_override.mstone': 'ignore'})
def browser_session(install):
    process = subprocess.Popen([shutil.which('firefox'), '--headless', '--no-remote',
                                '--marionette', '--profile', str(home / '.mozilla/firefox/cal-check')],
                               stdin=subprocess.DEVNULL)
    client = Marionette(host='127.0.0.1', port=2828, socket_timeout=90)
    try:
        deadline = time.monotonic() + 90
        while True:
            if process.poll() is not None:
                raise RuntimeError('Firefox exited before its automation endpoint opened')
            try:
                with socket.create_connection(('127.0.0.1', 2828), timeout=1):
                    break
            except OSError:
                if time.monotonic() >= deadline:
                    raise TimeoutError('Firefox automation endpoint did not open')
                time.sleep(0.25)
        client.start_session()
        if install:
            installed = Addons(client).install(str(xpi), temp=False)
            assert installed == addon_id, installed
        else:
            assert Addons(client).is_installed(addon_id), 'Permanent extension absent after restart'
        # close() supports an external browser; wait for a clean exit before restart.
        client.close()
        process.wait(timeout=30)
    finally:
        try:
            client.cleanup()
        finally:
            if process.poll() is None:
                process.terminate()
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

browser_session(install=True)
browser_session(install=False)
