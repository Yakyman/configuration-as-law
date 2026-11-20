#!/bin/bash
set -euxo pipefail
cd /root/E3
exec >raw/setup.log 2>&1
date -u
uname -a
cat /etc/os-release
free -m
nproc
mkdir -p downloads apps raw/sources
apt-get update
apt-get install -y --no-install-recommends libdbus-glib-1-2
for version in 115.0esr 128.0esr; do
 curl --fail --location --retry 2 "https://archive.mozilla.org/pub/firefox/releases/$version/linux-x86_64/en-US/firefox-$version.tar.bz2" -o "downloads/firefox-$version.tar.bz2"
 curl --fail --location --retry 2 "https://archive.mozilla.org/pub/firefox/releases/$version/SHA512SUMS" -o "raw/sources/firefox-$version-SHA512SUMS"
 (cd downloads; grep " linux-x86_64/en-US/firefox-$version.tar.bz2$" ../raw/sources/firefox-$version-SHA512SUMS | sed 's|linux-x86_64/en-US/||' | sha512sum -c -)
 mkdir -p "apps/firefox-$version"
 tar -xjf "downloads/firefox-$version.tar.bz2" --strip-components=1 -C "apps/firefox-$version"
 mkdir -p "apps/firefox-$version/distribution"
 echo '{"policies":{"DisableAppUpdate":true,"DisableTelemetry":true,"DisableFirefoxStudies":true}}' > "apps/firefox-$version/distribution/policies.json"
 "apps/firefox-$version/firefox" --version
 done
for version in 1.18.6 1.27.0; do
 curl --fail --location --retry 2 "https://github.com/syncthing/syncthing/releases/download/v$version/syncthing-linux-amd64-v$version.tar.gz" -o "downloads/syncthing-$version.tar.gz"
 curl --fail --location --retry 2 "https://github.com/syncthing/syncthing/releases/download/v$version/sha256sum.txt.asc" -o "raw/sources/syncthing-$version-sha256sum.txt.asc"
 (cd downloads; grep " syncthing-linux-amd64-v$version.tar.gz$" ../raw/sources/syncthing-$version-sha256sum.txt.asc | sed "s|syncthing-linux-amd64-v$version.tar.gz|syncthing-$version.tar.gz|" | sha256sum -c -)
 mkdir -p "apps/syncthing-$version"
 tar -xzf "downloads/syncthing-$version.tar.gz" --strip-components=1 -C "apps/syncthing-$version"
 "apps/syncthing-$version/syncthing" --version
 for source in lib/config/config.go lib/syncthing/utils.go; do
  curl -fsSL "https://raw.githubusercontent.com/syncthing/syncthing/v$version/$source" -o "raw/sources/syncthing-$version-${source##*/}"
 done
 done
curl -fL --retry 2 https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz -o downloads/geckodriver.tar.gz
tar -xzf downloads/geckodriver.tar.gz -C apps
sha256sum downloads/* > raw/downloads.sha256
sha256sum apps/firefox-*/firefox apps/syncthing-*/syncthing apps/geckodriver > raw/executables.sha256
echo SETUP_COMPLETE
