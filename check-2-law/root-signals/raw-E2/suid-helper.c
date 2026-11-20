#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
int main(int argc,char **argv){
 if(argc != 2 || strspn(argv[1],"abcdefghijklmnopqrstuvwxyz0123456789_-") != strlen(argv[1])) return 64;
 fprintf(stderr,"SUID_HELPER ruid=%d euid=%d rgid=%d egid=%d\n",getuid(),geteuid(),getgid(),getegid());
 /* Preserve real UID: the probe records the actual setuid transition. */
 execl("/usr/bin/python3","python3","/usr/local/lib/e2/probe.py",argv[1],(char*)0);
 perror("execl");return 1;
}
