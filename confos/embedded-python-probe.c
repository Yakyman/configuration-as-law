/* Recorded filename-based CPython embedding probe; no copied interpreter logic. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dlfcn.h>
int main(int argc,char **argv) {
 if(argc!=3 || (strcmp(argv[1],"file") && strcmp(argv[1],"typed"))) return 2;
 void *library=dlopen("libpython3.13.so.1.0",RTLD_NOW|RTLD_GLOBAL);
 if(!library){fprintf(stderr,"dlopen: %s\n",dlerror());return 3;}
 void (*initialize)(void)=dlsym(library,"Py_Initialize");
 int (*runfile)(FILE*,const char*,int,void*)=dlsym(library,"PyRun_SimpleFileExFlags");
 int (*runstring)(const char*,void*)=dlsym(library,"PyRun_SimpleStringFlags");
 int (*finalize)(void)=dlsym(library,"Py_FinalizeEx");
 if(!initialize || !runfile || !runstring || !finalize) return 4;
 initialize(); int result;
 if(!strcmp(argv[1],"file")) {
  FILE *input=fopen(argv[2],"rb");if(!input){perror("fopen");return 5;}
  result=runfile(input,argv[2],1,NULL);
 }else result=runstring(argv[2],NULL);
 int finish=finalize();
 return result || finish ? 1:0;
}
