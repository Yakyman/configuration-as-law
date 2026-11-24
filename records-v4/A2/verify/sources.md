# Sources fetched for A2-V (2026-11-23, UTC)

WX1 https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging
- "The extension must request the "nativeMessaging" permission or optional permission in the manifest.json file."
- "The native application is not installed or managed by the browser."
- "The app manifest file must be installed along with the native application."

WX2 https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/management/uninstall
- "This API requires the "management" API permission."

WX3 https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/open
- "The open() function of the downloads API opens the downloaded file with its associated application."
- "To use this function in your extension you must ask for the "downloads.open" manifest permission"

WX4 https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/management
- "Get information about installed add-ons."
- "Uninstalls a particular add-on, given its ID."

WX5 https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Anatomy_of_a_WebExtension
- "An extension consists of a collection of files, packaged for distribution and installation."
- "Scripts that respond to browser events."

WX6 https://raw.githubusercontent.com/darkreader/darkreader/main/src/manifest-firefox.json
- "permissions": ["alarms", "contextMenus", "storage", "tabs", "theme", "<all_urls>"]; "optional_permissions": []
- gecko id "<REDACTED>"; a background page and two content_scripts entries; no nativeMessaging,
  management, downloads, downloads.open, proxy, privacy or browserSettings anywhere in the file; no "extends" key.
- Listing named in https://raw.githubusercontent.com/darkreader/darkreader/main/README.md:
  "https://addons.mozilla.org/firefox/addon/darkreader/" (the listing page itself returned a client challenge).

Not obtained: support.mozilla.org articles on installing/removing add-ons (client challenge page).
