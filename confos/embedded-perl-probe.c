/* Recorded native filename interpreter using the documented embedding API. */
#include <dlfcn.h>
#include <stdio.h>
int main(int argc,char **argv,char **env) {
 void *library=dlopen("libperl.so.5.40",RTLD_NOW|RTLD_GLOBAL);
 if(!library){fprintf(stderr,"dlopen: %s\n",dlerror());return 3;}
 void (*init)(int*,char***,char***)=dlsym(library,"Perl_sys_init3");
 void *(*alloc)(void)=dlsym(library,"perl_alloc");
 void (*construct)(void*)=dlsym(library,"perl_construct");
 int (*parse)(void*,void*,int,char**,char**)=dlsym(library,"perl_parse");
 int (*run)(void*)=dlsym(library,"perl_run");
 int (*destruct)(void*)=dlsym(library,"perl_destruct");
 void (*release)(void*)=dlsym(library,"perl_free");
 void (*term)(void)=dlsym(library,"Perl_sys_term");
 if(!init||!alloc||!construct||!parse||!run||!destruct||!release||!term)return 4;
 init(&argc,&argv,&env);void *perl=alloc();if(!perl)return 5;
 construct(perl);int result=parse(perl,NULL,argc,argv,NULL);
 if(!result)result=run(perl);
 int finish=destruct(perl);release(perl);term();
 return result||finish?1:0;
}
