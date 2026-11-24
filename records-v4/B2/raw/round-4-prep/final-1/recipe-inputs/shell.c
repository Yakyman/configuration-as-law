#define _GNU_SOURCE
/* Ordinary command-shell entry. Kernel policy belongs to the declaration.
 * This does not try to classify text flowing through a pipe as code or data. */
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/file.h>
#include <sys/syscall.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (getuid()!=1000 || geteuid()!=1000) {
        fputs("REFUSED ordinary identity required\n",stderr); return 126;
    }
    if (access("/run/stand-ready",F_OK)) {
        fputs("REFUSED declaration replay incomplete\n",stderr); return 126;
    }
    int lock=open("/var/lib/stand/apply.lock",O_RDONLY|O_CLOEXEC);
    if (lock<0 || flock(lock,LOCK_SH|LOCK_NB)) {
        fputs("REFUSED application in progress\n",stderr); return 126;
    }
    if (!access("/var/lib/stand/pending.json",F_OK) || errno!=ENOENT) {
        fputs("REFUSED pending declaration recovery\n",stderr); return 126;
    }
    char *command=NULL;
    if (argc==3 && !strcmp(argv[1],"-c")) command=argv[2];
    else if (argc!=1) { fputs("Usage: stand-shell [-c command]\n",stderr); return 64; }
    clearenv();
    setenv("PATH","/usr/local/bin:/usr/bin:/usr/sbin",1);
    setenv("HOME","/home/stand",1);
    setenv("USER","stand",1);
    setenv("LOGNAME","stand",1);
    setenv("LANG","C.UTF-8",1);
    setenv("TERM","xterm",1);
    /* No command history is promoted to the primary declaration. */
    setenv("HISTFILE","/dev/null",1);
    if (chdir("/home/stand") || syscall(SYS_close_range,3,~0U,0)) {
        perror("shell setup"); return 126;
    }
    if (command) execl("/usr/bin/bash","bash","--noprofile","--norc","-c",command,NULL);
    else execl("/usr/bin/bash","bash","--noprofile","--norc",NULL);
    perror("recorded shell"); return 126;
}
