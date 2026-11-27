/* SPDX-License-Identifier: MIT */
/* Brought program of the cases: writes "executed" to $CASE_MARKER when it runs. */
#include <stdio.h>
#include <stdlib.h>
int main(void) {
    const char *m = getenv("CASE_MARKER");
    FILE *f = m ? fopen(m, "w") : NULL;
    if (!f) return 2;
    fputs("executed\n", f);
    return fclose(f) ? 2 : 0;
}
