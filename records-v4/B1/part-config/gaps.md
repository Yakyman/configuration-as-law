# Configuration-channel gaps

## Home-page navigation and launching something

C8.08: S8.2-14 does not define whether navigating to the chosen home page launches something, so its stored URL is either a setting requiring its own line under S8.2-17 and declaration-only change under S8.3-6/8, or a program record exempt under S8.2-2/14; the theme value is a program record under both readings.

S8.2-14: “A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.”

S8.2-17: “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.”

S8.3-6: “The system provides no ordinary path for changing what is installed and settings past the declaration.”

The two readings differ in whether a home-page preference change must change a declaration line. No enforcement mechanism is at issue. Documentation: [stored preferences](https://support.mozilla.org/en-US/kb/firefox-support-troubleshooting-guide?mobile=0), with short excerpt in [sources](sources.md#pref).
