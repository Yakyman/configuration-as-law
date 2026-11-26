# Invoked only inside the disposable guest.
sleep 86406 >/dev/null 2>&1 &
printf 'sleep 86407 &\n' >> "$HOME/.profile"
# Try the supplied system installer as well as saved startup execution.
confpkg install case-small-2.confpkg
