#!/bin/sh
# Reads installed manual page configuration.nix(5); no state change.
export MANWIDTH=110 PAGER=cat
echo "== configuration.nix(5): users.mutableUsers (full entry)"
man configuration.nix 2>/dev/null | col -b | awk '/^ +users\.mutableUsers$/{p=1;n=0} p{print; if(++n>24) p=0}'
