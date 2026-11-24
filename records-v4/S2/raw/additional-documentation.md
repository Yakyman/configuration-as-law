# Additional documented operations

Checked 2026-11-23 UTC. These are documented interfaces and source behavior, not newly performed operations.

## firefox-removal

Source: https://firefox-source-docs.mozilla.org/python/marionette_driver.html

> Uninstall a Firefox addon.

The `Addons` API accepts an extension archive for `install(path, temp=False)` and an add-on ID for
`uninstall(addon_id)`. The installed add-on ID is returned by installation. Removal may require a browser restart
for an add-on that is not restartless. The original action used permanent installation; removal was not performed.

## gem-removal

Source: https://raw.githubusercontent.com/rubygems/rubygems/v4.0.24/lib/rubygems/uninstaller.rb

> This removes the spec, the Gem
> directory, and the cached .gem file.

The upstream 4.0.24 `Gem::Uninstaller#remove` method obtains `spec.cache_file` and deletes that selected archive
as part of removing the selected gem version. The installed native unit reports RubyGems 4.0.24; this source
establishes the upstream operation for that version. No cache-removal command was executed in this task, and no
claim is made that the guest's complete downstream source bytes were recovered.

## runit-service-rights

Retrieved 2026-11-23 UTC. Source comparisons are saved in `S2/raw/runit-source-check.json`.

The complete retained digests (each file is shorter than 4096 bytes) match these authoritative sources:

- `/etc/sv/acpid/run`, 70 bytes: https://raw.githubusercontent.com/void-linux/void-packages/master/srcpkgs/acpid/files/acpid/run . Quote: `exec acpid -f ${OPTS:=-l}`.
- `/etc/runit/2`, 887 bytes: https://raw.githubusercontent.com/void-linux/void-runit/20250212/2 . Quote: `runsvdir -P /run/runit/runsvdir/current`.
- `/etc/sv/agetty-generic/run`, 281 bytes: https://raw.githubusercontent.com/void-linux/void-runit/20250212/services/agetty-generic/run . Quote: `exec chpst -P ${GETTY} ${GETTY_ARGS}`.
- `/etc/sv/agetty-tty1/conf`, 176 bytes: https://raw.githubusercontent.com/void-linux/void-runit/20250212/services/agetty-tty1/conf . Quote: `GETTY_ARGS="--noclear"`.

The filesystem traversal reports `complete: true` and `errors: 0`; it contains the acpid service directory but no
`/etc/sv/acpid/conf`. The retained agetty run symlink targets (not published: record outside this collection).
The package table records the acpid run script, agetty generic run script and agetty configuration unchanged.

https://smarden.org/runit/runit.8 — Quote: "runit runs /etc/runit/2".

https://smarden.org/runit/runsv.8 — Quote: "runsv switches to the directory service and starts ./run."

https://smarden.org/runit/chpst.8 — Quote: "Run prog in a new process group."
This describes `-P`; changing UID/GID is a separate `-u` option, absent from the recovered command.

Inference from the recovered scripts and the documented system-init chain: these two system services inherit
initial root credentials through PID 1, stage 2, runsvdir and runsv. The recovered launch scripts/configuration do
not request a user switch. This establishes the configured launch context, not a sampled process credential set
or a claim that a daemon/login descendant never changes identity later.
