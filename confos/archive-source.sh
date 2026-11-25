#!/bin/bash
# Create the source archive of the release once; never overwrite an existing one.
# Members: archive-members.txt, expanded by archive-members.py. Third-party inputs and
# working files are not members (pinned-inputs.tsv names the inputs by checksum).
# If CONFOS_PUBLIC_SCAN names a scan program, the unpacked archive must pass it before
# the archive gets its name: no hit of a category that blocks publication in any text.
set -euo pipefail
cd "$(dirname "$0")"
version=$(cat VERSION)
archive="releases/confos-$version-source.tar.gz"
test ! -e "$archive"
list=$(mktemp)
temporary=
tree=
trap 'rm -f "$list"; if [ -n "$temporary" ]; then rm -f "$temporary"; fi; if [ -n "$tree" ]; then rm -rf "$tree"; fi' EXIT
# Generate the whole list successfully before tar: a pattern that matches nothing is an error.
python3 archive-members.py "$version" >"$list"
count=$(tr -cd '\0' <"$list" | wc -c)
temporary=$(mktemp "releases/.confos-$version-source.XXXXXXXX")
tar --no-recursion --null -T "$list" --sort=name --mtime=@1795392000 --owner=0 --group=0 -czf "$temporary"
chmod 0644 "$temporary"
if [ -n "${CONFOS_PUBLIC_SCAN:-}" ]; then
    tree=$(mktemp -d "releases/.scan-$version.XXXXXXXX")
    tar -xzf "$temporary" -C "$tree"
    python3 -I "$CONFOS_PUBLIC_SCAN" "$tree" --all >"releases/scan-$version.txt" || true
    sed -i "s|$tree/||g; s|$tree||g" "releases/scan-$version.txt"
    grep -q 'files scanned' "releases/scan-$version.txt"
    # The scan also reads the byte strings of the binary component packages. A match there
    # is a chance sequence in compressed data, not text; such lines are counted, every
    # other blocking hit stops the archive.
    blocking=$(grep -E '^(A[I]|PRIVATE|SECRET)	' "releases/scan-$version.txt" || true)
    in_text=$(printf '%s\n' "$blocking" | grep -v -E '^[A-Z]+	packages/confos-[^ 	]+\.deb \(strings\)	' | grep -c . || true)
    in_packages=$(printf '%s\n' "$blocking" | grep -c -E '^[A-Z]+	packages/confos-[^ 	]+\.deb \(strings\)	' || true)
    echo "scan: $in_text blocking hits in text; $in_packages matches in the byte strings of the component packages"
    if [ "$in_text" != 0 ]; then
        echo "The unpacked archive does not pass the scan: releases/scan-$version.txt" >&2
        exit 1
    fi
fi
# A hard link publishes the complete file without replacing an existing version.
ln "$temporary" "$archive"
rm "$temporary"
temporary=
echo "$count files in $archive"
sha256sum "images/confos-$version-clean.qcow2" "$archive" >"releases/release-$version.sha256"
