#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/ptrace.h>
#include <sys/uio.h>
#include <sys/socket.h>
#include <sys/syscall.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <dlfcn.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/shm.h>
#include <mqueue.h>
#include <linux/keyctl.h>
static int failures;
static void denied(const char *id,int good){printf("%s %s errno=%d\n",id,good?"DENIED":"ESCAPE",errno);if(!good)failures++;}
int main(void){
#ifdef HOLDER
 pid_t descendant=fork();printf("HOLDER %d CHILD %d\n",getpid(),descendant);fflush(stdout);for(;;)pause();
#endif
 void *p=mmap(0,4096,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);denied("WX",p==MAP_FAILED);
 p=mmap(0,4096,PROT_READ|PROT_EXEC,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);denied("ANON_RX",p==MAP_FAILED);
 p=mmap(0,4096,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);denied("MPROTECT_RX",p!=MAP_FAILED && mprotect(p,4096,PROT_READ|PROT_EXEC)<0);
 int msg=msgget(IPC_PRIVATE,IPC_CREAT|0600);denied("SYSV_MSG",msg<0);if(msg>=0)msgctl(msg,IPC_RMID,NULL);
 int shm=shmget(IPC_PRIVATE,4096,IPC_CREAT|0600);denied("SYSV_SHM",shm<0);if(shm>=0)shmctl(shm,IPC_RMID,NULL);
 char mqname[80];snprintf(mqname,sizeof(mqname),"round2-%d",getpid());struct mq_attr mqattr={.mq_maxmsg=1,.mq_msgsize=16};
 int mq=syscall(SYS_mq_open,mqname,O_RDWR|O_CREAT|O_EXCL,0600,&mqattr);denied("POSIX_MQUEUE",mq<0);if(mq>=0){close(mq);syscall(SYS_mq_unlink,mqname);}
 denied("KEYRING",syscall(SYS_keyctl,KEYCTL_GET_KEYRING_ID,KEY_SPEC_SESSION_KEYRING,1)<0);
 denied("ADD_KEY",syscall(SYS_add_key,"user","round2","x",1,KEY_SPEC_SESSION_KEYRING)<0);
 denied("MEMFD",syscall(SYS_memfd_create,"unrecorded",0)<0);
 denied("PTRACE",ptrace(PTRACE_TRACEME,0,0,0)<0);
 char x=0;struct iovec v={&x,1};denied("PROCESS_VM",process_vm_writev(getpid(),&v,1,&v,1,0)<0);
 struct file_handle *handle=calloc(1,sizeof(*handle)+128);int mountid=0,oracle_errno[2],oracle_result[2];const char *oracle_paths[]={"/home/stand/round2/native","/home/stand/round2/absent-oracle"};
 for(int i=0;i<2;i++){handle->handle_bytes=128;oracle_result[i]=syscall(SYS_name_to_handle_at,AT_FDCWD,oracle_paths[i],handle,&mountid,0);oracle_errno[i]=errno;}
 printf("HANDLE_ORACLE results=%d,%d errno=%d,%d\n",oracle_result[0],oracle_result[1],oracle_errno[0],oracle_errno[1]);denied("HANDLE_ORACLE",oracle_result[0]<0&&oracle_result[1]<0&&oracle_errno[0]==oracle_errno[1]);free(handle);
 denied("PROC_MEM",open("/proc/self/mem",O_RDWR)<0);
 denied("DLOPEN",dlopen("/home/stand/round2/libprobe.so",RTLD_NOW)==0);
 int f=open("/home/stand/round2/native",O_RDONLY);denied("FILE_EXEC_MAP",f<0||mmap(0,4096,PROT_READ|PROT_EXEC,MAP_PRIVATE,f,0)==MAP_FAILED);
 int s=socket(AF_INET,SOCK_STREAM,0);struct sockaddr_in a={.sin_family=AF_INET,.sin_port=0};denied("LISTENER",s<0||bind(s,(void*)&a,sizeof(a))<0);
 fflush(stdout);pid_t child=fork();if(child==0){execl("/usr/bin/bash","bash","-c","printf UNRECORDED_CODE",NULL);_exit(errno==EACCES||errno==EPERM?0:2);}int status;waitpid(child,&status,0);denied("HELPER",WIFEXITED(status)&&WEXITSTATUS(status)==0);
 fflush(stdout);child=fork();if(child==0){int fd=open("/home/stand/round2/native",O_RDONLY);if(fd<0)_exit(0);char *args[]={"native",NULL},*env[]={NULL};fexecve(fd,args,env);_exit(errno==EACCES||errno==EPERM?0:2);}waitpid(child,&status,0);denied("FEXECVE",WIFEXITED(status)&&WEXITSTATUS(status)==0);
 fflush(stdout);child=fork();if(child==0){char *args[]={"native",NULL},*env[]={NULL};syscall(SYS_execveat,AT_FDCWD,"/home/stand/round2/native",args,env,0);_exit(errno==EACCES||errno==EPERM||errno==ENOENT?0:2);}waitpid(child,&status,0);denied("EXECVEAT",WIFEXITED(status)&&WEXITSTATUS(status)==0);
 int alias=open("/home/stand/round2/native",O_RDWR);void *rw=MAP_FAILED,*rx=MAP_FAILED;if(alias>=0){rw=mmap(0,4096,PROT_READ|PROT_WRITE,MAP_SHARED,alias,0);rx=mmap(0,4096,PROT_READ|PROT_EXEC,MAP_SHARED,alias,0);}denied("WRITABLE_ALIAS",alias<0||rw==MAP_FAILED||rx==MAP_FAILED);
 return failures?1:0;
}
