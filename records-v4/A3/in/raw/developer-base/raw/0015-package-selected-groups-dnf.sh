test -r /var/lib/dnf/history.sqlite || exit 127; python3 -I -c '"""Read DNF4'"'"'s persisted selected groups; never load repo or package code."""
import json
import dnf
import libdnf.transaction

with dnf.Base() as base:
    history = base.history.swdb
    user = libdnf.transaction.TransactionItemReason_USER
    selected = {}
    # The native search uses SQL LIKE. '"'"'%'"'"' includes every persisted ID; each
    # result is the latest successful nonremoved transaction for that ID.
    for item in history.getCompsEnvironmentItemsByPattern('"'"'%'"'"'):
        if item.getReason() != user:
            continue
        environment = item.getCompsEnvironmentItem()
        for group in environment.getGroups():
            if group.getInstalled():
                selected.setdefault(group.getGroupId(), []).append(
                    '"'"'environment:'"'"' + environment.getEnvironmentId())
    for item in history.getCompsGroupItemsByPattern('"'"'%'"'"'):
        group = item.getCompsGroupItem()
        provenance = selected.get(group.getGroupId(), [])[:]
        if item.getReason() == user:
            provenance.append('"'"'group:'"'"' + group.getGroupId())
        if not provenance:
            continue
        for package in group.getPackages():
            if package.getInstalled():
                print(json.dumps({'"'"'package'"'"': package.getName(),
                                  '"'"'group'"'"': group.getGroupId(),
                                  '"'"'selection'"'"': provenance}, sort_keys=True))
'
