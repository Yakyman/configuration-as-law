#!/bin/sh
set -u
echo "== date"; date -u +%FT%TZ
echo "== release"; nixos-version
echo "== declaration line"; grep -n 'extraGroups' /etc/nixos/configuration.nix
echo "== application 1: nixos-rebuild switch"; nixos-rebuild switch > /tmp/rb1.log 2>&1; echo "status=$?"; tail -n 15 /tmp/rb1.log
echo "== id before"; id -nG user
echo "== gpasswd -d user wheel"; gpasswd -d user wheel; echo "status=$?"
echo "== id after gpasswd"; id -nG user
echo "== declaration unchanged"; grep -c 'extraGroups = \[ "wheel" \]' /etc/nixos/configuration.nix
echo "== application 2: nixos-rebuild switch"; nixos-rebuild switch > /tmp/rb2.log 2>&1; echo "status=$?"; tail -n 15 /tmp/rb2.log
echo "== id after application 2"; id -nG user
if ! id -nG user | grep -qw wheel; then echo "== restore"; gpasswd -a user wheel; echo "status=$?"; fi
echo "== date"; date -u +%FT%TZ
