# Source from a persistent worker harness that needs a guest and an appliance.
confos_reserve_guest() {
    while true; do
        for slot in {1..6}; do
            exec {confos_guest_slot}>"$HOME/VMs/confos/slots/slot-$slot.lock"
            if flock -n "$confos_guest_slot"; then return; fi
            exec {confos_guest_slot}>&-
        done
        echo 'Waiting for one shared slot before starting the probe guest'
        sleep 5
    done
}

confos_reserve_pair() {
    while true; do
        for first in {1..6}; do
            exec {confos_inventory_slot}>"$HOME/VMs/confos/slots/slot-$first.lock"
            if flock -n "$confos_inventory_slot"; then
                for second in {1..6}; do
                    [ "$first" != "$second" ] || continue
                    exec {confos_guest_slot}>"$HOME/VMs/confos/slots/slot-$second.lock"
                    if flock -n "$confos_guest_slot"; then return; fi
                    exec {confos_guest_slot}>&-
                done
            fi
            exec {confos_inventory_slot}>&-
        done
        echo 'Waiting for two shared slots before starting the probe guest'
        sleep 5
    done
}
confos_boot_reserved() {
    CONFOS_SLOT_FD=$confos_guest_slot ./boot.sh "$@" &
    confos_vm_pid=$!
}
confos_stop_reserved() {
    if [ -n "${confos_vm_pid:-}" ]; then
        kill "$confos_vm_pid" 2>/dev/null || true
        wait "$confos_vm_pid" 2>/dev/null || true
        unset confos_vm_pid
    fi
}
