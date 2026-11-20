| Mechanism / run | Mutation errno | D | G | O0 | O1 | F | U | R | V | Reapply / revoke ACK |
|---|---:|---|---|---|---|---|---|---|---|---|
| bq-absent | 0 | ENOENT | ENOENT | A | A | A | A | A | EACCES | True / True |
| bq-atomic | 0 | EACCES | A | B | B | B | B | B | EACCES | True / True |
| bq-directory | 0 | EACCES | A | B | B | B | B | B | EACCES | True / True |
| bq-existing-r1 | 0 | EACCES | A | A | A | A | A | A | EACCES | True / True |
| bq-recreate | 0 | EACCES | A | A | A | A | A | A | EACCES | True / True |
| bq-rename | 0 | EACCES | A | B | B | B | B | B | EACCES | True / True |
| x3-absent | 0 | ENOENT | ENOENT | EACCES | EACCES | EACCES | A | A | EACCES | True / True |
| x3-atomic | 16 | EACCES | A | EACCES | A | A | A | A | EACCES | True / True |
| x3-directory | 0 | EACCES | A | EACCES | EACCES | EACCES | B | EACCES | EACCES | False / False |
| x3-directory-replay | 0 | EACCES | A | EACCES | EACCES | EACCES | B | EACCES | EACCES | False / False |
| x3-existing | 0 | EACCES | A | EACCES | A | A | A | A | EACCES | True / True |
| x3-recreate | 16 | EACCES | A | EACCES | A | A | A | A | EACCES | True / True |
| x3-rename | 16 | EACCES | A | EACCES | A | A | A | A | EACCES | True / True |
