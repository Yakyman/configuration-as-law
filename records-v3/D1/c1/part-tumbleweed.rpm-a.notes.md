# c1: first RPM inventory half

Scope: first 2,390 L1:package:rpm rows, in input order. COMMON.md, TEXT.md Sections 2 and 3, and SENTENCES.md were read. No other classification was consulted. No objects were removed.

The inventory lists installed package names, versions, and architecture, but `../in/raw/tumbleweed/raw/113-ownership-rpm.out` is empty. Public official repository descriptions and full file lists were therefore used. The package object is classified by its own payload, not by a similarly named application. A package containing both required code and documents is one package object, not an inventory group of independently classified stored files.

## Evidence

Official primary metadata: URL in (not published: downloaded distribution package metadata). Official file lists: URL in (not published: downloaded distribution package metadata). Compressed original metadata is retained. Installed versions were compared against file-list versions: all match except openSUSE-build-key (installed 1.0-69.1, available 1.0-68.1); its documented purpose is used without claiming byte identity. Five imported gpg-pubkey entries have no repository counterpart.

Additional documentation:

- https://rpm.org/docs/6.0.x/man/rpmkeys.8 : “Digital signatures cannot be verified without the corresponding public key (aka certificate).”
- https://gi.readthedocs.io/en/latest/ : “language bindings can read this metadata and automatically provide bindings to call into the C library.”
- https://docs.kde.org/trunk_kf6/en/kdebugsettings/kdebugsettings/categories-file.html describes category names, descriptions, defaults, and rename mappings consumed by the category editor.
- https://docs.kde.org/trunk_kf6/en/kdebugsettings/kdebugsettings/custom-rules-tab.html explains that categories can be configured without an installed category description. The executable libraries remain independently packaged.
- https://download.opensuse.org/tumbleweed/repo/oss/noarch/hicolor-icon-theme-0.18-1.5.noarch.rpm : inspected `usr/lib/rpm/macros.d/macros.hicolor`. Its `%icon_theme_cache_create_ghost` expands to shell `mkdir` and `touch` operations. This package is MUST despite its theme name.

## Literal grounds

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

S2.2-9: “a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;”

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

S3-2: “If what the object does remains unknown, the case yields ?.”

## Homogeneous rules and manual checks

Rules are implemented in `part-tumbleweed.rpm-a.classify.py`. Executable payload detection precedes names such as theme, presets, data, and branding. Explicit nonhomogeneous cases use named decisions. The following checks inspected actual paths and package descriptions, not just labels. Each rule below lists ten manually checked object IDs.

### code (2001 rows)

MUST: executable programs, native shared libraries, interpreter scripts, and runtime modules. These supply executable operations under S2.2-9/10/13. Only non-documentation paths count; executable content overrides a theme or data package name.

- `tumbleweed-2194ecddf8f96383cae8f9a9` — gxditview; inspected `/usr/bin/gxditview`.
- `tumbleweed-384b789273ac07e5b755d800` — python313-pycairo; inspected `/usr/lib64/python3.13/site-packages/cairo/__init__.py`.
- `tumbleweed-c7867d9621c22e0b97006af6` — python313-puremagic; inspected `/usr/bin/puremagic`.
- `tumbleweed-e880790a58444d3bafa14fa5` — python313-nftables; inspected `/usr/lib/python3.13/site-packages/nftables/__init__.py`.
- `tumbleweed-9746777c7b5f013afd157f4d` — python313-hyperframe; inspected `/usr/lib/python3.13/site-packages/hyperframe/__init__.py`.
- `tumbleweed-d33455986c66ff248d59eef2` — Mesa-libva; inspected `/usr/lib64/dri/nouveau_drv_video.so`.
- `tumbleweed-cc32ce44527335a224b417dd` — busybox-static; inspected `/usr/bin/busybox-static`.
- `tumbleweed-b891edce09972457274125e3` — compat-usrmerge-tools; inspected `/usr/bin/usrmergecheck`.
- `tumbleweed-4d8757f93c50b0bfcead2627` — debuginfod-profile; inspected `/etc/profile.d/debuginfod.sh`.
- `tumbleweed-668b190c43f169fc63e4be91` — freecell-solver-presets; inspected `/usr/share/freecell-solver/presets/abra-kadabra.sh`.

### category (62 rows)

NOT: packages whose non-documentation payload consists exclusively of diagnostic category and rename descriptions. These supply descriptive choices in the category editor; custom rules remain possible and executable libraries remain. S2.2-4 applies to descriptions, not to recorded log events.

- `tumbleweed-301c13d4a59931a7b5c91c83` — akonadi-calendar; inspected `/usr/share/qlogging-categories6/akonadi-calendar.categories`.
- `tumbleweed-c61693ca0d9c338b6719b0d3` — akonadi-mime; inspected `/usr/share/qlogging-categories6/akonadi-mime.categories`.
- `tumbleweed-7695b0145913f25106970cd7` — calendarsupport; inspected `/usr/share/qlogging-categories6/calendarsupport.categories`.
- `tumbleweed-413f0500532691a1403b99e4` — eventviews; inspected `/usr/share/qlogging-categories6/eventviews.categories`.
- `tumbleweed-2273f5235f66c502aa5c172b` — incidenceeditor; inspected `/usr/share/qlogging-categories6/incidenceeditor.categories`.
- `tumbleweed-cfbb9493d3cc953559180595` — kf6-attica; inspected `/usr/share/qlogging-categories6/attica.categories`.
- `tumbleweed-e51e5f35a865a939595bab30` — kf6-bluez-qt; inspected `/usr/share/qlogging-categories6/bluezqt.categories`.
- `tumbleweed-dd4240e6ee3b671d67697c5d` — kf6-karchive; inspected `/usr/share/qlogging-categories6/karchive.categories`.
- `tumbleweed-88fe72d3de4e08b187d1511a` — kf6-kbookmarks; inspected `/usr/share/qlogging-categories6/kbookmarks.categories`.
- `tumbleweed-764aa158abfb0c6a7192d979` — kf6-kcodecs; inspected `/usr/share/qlogging-categories6/kcodecs.categories`.

### document (12 rows)

NOT: documentation and license-only packages under S2.2-4. The text expressly introduces content as an exception, so inability to read the removed document is not counted again as loss of program behavior.

- `tumbleweed-ce54db5c43dcf480996ace27` — boost-license1_92_0; inspected `/usr/share/licenses/boost-license1_92_0/LICENSE_1_0.txt`.
- `tumbleweed-21c473dcf355645958b2923e` — cryptsetup-doc; inspected `/usr/share/doc/packages/cryptsetup-doc/AUTHORS`.
- `tumbleweed-34f1d68aa8f99541fd83b097` — kaddressbook-doc; inspected `/usr/share/doc/HTML/en/kaddressbook/KDE_logo.png`.
- `tumbleweed-48601afb75375826257791bf` — pam-manpages; inspected `/usr/share/man/man3/misc_conv.3.gz`.
- `tumbleweed-ce47e21fa36959c229791ea2` — unzip-doc; inspected `/usr/share/doc/packages/unzip-doc/BUGS`.
- `tumbleweed-4c680d99add6f6e22e4e15c9` — bash-doc; inspected `/usr/share/doc/packages/bash/BUGS`.
- `tumbleweed-0b374b0c6cdc5193e1c634a0` — coreutils-doc; inspected `/usr/share/info/coreutils.info.gz`.
- `tumbleweed-158dbe5ce67a1f463f677898` — coreutils-systemd-doc; inspected `/usr/share/man/man1/pinky.1.gz`.
- `tumbleweed-88c545e32bc24c4e9325ebcf` — info-std; inspected `/usr/share/info/info-stnd.info.gz`.
- `tumbleweed-1a2ff00a85c08b7185dc99db` — man-pages; inspected `/usr/share/doc/packages/man-pages/CONTRIBUTING`.

### translation (30 rows)

NOT: interface translations and translated names are content. Under S2.2-4 the same operation remains available while its translated wording is unavailable. This rule does not cover language-processing engines or dictionaries that enable distinct processing.

- `tumbleweed-69d8cbcefe0629f32ed6c8e8` — desktop-translations; inspected `/usr/share/locale/af/LC_MESSAGES/desktop_translations.mo`.
- `tumbleweed-e3ffdbeeab220be3a54cafba` — iso-codes; inspected `/usr/share/iso-codes/json/iso_15924.json`.
- `tumbleweed-cef9aa36975108f20d6841ff` — kImageAnnotator-lang; inspected `/usr/share/kImageAnnotator/translations/kImageAnnotator_ar.qm`.
- `tumbleweed-527aeb630ad9f2636cdd559f` — libksane-lang; inspected `/usr/share/locale/ar/LC_MESSAGES/libksane.mo`.
- `tumbleweed-6a567e1b020369e9b4a15b5e` — libqt5-qttranslations; inspected `/usr/share/qt5/translations/assistant_ar.qm`.
- `tumbleweed-debbb43da15a0050abbd7e0a` — libstorage-ng-lang; inspected `/usr/share/locale/af/LC_MESSAGES/libstorage-ng.mo`.
- `tumbleweed-af2b623383a61a33374a59f1` — qt6-translations; inspected `/usr/share/qt6/translations/assistant_ar.qm`.
- `tumbleweed-14b4feff4d3b3c916032ed56` — snapper-lang; inspected `/usr/share/locale/af/LC_MESSAGES/snapper.mo`.
- `tumbleweed-f73eeb400766d5a937dddc88` — kf6-kuserfeedback-lang; inspected `/usr/share/locale/ar/LC_MESSAGES/userfeedbackconsole6_qt.qm`.
- `tumbleweed-e4b043dbfeb54717e5f66dcc` — kidentitymanagement-lang; inspected `/usr/share/locale/ar/LC_MESSAGES/libkpimidentities6.mo`.

### asset (11 rows)

NOT: pictures, icons, audio samples, and card artwork under S2.2-4. The visual or audio work itself becomes unavailable; execution of the operation displaying or playing content remains. Packages with macros or code are excluded.

- `tumbleweed-f30a186bd1cff9957e0f7b5c` — kdegames-carddecks-default; inspected `/usr/share/carddecks/svg-oxygen-air/11.png`.
- `tumbleweed-39af3faa265fdda45dd7c62f` — kf6-breeze-icons; inspected `/usr/share/icons/breeze-dark/actions/12/external-link-symbolic.svg`.
- `tumbleweed-8deb6bea53de73438bc0b1e6` — kmail-application-icons; inspected `/usr/share/icons/breeze-dark/16x16/emblems/gpg-key-trust-level-0.svg`.
- `tumbleweed-d2388c321ef8b22307dcf7bd` — ocean-sound-theme6; inspected `/usr/share/licenses/ocean-sound-theme6/BSD-2-Clause.txt`.
- `tumbleweed-bf9029a4ec645e21be37f294` — wallpaper-branding-openSUSE; inspected `/usr/share/gnome-background-properties/wallpaper-branding-openSUSE.xml`.
- `tumbleweed-9fe77d5b5a8d7bb3aa41ea6a` — xbitmaps; inspected `/usr/include/X11/bitmaps/1x1`.
- `tumbleweed-6cc4dd2ccf77fb4f5b6b01f6` — distribution-logos-openSUSE-icons; inspected `/usr/share/icons/hicolor/scalable/apps/distributor-logo-Aeon.svg`.
- `tumbleweed-9d4553a31373cb92d9b4fd44` — sound-theme-freedesktop; inspected `/usr/share/doc/packages/sound-theme-freedesktop/README`.
- `tumbleweed-aa92a36c91f7c095a4cf0ae4` — hicolor-icon-theme-branding-openSUSE; inspected `/usr/share/icons/hicolor/16x16/apps/distributor.png`.
- `tumbleweed-0c9194115520ab49a173b08c` — libreoffice-icon-themes; inspected `/usr/share/libreoffice/share/config/images_breeze.zip`.

### presentation (15 rows)

NOT: nonexecuted presentation themes containing visual assets and color/style values, S2.2-4/7/13. Unlike code themes, these merely supply presentation content. Verified file lists exclude runtime scripts and shared-object implementations.

- `tumbleweed-694485646109ee5946fed689` — libplasma6-desktoptheme; inspected `/usr/share/plasma/desktoptheme/breeze-dark/colors`.
- `tumbleweed-ff8414e8fa9b41b847ba8f03` — metatheme-breeze6-common; inspected `/usr/share/doc/packages/metatheme-breeze6-common/README.md`.
- `tumbleweed-8e84d13ea1b940f02e6994e2` — gtk3-metatheme-breeze6; inspected `/usr/share/themes/Breeze-Dark/gtk-3.0/gtk.css`.
- `tumbleweed-c99ceaa989531e038628e42e` — gtk4-metatheme-breeze6; inspected `/usr/share/themes/Breeze-Dark/gtk-4.0/gtk.css`.
- `tumbleweed-8950e190d14060a369183dc1` — metatheme-adwaita-common; inspected `/usr/share/doc/packages/metatheme-adwaita-common/NEWS`.
- `tumbleweed-99e98e78a19742451d9457a5` — gtk3-metatheme-adwaita; inspected `/usr/share/themes/Adwaita-dark/gtk-3.0/gtk.css`.
- `tumbleweed-d095a3b61de32b1463d7c78b` — yast2-qt-branding-openSUSE; inspected `/usr/share/YaST2/theme/current/wizard/arr_down.png`.
- `tumbleweed-6ec882183d132324cb0208a4` — plymouth-theme-spinner; inspected `/usr/share/plymouth/themes/spinner/animation-0001.png`.
- `tumbleweed-4deaf55db08341f000a852f5` — yast2-theme; inspected `/etc/icewm/preferences.yast2`.
- `tumbleweed-65bfdabf3b6608dedffb67e5` — plymouth-theme-bgrt; inspected `/usr/share/plymouth/themes/bgrt/bgrt.plymouth`.

### selector (28 rows)

HOLE: dependency-only package selectors. Removal can leave installed implementations unchanged but alter future selection by package tools. S2.2-1/2 do not specify whether that future consequence belongs to the removal test; S2.2-7 offers a competing single-manager-values reading.

- `tumbleweed-37db51661957d09b5c15eacf` — patterns-games-games; inspected `/usr/share/doc/packages/patterns/games.txt`.
- `tumbleweed-8ebb5b342bc9dc105f0138a9` — patterns-glibc-hwcaps-x86_64_v3; inspected `/usr/share/doc/packages/patterns/x86_64_v3.txt`.
- `tumbleweed-296f03671ca8befb4893d5e2` — openSUSE-release-ftp; inspected `/usr/share/doc/packages/openSUSE-release-ftp/README`.
- `tumbleweed-4aa703e25ccc5895e1cee141` — patterns-base-minimal_base; inspected `/usr/share/doc/packages/patterns/minimal_base.txt`.
- `tumbleweed-604a999da494f2de35403dee` — patterns-base-sw_management; inspected `/usr/share/doc/packages/patterns/sw_management.txt`.
- `tumbleweed-2f7c08878cbbd469fe4f4547` — patterns-base-selinux; inspected `/usr/share/doc/packages/patterns/selinux.txt`.
- `tumbleweed-887caba836a7c23b3fedba9d` — patterns-fonts-fonts_opt; inspected `/usr/share/doc/packages/patterns/fonts_opt.txt`.
- `tumbleweed-7ff02912d648f6301fd0d572` — patterns-yast-x11_yast; inspected `/usr/share/doc/packages/patterns/x11_yast.txt`.
- `tumbleweed-8e6d6eb9be69c877faa7bd08` — patterns-kde-kde_yast; inspected `/usr/share/doc/packages/patterns/kde_yast.txt`.
- `tumbleweed-8ffe304c89c8c7e36f097d58` — patterns-fonts-fonts; inspected `/usr/share/doc/packages/patterns/fonts.txt`.

### introspection (18 rows)

MUST: runtime typelib interface metadata required to generate native language bindings. S2.2-1/2 apply because removing these descriptions prevents calls, rather than merely making explanatory content unavailable. They are not incorrectly called executable libraries.

- `tumbleweed-7a6ad33f358961bfad1a3cba` — typelib-1_0-GLib-2_0; inspected `/usr/lib64/girepository-1.0/GLib-2.0.typelib`.
- `tumbleweed-900dbc71741501e821d1c709` — typelib-1_0-GObject-2_0; inspected `/usr/lib64/girepository-1.0/GObject-2.0.typelib`.
- `tumbleweed-b7d547e3a754a9f5372ffdcf` — typelib-1_0-GModule-2_0; inspected `/usr/lib64/girepository-1.0/GModule-2.0.typelib`.
- `tumbleweed-50bd7f4cb772b73088964c52` — typelib-1_0-GLibUnix-2_0; inspected `/usr/lib64/girepository-1.0/GLibUnix-2.0.typelib`.
- `tumbleweed-272491cb93106d5053d88d39` — typelib-1_0-Atk-1_0; inspected `/usr/lib64/girepository-1.0/Atk-1.0.typelib`.
- `tumbleweed-c94a1b3acbd79a0bc4cb5cf6` — typelib-1_0-HarfBuzz-0_0; inspected `/usr/lib64/girepository-1.0/HarfBuzz-0.0.typelib`.
- `tumbleweed-80a3e282e5b79c37931671ce` — typelib-1_0-Gio-2_0; inspected `/usr/lib64/girepository-1.0/Gio-2.0.typelib`.
- `tumbleweed-e61016bde855c68fde4fd1ec` — typelib-1_0-Secret-1; inspected `/usr/lib64/girepository-1.0/Secret-1.typelib`.
- `tumbleweed-70589ea9923cebb923c91aef` — typelib-1_0-Pango-1_0; inspected `/usr/lib64/girepository-1.0/Pango-1.0.typelib`.
- `tumbleweed-e7b05fc9fc3e1f0f168dfc36` — typelib-1_0-GdkPixbuf-2_0; inspected `/usr/lib64/girepository-1.0/GdkPixbuf-2.0.typelib`.

### font (35 rows)

HOLE: font glyphs and associated font substitution mappings. S2.2-2 can count losing character rendering as lost capability; S2.2-4 can treat the typeface as unavailable content. The text does not define this boundary.

- `tumbleweed-33499c40cabacd70ef4d21d9` — urw-base35-fonts-Z003; inspected `/usr/share/fonts/truetype/Z003-MediumItalic.otf`.
- `tumbleweed-862ddc569edf79ec6aece441` — urw-base35-fonts-URWGothic; inspected `/usr/share/fonts/truetype/URWGothic-Book.otf`.
- `tumbleweed-0e9ba7156c0c20c550992121` — urw-base35-fonts-URWBookman; inspected `/usr/share/fonts/truetype/URWBookman-Demi.otf`.
- `tumbleweed-1a229bd3c5b65cda8f942bd8` — urw-base35-fonts-StandardSymbolsPS; inspected `/usr/share/fonts/truetype/StandardSymbolsPS.otf`.
- `tumbleweed-296a32b8080e5f74e2f35430` — urw-base35-fonts-P052; inspected `/usr/share/fonts/truetype/P052-Bold.otf`.
- `tumbleweed-59566a89cf17ed81b1692100` — urw-base35-fonts-NimbusSans; inspected `/usr/share/fonts/truetype/NimbusSans-Bold.otf`.
- `tumbleweed-74d9d28ed3c6446f8ad2696e` — urw-base35-fonts-NimbusRoman; inspected `/usr/share/fonts/truetype/NimbusRoman-Bold.otf`.
- `tumbleweed-ed87f367256d9993c15e4c83` — urw-base35-fonts-NimbusMonoPS; inspected `/usr/share/fonts/truetype/NimbusMonoPS-Bold.otf`.
- `tumbleweed-96e3075e617c5983470c405d` — urw-base35-fonts-D050000L; inspected `/usr/share/fonts/truetype/D050000L.otf`.
- `tumbleweed-40516f5352772e4cca300618` — urw-base35-fonts-C059; inspected `/usr/share/fonts/truetype/C059-BdIta.otf`.

### firmware (34 rows)

MUST: firmware images supplied to drivers for loading into supported devices, S2.2-1/2/16. Their documented role enables device behavior. Catch-all dependency metapackages are excluded.

- `tumbleweed-412a36df79780b825ecaee73` — kernel-firmware-usb-network; inspected `/usr/lib/firmware/aic/aic8800d80/fmacfw_8800d80_u02.bin.xz`.
- `tumbleweed-c0ef9ecf5b546861a2691bb0` — kernel-firmware-ueagle; inspected `/usr/lib/firmware/ueagle-atm/CMV4p.bin.v2.xz`.
- `tumbleweed-798825e63087dcf733dd5a63` — kernel-firmware-ti; inspected `/usr/lib/firmware/ti-connectivity/TIInit_6.2.31.bts.xz`.
- `tumbleweed-b3a3ec819bae794ee9f21037` — kernel-firmware-sound; inspected `/usr/lib/firmware/1534-2-0x8.bin.xz`.
- `tumbleweed-c7e4a57192087cdf95acd8e8` — kernel-firmware-serial; inspected `/usr/lib/firmware/edgeport/boot.fw.xz`.
- `tumbleweed-5da966f776fc272cbd679806` — kernel-firmware-realtek; inspected `/usr/lib/firmware/realtek/rt1320/rt1320-patch-code-vab.bin.xz`.
- `tumbleweed-8c2e91ec924f052ebbc3b8a8` — kernel-firmware-radeon; inspected `/usr/lib/firmware/radeon/ARUBA_me.bin.xz`.
- `tumbleweed-f057cdb52209ca0d28de1bf1` — kernel-firmware-qlogic; inspected `/usr/lib/firmware/cbfw-3.2.5.1.bin.xz`.
- `tumbleweed-c588fd227e5e14b1a8d6fcf2` — kernel-firmware-qcom; inspected `/usr/lib/firmware/a300_pfp.fw.xz`.
- `tumbleweed-8bfe28daef97939f9944f764` — kernel-firmware-platform; inspected `/usr/lib/firmware/Lontium/lt7911exc_fw.bin.xz`.

## Individual cases

All cases outside the homogeneous rules were considered individually using their specific payload and description. Their per-row grounds and uncertainty are recorded in the TSV. Notable distinctions: installed public-key copies explicitly unused by RPM are content; imported RPM verification keys are operational trust values with a setting/capability boundary; account definitions and multi-application policies are MUST. Systemd defaults have an unresolved single-reader versus multiple-affected-programs scope. No decision is based merely on the inventory word “package”.

Three UNKNOWN rows remain: the GNOME resource bundle whose internal payload is unspecified, and two XSLT transformation packages whose execution-rights/confinement evidence is insufficient. This is uncertainty about object behavior under S3-2, not a declaration-design question.

Validation: 2,390 unique output IDs equal the assigned input IDs, each once; all decisions are allowed; descriptions and reasons satisfy word limits. Final counts: MUST 2,119; NOT 158; HOLE 110; UNKNOWN 3; MIXED 0.
