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
client = Marionette(bin=shutil.which("firefox"), app="fxdesktop", profile=profile,
                    headless=True, app_args=["--no-remote"], socket_timeout=90,
                    startup_timeout=90)
try:
    client.start_session()
    installed = Addons(client).install(str(xpi), temp=False)
    assert installed == addon_id, installed
    client.quit(in_app=True)
finally:
    client.cleanup()
