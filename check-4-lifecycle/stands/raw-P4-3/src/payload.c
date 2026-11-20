#define _GNU_SOURCE
#include <sys/random.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#ifndef STATE_KEY
#define STATE_KEY "local-alice-cache"
#endif
#ifndef PROGRAM
#define PROGRAM "primary"
#endif
/* Fixed operational location: no HOME/XDG/argv path supplied by caller. */
static const char *path="/var/lib/cal/active/" STATE_KEY "/operational.bin";
int main(int argc,char **argv) {
 uint64_t table[128], result=0;
 if(argc!=2 || (strcmp(argv[1],"create") && strcmp(argv[1],"read")))return 2;
 if(!strcmp(argv[1],"create")) {
  if(getrandom(table,sizeof(table),0)!=sizeof(table)){perror("getrandom");return 3;}
  int fd=open(path,O_WRONLY|O_CREAT|O_EXCL|O_CLOEXEC,0600);
  if(fd<0){perror("create");return 4;}
  if(write(fd,table,sizeof(table))!=sizeof(table)||fsync(fd)){perror("write/fsync");close(fd);return 5;}
  close(fd);
 }
 int fd=open(path,O_RDONLY|O_CLOEXEC);
 if(fd<0){perror("read-open");return 6;}
 struct stat st;if(fstat(fd,&st)||read(fd,table,sizeof(table))!=sizeof(table)){perror("read");close(fd);return 7;}
 for(unsigned i=0;i<128;i++)result=(result*UINT64_C(1099511628211))^table[(i*37)%128];
 close(fd);
 char exe[4096]={0};readlink("/proc/self/exe",exe,sizeof(exe)-1);
 printf("{\"program\":\"%s\",\"operation\":\"%s\",\"pid\":%d,\"uid\":%d,\"executable\":\"%s\",\"path\":\"%s\",\"dev\":%lu,\"ino\":%lu,\"nlink\":%lu,\"size\":%lu,\"lookup\":\"%016lx\"}\n",PROGRAM,argv[1],getpid(),getuid(),exe,path,(unsigned long)st.st_dev,(unsigned long)st.st_ino,(unsigned long)st.st_nlink,(unsigned long)st.st_size,(unsigned long)result);
 return 0;
}
