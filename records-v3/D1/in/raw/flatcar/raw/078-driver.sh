find /sys/devices -type l -name driver -exec sh -c 'for p do printf "%s\t%s\n" "$p" "$(readlink "$p")"; done' sh {} +
