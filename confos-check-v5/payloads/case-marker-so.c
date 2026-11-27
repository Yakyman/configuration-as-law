/* SPDX-License-Identifier: MIT */
/* Library of the cases: writes "executed" to $CASE_MARKER when it is loaded. */
#include <stdio.h>
#include <stdlib.h>
int plugin_is_GPL_compatible;
int plugin_init(void) { return 0; }
__attribute__((constructor)) static void mark(void) {
    const char *m = getenv("CASE_MARKER");
    FILE *f = m ? fopen(m, "w") : NULL;
    if (f) { fputs("executed\n", f); fclose(f); }
}
