# New hole kind found in part l2-other

## `code-inside-program-package` — a package of a program's built-in installer whose code runs only inside that program

A browser extension that Firefox's own AddonManager installed permanently is a package (S8.1-5, S8.1-6), so by question 1 it is an installed object that must be recorded. But its code runs inside a recorded program and cannot launch programs or change what is installed or the settings: the ClearURLs manifest asks for `downloads` but not `downloads.open`, and MDN says `downloads.open()` needs both. The clarification S8.2-21 says such code need not be recorded, and no sentence says which of the two prevails (S8.2-6 fixes only the order of the four questions).

- S8.2-1: «Everything that is installed and every setting must be recorded.»
- S8.1-6: «Package—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.»
- S8.2-7: «Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?»
- S8.2-21: «Code that runs inside a recorded program and cannot itself launch programs or change what is installed and the computer’s settings—a web page in a browser, a guest system in a virtual machine—need not be recorded.»

Decision A: INSTALLED-OWN, which must be recorded (S8.1-5, S8.1-6, S8.2-7, S8.2-1). Decision B: need not be recorded (S8.2-21).

Evidence: `D1/in/raw/void/members/61a9a88ad2b852b6cf106db6.tsv` and `D1/in/raw/alma/members/2ea4b9f74eb9ce06f9d317ff.tsv` (one `{<REDACTED>}.xpi` each); permissions from https://raw.githubusercontent.com/ClearURLs/Addon/master/manifest.json (`"downloads"`, no `"downloads.open"`, no `nativeMessaging`); https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/open: “To use this function in your extension you must ask for the "downloads.open" manifest permission, as well as the "downloads" permission.”

Example ids: void-61a9a88ad2b852b6cf106db6, alma-2ea4b9f74eb9ce06f9d317ff.
