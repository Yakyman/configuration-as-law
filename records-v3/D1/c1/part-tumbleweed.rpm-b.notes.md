# RPM second-half classification notes

Scope: last 2390 RPM rows, original input order. No other classification was consulted.

The ownership dump `../in/raw/tumbleweed/raw/113-ownership-rpm.out` is empty. Package names and versions are established by input evidence. Public repository descriptions establish the package roles. The public repository is a rolling source: it establishes purpose, not identity of every historical byte. No claim of exact installed file identity is made.

Source: https://download.opensuse.org/tumbleweed/repo/oss/repodata/27d143aba154b3643c2f0190d4849cfbe4f4e9da1d112131a8aa743f4b8e8e4c298349e2fe066d304f50c27cab559110b91228bd7ae9d8f5976fb08bccd3d06b-primary.xml.zst

Metadata summaries/descriptions and selected primary file paths are preserved in (not published: downloaded distribution package metadata). The scripts contain the explicit role selection and corrections. Every output is one package object, not a group of its files.

## Rule code

S2.2-9,S2.2-10: Executable programs and native/interpreter library code must be recorded. Descriptions or documented binary paths establish code; package names alone do not. Translation, content, config and metapackage exceptions are reviewed first.

Ten hand-checked examples (description checked against role):

- tumbleweed-60c4817b88fb7bd852b85007 — `gxditview`: Ditroff Output Displayer for Groff. Check: MUST; Ditroff Output Displayer for Groff.
- tumbleweed-197b296a65b71dde96352fc5 — `python313-pycairo`: Python Bindings for Cairo. Check: MUST; Python Bindings for Cairo.
- tumbleweed-431845990e7a6c4e40daa124 — `python313-puremagic`: Pure python implementation of magic file detection. Check: MUST; Pure python implementation of magic file detection.
- tumbleweed-9d78f81908b4597563af8e98 — `python313-nftables`: Python bindings for nftables. Check: MUST; Python bindings for nftables.
- tumbleweed-694c4e45b94cb4ea75d264d0 — `python313-hyperframe`: HTTP/2 framing layer for Python. Check: MUST; HTTP/2 framing layer for Python.
- tumbleweed-57b744fba8565804434dea06 — `Mesa-libva`: Mesa VA-API implementation. Check: MUST; Mesa VA-API implementation.
- tumbleweed-ad71216d622d1dca6742e261 — `akonadi-calendar`: Akonadi calendar integration. Check: MUST; Akonadi calendar integration.
- tumbleweed-effe590234671115bf028903 — `akonadi-contacts`: KDE PIM Libraries for Akonadi Contacts. Check: MUST; KDE PIM Libraries for Akonadi Contacts.
- tumbleweed-dcb819e6db4b67a32f27764f — `akonadi-mime`: MIME email parser for KDE PIM. Check: MUST; MIME email parser for KDE PIM.
- tumbleweed-6b071013d72da654f2636b71 — `busybox-static`: Static linked version of Busybox, a compact UNIX utility collection. Check: MUST; Static linked version of Busybox, a compact UNIX utility collection.

## Rule data

S2.2-2,S2.2-4: Operational text, icons, fonts and reference datasets lose their particular content when removed, but also stop corresponding rendering/language/recognition results. The text supplies no boundary between these two readings: HOLE.

Ten hand-checked examples (description checked against role):

- tumbleweed-d4ff03222fe3efc98f95872f — `desktop-translations`: Desktop Files Translations. Check: HOLE; Desktop Files Translations.
- tumbleweed-88c6d153fb922b34384bb62c — `distribution-logos-openSUSE-Tumbleweed`: Logos for openSUSE Tumbleweed. Check: HOLE; Logos for openSUSE Tumbleweed.
- tumbleweed-3b3aed8cb0eceacdbdbe6dec — `file-magic`: Database for libmagic to help identify files. Check: HOLE; Database for libmagic to help identify files.
- tumbleweed-c3769a3b91a480a1eb8680b6 — `gnome-tour-data`: GNOME Tour data. Check: HOLE; GNOME Tour data.
- tumbleweed-753ec04c3399c7c24f6764f9 — `gtk3-data`: Data files for the GTK+ toolkit library v3. Check: HOLE; Data files for the GTK+ toolkit library v3.
- tumbleweed-628aba51170df68037b752da — `hicolor-icon-theme`: Fallback Icon Theme. Check: HOLE; Fallback Icon Theme.
- tumbleweed-fb37a4a8d9cbdde019568fee — `iso-codes`: ISO Code Lists and Translations. Check: HOLE; ISO Code Lists and Translations.
- tumbleweed-803cd9885d5ac3af08d2e0a6 — `kImageAnnotator-lang`: Translations for package kImageAnnotator. Check: HOLE; Translations for package kImageAnnotator.
- tumbleweed-10a7e6c22aeeee7b7f43e322 — `kdegames-carddecks-default`: Default Card Decks for KDE Games. Check: HOLE; Default Card Decks for KDE Games.
- tumbleweed-9b979d05f7cbf004bcb901d2 — `kf6-breeze-icons`: Breeze icon theme. Check: HOLE; Breeze icon theme.

## Rule metadata

S2.2-1,S2.2-2,S2.2-4,S2.2-13: Structural/package/introspection metadata has downstream operational uses without itself being the program. The text does not distinguish that behavior dependence from descriptive data or settings: HOLE.

Ten hand-checked examples (description checked against role):

- tumbleweed-afd24c8aacb62bb4d83a4713 — `branding-openSUSE`: openSUSE Tumbleweed Brand File. Check: HOLE; openSUSE Tumbleweed Brand File.
- tumbleweed-7a02732097fb92ad188d98e9 — `javapackages-filesystem`: Java packages filesystem layout. Check: HOLE; Java packages filesystem layout.
- tumbleweed-2f4b0dcaee7ccc4ae3445c43 — `patterns-games-games`: Games. Check: HOLE; Games.
- tumbleweed-cae0778ca79df14155e00d1c — `filesystem`: Basic Directory Layout. Check: HOLE; Basic Directory Layout.
- tumbleweed-46d7dfbc72a2231daf3f2e00 — `patterns-glibc-hwcaps-x86_64_v3`: Install x86-64-v3 optimized libraries. Check: HOLE; Install x86-64-v3 optimized libraries.
- tumbleweed-b6506c20dbd511bc9d1cea43 — `typelib-1_0-GLib-2_0`: Object-Oriented Framework for C. Check: HOLE; Supplies binary invocation metadata allowing language bindings to call native library functions.
- tumbleweed-54f349aab25a45dcdffb851f — `typelib-1_0-GObject-2_0`: Object-Oriented Framework for C. Check: HOLE; Supplies binary invocation metadata allowing language bindings to call native library functions.
- tumbleweed-6f6fb0bebafbad99f7e14193 — `typelib-1_0-GModule-2_0`: Object-Oriented Framework for C. Check: HOLE; Supplies binary invocation metadata allowing language bindings to call native library functions.
- tumbleweed-1071b28ebfc759ac33f9c4d0 — `typelib-1_0-GLibUnix-2_0`: Object-Oriented Framework for C. Check: HOLE; Supplies binary invocation metadata allowing language bindings to call native library functions.
- tumbleweed-4427d7290d8883e9a3b55338 — `typelib-1_0-Atk-1_0`: Introspection bindings for the ATK accessibility toolkit. Check: HOLE; Supplies binary invocation metadata allowing language bindings to call native library functions.

## Rule settings

S2.2-7,S2.2-13: passive settings or visual resources whose documented effects remain in the named application are NOT. Passive values alone are insufficient: shared/system effects are individually reviewed.

Ten final hand-checked IDs:

- tumbleweed-a8553410b9fddc2ff2491faa — MozillaFirefox-branding-openSUSE: openSUSE branding of MozillaFirefox; NOT.
- tumbleweed-d86c1763518f3862d3fda0c3 — libreoffice-branding-openSUSE: openSUSE Tumbleweed branding for LibreOffice; NOT.
- tumbleweed-c7b91f63ad8ffcdf6acafdc6 — ImageMagick-config-7-SUSE: SUSE Provided Configuration; NOT.
- tumbleweed-0159ede568ef0c869d94d259 — yast2-trans-stats: YaST2 - Translation Statistics; NOT.
- tumbleweed-c8f4c2c6d01069dd3d2fc4b0 — breeze6-wallpapers: Plasma Desktop artwork, styles and assets; NOT.
- tumbleweed-f510b3dff6fb9aea54ecde4b — yast2-qt-branding-openSUSE: openSUSE Tumbleweed branding for YaST2 Qt; NOT.
- tumbleweed-1aab5a897328c80e9013865f — plymouth-theme-spinner: Plymouth "Spinner" theme; NOT.
- tumbleweed-6d886abe9a6cda2c58a8257c — yast2-theme: YaST2 - Theme; NOT.
- tumbleweed-9204233e0aa0cf9aab69c1ef — plymouth-theme-bgrt: Plymouth "bgrt" theme; NOT.
- tumbleweed-9fc24fec2b1fcf347973ce46 — plymouth-branding-openSUSE: openSUSE Tumbleweed branding for Plymouth bootsplash; NOT.

## Rule firmware

S2.2-2,S2.2-16: Firmware files supplied to drivers implement device capabilities and are system-changeable; MUST. The firmware metapackage is reviewed separately.

Ten hand-checked examples (description checked against role):

- tumbleweed-724711caee15a8fa7ea2080c — `kernel-firmware-usb-network`: Kernel firmware files for various USB WiFi / Ethernet drivers. Check: MUST; Kernel firmware files for various USB WiFi / Ethernet drivers.
- tumbleweed-dd8ee3785f6f285fb48e576f — `kernel-firmware-ueagle`: Kernel firmware files for Eagle IV USB ADSL modem driver. Check: MUST; Kernel firmware files for Eagle IV USB ADSL modem driver.
- tumbleweed-bd29f6f54c4489b6a855d409 — `kernel-firmware-ti`: Kernel firmware files for Texas Instruments wireless drivers. Check: MUST; Kernel firmware files for Texas Instruments wireless drivers.
- tumbleweed-e03a008188b0349326fcc821 — `kernel-firmware-sound`: Kernel firmware files for various sound drivers. Check: MUST; Kernel firmware files for various sound drivers.
- tumbleweed-cdc3b0868985c57eb8fec9e2 — `kernel-firmware-serial`: Kernel firmware files for various serial drivers. Check: MUST; Kernel firmware files for various serial drivers.
- tumbleweed-c7befae8bed637e53273cfea — `kernel-firmware-realtek`: Kernel firmware files for Realtek wireless drivers. Check: MUST; Kernel firmware files for Realtek wireless drivers.
- tumbleweed-425c386939a5e074eab65e53 — `kernel-firmware-radeon`: Kernel firmware files for Radeon graphics driver. Check: MUST; Kernel firmware files for Radeon graphics driver.
- tumbleweed-70d07efd9d1f5cffc3cb0921 — `kernel-firmware-qlogic`: Kernel firmware files for QLogic network drivers. Check: MUST; Kernel firmware files for QLogic network drivers.
- tumbleweed-37e13f1077d9f71f79cb9837 — `kernel-firmware-qcom`: Kernel firmware files for Qualcomm device drivers. Check: MUST; Kernel firmware files for Qualcomm device drivers.
- tumbleweed-2c5c2e67d511379fe0eedc3f — `kernel-firmware-platform`: Kernel firmware files for various platform drivers. Check: MUST; Kernel firmware files for various platform drivers.

## Rule systemrules

S2.2-1,S2.2-2,S2.2-15: Documented rules affecting system-wide accounts, access, multiple programs, hardware handling or service activation change system behavior; MUST.

Ten hand-checked examples (description checked against role):

- tumbleweed-9c9a31c174eb5087255797d8 — `btrfsprogs-udev-rules`: Udev rules for configuring btrfs file systems. Check: MUST; Udev rules for configuring btrfs file systems.
- tumbleweed-81ef65c1ae2937fc90855b48 — `systemd-presets-common-SUSE`: Systemd default presets for SUSE distributions. Check: MUST; Systemd default presets for SUSE distributions.
- tumbleweed-5b055dad34fdb2510e5fbec4 — `permissions-config`: SUSE Linux Default Permissions config files. Check: MUST; SUSE Linux Default Permissions config files.
- tumbleweed-d662b0ca91e5066d46c114e5 — `login_defs`: The login.defs configuration file. Check: MUST; The login.defs configuration file.
- tumbleweed-7d45a3b81903e644cb0a1a7b — `systemd-presets-branding-openSUSE`: Systemd default presets for openSUSE. Check: MUST; Systemd default presets for openSUSE.
- tumbleweed-255999ada4afb173b049b428 — `permissions`: SUSE Linux Default Permissions. Check: MUST; SUSE Linux Default Permissions.
- tumbleweed-bda85357fedd335a5cb58962 — `crypto-policies`: System-wide crypto policies. Check: MUST; System-wide crypto policies.
- tumbleweed-56798c3832841b5fa72f428c — `polkit-default-privs`: SUSE PolicyKit default permissions. Check: MUST; SUSE PolicyKit default permissions.
- tumbleweed-1a1a7279a135dfcb57862153 — `selinux-policy`: SELinux policy configuration. Check: MUST; SELinux policy configuration.
- tumbleweed-af1e8e3ac0ae67a3d1085d6b — `selinux-policy-targeted`: SELinux targeted base policy. Check: MUST; SELinux targeted base policy.

## Rule docs

S2.2-4: Documentation, man pages and license texts are content. Removing them removes only the supplied documents: NOT.

Ten hand-checked examples (description checked against role):

- tumbleweed-0f41df0655e967611e3bf2d4 — `boost-license1_92_0`: Boost License. Check: NOT; Boost License.
- tumbleweed-82f198b84f0a837b3d019a68 — `cryptsetup-doc`: Cryptsetup Documentation. Check: NOT; Cryptsetup Documentation.
- tumbleweed-3fe4a22b49973ebea268d0e2 — `kaddressbook-doc`: Documentation for kaddressbook. Check: NOT; Documentation for kaddressbook.
- tumbleweed-c028a41281b0380c204f3025 — `pam-manpages`: Manualpages for Pluggable Authentication Modules. Check: NOT; Manualpages for Pluggable Authentication Modules.
- tumbleweed-64435b11463ed9cdda92a153 — `unzip-doc`: Documentation files for unzip. Check: NOT; Documentation files for unzip.
- tumbleweed-17fdad9c009ebecc797d552f — `bash-doc`: Documentation on how to use the GNU Bourne-Again Shell. Check: NOT; Documentation on how to use the GNU Bourne-Again Shell.
- tumbleweed-503a2a8840f0eee326685f81 — `coreutils-doc`: Documentation for the GNU Core Utilities. Check: NOT; Documentation for the GNU Core Utilities.
- tumbleweed-1262fb67b31e2d0ce2899fd8 — `coreutils-systemd-doc`: Documentation for the GNU Core Utilities. Check: NOT; Documentation for the GNU Core Utilities.
- tumbleweed-584ac100b9634a333ea60306 — `info-std`: The info pages of the Info Browser. Check: NOT; The info pages of the Info Browser.
- tumbleweed-932ec7bb00e03939ae99dec9 — `man-pages`: Linux Manual Pages. Check: NOT; Linux Manual Pages.

## Rule accounts

S2.2-1,S2.2-15: Packages expressly providing system accounts or groups establish accounts/access rights: MUST.

Ten hand-checked examples (description checked against role):

- tumbleweed-581dc7f25f20a1e28db1ed8a — `system-user-root`: System user and group root. Check: MUST; System user and group root.
- tumbleweed-21147f7a49a36d49f7e90a1b — `system-user-tftp`: System user and group tftp. Check: MUST; System user and group tftp.
- tumbleweed-199aefaf0b2e48faf3b4ecbf — `system-user-nobody`: System user and group nobody. Check: MUST; System user and group nobody.
- tumbleweed-c1b44d232b18646f973866a6 — `system-user-man`: System user and group 'man'. Check: MUST; System user and group 'man'.
- tumbleweed-7a50559cd5b0631eef1c29a5 — `system-user-lp`: System user lp. Check: MUST; System user lp.
- tumbleweed-aadadfa0b4d6b609a064b9a4 — `system-user-flatpak`: System user for the flatpak system helper. Check: MUST; System user for the flatpak system helper.
- tumbleweed-3007827ae54d64f608b15663 — `system-user-daemon`: System user and group 'daemon'. Check: MUST; System user and group 'daemon'.
- tumbleweed-c05e5872551d2cca1bb3ac4c — `system-user-bin`: System user and group 'bin'. Check: MUST; System user and group 'bin'.
- tumbleweed-d0d7287450da9982552a7ec9 — `system-group-wheel`: System group 'wheel'. Check: MUST; System group 'wheel'.
- tumbleweed-5e72b8b86230d393ccaa6a34 — `system-group-kvm`: System group kvm. Check: MUST; System group kvm.

## Individual exceptions

- tumbleweed-c7ac4a140066a37feed0450b — `dbus-broker-block-restart`: HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- tumbleweed-57e50cddde9ed86fbce3d1d5 — `libnl-config`: HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- tumbleweed-ad652a1173c64b17a408185a — `libsemanage-conf`: HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- tumbleweed-ef50d89379c7e871dae8bd93 — `libtirpc-netconfig`: HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- tumbleweed-d498682ee466c92a9bda41af — `openal-soft-data`: HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- tumbleweed-0e525d3910526d6eee658d42 — `xorg-x11-libX11-ccache`: NOT. Precomputed compose-file cache accelerates processing; removing it leaves the underlying functionality available.
- tumbleweed-d8740b0efbb387551a5f8266 — `gpg-pubkey`: HOLE. Without the key signatures cannot be verified; keys can be read as single-program settings or capability-enabling data, and the text does not distinguish these.
- tumbleweed-555aaab3c0b41a2d668cec0d — `gpg-pubkey`: HOLE. Without the key signatures cannot be verified; keys can be read as single-program settings or capability-enabling data, and the text does not distinguish these.
- tumbleweed-f0da0e6ac4776e60abf294fc — `alsa-ucm-conf`: HOLE. These values configure a library or service used by other programs; the text does not define whether their effects remain inside one program.
- tumbleweed-e3d3873501cf7db4507694a3 — `gpg-pubkey`: HOLE. Without the key signatures cannot be verified; keys can be read as single-program settings or capability-enabling data, and the text does not distinguish these.
- tumbleweed-a6fae8b63e5f860e9a3120a9 — `gpg-pubkey`: HOLE. Without the key signatures cannot be verified; keys can be read as single-program settings or capability-enabling data, and the text does not distinguish these.
- tumbleweed-e6a0cad2e99c05eaa9b60f3d — `gpg-pubkey`: HOLE. Without the key signatures cannot be verified; keys can be read as single-program settings or capability-enabling data, and the text does not distinguish these.
- tumbleweed-27de7a07eb2d915e8d077283 — `libplasma6-desktoptheme`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-dc765c68f43062a7012cce85 — `mozilla-nss-certs`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-58bfaed75b767465bff8e84a — `augeas-lenses`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-76b744f6e5224226b42c953c — `ca-certificates-mozilla`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-56e10a9583dfdf4bb1f034fc — `docbook-xsl-stylesheets`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-f1666f13a7a062c4114b60de — `breeze6-decoration`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-2a26e0ab4eebc2800ede336b — `breeze6-style-qt5`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-8d42513019a08c5e53a35728 — `breeze6`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.
- tumbleweed-13ac61f8cda40017b6ecc6dc — `pam_kwallet6-common`: UNKNOWN. Documentation names support files or providers without establishing whether they are executable code or passive values; ownership inventory is empty.
- tumbleweed-88ccab0957f9ba5efef032af — `kaccounts-providers`: UNKNOWN. Documentation names support files or providers without establishing whether they are executable code or passive values; ownership inventory is empty.
- tumbleweed-b8d3bce61d0c4d8c4fd618cc — `plasma6-theme-openSUSE`: HOLE. Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.

Introspection source: https://gi.readthedocs.io/en/latest/architecture.html describes typelibs as “Binary version of the invocation info” and shows libgirepository presenting them to language bindings.

RPM key source: https://rpm.org/docs/6.0.x/man/rpmkeys.8 states: “Digital signatures cannot be verified without the corresponding public key (aka certificate).”

No removal experiment was performed. UNKNOWN support/provider packages have descriptions insufficient to establish executable versus passive payload, and their ownership dump is empty.

## Payload verification and superseding corrections

Public filelists were checked because source-level summaries can describe code held in a separate library package. Source: https://download.opensuse.org/tumbleweed/repo/oss/repodata/7b1bc6a47608886f73287d87e0d5118aa88c8359e40cf145e5da198474c57a078c8a4ed47018525d2378f13081428c790d370005a0ab7e1de42563d55275c9a1-filelists.xml.zst. This verification supersedes any earlier example wording based solely on source summaries.

Rule logginglabels: S2.2-4,S2.2-7,S2.2-13. Packages containing only category labels/aliases plus documentation supply descriptive labels, not code; NOT. Ten manually checked examples:

- tumbleweed-ad71216d622d1dca6742e261 — akonadi-calendar: /usr/share/qlogging-categories6/akonadi-calendar.categories, /usr/share/qlogging-categories6/akonadi-calendar.renamecategories.
- tumbleweed-dcb819e6db4b67a32f27764f — akonadi-mime: /usr/share/qlogging-categories6/akonadi-mime.categories.
- tumbleweed-4177d74ef2db56b8164d8bd8 — calendarsupport: /usr/share/qlogging-categories6/calendarsupport.categories, /usr/share/qlogging-categories6/calendarsupport.renamecategories.
- tumbleweed-b92dc84facf07c5fdd78716c — eventviews: /usr/share/qlogging-categories6/eventviews.categories, /usr/share/qlogging-categories6/eventviews.renamecategories.
- tumbleweed-a4301a99f972fd14517f3acd — incidenceeditor: /usr/share/qlogging-categories6/incidenceeditor.categories, /usr/share/qlogging-categories6/incidenceeditor.renamecategories.
- tumbleweed-4932a4e38ea53c0c0477596b — kf6-attica: /usr/share/qlogging-categories6/attica.categories, /usr/share/qlogging-categories6/attica.renamecategories.
- tumbleweed-5405e6ac25114b7cd58058dd — kf6-bluez-qt: /usr/share/qlogging-categories6/bluezqt.categories, /usr/share/qlogging-categories6/bluezqt.renamecategories.
- tumbleweed-58983866de0f514269a145cf — kf6-karchive: /usr/share/qlogging-categories6/karchive.categories, /usr/share/qlogging-categories6/karchive.renamecategories.
- tumbleweed-1c63df883d1b5778cf7c76e9 — kf6-kbookmarks: /usr/share/qlogging-categories6/kbookmarks.renamecategories, /usr/share/qlogging-categories6/kbookmarkswidgets.categories.
- tumbleweed-ddfc3f6ce3f0979f9e904359 — kf6-kcodecs: /usr/share/qlogging-categories6/kcodecs.categories, /usr/share/qlogging-categories6/kcodecs.renamecategories.

Individual corrected payload inspections:

- tumbleweed-ad71216d622d1dca6742e261 — akonadi-calendar: NOT. Payload: /usr/share/qlogging-categories6/akonadi-calendar.categories, /usr/share/qlogging-categories6/akonadi-calendar.renamecategories.
- tumbleweed-effe590234671115bf028903 — akonadi-contacts: HOLE. Payload: /usr/share/kf6/akonadi/contact/data/zone.tab, /usr/share/kf6/akonadi/contact/pics/world.jpg, /usr/share/qlogging-categories6/akonadi-contacts.categories.
- tumbleweed-dcb819e6db4b67a32f27764f — akonadi-mime: NOT. Payload: /usr/share/qlogging-categories6/akonadi-mime.categories.
- tumbleweed-4177d74ef2db56b8164d8bd8 — calendarsupport: NOT. Payload: /usr/share/qlogging-categories6/calendarsupport.categories, /usr/share/qlogging-categories6/calendarsupport.renamecategories.
- tumbleweed-238e48ea1ab5728fcde3b110 — cracklib-dict-full: HOLE. Payload: /usr/share/cracklib/pw_dict.hwm, /usr/share/cracklib/pw_dict.pwd, /usr/share/cracklib/pw_dict.pwi.
- tumbleweed-b92dc84facf07c5fdd78716c — eventviews: NOT. Payload: /usr/share/qlogging-categories6/eventviews.categories, /usr/share/qlogging-categories6/eventviews.renamecategories.
- tumbleweed-66ed6c20efbe0f068d1a3273 — freecell-solver-presets: MUST. Payload: /usr/share/freecell-solver/presetrc, /usr/share/freecell-solver/presets/abra-kadabra.sh, /usr/share/freecell-solver/presets/amateur-star.sh.
- tumbleweed-94733f055f9f9e259def1555 — gtk3-schema: HOLE. Payload: /usr/share/glib-2.0/schemas/org.gtk.Demo.gschema.xml, /usr/share/glib-2.0/schemas/org.gtk.Settings.ColorChooser.gschema.xml, /usr/share/glib-2.0/schemas/org.gtk.Settings.Debug.gschema.xml.
- tumbleweed-1c13d4d6011ae45ca83363fb — gtk4-schema: HOLE. Payload: /usr/share/glib-2.0/schemas/org.gtk.gtk4.Inspector.gschema.xml, /usr/share/glib-2.0/schemas/org.gtk.gtk4.Settings.ColorChooser.gschema.xml, /usr/share/glib-2.0/schemas/org.gtk.gtk4.Settings.Debug.gschema.xml.
- tumbleweed-a4301a99f972fd14517f3acd — incidenceeditor: NOT. Payload: /usr/share/qlogging-categories6/incidenceeditor.categories, /usr/share/qlogging-categories6/incidenceeditor.renamecategories.
- tumbleweed-4932a4e38ea53c0c0477596b — kf6-attica: NOT. Payload: /usr/share/qlogging-categories6/attica.categories, /usr/share/qlogging-categories6/attica.renamecategories.
- tumbleweed-5405e6ac25114b7cd58058dd — kf6-bluez-qt: NOT. Payload: /usr/share/qlogging-categories6/bluezqt.categories, /usr/share/qlogging-categories6/bluezqt.renamecategories.
- tumbleweed-58983866de0f514269a145cf — kf6-karchive: NOT. Payload: /usr/share/qlogging-categories6/karchive.categories, /usr/share/qlogging-categories6/karchive.renamecategories.
- tumbleweed-1c63df883d1b5778cf7c76e9 — kf6-kbookmarks: NOT. Payload: /usr/share/qlogging-categories6/kbookmarks.categories, /usr/share/qlogging-categories6/kbookmarks.renamecategories, /usr/share/qlogging-categories6/kbookmarkswidgets.categories.
- tumbleweed-ddfc3f6ce3f0979f9e904359 — kf6-kcodecs: NOT. Payload: /usr/share/qlogging-categories6/kcodecs.categories, /usr/share/qlogging-categories6/kcodecs.renamecategories.
- tumbleweed-3ca96ec2e4dad04e30927bb1 — kf6-kcolorscheme: NOT. Payload: /usr/share/qlogging-categories6/kcolorscheme.categories.
- tumbleweed-9321e330cfc32c06a725a989 — kf6-kcompletion: NOT. Payload: /usr/share/qlogging-categories6/kcompletion.categories.
- tumbleweed-6a50fe2fbf58a513826d1501 — kf6-kconfigwidgets: HOLE. Payload: /usr/share/locale/af/kf6_entry.desktop, /usr/share/locale/ar/kf6_entry.desktop, /usr/share/locale/as/kf6_entry.desktop.
- tumbleweed-3aecb042f881b2a94ac5abce — kf6-kcontacts: NOT. Payload: /usr/share/qlogging-categories6/kcontacts.categories, /usr/share/qlogging-categories6/kcontacts.renamecategories.
- tumbleweed-40dd874ebc42494ff32aef06 — kf6-kcrash: NOT. Payload: /usr/share/qlogging-categories6/kcrash.categories, /usr/share/qlogging-categories6/kcrash.renamecategories.
- tumbleweed-546164c6e23808c3873d5591 — kf6-kdav: NOT. Payload: /usr/share/qlogging-categories6/kdav.categories, /usr/share/qlogging-categories6/kdav.renamecategories.
- tumbleweed-ce2e994a9b7e086f585b0ae7 — kf6-kdbusaddons: NOT. Payload: /usr/share/qlogging-categories6/kdbusaddons.categories, /usr/share/qlogging-categories6/kdbusaddons.renamecategories.
- tumbleweed-a46f3cb29437313807396ce6 — kf6-kglobalaccel: NOT. Payload: /usr/share/qlogging-categories6/kglobalaccel.categories, /usr/share/qlogging-categories6/kglobalaccel.renamecategories.
- tumbleweed-49cf0696219df6d1fef9d0c8 — kf6-kholidays: NOT. Payload: /usr/share/qlogging-categories6/kholidays.categories.
- tumbleweed-4f9b8ac208e593f05af10108 — kf6-kidletime: NOT. Payload: /usr/share/qlogging-categories6/kidletime.categories, /usr/share/qlogging-categories6/kidletime.renamecategories.
- tumbleweed-3dbbb8eeb29fac511481e787 — kf6-kitemviews: NOT. Payload: /usr/share/qlogging-categories6/kitemviews.categories.
- tumbleweed-cf13112a814714d9e4d7c14a — kf6-kjobwidgets: NOT. Payload: /usr/share/qlogging-categories6/kjobwidgets.categories, /usr/share/qlogging-categories6/kjobwidgets.renamecategories.
- tumbleweed-3410446f1ed72703ac24b55d — kf6-kmime: NOT. Payload: /usr/share/qlogging-categories6/kmime.categories, /usr/share/qlogging-categories6/kmime.renamecategories.
- tumbleweed-b2cf17e87aa6993326191dda — kf6-knotifications: NOT. Payload: /usr/share/qlogging-categories6/knotifications.categories, /usr/share/qlogging-categories6/knotifications.renamecategories.
- tumbleweed-cb16344a8ce1ddc867d25f01 — kf6-knotifyconfig: NOT. Payload: /usr/share/qlogging-categories6/knotifyconfig.categories.
- tumbleweed-c265baa129e0a3048ca3783c — kf6-kparts: NOT. Payload: /usr/share/qlogging-categories6/kparts.categories.
- tumbleweed-7b6aa4e6c7766d530389c967 — kf6-kpty: NOT. Payload: /usr/share/qlogging-categories6/kpty.categories.
- tumbleweed-d3ede3314d71b10c5ccf6bc1 — kf6-krunner: NOT. Payload: /usr/share/qlogging-categories6/krunner.categories, /usr/share/qlogging-categories6/krunner.renamecategories.
- tumbleweed-3905173803e5628b56b34e44 — kf6-kstatusnotifieritem: NOT. Payload: /usr/share/qlogging-categories6/kstatusnotifieritem.categories.
- tumbleweed-b662958ef523497c1a6b6f7e — kf6-kunitconversion: NOT. Payload: /usr/share/qlogging-categories6/kunitconversion.categories.
- tumbleweed-a9a509d26eddcee3768333c7 — kf6-kuserfeedback: NOT. Payload: /usr/share/qlogging-categories6/org_kde_UserFeedback.categories.
- tumbleweed-8bb555ff0660f03cd18f62f1 — kf6-kwallet: NOT. Payload: /usr/share/qlogging-categories6/kwallet.categories, /usr/share/qlogging-categories6/kwallet.renamecategories.
- tumbleweed-95730b8532cda7be903ef338 — kf6-kwidgetsaddons: NOT. Payload: /usr/share/qlogging-categories6/kwidgetsaddons.categories.
- tumbleweed-1b0524dd130f0ac4bd3d3a7c — kf6-kxmlgui: NOT. Payload: /usr/share/qlogging-categories6/kxmlgui.categories, /usr/share/qlogging-categories6/kxmlgui.renamecategories.
- tumbleweed-a209572637b5cb0c0001cb10 — kf6-modemmanager-qt: NOT. Payload: /usr/share/qlogging-categories6/modemmanagerqt.categories, /usr/share/qlogging-categories6/modemmanagerqt.renamecategories.
- tumbleweed-811408d0a9f055f84c15e74d — kf6-networkmanager-qt: NOT. Payload: /usr/share/qlogging-categories6/networkmanagerqt.categories, /usr/share/qlogging-categories6/networkmanagerqt.renamecategories.
- tumbleweed-20f37ce3fde24cfe6a9cc3fe — kf6-prison: NOT. Payload: /usr/share/qlogging-categories6/prison.categories, /usr/share/qlogging-categories6/prison.renamecategories.
- tumbleweed-064a19e73856f6118be94f4c — kf6-solid: NOT. Payload: /usr/share/qlogging-categories6/solid.categories, /usr/share/qlogging-categories6/solid.renamecategories.
- tumbleweed-059593370a95934f4cb8f7fd — kf6-syndication: NOT. Payload: /usr/share/qlogging-categories6/syndication.categories, /usr/share/qlogging-categories6/syndication.renamecategories.
- tumbleweed-324e8048b157aca3c0d3e352 — kglobalacceld6: NOT. Payload: /usr/share/qlogging-categories6/kglobalacceld.categories.
- tumbleweed-718448a6a632567a048d5041 — kidentitymanagement: NOT. Payload: /usr/share/qlogging-categories6/kidentitymanagement.categories, /usr/share/qlogging-categories6/kidentitymanagement.renamecategories.
- tumbleweed-1cb70a69bdb75319620778db — kimap: NOT. Payload: /usr/share/qlogging-categories6/kimap.categories, /usr/share/qlogging-categories6/kimap.renamecategories.
- tumbleweed-6c6b04c67e41eebd25d6632a — kmbox: NOT. Payload: /usr/share/qlogging-categories6/kmbox.categories, /usr/share/qlogging-categories6/kmbox.renamecategories.
- tumbleweed-cf356d684d50cb522b4a7456 — kontactinterface: NOT. Payload: /usr/share/qlogging-categories6/kontactinterface.categories, /usr/share/qlogging-categories6/kontactinterface.renamecategories.
- tumbleweed-e3ec7c645d0303a75a81af0c — kpimtextedit: NOT. Payload: /usr/share/qlogging-categories6/kpimtextedit.categories.
- tumbleweed-5e271c939fb929db0c8692be — kpkpass: NOT. Payload: /usr/share/qlogging-categories6/org_kde_kpkpass.categories.
- tumbleweed-142611cc5e946fee6c2cbd1e — kscreenlocker6-imports: HOLE. Payload: /usr/lib64/qt6/qml/org/kde/kscreenlocker/kscreenlocker_greet.qmltypes, /usr/lib64/qt6/qml/org/kde/kscreenlocker/qmldir.
- tumbleweed-30ef83f71326677301415692 — ksmtp: NOT. Payload: /usr/share/qlogging-categories6/ksmtp.categories.
- tumbleweed-54ffce2db8ebee996775a4a3 — kwayland6: NOT. Payload: /usr/share/qlogging-categories6/kwayland.categories, /usr/share/qlogging-categories6/kwayland.renamecategories.
- tumbleweed-ff341235b6a6b85b4a229442 — libX11-data: HOLE. Payload: /usr/share/X11/XErrorDB, /usr/share/X11/Xcms.txt, /usr/share/X11/locale/C/Compose.
- tumbleweed-8da91186d1f050933803f022 — libgravatar: NOT. Payload: /usr/share/qlogging-categories6/libgravatar.categories, /usr/share/qlogging-categories6/libgravatar.renamecategories.
- tumbleweed-ff5a40235b19dda44ab14272 — libkdcraw-qt6: NOT. Payload: /usr/share/qlogging-categories6/libkdcraw.categories.
- tumbleweed-d098194c82a02b391c39a274 — libkexiv2-qt6: NOT. Payload: /usr/share/qlogging-categories6/libkexiv2.categories.
- tumbleweed-f930414351a4a1b2409054de — libksieve: HOLE. Payload: /usr/share/knsrcfiles/ksieve_script.knsrc, /usr/share/qlogging-categories6/libksieve.categories, /usr/share/qlogging-categories6/libksieve.renamecategories.
- tumbleweed-16fb885c3a893800e8e1b4b5 — libqaccessibilityclient-qt6: NOT. Payload: /usr/share/qlogging-categories6/libqaccessibilityclient.categories.
- tumbleweed-389082f789dff57ea9a3006e — mailcommon: NOT. Payload: /usr/share/qlogging-categories6/mailcommon.categories, /usr/share/qlogging-categories6/mailcommon.renamecategories.
- tumbleweed-c95b5e50b33872fb68a16eb6 — mailimporter: NOT. Payload: /usr/share/qlogging-categories6/mailimporter.categories, /usr/share/qlogging-categories6/mailimporter.renamecategories.
- tumbleweed-7227fee0dfbb99b63174d021 — mimetreeparser: NOT. Payload: /usr/share/qlogging-categories6/mimetreeparser.categories.
- tumbleweed-78b05b6d088bac9e598205f7 — pimcommon: NOT. Payload: /usr/share/qlogging-categories6/pimcommon.categories, /usr/share/qlogging-categories6/pimcommon.renamecategories.
- tumbleweed-816d6c5d6a1ef36b976abcfb — plasma6-activities: NOT. Payload: /usr/share/qlogging-categories6/plasma-activities.categories, /usr/share/qlogging-categories6/plasma-activities.renamecategories.
- tumbleweed-4ea8d2ead3a27fdab0050c13 — plasma6-activities-stats: NOT. Payload: /usr/share/qlogging-categories6/plasma-activities-stats.categories, /usr/share/qlogging-categories6/plasma-activities-stats.renamecategories.
- tumbleweed-3d4c57fc4aefee47626583de — rgb: MUST. Payload: /usr/bin/showrgb, /usr/share/X11/rgb.txt.
- tumbleweed-bd1b1ad9cc51890ba30622ec — terminfo-base: MUST. Payload: /etc/termcap, /usr/bin/termerase, /usr/share/misc/termcap.
- tumbleweed-b8844433a232609731e25abb — girepository-1_0: HOLE. Payload: /usr/lib64/girepository-1.0/DBus-1.0.typelib, /usr/lib64/girepository-1.0/DBusGLib-1.0.typelib, /usr/lib64/girepository-1.0/GIRepository-2.0.typelib.
- tumbleweed-67486972373cb0f28ea8c779 — Mesa: HOLE. Payload: .
- tumbleweed-e605cf8492e45b603637b5d5 — rpm-config-SUSE: MUST. Payload: /usr/lib/rpm/brp-suse, /usr/lib/rpm/fileattrs/firmware.attr, /usr/lib/rpm/fileattrs/kernel.attr.
- tumbleweed-4545c25860335fbbb54f7242 — shared-mime-info: MUST. Payload: /usr/bin/update-mime-database, /usr/lib/rpm/macros.d/macros.shared-mime-info, /usr/share/gettext/its/shared-mime-info.its.
- tumbleweed-95709d632bb78c758db4db62 — libssh-config: HOLE. Payload: /usr/etc/libssh/libssh_client.config, /usr/etc/libssh/libssh_server.config.
- tumbleweed-c9074ea775e56a8c729f3272 — kf6-kcoreaddons: HOLE. Payload: /usr/share/mime/packages/kde6.xml, /usr/share/qlogging-categories6/kcoreaddons.categories, /usr/share/qlogging-categories6/kcoreaddons.renamecategories.
- tumbleweed-7781b81cdd531b4c92391295 — kcoreaddons: HOLE. Payload: /usr/share/kf5/licenses/ARTISTIC, /usr/share/kf5/licenses/BSD, /usr/share/kf5/licenses/GPL_V2.
- tumbleweed-a2af4e5d036288899230dad9 — kdoctools: MUST. Payload: /usr/bin/checkXML5, /usr/bin/meinproc5, /usr/share/kf5/kdoctools/customization/README.
- tumbleweed-4b07c4c7f4e07e54f7d27a8e — libKF5DocTools5: MUST. Payload: /usr/lib64/libKF5DocTools.so.5, /usr/lib64/libKF5DocTools.so.5.116.0.
- tumbleweed-5cb38da8ace4818e55967f7b — ruby: HOLE. Payload: .
- tumbleweed-cb7a1b9080ffbdae219abc2c — kf6-kdoctools: MUST. Payload: /usr/bin/checkXML6, /usr/bin/meinproc6, /usr/share/kf6/kdoctools/customization/af/catalog.xml.
- tumbleweed-c77ebc23069bbe8596dff10d — yast2-country-data: MUST. Payload: /usr/share/YaST2/data/languages/language_af_ZA.ycp, /usr/share/YaST2/data/languages/language_ar_EG.ycp, /usr/share/YaST2/data/languages/language_ast_ES.ycp.
- tumbleweed-5fa45966f561960d04de8d01 — openssl: HOLE. Payload: .
- tumbleweed-62806377d9c1aad47a8a1587 — libKF6DocTools6: MUST. Payload: /usr/lib64/libKF6DocTools.so.6, /usr/lib64/libKF6DocTools.so.6.32.0.
- tumbleweed-d5d61f27fcecb455461283e1 — qalculate-data: HOLE. Payload: /usr/share/qalculate/currencies.xml, /usr/share/qalculate/datasets.xml, /usr/share/qalculate/elements.xml.
- tumbleweed-0b930082aeaa5454d0b21f09 — tesseract-ocr-common: HOLE. Payload: /usr/share/tessdata/configs/alto, /usr/share/tessdata/configs/ambigs.train, /usr/share/tessdata/configs/api_config.
- tumbleweed-f0209fbc9694ef2b0a11140d — kf6-ksvg: NOT. Payload: /usr/share/qlogging-categories6/ksvg.categories.
- tumbleweed-1c7bbc9651e3117e1332ebc5 — dbus-1: HOLE. Payload: .
- tumbleweed-2704d243d710bba19ef6616f — openssh: HOLE. Payload: .
- tumbleweed-974c6a6e6058683d4f9f985d — yast2-control-center: HOLE. Payload: /usr/share/applications/org.opensuse.YaST.desktop, /usr/share/icons/hicolor/scalable/apps/yast-control-center.svg, /usr/share/icons/hicolor/symbolic/apps/yast-control-center-symbolic.svg.
- tumbleweed-5917e63796071bd56bc521c5 — xterm: HOLE. Payload: /usr/share/applications/xterm.desktop, /usr/share/pixmaps/filled-xterm_16x16.xpm, /usr/share/pixmaps/filled-xterm_32x32.xpm.
- tumbleweed-49b7e58c9ade1153330e3892 — yast2-theme-breeze: HOLE. Payload: /usr/share/icons/breeze-dark/apps/32/pattern-basis-addon.svg, /usr/share/icons/breeze-dark/apps/32/pattern-basis-devel.svg, /usr/share/icons/breeze-dark/apps/32/pattern-basis.svg.
- tumbleweed-53b281acb9a167690cdee264 — khelpcenter: MUST. Payload: /usr/bin/khelpcenter, /usr/libexec/khc_mansearch.py, /usr/libexec/khc_xapianindexer.
- tumbleweed-a7932bee81af8eff1a35652f — kf6-purpose-services: HOLE. Payload: /usr/share/accounts/services/kde/google-youtube.service, /usr/share/accounts/services/kde/nextcloud-upload.service.
- tumbleweed-ccbf06b5d53eb0e656661f73 — ktnef-debug-categories: NOT. Payload: /usr/share/qlogging-categories6/ktnef.categories, /usr/share/qlogging-categories6/ktnef.renamecategories.
- tumbleweed-98ea5f9f5792a1578edd7016 — libkdegames: NOT. Payload: /usr/share/qlogging-categories6/libkdegames.categories.
- tumbleweed-3b3a80c65b40f0cd6d838b21 — libkdepim: NOT. Payload: /usr/share/qlogging-categories6/libkdepim.categories, /usr/share/qlogging-categories6/libkdepim.renamecategories.
- tumbleweed-0e7d57f7eff2ff2d962b042f — libkgapi6: NOT. Payload: /usr/share/qlogging-categories6/libkgapi.categories.
- tumbleweed-6133fb619cc177cebd450517 — libkleo: HOLE. Payload: /etc/xdg/libkleopatrarc, /usr/share/libkleopatra/pics/smartcard.xpm, /usr/share/qlogging-categories6/libkleo.categories.
- tumbleweed-139df17d42bdf459183ce14d — libkmahjongg: HOLE. Payload: /usr/share/kmahjongglib/backgrounds/chinese_landscape.desktop, /usr/share/kmahjongglib/backgrounds/chinese_landscape.svgz, /usr/share/kmahjongglib/backgrounds/color_plain.desktop.
- tumbleweed-a9f781f6fa923e586a78340a — libpaper: HOLE. Payload: /etc/paperspecs.
- tumbleweed-f3e1feec55bb77366429903b — myspell-lightproof-en: MUST. Payload: /usr/lib64/libreoffice/share/extensions/lightproof-en/Lightproof.components, /usr/lib64/libreoffice/share/extensions/lightproof-en/Lightproof.py, /usr/lib64/libreoffice/share/extensions/lightproof-en/Linguistic.xcu.
- tumbleweed-dc765c68f43062a7012cce85 — mozilla-nss-certs: MUST. Payload: /usr/lib64/libnssckbi.so.
- tumbleweed-1045ff1e7efbe5cb410ee837 — libfido2-udev: MUST. Payload: /usr/lib/udev/rules.d/70-fido2.rules.
- tumbleweed-d04fc937c2b7df2241677eaf — desktop-data-openSUSE: MUST. Payload: /etc/profile.d/desktop-data.csh, /etc/profile.d/desktop-data.sh, /etc/xdg/menus/applications.menu.
- tumbleweed-56e10a9583dfdf4bb1f034fc — docbook-xsl-stylesheets: MUST. Payload: /etc/xml/catalog.d/docbook-xsl-stylesheets.xml, /usr/share/xml/docbook/stylesheet/nwalsh/1.79.2/VERSION, /usr/share/xml/docbook/stylesheet/nwalsh/1.79.2/VERSION.xsl.
- tumbleweed-f1666f13a7a062c4114b60de — breeze6-decoration: MUST. Payload: /usr/lib64/qt6/plugins/org.kde.kdecoration3.kcm/kcm_breezedecoration.so, /usr/lib64/qt6/plugins/org.kde.kdecoration3/org.kde.breeze.so, /usr/share/applications/kcm_breezedecoration6.desktop.
- tumbleweed-2a26e0ab4eebc2800ede336b — breeze6-style-qt5: MUST. Payload: /usr/lib64/qt5/plugins/styles/breeze5.so.
- tumbleweed-39868119fbc3c121f2e07895 — purge-kernels-service: MUST. Payload: /usr/lib/systemd/system/purge-kernels.service.
- tumbleweed-aac6aa8494b1f3e8c0028242 — grub2: HOLE. Payload: .
- tumbleweed-13ac61f8cda40017b6ecc6dc — pam_kwallet6-common: MUST. Payload: /etc/xdg/autostart/pam_kwallet_init.desktop, /usr/lib/systemd/user/plasma-kwallet-pam.service, /usr/libexec/pam_kwallet_init.
- tumbleweed-344dbaf5493cb095a81695b2 — vlc: HOLE. Payload: /usr/share/applications/vlc-openbd.desktop, /usr/share/applications/vlc-opencda.desktop, /usr/share/applications/vlc-opendvd.desktop.
- tumbleweed-88ccab0957f9ba5efef032af — kaccounts-providers: MUST. Payload: /usr/lib64/qt6/plugins/kaccounts/ui/nextcloud_plugin_kaccounts.so, /usr/lib64/qt6/plugins/kaccounts/ui/owncloud_plugin_kaccounts.so, /usr/share/accounts/providers/kde/google.provider.
- tumbleweed-c225ad126cda23f96aa4609e — plasma6-sddm-theme-openSUSE: HOLE. Payload: /usr/lib/sddm/sddm.conf.d/20-breeze-openSUSE.conf, /usr/share/sddm/themes/breeze-openSUSE/Background.qml, /usr/share/sddm/themes/breeze-openSUSE/KeyboardButton.qml.
- tumbleweed-b8d3bce61d0c4d8c4fd618cc — plasma6-theme-openSUSE: MUST. Payload: /usr/share/color-schemes/openSUSE.colors, /usr/share/color-schemes/openSUSEdark.colors, /usr/share/icons/breeze-dark/places/16/start-here-branding.svg.
- tumbleweed-7920eda55c2de20a6c5a0725 — plasma6-session: HOLE. Payload: /usr/share/wayland-sessions/plasmawayland.desktop.

Source summaries were not used to claim shared libraries in packages whose filelists only contain descriptions. Browser help JavaScript is confined to rendering help; its presence does not turn help data into unrestricted code.

## Final rule samples after payload corrections

These final ten-row checks supersede initial samples for code, settings, data and metadata. Each listed payload was inspected; irrelevant documentation paths are excluded from the examples.

### code

- tumbleweed-60c4817b88fb7bd852b85007 — gxditview; MUST; payload example: /usr/bin/gxditview, /usr/share/X11/app-defaults/GXditview.
- tumbleweed-197b296a65b71dde96352fc5 — python313-pycairo; MUST; payload example: /usr/lib64/python3.13/site-packages/cairo/__init__.py, /usr/lib64/python3.13/site-packages/cairo/__init__.pyi.
- tumbleweed-431845990e7a6c4e40daa124 — python313-puremagic; MUST; payload example: /usr/bin/puremagic, /usr/bin/puremagic-3.13.
- tumbleweed-9d78f81908b4597563af8e98 — python313-nftables; MUST; payload example: /usr/lib/python3.13/site-packages/nftables-0.1.dist-info/INSTALLER, /usr/lib/python3.13/site-packages/nftables-0.1.dist-info/METADATA.
- tumbleweed-694c4e45b94cb4ea75d264d0 — python313-hyperframe; MUST; payload example: /usr/lib/python3.13/site-packages/hyperframe-6.1.0.dist-info/INSTALLER, /usr/lib/python3.13/site-packages/hyperframe-6.1.0.dist-info/METADATA.
- tumbleweed-57b744fba8565804434dea06 — Mesa-libva; MUST; payload example: /usr/lib64/dri/nouveau_drv_video.so, /usr/lib64/dri/r600_drv_video.so.
- tumbleweed-6b071013d72da654f2636b71 — busybox-static; MUST; payload example: /usr/bin/busybox-static.
- tumbleweed-f627c6779989d2a4bdc9eb96 — compat-usrmerge-tools; MUST; payload example: /usr/bin/usrmergecheck, /usr/libexec/convertfs.
- tumbleweed-50852ceddd763a29a0118542 — debuginfod-profile; MUST; payload example: /etc/debuginfod/elfutils.urls, /etc/profile.d/debuginfod.csh.
- tumbleweed-66ed6c20efbe0f068d1a3273 — freecell-solver-presets; MUST; payload example: /usr/share/freecell-solver/presetrc, /usr/share/freecell-solver/presets/abra-kadabra.sh.
### settings

- tumbleweed-a8553410b9fddc2ff2491faa — MozillaFirefox-branding-openSUSE; NOT; payload example: /usr/lib64/firefox/browser/defaults/preferences/firefox-openSUSE.js, /usr/lib64/firefox/defaults/pref/all-openSUSE.js.
- tumbleweed-d86c1763518f3862d3fda0c3 — libreoffice-branding-openSUSE; NOT; payload example: /usr/share/libreoffice/program/flat_logo.svg, /usr/share/libreoffice/program/intro.png.
- tumbleweed-c7b91f63ad8ffcdf6acafdc6 — ImageMagick-config-7-SUSE; NOT; payload example: /etc/IM-7/policy.xml.
- tumbleweed-0440ecd1e9571cf8cde1be87 — chrony-pool-openSUSE; NOT; payload example: /usr/etc/chrony.d/pool.conf.
- tumbleweed-e788c0407bc909d3a1ff0c64 — NetworkManager-branding-openSUSE; NOT; payload example: /usr/lib/NetworkManager/conf.d/conncheck-openSUSE.conf.
- tumbleweed-88de43bb31abf3d91ab8c376 — PackageKit-branding-openSUSE; NOT; payload example: /etc/PackageKit/PackageKit.conf, /etc/PackageKit/Vendor.conf.
- tumbleweed-a08bac3bb4eead7e0306e601 — flatpak-remote-flathub; NOT; payload example: /etc/flatpak/remotes.d/flathub.flatpakrepo.
- tumbleweed-8fba25fb55f307fa4b8ffcd0 — gtk4-branding-openSUSE; NOT; payload example: /usr/share/gtk-4.0/settings.ini.
- tumbleweed-7b897cdfd9256cc00b039c05 — gtk3-branding-openSUSE; NOT; payload example: /etc/gtk-3.0/settings.ini.
- tumbleweed-20e31b9f2ffa6df7884e3b3d — registries-conf-default; NOT; payload example: /usr/share/containers/registries.conf.d/00-suse-registries.conf.
### data

- tumbleweed-effe590234671115bf028903 — akonadi-contacts; HOLE; payload example: /usr/share/kf6/akonadi/contact/data/zone.tab, /usr/share/kf6/akonadi/contact/pics/world.jpg.
- tumbleweed-238e48ea1ab5728fcde3b110 — cracklib-dict-full; HOLE; payload example: /usr/share/cracklib/pw_dict.hwm, /usr/share/cracklib/pw_dict.pwd.
- tumbleweed-d4ff03222fe3efc98f95872f — desktop-translations; HOLE; payload example: /usr/share/locale/af/LC_MESSAGES/desktop_translations.mo, /usr/share/locale/af/LC_MESSAGES/polkit-action-distro-translations.mo.
- tumbleweed-88c6d153fb922b34384bb62c — distribution-logos-openSUSE-Tumbleweed; HOLE; payload example: /usr/share/pixmaps/distribution-logos/apple-touch-icon.png, /usr/share/pixmaps/distribution-logos/apple-touch-icon.svg.
- tumbleweed-3b3aed8cb0eceacdbdbe6dec — file-magic; HOLE; payload example: /etc/magic, /usr/share/file/magic.
- tumbleweed-c3769a3b91a480a1eb8680b6 — gnome-tour-data; HOLE; payload example: /usr/share/gnome-tour/resources.gresource, /usr/share/icons/hicolor/scalable/apps/org.gnome.Tour.svg.
- tumbleweed-753ec04c3399c7c24f6764f9 — gtk3-data; HOLE; payload example: /usr/share/locale/en/LC_MESSAGES/gtk30-properties.mo, /usr/share/locale/en/LC_MESSAGES/gtk30.mo.
- tumbleweed-628aba51170df68037b752da — hicolor-icon-theme; HOLE; payload example: /usr/lib/rpm/macros.d/macros.hicolor, /usr/share/icons/hicolor/icon-theme.cache.
- tumbleweed-fb37a4a8d9cbdde019568fee — iso-codes; HOLE; payload example: /usr/share/iso-codes/json/iso_15924.json, /usr/share/iso-codes/json/iso_3166-1.json.
- tumbleweed-803cd9885d5ac3af08d2e0a6 — kImageAnnotator-lang; HOLE; payload example: /usr/share/kImageAnnotator/translations/kImageAnnotator_ar.qm, /usr/share/kImageAnnotator/translations/kImageAnnotator_bg.qm.
### metadata

- tumbleweed-afd24c8aacb62bb4d83a4713 — branding-openSUSE; HOLE; payload example: /usr/etc/SUSE-brand.
- tumbleweed-7a02732097fb92ad188d98e9 — javapackages-filesystem; HOLE; payload example: /usr/lib/rpm/macros.d/macros.javapackages-filesystem.
- tumbleweed-142611cc5e946fee6c2cbd1e — kscreenlocker6-imports; HOLE; payload example: /usr/lib64/qt6/qml/org/kde/kscreenlocker/kscreenlocker_greet.qmltypes, /usr/lib64/qt6/qml/org/kde/kscreenlocker/qmldir.
- tumbleweed-2f4b0dcaee7ccc4ae3445c43 — patterns-games-games; HOLE; payload example: no operational payload listed.
- tumbleweed-cae0778ca79df14155e00d1c — filesystem; HOLE; payload example: /bin, /lib.
- tumbleweed-46d7dfbc72a2231daf3f2e00 — patterns-glibc-hwcaps-x86_64_v3; HOLE; payload example: no operational payload listed.
- tumbleweed-b6506c20dbd511bc9d1cea43 — typelib-1_0-GLib-2_0; HOLE; payload example: /usr/lib64/girepository-1.0/GLib-2.0.typelib.
- tumbleweed-b8844433a232609731e25abb — girepository-1_0; HOLE; payload example: /usr/lib64/girepository-1.0/DBus-1.0.typelib, /usr/lib64/girepository-1.0/DBusGLib-1.0.typelib.
- tumbleweed-54f349aab25a45dcdffb851f — typelib-1_0-GObject-2_0; HOLE; payload example: /usr/lib64/girepository-1.0/GObject-2.0.typelib.
- tumbleweed-6f6fb0bebafbad99f7e14193 — typelib-1_0-GModule-2_0; HOLE; payload example: /usr/lib64/girepository-1.0/GModule-2.0.typelib.

Verification: 2390 input IDs and 2390 output IDs; equal sets, each ID once; all decisions allowed; description and reason word limits passed. Counts: MUST 2082, NOT 103, HOLE 205, UNKNOWN 0, MIXED 0.

## Confinement re-review amendment

The initial settings samples below are retained only as an audit record and are superseded by the replacement Rule settings list above.

S2.2-7,S2.2-13: Documented passive settings or themes confined to one program need not be recorded. Values are not treated as executable merely because shipped in a package.

Ten hand-checked examples (description checked against role):

- tumbleweed-a8553410b9fddc2ff2491faa — `MozillaFirefox-branding-openSUSE`: openSUSE branding of MozillaFirefox. Check: NOT; openSUSE branding of MozillaFirefox.
- tumbleweed-66ed6c20efbe0f068d1a3273 — `freecell-solver-presets`: Freecell Solver presets. Check: NOT; Freecell Solver presets.
- tumbleweed-d86c1763518f3862d3fda0c3 — `libreoffice-branding-openSUSE`: openSUSE Tumbleweed branding for LibreOffice. Check: NOT; openSUSE Tumbleweed branding for LibreOffice.
- tumbleweed-e605cf8492e45b603637b5d5 — `rpm-config-SUSE`: SUSE specific RPM configuration files. Check: NOT; SUSE specific RPM configuration files.
- tumbleweed-c7b91f63ad8ffcdf6acafdc6 — `ImageMagick-config-7-SUSE`: SUSE Provided Configuration. Check: NOT; SUSE Provided Configuration.
- tumbleweed-0440ecd1e9571cf8cde1be87 — `chrony-pool-openSUSE`: Chrony preconfiguration for openSUSE. Check: NOT; Chrony preconfiguration for openSUSE.
- tumbleweed-e788c0407bc909d3a1ff0c64 — `NetworkManager-branding-openSUSE`: Default openSUSE branding for NetworkManager configuration file. Check: NOT; Default openSUSE branding for NetworkManager configuration file.
- tumbleweed-88de43bb31abf3d91ab8c376 — `PackageKit-branding-openSUSE`: Simple software installation management software -- openSUSE default configuration. Check: NOT; Simple software installation management software -- openSUSE default configuration.
- tumbleweed-a08bac3bb4eead7e0306e601 — `flatpak-remote-flathub`: Add Flathub repository to system flatpak. Check: NOT; Add Flathub repository to system flatpak.
- tumbleweed-8fba25fb55f307fa4b8ffcd0 — `gtk4-branding-openSUSE`: The GTK+ toolkit library (version 3) -- openSUSE theme configuration. Check: NOT; The GTK+ toolkit library (version 3) -- openSUSE theme configuration.


Reviewed corrections:

- tumbleweed-0440ecd1e9571cf8cde1be87 — chrony-pool-openSUSE: MUST. Configures system clock synchronization or system network connectivity assessment; these effects extend beyond the consuming program to other system users.
- tumbleweed-e788c0407bc909d3a1ff0c64 — NetworkManager-branding-openSUSE: MUST. Configures system clock synchronization or system network connectivity assessment; these effects extend beyond the consuming program to other system users.
- tumbleweed-88de43bb31abf3d91ab8c376 — PackageKit-branding-openSUSE: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-a08bac3bb4eead7e0306e601 — flatpak-remote-flathub: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-8fba25fb55f307fa4b8ffcd0 — gtk4-branding-openSUSE: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-7b897cdfd9256cc00b039c05 — gtk3-branding-openSUSE: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-20e31b9f2ffa6df7884e3b3d — registries-conf-default: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-604e994fbd779b550d9377de — breeze6-cursors: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-b9c111aab7a79f2e0d7c33b6 — metatheme-breeze6-common: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-132eadc911f7cc2633da5ffd — gtk3-metatheme-breeze6: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-819b570cdea5ea55df85afe1 — gtk4-metatheme-breeze6: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-1b6ff4c84ec0c06e7e9cac74 — metatheme-adwaita-common: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-b323fb0780ed0774fe52a8c7 — gtk3-metatheme-adwaita: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-21c689370df3d76a7ab7285f — sddm-qt6-branding-openSUSE: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-398f3c80654469a71f15a2fe — sddm-branding-openSUSE: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-06d3881473145922f997835c — plasma6-branding-openSUSE: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.
- tumbleweed-4c394b49c4edbaf1ac753966 — libcontainers-default-policy: HOLE. Values affect shared libraries, system appearance, sessions, or installation choices; the text does not establish that their effects remain inside one program.

Final counts after confinement review: MUST 2084, NOT 86, HOLE 220, UNKNOWN 0, MIXED 0.
