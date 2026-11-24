# Facts for families 13–15

21 disk-object examples are retained from the eight named channels. Where a channel lists an executable or a shared library, each receives a separate ID. Typed commands and runtime-only processes are not added. Family 15 retains only the two history objects named by its card.

B1 describes documented channels, not measured instances. `unspecified` is not a machine. Path templates are preserved and do not assert existence. No inventory ID or operator run is linked in B1, so an unrelated inventory object is not substituted. Historical bytes, identities and times cannot be recovered by a fresh probe. Documented semantics were checked in primary sources before considering probes; no fresh machine was needed for those semantics.

The precise facts and their sources are in `facts.tsv`. `SOURCES.md` contains short checked quotations and primary URLs. No classification columns are included. UNKNOWN counts here count rows, not different people or hypotheses.

## 13. a browser's home page and “launches something”

### s2-1 — <Firefox-profile>/prefs.js: activated theme preference

Channel: C8.08 a. A selected preference value retained in the profile file. Producer: Firefox preference storage. Derived from: User selection of a theme. The selected value is read by Firefox, not supplied as executable statements.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
### s2-2 — <Firefox-profile>/prefs.js: home-page URL preference

Channel: C8.08 b. A selected URL retained in the profile file. Producer: Firefox preference storage. Derived from: User selection of a home page. The URL is read as a navigation value; this object is not the fetched page or its scripts.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `additional_launch_or_access`: No selected URL, protocol handler or target contents are recorded; behavior beyond page navigation cannot be established.

## 14. a compiler or a build tool as a built-in tool or as general-purpose work

### s2-3 — ./a.out or <-o-path>

Channel: C5.1 a. Native linked executable. Producer: GCC compilation/linking. Derived from: C source and linker inputs. The channel specifies native output then execution as a process.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `launch_change_access_behavior`: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.
### s2-4 — ./<name>.c

Channel: C5.1 b. C source file. Producer: UNKNOWN: The writing program or creator of the source is not identified.. Derived from: C source input; earlier origin not given. Compilation is needed before the native execution described; source is compiler input.

Unknown facts:

- `package_origin`: B1 names a C source input but gives no package-delivery provenance.
- `producer`: The writing program or creator of the source is not identified.
- `human_creation_or_bringing`: B1 names the source input but does not identify its creator or whether the operator brought it.
- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `launch_change_access_behavior`: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.
### s2-5 — ./<name>.o

Channel: C5.1 d. Unlinked object file. Producer: GCC compilation/assembly. Derived from: C source and compilation inputs. The described intermediate needs linking before execution; the linker consumes it.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `launch_change_access_behavior`: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.
### s2-6 — CMakeLists.txt

Channel: C5.2 a recipe. Project file with CMake-language commands. Producer: Project author. Derived from: Project build instructions. CMake evaluates this project file; its command language can start child processes.

Unknown facts:

- `human_creation_or_bringing`: B1 names the project recipe without stating whether the invoking person wrote it or brought it.
- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `writing_program`: The editor or link-creation program is not named in the channel.
### s2-7 — <try_run COPY_FILE destination>

Channel: C5.2 a executable. Copied configure-test executable. Producer: CMake try_run and invoked compiler/linker. Derived from: Source files passed to try_run. try_run builds and runs a test executable; COPY_FILE retains it when requested.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `launch_change_access_behavior`: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.
### s2-8 — build/CMakeCache.txt: compile/run result entries

Channel: C5.2 b cache. Cached result values. Producer: CMake try_run. Derived from: Build success/failure and test exit result. CMake reads cached results as values.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
### s2-9 — <build>/CMakeFiles/CMakeConfigureLog.yaml: try_run event

Channel: C5.2 b log. YAML event in the configure log. Producer: CMake during configuration. Derived from: Compile/run event details. The event is written/read as log data.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
### s2-10 — <prefix>/bin/<program>

Channel: C5.3 a executable. Executable copied by install rules. Producer: CMake-generated install operation. Derived from: Built executable selected by project install rules. The copied target is an executable; launch uses the operating-system loader.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `launch_change_access_behavior`: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.
### s2-11 — <prefix>/lib/<library>.so

Channel: C5.3 a library. Shared library copied by install rules. Producer: CMake-generated install operation. Derived from: Built library selected by project install rules. Shared-library machine code is loaded into a consuming process.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `launch_change_access_behavior`: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.
- `specific_consumer`: B1 identifies a shared library but no named process or program that loads it.
### s2-12 — build/cmake_install.cmake

Channel: C5.3 b. Generated CMake script. Producer: CMake install() processing. Derived from: Project install rules. Executed by generated install target, CPack, or cmake -P.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
### s2-13 — <shell-startup-file>: PATH assignment

Channel: C5.3 c. Persisted shell assignment. Producer: Person editing a shell startup file. Derived from: Person-selected command-search path. Bash reads and executes startup-file statements; PATH changes command lookup.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `writing_program`: The editor or link-creation program is not named in the channel.
### s2-14 — <prefix>/bin/<alias>

Channel: C5.3 d. Symbolic link to an executable. Producer: Person creating a link. Derived from: Chosen target executable path. A link resolves to its target; invocation via the alias executes the target.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `channel_tool_purpose`: The channel does not identify the program used to create the link.
- `writing_program`: The editor or link-creation program is not named in the channel.
### s2-15 — ./<program> (replacement)

Channel: C5.4 a executable. Executable bytes replacing previous contents at the same path. Producer: Compiler/build operation. Derived from: New source/build inputs replacing earlier output. Native executable can be started as a process in the described channel.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `launch_change_access_behavior`: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.
### s2-16 — ./<library>.so (replacement)

Channel: C5.4 a library. Shared-library bytes replacing previous contents at the same path. Producer: Compiler/build operation. Derived from: New source/build inputs replacing earlier output. Library code can execute within a process that loads it.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `launch_change_access_behavior`: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.
- `specific_consumer`: B1 identifies a shared library but no named process or program that loads it.
### s2-17 — ./<plugin>.so

Channel: C5.5 a. Locally built compiler plugin shared library. Producer: Local compiler/linker build. Derived from: Plugin source and build inputs. GCC loads the plugin into its own process; plugin extends compiler behavior.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `launch_change_access_behavior`: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.
### s2-18 — <packaged-plugin-path>

Channel: C5.5 b. Unchanged plugin obtained in an installed package. Producer: Package installation in the described channel. Derived from: Installed package containing the plugin. GCC plugin module loaded into compiler process.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `launch_change_access_behavior`: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.
### s2-19 — ./a.out or <-o-path> (plugin-enabled build)

Channel: C5.5 c. Generated executable. Producer: Compiler/linker with plugin loaded. Derived from: Source, linker inputs and compilation affected by the plugin. Linked output can execute as its own process in the described channel.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `launch_change_access_behavior`: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.

## 15. saved history as values read or as executable statements

### s2-20 — ~/.python_history

Channel: C7.06 b. Saved interactive Python history entries. Producer: Interactive Python history facility. Derived from: Retained user input from interactive sessions. History is loaded for recall/editing. Retained statements can be submitted to Python.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `launch_change_access_behavior`: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.
- `whole_file_executability`: Actual retained bytes and interpreter state are absent; the validity of the entire file as a script cannot be established.
### s2-21 — <HISTFILE> (default ~/.bash_history)

Channel: C7.17 c. Saved shell command text. Producer: Bash history facility. Derived from: Retained shell history list entries. History reading populates a list; recalled commands can be executed through fc or history substitution.

Unknown facts:

- `observed_presence`: B1 specifies no machine observation or inventory object for this channel; current or first-night presence cannot be established.
- `exact_bytes_or_selected_value`: B1 supplies a path template/operation but no retained bytes or exact selected value for an instance.
- `package_name`: No package identity for this object is given by B1; inventories cannot be joined without an identified machine/object.
- `package_version`: No delivering package version is given for an identified instance.
- `producer_version`: No observed version of the writing/building program is given for an instance.
- `actor_identity`: Only the generic role of a user is described; no person identity is recorded.
- `choice_time`: No UTC choice time is recorded for an identified instance.
- `production_time`: The documented producing operation has no observed run or UTC timestamp in B1.
- `effective_rights`: B1 gives no concrete execution credentials, file mode/capabilities, or confinement configuration for an instance.
- `primary_description`: No person-designated primary description for this object is supplied by B1.
- `source_build_line`: No exact source/build line for this object is supplied by B1.
- `persistent_backing`: The channel specifies a saved file but names no observed filesystem backing or restart survival.
- `remains_as_received`: No delivered package baseline and corresponding instance digest are provided; local generation does not identify any earlier package ownership.
- `launch_change_access_behavior`: The concrete code, retained statements or source inputs are not supplied, so actual child launches, changes to other files and access grants cannot be enumerated.
- `whole_file_executability`: Actual retained bytes and interpreter state are absent; the validity of the entire file as a script cannot be established.
