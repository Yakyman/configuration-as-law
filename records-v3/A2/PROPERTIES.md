# Properties, consequences and all four indicators: attack record

Status: exploratory work beyond the published plan. Recorded: 2026-11-22 04:40:02 UTC.
Method: sources and literal reasoning only; no virtual machines or execution probes. Primary-source extracts are in `raw/properties/SOURCES.md`. This sweep does not ask whether a system can close an installation or launch channel. It excludes the three case families reserved to other work.

Outcome key: 0 = proposed counterexample to the text; 1 = this particular attack was refuted by the text; ? = a stronger claim remains unsupported. A 1 below is not a proof of the whole property. Candidate cards are in `PROPERTY-CANDIDATES.md`; final acceptance remains independent.

## Coverage table

| Required target | Attack examined | Result and controlling reason |
|---|---|---|
| P1 | Required object present after removing its only declaring line | 1 for alleged contradiction: P1 expressly forbids it, so this would be nonconformance, not inconsistency. Whether it can be prevented is reserved channel work. |
| P1 | Running but disabled service, distinct from its recorded executable | ? for a separate conflict: E5 establishes distinct runtime activity and enablement, but the definition and Removal can impose different strengths without being inconsistent; no card. |
| P2 | A declaration asks for mutually inconsistent states | 1: no sentence promises a successful application of every possible declaration; application can fail. |
| P2 | Successful report followed by loss of required state at power cut | 1: S3-5 explicitly calls this a P2 failure; no contradictory verdict. |
| P2 | A recorded line requires that a program not run | 1: the phrase as its line requires plus S2.1-4 controls; do not invent an unconditional running obligation. |
| P2 | Voluntarily recorded exempt content lacks its own in-force branch | 1 for an independent card: S2.1-4 lets the line state its required state, and treatment of data is outside the definition. |
| P4 | A program is both an editor and a package manager | 0 candidate P-C1: S3-6 includes the program and S3-7 excludes it. The contradictory tool classification precedes any particular channel action. |
| P4 | Automatic changes to temporary settings consume a declared one-time operation | 1 for unavoidable conflict: a declaration can state temporal requirements; S2.5-3 does not restrict its form. No claim about practical enforcement. |
| Understanding | A declaration leaves actual program activity unspecified | 1: S2.1-4 expressly says present running state does not matter unless required by the line. |
| Understanding | Unknown content or program state cannot be read from the declaration | 1: S2.1-3 scopes in force to objects that must be recorded; treatment of content/state is excluded by S2.5-1. |
| Understanding | No application has yet succeeded | 1 for a global contradiction: the properties' scope is after completed application; no assertion of a successfully conforming initial machine is supplied. |
| Understanding | A static line relies on external documented defaults | ? for conflict: Understanding may describe which objects are in force rather than every unspecified value; cannot establish opposite decisions without a scope assumption. No card. |
| Reproducibility | Boot-order description falls outside both unambiguity branches | 0 candidate P-C2, subject to independent review of whether rule is broad enough to subsume boot order. |
| Reproducibility | Installed package bytes are pinned but accumulated application data differ | 1: transferred accumulated state and treatment of program state are excluded; result described in the declaration need not include that state. |
| Reproducibility | Account password is omitted although S3-10 demands every value | 1 for contradiction: need not record is permission, not a prohibition; unambiguity may impose an additional condition on a particular declaration. Any broader conflict requires an interpretation of value. |
| Removal | A program's files remain after its declaring line is removed | 1: remains are explicitly outside definition; the asserted obligation concerns in force, including ability to start, not physical erasure. |
| Removal | Another remaining line requires the same program or service | 1: S2.4-4 expressly permits remaining lines to cover the contribution. |
| Removal | Disabled service keeps running | ? for conflict: E5 shows the states differ, but the extra explicit Removal requirement can constrain this case without contradicting P1/P2. No unavoidable conflict established. |
| Indicator: must record | Documentation establishes behavior but Section 2.2 classifications collide | 0 if a collision survives the pair sweep: S3-1 supplies evidence methods, not precedence; S3-2 only addresses unknown behavior. Handed to pair sweep, no duplicate card here. |
| Indicator: declaration in force/completed application | Failed application modifies some state | 1: S3-4 retains the prior declaration; nonconformance is then an ordinary property failure, not two definitions of the declaration in force. |
| Indicator: declaration in force/completed application | No success report within one hour, then a late success report | 1 for claimed forced contradiction: S3-4 gives the old declaration at timeout and S3-3 supplies a newer successful application at the later report. A permanent freeze is not stated. |
| Indicator: declaration in force/completed application | First application fails, so no previous successful declaration exists | ? for assessment before any completed application; no card because S2.3-1 excludes that phase from the properties. |
| Indicator: built-in tool | Documented editor package manager | 0 candidate P-C1, including the explicit S3-8 outcome. |
| Indicator: built-in tool | Documentation does not state purpose | 1: S3-8 explicitly supplies ?. This is an assigned result, not a missing indicator answer. |
| Indicator: unambiguous line | Installation pins unique content | 1 for a direct missing test: S3-9 gives the criterion. A source name alone does not establish unique content. |
| Indicator: unambiguous line | Account, service or rule omits an unfixed value | 1: S3-10 does not call the line unambiguous. |
| Indicator: unambiguous line | Existing boot-order value changes without installation | 0 candidate P-C2: no explicit applicable branch; the same gap may extend to saved networks and keys. |

## Refutation notes

The table deliberately rejects failures specific to an implementation. A failed application, incorrect success report, unresolved restart state, or inability to fulfill contradictory lines does not by itself establish that the definitions contradict one another. The text is allowed to impose a strict property that an existing system fails.

Neither P-C1 nor P-C2 requires a privileged bypass: P-C1 classifies a documented program before any action, and P-C2 classifies a declaration line for a changeable object. No code entered into a shell or interpreter, data executed as code by a recorded program, or declaration algorithm reading machine state is used as a card.

Service enablement and running state warrant attention, but their distinction alone is not a contradiction. The text can consistently demand a stronger post-removal condition than mere absence from P1. Similarly, an exempt item being optionally recorded does not establish a ban on its presence in the declaration.

## Controlling sentences used in rejected attacks

- S2.1-3: “**In force**—for an object that must be recorded (Section 2.2): a program or code runs or can be started, a service is enabled, an account exists, a rule is applied, a saved network or a login key is available to the program that uses it, firmware or a boot order is set on the device.”
- S2.1-4: “For a recorded object, its line states the required state; whether a recorded program is running at a given moment does not matter unless its line requires it.”
- S2.3-1: “The properties concern the computer after a completed application of the declaration, provided there was no breaking.”
- S2.3-4: “**P1. Completeness.** Everything that must be recorded under Section 2.2 and is in force on the computer is recorded.”
- S2.3-5: “**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.”
- S2.3-6: “**P4. Law.** The system provides no path for changing, past the declaration, anything that must be recorded.”
- S2.4-1: “**Understanding.** If there was no breaking, what is in force on the computer can be read from the declaration alone, without inspecting the computer.”
- S2.4-2: “**Reproducibility.** The same declaration on another computer yields exactly the result described in it, provided the description is unambiguous.”
- S2.4-4: “**Removal.** After application of a declaration from which a line has been removed, nothing the line contributed is in force unless the remaining lines cover it: the program is stopped and cannot be started, the service does not run and is not enabled, the rule is not in force.”
- S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”
- S2.5-3: “Nor is the form of the declaration part of the definition: it may be a list or an algorithm that computes what is recorded.”
- S3-1: “**Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.”
- S3-2: “If what the object does remains unknown, the case yields ?.”
- S3-3: “**Declaration in force and completed application.** The declaration in force is the declaration of the last application that the system has reported as successful; that report completes the application.”
- S3-4: “If the system reports an application as failed, or gives no report within one hour, the previous declaration stays in force.”
- S3-5: “The properties are checked against the declaration in force, including after an immediate power cut right after the success report and a new boot; a state that then differs from the declaration reported as applied is a failure of P2.”
- S3-8: “If a program’s documentation does not state its purpose, the case yields ?; if it does and this indicator still does not decide whether the program is a built-in tool, the case is a counterexample to the definitions and yields 0.”
- S3-9: “**Unambiguous line.** A line that installs something is unambiguous when it states the version and the source so that the content to be installed is uniquely determined, for example by a checksum.”
- S3-10: “A line for an account, a service or a rule is unambiguous when every value of the object is either stated in the line or fixed by the system as a documented default.”

## Provisional result

Two distinct indicator candidates survive this sweep's initial self-refutation; P-C1 is stronger. No independent unavoidable conflict among P1, P2, P4, Understanding and Removal was established beyond the ambiguous predicates they use. No result is claimed for implementation feasibility or the published checks.
