#!/bin/sh
find /var/log/zypp /var/log/YaST2 /var/log/transactional-update /var/log/combustion /var/lib/combustion -type f -size -16M -exec grep -aEn -- 'ca-certificates|update-ca-certificates|p11-kit|trust anchor' {} +
command -v trust >/dev/null && trust list
command -v pkg-config >/dev/null && pkg-config --variable p11_trust_paths p11-kit-1
command -v openssl >/dev/null && openssl version -d
printf "CURRENT_FD_BEGIN\n"
for p in /proc/[0-9]*/fd/*; do t=$(readlink "$p") || continue; case "$t" in /var/lib/ca-certificates/openssl/*|/etc/ssl/certs/*|/etc/pki/trust/*) printf "%s\t%s\n" "$p" "$t";; esac; done
printf "CURRENT_FD_END\nCURRENT_MAPS_BEGIN\n"
grep -lE "p11-kit-trust|/var/lib/ca-certificates/openssl/|/etc/ssl/certs/|/etc/pki/trust/" /proc/[0-9]*/maps
printf "CURRENT_MAPS_END\n"
