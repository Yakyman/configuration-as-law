# Review of the current Flatcar classification

The review found two material issue families. The current table has exact input-ID coverage, and every `MIXED` reason maps every member exactly once with no duplicate or out-of-range member indices.

## 1. Bootloader value lists are incorrectly classified as `HOLE`

Affected IDs:

`flatcar-e5869975107dd1606ec51809`, `flatcar-1d509ff72f6ebda06a74f24b`, `flatcar-a57831f044e17b543418e523`, `flatcar-7904e536689dfb4920c065e2`, `flatcar-85dcb992af130d2188c69228`, `flatcar-0a3e3cfe3ac4624ab107909d`, `flatcar-0e6c4297e1c7ee27ea640213`, `flatcar-cbb532e843582afa0c475968`, `flatcar-772bb06922e0fe319ced9341`, `flatcar-5c299521082131f80720b170`, `flatcar-6cf96cf62a5c025915a5304f`, `flatcar-169971c66f71b58b99c4405f`, `flatcar-835444a1e99d596b1bb77428`, `flatcar-452c72fd408533fcf34dd6a6`, `flatcar-77796baf3bc41ca5cf2c1fd9`, `flatcar-87d65840836e70d225b4fbf3`, `flatcar-974618a7c5fc08b7d44dc4e8`, `flatcar-a38dc4a119724473b97a7092`.

The rows and notes establish that these files contain values, not code, and say that the values “configure only [the bootloader] internally.” That factual finding satisfies the literal exemption in S2.2-7: “settings that are in force only inside one program ... need not be recorded.” S2.2-13 confirms that a value-only file is a setting; it does not create a competing requirement. The stated counterpoint, that the values govern the program's available capabilities, only restates the general behavioral-dependence rule in S2.2-1. Treating that ordinary consequence as a conflict would make S2.2-7 ineffective for any setting, including its published examples. On the current factual record these rows are `NOT`, not `HOLE`.

## 2. Driver-link `MUST` decisions claim a removal effect not established by the evidence

Affected IDs:

`flatcar-f680f2ced5cbbbb98c0f7e6e`, `flatcar-4ff7c0363c7bcaed36cee8c4`, `flatcar-3ec540466dde50c24e4e6a58`, `flatcar-f0515208c7470ebde5ef43b0`, `flatcar-bafb06ed0c03f82136071d0b`, `flatcar-dc571710b764793b61bfe463`, `flatcar-1f9163a7e2f94b85174294f1`, `flatcar-44bd92356b91b0b47cf8277a`, `flatcar-6861c749394b4335ae375e11`, `flatcar-3d0421dd3fe9ece92d5747d4`, `flatcar-1128670a5a25b7b1f8a632e0`, `flatcar-2e4abf014c9f5c027acc6433`, `flatcar-56a7db23ffbc04132a032ab1`, `flatcar-e9f177838b9a761d15cf452b`, `flatcar-5d9d484c902a569329c93c72`, `flatcar-ccb25ba2988673ebec8ccad2`, `flatcar-b605afe2f102578e85a9a076`, `flatcar-89d438992a2c46b8ea08996f`, `flatcar-5ae1a90eca7d132edec44169`, `flatcar-d02f30a66be6bd18bdc29171`, `flatcar-57373642645c995183799934`, `flatcar-be30a9cb642c5adc4dd18aa2`, `flatcar-bc8c732576c2b08f4d089545`, `flatcar-38e53d99da881f7e44f46688`, `flatcar-6bf1b86ad3b604206c315930`, `flatcar-075f446569106f7b41ed3158`, `flatcar-541edec51d6ad87c14a2bfdd`, `flatcar-df01bcfe563b4d2806ab81ed`, `flatcar-130d22dd45e97d035accd37e`.

The saved inventory proves that each object is a symbolic link exposing the identity of an already bound driver. The cited documentation establishes how a consumer reads that identity and separately explains driver binding; it does not establish that removal of the link as an object removes or changes the binding. The notes expressly avoid claiming that removal unloads code and instead rely only on loss of userspace discovery. That is loss of exposed information, which fits S2.2-4's content exception: the machine otherwise does and can do the same, and only the content is unavailable. If the virtual link cannot be removed independently and the intended object is instead the underlying binding, the saved evidence does not establish the effect of that different removal and S3-2 requires `UNKNOWN`. Either way, `MUST` is not supported by the recorded evidence.

## History and state cases checked

No material issue was found for `flatcar-14a05bb2f57c924ebf089310`, `flatcar-cca2563c4725e464a155518c`, `flatcar-02e4eb0675d16e40996fe023`, `flatcar-e6b07d2a5d52c2937f4ea625`, or members 8 and 9 of `flatcar-d11cff71d6ec6e8beafbf4e9`. The saved documentation establishes both that each object records a past event or value and that its retained state changes a future operation. S2.2-6 therefore says `NOT`, while S2.2-1 and S2.2-2 say `MUST`; the text supplies no precedence. Section 2.5 excludes choices about how a design treats state, but it does not say that a state object is outside the Section 2.2 removal test. `HOLE` is supported for these direct two-way cases.

## Closure after corrections

Both findings are resolved in the current main table. All 18 bootloader value-list rows are now `NOT`, consistently applying S2.2-7 to values established as internal to one program. All 29 driver-link rows are now `UNKNOWN` under S3-2. This is preferable to asserting `NOT`: the inventory and documentation identify metadata links, but do not establish whether actual consumers use them operationally or merely display their contents. The revised wording states exactly that evidentiary limit and no longer conflates the links with driver code or the underlying binding. No material objection remains within the review scope.
