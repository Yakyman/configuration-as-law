#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>
#include <stddef.h>
#include <stdint.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <sys/syscall.h>
#include <sys/stat.h>
#include <sys/file.h>
#include <sys/wait.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
#include <linux/landlock.h>
/* The image supplies this recorded runtime library; no development package needed. */
extern unsigned char *SHA256(const unsigned char *,size_t,unsigned char *);
static void fail(const char *s){dprintf(2,"REFUSED %s: %s\n",s,strerror(errno));exit(126);}
static void refuse(const char *s){dprintf(2,"REFUSED %s\n",s);exit(126);}
static void hashcheck(const char *path,const char *wanted){
 int fd=open(path,O_RDONLY|O_NOFOLLOW);if(fd<0)fail("recorded input");struct stat s;
 if(fstat(fd,&s)||!S_ISREG(s.st_mode)||s.st_uid|| (s.st_mode&0022))refuse("mutable input");
 void *p=mmap(0,s.st_size,PROT_READ,MAP_PRIVATE,fd,0);if(p==MAP_FAILED)fail("hash map");
 unsigned char digest[32];char hex[65];SHA256(p,s.st_size,digest);
 for(int i=0;i<32;i++)sprintf(hex+2*i,"%02x",digest[i]);
 munmap(p,s.st_size);close(fd);if(strcmp(hex,wanted))refuse("checksum mismatch");
}
static void readonly_closure(void){
 struct landlock_ruleset_attr rs={.handled_access_fs=LANDLOCK_ACCESS_FS_READ_FILE|LANDLOCK_ACCESS_FS_READ_DIR};
 int rules=syscall(SYS_landlock_create_ruleset,&rs,sizeof(rs),0);if(rules<0)fail("Landlock required");
 FILE *f=fopen("/etc/stand/read-closure","r");if(!f)fail("read closure");char *line=0;size_t n=0;
 while(getline(&line,&n,f)>0){line[strcspn(line,"\n")]=0;int fd=open(line,O_PATH|O_CLOEXEC);if(fd<0)fail("closure member");
  struct stat st;if(fstat(fd,&st))fail("closure stat");
  struct landlock_path_beneath_attr p={.parent_fd=fd,.allowed_access=S_ISDIR(st.st_mode)?LANDLOCK_ACCESS_FS_READ_DIR:LANDLOCK_ACCESS_FS_READ_FILE};
  if(syscall(SYS_landlock_add_rule,rules,LANDLOCK_RULE_PATH_BENEATH,&p,0))fail("Landlock rule");close(fd);
 }free(line);fclose(f);
 if(prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0)||syscall(SYS_landlock_restrict_self,rules,0))fail("Landlock restrict");close(rules);
}
static struct sock_filter filter[256];static int nf;
static void ins(unsigned short c,unsigned char t,unsigned char f,unsigned int k){filter[nf++]=(struct sock_filter){c,t,f,k};}
#define LD(off) ins(BPF_LD|BPF_W|BPF_ABS,0,0,off)
#define EQ(n,t,f) ins(BPF_JMP|BPF_JEQ|BPF_K,t,f,n)
#define RET(n) ins(BPF_RET|BPF_K,0,0,n)
static void deny_nr(int nr){EQ(nr,0,1);RET(SECCOMP_RET_ERRNO|EPERM);}
static void secure(int sealed){
 LD(offsetof(struct seccomp_data,arch));EQ(AUDIT_ARCH_X86_64,1,0);RET(SECCOMP_RET_KILL_PROCESS);
 LD(offsetof(struct seccomp_data,nr));ins(BPF_JMP|BPF_JGE|BPF_K,0,1,0x40000000);RET(SECCOMP_RET_ERRNO|EPERM);
 int denied[]={SYS_memfd_create,SYS_ptrace,SYS_process_vm_writev,SYS_process_vm_readv,SYS_pidfd_getfd,SYS_userfaultfd,SYS_unshare,SYS_setns,SYS_mount,SYS_umount2,SYS_pivot_root,SYS_chroot,SYS_bpf,SYS_perf_event_open,SYS_kexec_load,SYS_init_module,SYS_finit_module,SYS_delete_module,SYS_io_uring_setup,SYS_personality,SYS_bind,SYS_listen,SYS_shmat,SYS_pkey_mprotect};
 for(unsigned i=0;i<sizeof(denied)/sizeof(denied[0]);i++)deny_nr(denied[i]);
 /* clone3 ENOSYS permits libc's non-namespace clone fallback. */
 EQ(SYS_clone3,0,1);RET(SECCOMP_RET_ERRNO|ENOSYS);
 EQ(SYS_clone,0,4);LD(offsetof(struct seccomp_data,args[0]));
 ins(BPF_JMP|BPF_JSET|BPF_K,0,1,0x7e020000);RET(SECCOMP_RET_ERRNO|EPERM);LD(offsetof(struct seccomp_data,nr));
 if(sealed){deny_nr(SYS_socket);deny_nr(SYS_socketpair);deny_nr(SYS_connect);}
 /* No executable anonymous mapping; no W+X, including file-backed aliases. */
 EQ(SYS_mmap,0,7);LD(offsetof(struct seccomp_data,args[2]));
 ins(BPF_JMP|BPF_JSET|BPF_K,0,4,PROT_EXEC);ins(BPF_JMP|BPF_JSET|BPF_K,2,0,PROT_WRITE);
 LD(offsetof(struct seccomp_data,args[3]));ins(BPF_JMP|BPF_JSET|BPF_K,0,1,MAP_ANONYMOUS);
 RET(SECCOMP_RET_ERRNO|EPERM);LD(offsetof(struct seccomp_data,nr));
 EQ(SYS_mprotect,0,4);LD(offsetof(struct seccomp_data,args[2]));
 ins(BPF_JMP|BPF_JSET|BPF_K,0,1,PROT_EXEC);RET(SECCOMP_RET_ERRNO|EPERM);LD(offsetof(struct seccomp_data,nr));
 RET(SECCOMP_RET_ALLOW);struct sock_fprog p={.len=nf,.filter=filter};
 if(prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0)||prctl(PR_SET_SECCOMP,SECCOMP_MODE_FILTER,&p))fail("seccomp required");
}
static void profile(const char *name){
 int fd=open("/proc/self/attr/current",O_WRONLY);if(fd<0)fail("profile control");char s[200];int n=snprintf(s,sizeof(s),"changeprofile %s",name);
 if(write(fd,s,n)!=n)fail("profile transition");close(fd);
}
int main(int argc,char **argv){
 char *request=0;size_t cap=0;int service=0;
 if(argc==3&&!strcmp(argv[1],"-c"))request=strdup(argv[2]);
 else if(argc==3&&!strcmp(argv[1],"--service")){service=1;asprintf(&request,"run\tservice:%s",argv[2]);}
 else if(argc==1){setvbuf(stdin,0,_IONBF,0);if(isatty(0))dprintf(1,"Enter run<TAB>recorded path or broker<TAB>tool<TAB>arguments. No shell syntax.\n");if(getline(&request,&cap,stdin)<0)return 0;request[strcspn(request,"\n")]=0;}
 else refuse("only a structured launch request is accepted");
 char *tokens[70],*save=0;int nt=0;
 for(char *s=strtok_r(request,"\t",&save);s&&nt<69;s=strtok_r(0,"\t",&save))tokens[nt++]=s;
 tokens[nt]=0;if(nt<2)refuse("use tab-separated run or broker request; free command text is not code input");
 clearenv();setenv("PATH","/usr/local/bin:/usr/bin:/usr/sbin",1);setenv("HOME","/home/stand",1);setenv("LANG","C.UTF-8",1);setenv("LC_ALL","C.UTF-8",1);
 if(!strcmp(tokens[0],"broker")){
  const char *names="|stand-apply|stand-verify|stand-compare|stand-pkg|stand-line|apt|apt-get|pip|pip3|npm|flatpak|podman|crontab|at|systemd-run|systemctl|nmcli|nft|useradd|usermod|userdel|groupadd|groupdel|bluetoothctl|";
  char needle[100];snprintf(needle,sizeof(needle),"|%s|",tokens[1]);if(!strstr(names,needle))refuse("unknown broker");
  char path[160];snprintf(path,sizeof(path),"/usr/local/bin/%s",tokens[1]);char *v[74]={"sudo","-n",path};for(int i=2;i<nt;i++)v[i+1]=tokens[i];
  syscall(SYS_close_range,3,~0U,0);execv("/usr/bin/sudo",v);fail("broker");
 }
 if(strcmp(tokens[0],"run"))refuse("unknown request type");
 int lock=open("/var/lib/stand/apply.lock",O_RDONLY|O_CLOEXEC);if(lock<0||flock(lock,LOCK_SH|LOCK_NB))refuse("application in progress");
 FILE *f=fopen("/etc/stand/launch.tsv","r");if(!f)fail("launch table");char *line=0;size_t size=0;char *fields[12];int found=0;
 while(getline(&line,&size,f)>0){char *p=line;int k=0;line[strcspn(line,"\n")]=0;while(k<12&&(fields[k]=strsep(&p,"\t")))k++;if(k>=8&&!strcmp(fields[0],tokens[1])){found=1;break;}}
 fclose(f);if(!found)refuse("entry is not a declared ordinary launch");
 int sealed=strcmp(fields[1],"data")!=0;if(sealed&&nt!=2)refuse("recorded code accepts no caller arguments");
 if(service&&strncmp(fields[0],"service:",8))refuse("invalid service entry");
 hashcheck(fields[3],fields[4]);if(strcmp(fields[5],"-"))hashcheck(fields[5],fields[6]);
 int pipefd[2],ready[2];if(pipe2(pipefd,O_CLOEXEC)||pipe2(ready,O_CLOEXEC))fail("output pipe");pid_t child=fork();if(child<0)fail("fork");
 if(!child){
  close(pipefd[0]);close(ready[0]);dup2(pipefd[1],1);dup2(pipefd[1],2);
  if(sealed){int fd=open("/dev/null",O_RDONLY);if(fd<0)fail("null input");dup2(fd,0);close(fd);}
  if(chdir(sealed?"/":"/home/stand"))fail("working directory");
  char *args[80];int n=0;args[n++]=fields[3];
  if(strcmp(fields[5],"-")){if(strstr(fields[3],"python")){args[n++]="-I";args[n++]="-S";args[n++]="-B";}else if(strstr(fields[3],"bash")){args[n++]="--noprofile";args[n++]="--norc";}args[n++]=fields[5];}
  if(!strcmp(fields[7],"ed"))args[n++]="-r";
  if(!strcmp(fields[7],"w3m")){args[n++]="-dump";args[n++]="-config";args[n++]="/etc/stand/w3m.conf";}
  if(!strncmp(fields[0],"service:",8)&&strcmp(fields[7],"-")){char *x=fields[7],*a;while((a=strsep(&x,"|")))if(*a)args[n++]=a;}
  for(int i=2;i<nt;i++){if(tokens[i][0]=='-')refuse("data-tool options are fixed");args[n++]=tokens[i];}args[n]=0;
  if(sealed)readonly_closure();profile(fields[2]);secure(sealed);
  /* Parent's application lock is released only after child confinement. */
  if(write(ready[1],"1",1)!=1)fail("ready");syscall(SYS_close_range,3,~0U,0);execv(args[0],args);fail("recorded launch");
 }
 close(pipefd[1]);close(ready[1]);char ack;read(ready[0],&ack,1);close(ready[0]);close(lock);
 char buf[8192];ssize_t n;while((n=read(pipefd[0],buf,sizeof(buf)))>0){ssize_t off=0;while(off<n){ssize_t w=write(1,buf+off,n-off);if(w<0)break;off+=w;}}close(pipefd[0]);
 int status;waitpid(child,&status,0);return WIFEXITED(status)?WEXITSTATUS(status):128+WTERMSIG(status);
}
