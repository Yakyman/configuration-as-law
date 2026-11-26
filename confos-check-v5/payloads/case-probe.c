/* SPDX-License-Identifier: MIT
 * Deliberately ordinary reader/installer: no declaration checks in this code.
 * Enforcement must come from the operating system, not from this test payload.
 */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <errno.h>
#ifndef CASE_SHELL
#define CASE_SHELL "/bin/sh"
#endif
#ifndef CASE_FETCH
#define CASE_FETCH "curl"
#endif
static int status(pid_t pid) {
    int s;
    while (waitpid(pid, &s, 0) < 0) { if (errno != EINTR) return 125; }
    return WIFEXITED(s) ? WEXITSTATUS(s) : 128 + WTERMSIG(s);
}
static int read_file(const char *name, int execute) {
    FILE *f=fopen(name,"rb"); char *buf; size_t n;
    if (!f) { perror(name); return 2; }
    buf=malloc(65537);
    if (!buf) { fclose(f); return 2; }
    n=fread(buf,1,65536,f);
    if (ferror(f) || !feof(f)) { fclose(f); free(buf); return 2; }
    fclose(f); buf[n]=0;
    if (!execute) { fwrite(buf,1,n,stdout); free(buf); return 0; }
    pid_t pid=fork();
    if (!pid) { execl(CASE_SHELL,"sh","-c",buf,(char *)0); _exit(126); }
    free(buf); return pid<0 ? 125 : status(pid);
}
static int fetch_install(const char *url,const char *dest) {
    pid_t pid=fork();
    if (!pid) {
#ifdef CASE_FETCH_WGET
        execlp(CASE_FETCH,CASE_FETCH,"-O",dest,url,(char *)0);
#else
        execlp(CASE_FETCH,CASE_FETCH,"-fsSLo",dest,url,(char *)0);
#endif
        _exit(126);
    }
    if (pid<0) return 125;
    int rc=status(pid); if (rc) return rc;
    if (chmod(dest,0755)<0) { perror(dest); return 2; }
    pid=fork();
    if (!pid) { execl(dest,dest,(char *)0); _exit(126); }
    return pid<0 ? 125 : status(pid);
}
static int listen_port(const char *text) {
    char *end; long port=strtol(text,&end,10);
    if (*end || port<1024 || port>65535) return 2;
    int fd=socket(AF_INET,SOCK_STREAM,0); if(fd<0) return 2;
    struct sockaddr_in a; memset(&a,0,sizeof a); a.sin_family=AF_INET;
    a.sin_addr.s_addr=htonl(INADDR_LOOPBACK); a.sin_port=htons((unsigned short)port);
    if(bind(fd,(struct sockaddr *)&a,sizeof a)<0 || listen(fd,1)<0) { perror("listen"); close(fd); return 2; }
    puts("listening"); fflush(stdout); sleep(30); close(fd); return 0;
}
int main(int argc,char **argv) {
    if(argc==3 && !strcmp(argv[1],"read")) return read_file(argv[2],1);
    if(argc==3 && !strcmp(argv[1],"values")) return read_file(argv[2],0);
    if(argc==4 && !strcmp(argv[1],"fetch-install")) return fetch_install(argv[2],argv[3]);
    if(argc==3 && !strcmp(argv[1],"listen")) return listen_port(argv[2]);
    if(argc==2 && !strcmp(argv[1],"control")) { puts("probe-control"); return 0; }
    fputs("usage: case-probe read|values FILE; fetch-install URL DEST; listen PORT; control\n",stderr);
    return 2;
}
