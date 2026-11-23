command -v apk >/dev/null 2>&1 || exit 127; apk info | xargs -r apk info -L
