# Independent review of the current c1 stored-object classification

## Scope

This review covered the 1,275 stored-object rows present in `part-1.tsv` at the start of review. It checked the first ten rows assigned by each homogeneous rule against their raw member paths, then examined 26 individually reasoned or suspicious rows in more detail. It did not inspect another classification or any adjudication material. The review is not an acceptance decision.

## Findings

### 1. Concrete unsupported decision: a password-history file was assumed to be passive

Row `a353d93e7cf56eb59ae5f136` (`/etc/security`, member `/etc/security/opasswd`) is `NOT` because the file allegedly only “preserves previous password hashes.” The allowed evidence establishes only the path; it does not establish whether password-history enforcement currently consults the file. If it does, removing the object changes which password-setting operation can be completed. The applicable literal rule would then be S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.” S2.2-6, “records of the past—logs, history;”, does not by itself resolve an object whose retained history enforces a current restriction.

Proposed correction: `UNKNOWN` under S3-2 on the current evidence. Change it to `MUST`, citing S2.2-1 and S2.2-2, only if evidence establishes that the file currently participates in password-reuse enforcement.

### 2. The MIME homogeneous rule applies an unsupported cache premise to source definition files

Rows `4aba607ff59c3ee376310758`, `4ff815d792c6f07c0e70cdd2`, `a1bc9af2c8b24e04764d16e0`, `2c84f6f7d6b126564d10c278`, `946c59a84dd618138088be86`, `a3a29542d4b538e850acb99b`, `7d4c3c7f666b1008ee71489d`, `a57811114eec1362d29f52a8`, `f4785d34ecdd63e5d9727007`, `f9b368f6ebd3f6e3a358d20e`, `b4719b4d765ff90d4af34b9b`, `1ac91867a5ba1ff1225fe23c`, and `e5ab7eeee3f7f8114537bfea` are the `/usr/share/mime/{application,audio,chemical,font,image,inode,message,model,multipart,text,video,x-content,x-epoc}` groups. Their raw members are XML MIME definitions, for example `application/pdf.xml` and `audio/mpeg.xml`. The shared rationale calls all of them “generated cache-like data” and invokes S2.2-5, but neither the member lists nor the cited build record establishes that these XML definitions are generated or regenerable caches. The fact that the parent `/usr/share/mime` row also contains `mime.cache` does not turn every child XML definition into a cache.

S2.2-5 says only: “cache: after it is removed, the computer does the same, only more slowly;”. The current evidence does not show that removing the XML definitions leaves the same file-recognition behavior. Therefore the `HOLE` result and its claimed S2.2-5 conflict are unsupported for these thirteen rows.

Proposed correction: remove these rows from the `mime-generated` rule and classify them from established removal behavior. With only the current member-path evidence, use `UNKNOWN` under S3-2; do not claim a cache/code or cache/capability conflict without evidence that the cache definition applies.

### 3. Two catalog rows use the one-program exception without establishing the required one-program fact

Row `3361d2f0b3bef050bd3ddbc2` (`/etc/sgml/catalog`) is `NOT` because catalog values allegedly “act within document processing.” Row `f3a65b5de1d9ef2e9b757c12` (`/etc/xml`, active catalogs plus `.old` copies) is also `NOT` because the catalogs allegedly act within a parser. S2.2-7 is narrower: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.” “Document processing” and “a parser” are categories, not evidence that each catalog is in force only inside one program. The raw member paths establish neither the consumers nor the removal effect.

Proposed correction: `UNKNOWN` for `/etc/sgml/catalog` unless its consumers and removal effect are evidenced. The `/etc/xml` group should at least separate active catalogs from `.old` historical copies; absent facts about the active files, `MIXED` with `UNKNOWN` active members and `NOT` old copies is supportable, while the current all-`NOT` decision is not.

## Homogeneous-rule check

The first ten examples of the Go build-cache, Mesa shader-cache, manual-page cache, shell-plugin-with-documents, Lisp source/bytecode, Python bytecode, retrieval/index cache, history, and MIME rules were checked against their raw members. No mislabeled member was found in the first eight groups beyond the evidence limitation described above. The MIME rule failed at its factual premise for every checked child group. The output contains no duplicate identifiers, and all 1,275 reviewed stored identifiers had one result row.

## Follow-up after correction

The MIME finding above is superseded. The Shared MIME-info specification explicitly lists `<MIME>/MEDIA/SUBTYPE.xml` among generated output, establishing the fact that the review found missing. The final MIME rationale no longer invokes S2.2-5; it cites S2.2-2 and S2.2-4 for the unresolved descriptive-database versus enabling-value readings.

The other two findings were corrected in the merged output. Row `a353d93e7cf56eb59ae5f136` is now `UNKNOWN` under S3-2 because the saved evidence does not establish whether the password-history file is operative. Row `3361d2f0b3bef050bd3ddbc2` is now `UNKNOWN` under S3-2 because its exact catalog entries and consumers are not captured. Row `f3a65b5de1d9ef2e9b757c12` is now `MIXED`: `.old` copies are `NOT` historical records and active catalogs are `UNKNOWN`.
