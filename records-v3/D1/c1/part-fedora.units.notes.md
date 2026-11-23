# Service and timer classification

Scope: exactly 838 rows of kinds L1:service, L1:timer, L1:unit-file, L1:user-service, L1:user-timer, and L1:user-unit-file in the supplied part. All represented units have service or timer suffixes. Classification concerns the represented service, timer, or unit definition, not the inventory text as a historical document. No removal was performed. No earlier classification was consulted.

## Deciding text

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

S3-2: “If what the object does remains unknown, the case yields ?.”

The relevant function is activation or supervision, rather than every operation performed by the activated executable. Service configurations affect separate processes. Their effects are not confined inside the service manager, so S2.2-7 does not exempt them. Disabled or static unit definitions still supply an activation capability; the test is not restricted to currently running services. Templates supply instantiated activation. Timers for cache creation or log rotation are schedulers, not caches or logs themselves.

## Documentation checked

- https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html: “A unit configuration file whose name ends in ".service" encodes information about a process controlled and supervised by systemd.” The same page explains parameterized service templates.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html: “For each timer file, a matching unit file must exist, describing the unit to activate when the timer elapses.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html: “Units can be aliased (have an alternative name), by creating a symlink from the new name to the existing name”. Alias names participate in activation and dependencies.
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html: “not-found” means “The unit file does not exist.” The documentation distinguishes loaded inactive units from missing definitions and explains enabled, disabled, static, indirect, alias, and generated states. Generated service definitions are implicitly enabled by their generator; generation alone does not make them a speed-only cache.

Local evidence: each input row points to a numbered raw listing line under D1/in/raw/fedora/raw/. The inspected files are 070-user-user-service.out, 071-user-user-timer.out, 072-user-user-unit-file.out, 073-service.out, 074-timer.out, and 075-unit-file.out. The input members field reproduces these listing lines. The public documentation supplies semantics of the observed type and state. No behavior is inferred from earlier inventory classification labels.

## Homogeneous rules and manual checks

The script part-fedora.units.rules.py applies the following mutually exclusive rules in order and flushes every appended row. Manual checks inspect the individual name, type, state, and, where present, description in the raw listing reproduced by members. They check whether the documented common activation function fits; they do not infer executable contents from names.

### Missing references: 25 NOT

Require not-found and inactive/dead in the listing. These entries name no present service definition or active process. The reference cannot contribute the activation capability of a nonexistent service. The represented absent service supplies no capability whose removal could change behavior, giving NOT under S2.2-1 and S2.2-2. This does not classify any referring dependency file or a hypothetical installed version of the service.

Ten inspected IDs, all explicitly not-found inactive dead:

- fedora-5bce747654431241a4d6bc20
- fedora-c4ba1e303a5b06a244a2c543
- fedora-ab84f6b9e1ecca8b4b1856b1
- fedora-23ade8bacea1099397d76aaa
- fedora-e7583a06ca8dfc7bcc4d7160
- fedora-24130668c2ebf98dc9f4044c
- fedora-044a62eb377fe1b5f6d7e42e
- fedora-80fb7cc958ad23682989d6e0
- fedora-73b6736a48ef2979375baf88
- fedora-59df04a65312698106bfa46a

### Aliases: 34 MUST

Require alias state. The name provides an alternate activation route. Removal loses activation through that name even if the canonical unit remains. S2.2-1 and S2.2-2 apply to that capability.

Ten inspected IDs, all explicitly alias state (the last is a timer; the others are services):

- fedora-f92d69422a90f003ac015874
- fedora-7cd81feb1d2fb5406b9249c7
- fedora-87cf507caf824ef3cf35c2a1
- fedora-03f1f55f3416f6012ccc8e20
- fedora-7e765dd0af40adb9e39cbbd9
- fedora-2cca1132663f2d2e49f5979e
- fedora-dae8f067d32a55e5fd79017d
- fedora-2ffadba1415671bd1377a609
- fedora-4ea2a9cf3345ef2c54842db0
- fedora-513c98e74b27b2c622b44332

### Non-alias timers: 30 MUST

Require timer suffix, either a listed timer with activation target or an installed timer unit file. Removal loses the defined scheduled activation. S2.2-1 and S2.2-2 apply even when its timer has no next deadline or is disabled.

Ten inspected IDs:

- fedora-c0bce46ab638fcb6c9e46ed8: scheduled greeting service activation.
- fedora-8d5f91d9f6cf286e5f87e057: enabled greeting timer definition.
- fedora-7dca37cb0ca3a8d59904101c: enabled temporary-file cleanup timer definition.
- fedora-ec10a3f2d2519412545f1958: scheduled anchor service activation.
- fedora-3a14403d9a02cffeee58c8a0: scheduled log rotation activation.
- fedora-d1955eb82588abebd52fd46b: disabled timer definition; activation remains definable.
- fedora-d23c67bac03e17e8a6a4b727: static timer template; supplies instances.
- fedora-8f622caccf1fdd031295ac69: disabled timer definition.
- fedora-f46f15409eeaf32abea9354b: enabled raid-check timer definition.
- fedora-3e479dbd339f437ef4e385a6: enabled anchor timer definition.

### Present non-alias services: 749 MUST

Require service suffix and either loaded state in the service listing or an installed unit-file listing with enabled, enabled-runtime, disabled, static, indirect, or generated state. These are activation/supervision definitions for separate processes. S2.2-1 and S2.2-2 require recording the supplied capability. The rule does not claim that a loaded inactive service is currently executing.

Ten inspected IDs:

- fedora-af780df7858da6b4e6b6bf49: loaded inactive greeting service.
- fedora-d60236de2dd55e421870952e: static service definition.
- fedora-b8578c1bee42b665078317c0: loaded inactive service; process activation definition present.
- fedora-39ebb2564c943b45b01d8ad9: loaded active running journal service.
- fedora-e7b7a4af481719edd89fa924: static service definition.
- fedora-c39b6bdb3f742383e8e9dd64: disabled service definition.
- fedora-12da29ca3a02120dce8ff699: static service definition.
- fedora-9a52e02b6c7ef113248b233b: static service definition.
- fedora-245444cddcb7003ef53b36b7: static service template, supplies instance definitions.
- fedora-bba51b40dc7e5e7653bec176: disabled service definition.

Additionally all five generated user service definitions were individually inspected: fedora-c9dbd9bdf1fc3c59975f7e12, fedora-b7cf28ddde9848c778fd6e05, fedora-854247fcecbb4e66fc8bfd9b, fedora-985d4a5a2683f835e235312b, and fedora-bb51b9533828b697b1ed77dd. Each is explicitly a generated autostart service. Each supplies process activation, so the same service rule fits. The evidence does not describe them as speed-only caches.

## Verification

The script verified exact identity and cardinality of the assigned input/output IDs, each once, and all decisions in the permitted vocabulary. All rows meet the 15-word function and 30-word reason limits. Result: 813 MUST, 25 NOT, 0 HOLE, 0 UNKNOWN, 0 MIXED.

Review correction: the 25 absent-service reasons now concern the represented absent service itself, not removal of its inventory listing. Decisions and counts remain unchanged.
