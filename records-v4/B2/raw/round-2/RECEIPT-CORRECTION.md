# Native package receipt correction

Recorded 2026-11-23 UTC, before final rebuilt-image tests. The frozen development source and its hash record remain unchanged; this correction applies to the final recipe source.

S8.2-7 asks: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?” Native package membership and a checksum captured after the factory build do not establish the original package receipt. The build can change bytes and permissions before capture. The original cloud image digest also cannot establish receipt of files modified by the build.

`B2/build/recorded_objects.py` now leaves `remains_as_received` unknown for native package members without an independently established receipt. Native installed package objects still use exact live package-manager identity/status. An exact installed artifact obtained through the finite testbed installer retains its validated receipt. If both origins exist, an exact validated receipt is sufficient; a native origin alone cannot manufacture it. A known absent package supplies no current membership.

The correction does not describe the post-build machine as an immutable image package merely because its declaration contains file hashes. That stronger provenance would require independent evidence that this computer was installed or updated as the identified final image.

Coverage matching now uses the origins already returned in the independent census snapshot. It no longer invokes another census while matching declaration claims. Derived-output matching uses the source and target states from that same snapshot, bound to the algorithm validated at admission and executed at activation; it does not reread live source files during matching. Within one census, native package observations are reused from the package-state snapshot rather than queried twice. These changes preserve the separation between collecting facts and matching declaration lines and avoid inconsistent duplicate package readings.

Expected final checks: native package objects can be covered while native file receipt remains `FACT_UNKNOWN`; exact finite-installer package artifacts remain covered; changing their bytes or removing their owning declaration must not become coverage. No closure is established by this source correction alone.
