command -v dpkg-query >/dev/null 2>&1 || exit 127; dpkg-query -W -f='${binary:Package}\n' | xargs -r dpkg-query -L
