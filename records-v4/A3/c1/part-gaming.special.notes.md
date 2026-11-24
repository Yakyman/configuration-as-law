# Special rows: independent classification c1

Scope: 590 rows other than stored-ownership-unresolved and code-ownership-unresolved. Only the fixed text, sentence index, FACTS, gaming inventory and relevant gaming action logs were consulted. No previous classifications were consulted.

The executable rule implementation is `part-gaming.special.py`. It appends and flushes rows, preserving completed IDs on rerun. The package/file integrity join uses original collector IDs and exact paths. No prefix digest was treated as full-file integrity. These rows are packages or runtime observations, except two unit files, a connection profile and an unexpanded persistent directory.

## Literal rules

S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”

S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

Rule P: installed dpkg packages with explicit reason get INSTALLED-OWN; packages with dependency reason get INSTALLED-DERIVED. The package itself answers question one, so no claim about the contents' executable status is needed. Native manual/automatic reason records were used. Three Python distributions have unknown reason; metadata ownership does not transfer native installation reason, as FACTS explicitly states.

The six Flatpak rows were considered individually. Chess is the installed application marked explicit. The other five rows are runtime/extensions marked dependency solely by application/runtime distinction; the inventory explicitly disclaims historical user intent. The official documentation permits manual runtime installation, so UNKNOWN identifies the missing installation reason. The action log shows a series of installations and Chess's runtime identity but does not record the initiating command or distinguish which runtimes were explicitly requested.

S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”

Rule R: observed processes and sockets are RUNTIME. Known executable paths are joined to package-files.tsv; every matched executable here is unchanged, giving creator INSTALLED-PACKAGE. Missing executable/owner identity leaves creator decision UNKNOWN, but every possible identity still gives the row RUNTIME. The collector probe is executing code, but its acquisition/derivation provenance is not established by the allowed inventory.

Rule T: list-units and list-timers observations describe current in-memory state, not an independent persistent declaration of enablement. These are RUNTIME; unchanged packaged unit files give creator INSTALLED-PACKAGE. Each unit filename was extracted from the actual record, not the inventory name (which is a weekday for timers). All 18 service/timer observations join unchanged packaged unit files.

Two unit-file rows were considered separately. FluidSynth names an unchanged packaged user unit file: INSTALLED-PACKAGE by the first question. The generated Lutris service unit is runtime output of the XDG generator; the persistent autostart entry is an individual launch choice, SETTING-OWN. The filesystem lists the autostart entry as persistent, outside package manifests.

The loopback connection row is UNKNOWN: nmcli connection show does not establish that a profile is persistent or chosen, and NetworkManager can generate an in-memory profile for an existing interface. The unexpanded Flatpak directory is UNKNOWN: its persistence is established, but a directory observation does not supply complete members or their provenance. No executable classification is inferred from a directory's executable permission bit.

## Documentation and factual checks

- https://docs.flatpak.org/en/latest/dependencies.html — “manually install your chosen runtime”; runtimes can be explicitly installed, so runtime type alone does not prove historical dependency acquisition.
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html — “List units that systemd currently has in memory.” The list-timers description likewise specifies current memory and next/last firing times.
- https://www.freedesktop.org/software/systemd/man/254/systemd-xdg-autostart-generator.html — the documented generator creates service units for XDG autostart files.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.generator.html — “By default, those paths are runtime directories”; user generator output belongs under the runtime directory.
- https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/NetworkManager.conf.html — “generating a in-memory connection based on the interface current configuration.”
- Raw basis: (not published: over 20 MB); raw/0079-package-reasons-apt-manual.out; raw/0080-package-reasons-apt-auto.out; raw/0433-process-executables.out; raw/0417-service.out; raw/0418-timer.out; raw/0442-user-user-service.out; raw/0443-user-user-timer.out; raw/0444-user-user-unit-file.out; raw/0427-saved-network.sh; raw/0004-filesystem.out.
- Action evidence: A3/in/operator/gaming/actions-logs/actions-logs/gaming_flatpak_game.log, gaming_autostart.log, gaming_user_settings.log. The autostart log is empty; no command was invented from it.

## Manual rule checks

The following rows were individually inspected in input and the cited raw records before applying the corresponding rule. For package checks, each reason was confirmed in apt manual/auto output. For process checks, each executable was inspected against its unchanged manifest row. For timers, each complete record and unchanged unit-file join was checked. Smaller classes were checked in full.

P explicit (first ten native rows): gaming-c7f293bcc7bcf4817808578f, gaming-930e136beb07b315522fcf91, gaming-3cf14c7ed1354d58ec624b62, gaming-420feed371f78300f90fc7e4, gaming-68a8510ef612ec646111c30c, gaming-5fd7a551afe2bf1d7f0c0727, gaming-208a407e9b8ad788f9ed65e5, gaming-5b8937a1441f3afbb07fde65, gaming-6ff4bb862fc7c9a79185e240, gaming-92756e5c1784395c54d48044.

P dependency (first ten native rows): gaming-7406448a9fd1148b0b19ef51, gaming-f1783669f0787c3564a8ecfe, gaming-9142e5339fc6ea84e461b278, gaming-42b7e42a0a1a999533c97971, gaming-22a8e0654be5e800ef2f6bc7, gaming-e1799827c801c18831d4bcb8, gaming-2f1d6d4ca9d1b8351b2d4a03, gaming-a473e408dbb41d6075eafd82, gaming-70a4b47581b29d4eb275deb2, gaming-afd13d1696a86c8581a52644.

R packaged processes (ten): gaming-a6b6b058fce1692666587ec9, gaming-77f39ce29145b21233ae617e, gaming-f331c20b851fe6575db44a02, gaming-e5663600fbffa42ed23c8cbe, gaming-c10c8b660c72066cb7f3c962, gaming-e4d4ebec90d074553f5725c5, gaming-d9efe4b8abfb75ea3f9c020c, gaming-0cb7818fab83e10338da62ab, gaming-642b769dc51f531677cacf2a, gaming-664654ffa9e3f71c098eec17.

R unknown executable identity (ten): gaming-ad80cfa51beac9c25cd7440b, gaming-e9179fe81245ffd3992a4cb1, gaming-fd41e05178017214ddd69c2a, gaming-01d40bf1231fb8db16256a7e, gaming-42390cbbf0b651683170de80, gaming-2a2e7c46defeb7dd95c48a5f, gaming-84634229f7f9364537f20bd6, gaming-0fc0effde8d7359f4fb826cc, gaming-354ea917032345dc2ba7493f, gaming-329a0e29c581ef1941c6d87d.

R ports (all three): gaming-73547c53129fe57e55cbd39c, gaming-334d7e6ea2c8abcbbfae69e0, gaming-3d48195e703e3661e833221e.

T timers (ten): gaming-800b4718bbcdaef798050f69, gaming-ac06b4cde0da2f84829fcade, gaming-99ae628343ffb742cd897b01, gaming-e8dc6daa0166d2d315182b22, gaming-d00aa23e09d01e6b65045db5, gaming-181d0ead3d9b9aa3b67c987f, gaming-30db09b3b7343da38e3873dc, gaming-3c04817973c2c4ff96599d25, gaming-05fa1da6777a4976051c47cd, gaming-eb7b5e337ea143949bd9a31a.

T services (all five): gaming-e4d6e5e83a4ace5785f13e26, gaming-d0fea8ad2579a8323d482fd9, gaming-cd58d8cd105823bb7f4d80e7, gaming-4ab7eabe1911a3b0d19ba92c, gaming-b2da6817c8af70e071138781.

Python packages (all three): gaming-15a5df1726b5e762eb665dc0, gaming-9fcda2e5da0da17c5c7b04bc, gaming-81623cd696d6fa4dcfb9b26e.

Flatpak packages (all six): gaming-0bf2c7ef261b932eddadd387, gaming-94af2c167b7a79b710953f0f, gaming-3744c51d50c0773cd9a880a4, gaming-a079c47a274e46f0230f0608, gaming-7f6321f4b0c51538073f240a, gaming-a77288b7225b9c0ae94074a4.

Validation: exact 590 input IDs, each once; all decisions allowed; all descriptions within 15 words and reasons within 30 words. Counts: {'INSTALLED-OWN': 424, 'INSTALLED-DERIVED': 58, 'UNKNOWN': 10, 'RUNTIME': 97, 'INSTALLED-PACKAGE': 1}.
