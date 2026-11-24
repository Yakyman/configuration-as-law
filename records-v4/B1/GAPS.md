# Gaps in the 88-row classification

This is the separate, unweighted investigation required by PROTOCOL.md Section 5. The sole TWO_WAYS row is C8.08; there are no NOT_DECIDED rows. Missing tool/artifact facts are listed in the table as FACT_UNKNOWN and are not textual gaps.

## Home-page navigation and launching something

S8.2-14 does not say whether opening the chosen home page is launching something: for C8.08 the same stored URL is either a setting under S8.2-14 requiring its own line under S8.2-17, or a program record under S8.2-14 that need not be recorded under S8.2-2.

The documented objects are a chosen theme value and a home-page URL in the browser profile preferences. The homepage is opened on browser start, a new window, or the Home button, as documented in [home-page behavior](https://support.mozilla.org/en-US/kb/how-to-set-the-home-page); [preference storage](https://support.mozilla.org/en-US/kb/firefox-support-troubleshooting-guide?mobile=0) documents the stored values. Short primary excerpts are in [SOURCES.md](SOURCES.md).

Both values fail Q1 (not unchanged package contents) and Q2 (read as values, not executed as code). The theme is a program record under S8.2-14 under both readings. For the URL, the broad reading includes page opening in launching something; the narrow reading means launching an executable/program and treats page display as ordinary work within the already-running browser. No sentence selects between these meanings.

The declarations differ by the required home-page setting line. Under the broad reading, changing that URL must follow the declaration and P4 disallows an ordinary bypass; under the narrow reading, the URL need not be recorded and this preference change is outside P4's installed-object/setting requirement. Voluntary recording remains permitted by S8.2-19. The result concerns the requirement, not the mechanism by which it is enforced.

S8.2-6: «What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.»

S8.2-14: «A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.»

S8.2-17: «A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.»

S8.2-2: «The rest need not be recorded.»

S8.3-6: «P4. Law. The system provides no ordinary path for changing what is installed and settings past the declaration.»

S8.3-8: «What is installed and settings can be changed past the declaration only by breaking.»

