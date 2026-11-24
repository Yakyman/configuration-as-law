/* ConfOS code-input policy, prototype 1. Included in code readers only.
 * fstatvfs checks the opened object, including /proc and /dev/fd aliases.
 * Never use this helper for ordinary data reads.
 */
#include <sys/stat.h>
#include <sys/statvfs.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

static int
confos_code_fd_allowed (int fd)
{
  struct stat st;
  struct statvfs fs;
  char profile[128];
  int pfd, saved_errno = errno;
  ssize_t n;

  /* The boot/application service runs outside the session profile. Its
   * staging interpreter must run the previously recorded build inputs.
   * This is kernel state, not a caller-controlled environment switch. */
  pfd = open ("/proc/self/attr/current", O_RDONLY | O_CLOEXEC);
  if (pfd < 0) goto denied;
  n = read (pfd, profile, sizeof profile);
  close (pfd);
  if ((n == 11 && memcmp (profile, "unconfined\n", 11) == 0)
      || (n == 10 && memcmp (profile, "unconfined", 10) == 0))
    { errno = saved_errno; return 1; }
  if (n <= 0) goto denied;
  if (fstat (fd, &st) != 0) goto denied;
  /* Typed input, pipes and process substitutions remain available. */
  if (!S_ISREG (st.st_mode))
    { errno = saved_errno; return 1; }
  if (fstatvfs (fd, &fs) != 0) goto denied;
  if ((fs.f_flag & ST_RDONLY) && !(fs.f_flag & ST_NOEXEC))
    { errno = saved_errno; return 1; }
denied:
  {
    static const char message[] = "ConfOS: Permission denied for saved code input\n";
    (void) write (2, message, sizeof message - 1);
  }
  errno = EACCES;
  return 0;
}
