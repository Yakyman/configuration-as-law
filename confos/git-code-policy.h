/* Code-valued Git configuration. Repository metadata remains a data input. */
#include "confos-code-policy.h"

static int confos_git_code_key(const char *key, const char *value)
{
  static const char *exact[] = {
    "core.editor", "core.pager", "core.sshcommand", "core.gitproxy",
    "core.askpass", "core.hookspath", "core.fsmonitor", "sequence.editor",
    "interactive.difffilter", "diff.external", "gpg.program", "uploadpack.packobjectshook",
    NULL
  };
  static const char *prefix[] = {
    "alias.", "pager.", "filter.", "difftool.", "mergetool.", "guitool.",
    "browser.", "man.", "tar.", "credential.", NULL
  };
  const char *last = strrchr(key, '.');
  int i;
  for (i = 0; exact[i]; i++) if (!strcasecmp(key, exact[i])) return 1;
  for (i = 0; prefix[i]; i++)
    if (!strncasecmp(key, prefix[i], strlen(prefix[i]))) return 1;
  if (!last) return 0;
  if (!strncasecmp(key, "diff.", 5) &&
      (!strcasecmp(last, ".command") || !strcasecmp(last, ".textconv"))) return 1;
  if (!strncasecmp(key, "merge.", 6) && !strcasecmp(last, ".driver")) return 1;
  if (!strncasecmp(key, "gpg.", 4) && !strcasecmp(last, ".program")) return 1;
  if (!strncasecmp(key, "remote.", 7)) {
    if (!strcasecmp(last, ".uploadpack") || !strcasecmp(last, ".receivepack") ||
        !strcasecmp(last, ".vcs")) return 1;
    if ((!strcasecmp(last, ".url") || !strcasecmp(last, ".pushurl")) &&
        value && strstr(value, "::")) return 1;
  }
  if (!strncasecmp(key, "url.", 4) && strstr(key + 4, "::")) return 1;
  if (!strcasecmp(key, "sendemail.smtpserver") && value && value[0] == '/') return 1;
  return 0;
}
