# Unresolved recording question

DNF records “installed by group” separately from “user” and “dependency”.
Section 9.2 asks whether each package was installed explicitly or as a dependency
but does not state a translation for this manager category. The collector
preserves native_reason=group and reason=unknown. A translation requires an
argument from the fixed text or an author decision; it is not guessed to meet
the readiness threshold. The numerical rehearsal reduction reports 261 such
records, without exposing their identities.

Follow-up before FX3: positive saved selection linkage may settle a narrower
case without translating GROUP alone. The adapter now preserves the group
reason and records explicit selection through a native USER-marked installed
group/environment, only where the native history explicitly links that package
as an installed member. GROUP records without that linkage remain unknown.
Independent review of this selected-set expansion is requested.

Independent review rejected that expansion as a way to establish individual
package reason. Selection provenance is retained separately; GROUP is unknown.
The rejected mapping was removed before the FX3 collector began.
