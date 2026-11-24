/* GNU make's checked stdin is represented by sealed anonymous memory, never
 * a mutable temporary pathname. Anonymous byte streams are data routes (R1);
 * copying a saved file into such a stream is not claimed as a closed route. */
#include "confos-code-file-policy.h"
#include <sys/mman.h>
#include <stdlib.h>
#include <stdio.h>

static int confos_make_fd_allowed(int fd)
{
  struct stat st;
  int seals = fcntl(fd, F_GET_SEALS);
  int required = F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL;
  if (seals >= 0 && (seals & required) == required
      && fstat(fd, &st) == 0 && st.st_nlink == 0)
    return 1;
  return confos_code_fd_allowed(fd);
}

static FILE *confos_make_stdin_open(char **name)
{
  int fd, output_fd;
  FILE *fp;
  char path[64];
  if (!confos_code_fd_allowed(fileno(stdin))) return NULL;
  fd = memfd_create("confos-make-stdin", MFD_ALLOW_SEALING);
  if (fd < 0) return NULL;
  output_fd = dup(fd);
  if (output_fd < 0) { close(fd); return NULL; }
  fp = fdopen(output_fd, "w+");
  if (!fp) { close(output_fd); close(fd); return NULL; }
  snprintf(path, sizeof path, "/proc/self/fd/%d", fd);
  *name = strdup(path);
  if (!*name) { fclose(fp); close(fd); return NULL; }
  /* fd stays open across make's re-exec. The sealed bytes cannot be changed. */
  return fp;
}

static int confos_make_stdin_finish(FILE *fp)
{
  if (fflush(fp) != 0) return -1;
  if (fcntl(fileno(fp), F_ADD_SEALS,
            F_SEAL_WRITE | F_SEAL_GROW | F_SEAL_SHRINK | F_SEAL_SEAL) < 0)
    return -1;
  return fclose(fp);
}
