command -v dconf >/dev/null || exit 127
profile=$(mktemp /tmp/s4-dconf-profile.XXXXXX) || exit 1
trap 'rm -f "$profile"' EXIT HUP INT TERM
printf "%s\n" system-db:distro > "$profile"
DCONF_PROFILE="$profile" dconf dump /

