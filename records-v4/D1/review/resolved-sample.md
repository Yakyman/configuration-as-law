# Resolved-row sample review

Seed: `112340`. Method: `random.Random(112340).sample(pool, 40)`, where pool is all verdicts beginning `RESOLVED:` sorted by id. Pool size: 5994. Draw order and per-row evidence are preserved in `resolved-sample.tsv`.

Result: 38 verdicts supported; 2 verdicts fail as homogeneous decisions for mixed buckets. Both failed rows were tested as gap candidates and REFUTED: their members are decided by the fixed order and literal sentences. CONFIRMED 0; FACT-WRONG 0; OUTSIDE 0; FACT_UNKNOWN 0. This audits row verdicts as well as their explanatory notes; neither mixed-row note cures its bucket-wide RECORD verdict.

## Candidate 1: Mixed product-file bucket

`microos-0de7d07fa699fb469d565850` (`/.snapshots/1/snapshot/etc/products.d`): adjudication itself says one member is unchanged packaged MicroOS.prod and one is a generated baseproduct link. The first is installed package content, the second program-created state. REFUTED as a text gap; the RECORD label loses the first member.

S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”

S8.2-8: “Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.”

S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

The package member satisfies Q1. The generated noncode link reaches Q4. Evidence: `D1/adjudication/raw/microos-members.tsv` entries for this id; its member TSV under `D1/in/raw/microos/members/`; its adjudication note.

## Candidate 2: Mixed boot-theme bucket

`microos-1a6267884f7ab2f53a5d9b6a` (`/boot/grub2/themes/openSUSE`): twelve noncode members are program-created copies, while activate-theme is executable copied code. REFUTED as a text gap; the RECORD label loses that program.

S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”

S8.2-10: “Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.”

S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

S8.2-15: “Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”

The copied executable satisfies Q2 and has source-line coverage. The noncode copies reach Q4. Evidence: `D1/in/raw/microos/members/1a6267884f7ab2f53a5d9b6a.tsv`; full-digest source comparison described in `D1/adjudication/parts/l1-microos.facts.md`; adjudication note explicitly identifying the program member.

No confirmed candidate requires an extent set. Existing cards are not multiplied by these two aggregation errors.

## Drawn ids

1. `microos-9a780ede31bf92dca65d7be4`
2. `microos-4c8d2fcd40a5e71cec9c176a`
3. `microos-24566bd8590b09840306e65a`
4. `alma-79bd7bbfa908005fe50c3529`
5. `microos-476f86fc6c4fb2ddb7fa5612`
6. `microos-a80457a27b7a3e0f5c1c276e`
7. `microos-791c769aebf8943bb96eacc0`
8. `microos-40bd9f6265012d0798970c35`
9. `microos-b53aca063cb71552c76ccd12`
10. `microos-0de7d07fa699fb469d565850`
11. `microos-1a6267884f7ab2f53a5d9b6a`
12. `microos-14aeaca184393fc4deaacce6`
13. `alma-fa7a5bfbef21af1d6bd587ab`
14. `microos-f18fe034f10ef27e358e9d7a`
15. `microos-e66e8b9327d8acfeb4c17ee9`
16. `microos-a1e73bccf1a4585107d323ee`
17. `microos-fea15663186a6ea1a1e4f72f`
18. `microos-258bb029047f178b10c4ab55`
19. `microos-b7732f88b15138c77ebd00fd`
20. `microos-7737c101a0ca12a936b3f18a`
21. `microos-0eb3832b3580e8fb7d9d6d57`
22. `void-c62ebee38bad9fd878b1ba0f`
23. `microos-a43ce92bd09659903332805b`
24. `microos-53db5462f18daecbf746e3e7`
25. `microos-ecd88ef82d1259e72e09f5ba`
26. `microos-547ad18f8d788441f8974695`
27. `microos-c1cc4875671392e967cf9dcb`
28. `void-550f65f7231516ef366c90b4`
29. `microos-503a602a046ec2bfd0de28e3`
30. `void-52743bf71ba6e8960449ad93`
31. `microos-76caa4c92d53456d839f830b`
32. `alma-8ad26fd1c760c7fcf153b88e`
33. `microos-2376bf40a5592a919973a1f6`
34. `microos-8ef8410d65d891da2d8c2c36`
35. `microos-230864c607d1cffde69583f3`
36. `microos-7498ba233df8431e0868598a`
37. `microos-280f9455d4cb4c7bc4f5367a`
38. `alma-c36571003df52f1a9cdb7527`
39. `microos-6fd680f06a29fef2bf7830e5`
40. `microos-da42e410a83fe28b5c8d9d84`
