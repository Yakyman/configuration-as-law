#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
int main(int argc,char **argv) {
 if(argc==3 && !strcmp(argv[1],"--read-shared")) {
   FILE *f=fopen(argv[2],"r");if(!f){perror(argv[2]);return 1;}
   char buf[256];while(fgets(buf,sizeof(buf),f))fputs(buf,stdout);fclose(f);return 0;
 }
 if(argc>=2 && !strcmp(argv[1],"--probe")) {
   FILE *f=fopen("/usr/local/lib/cal/illegal-root-program-write","w");
   if(!f) {perror("managed root write");return 13;}
   fputs("unexpected\n",f); fclose(f);return 0;
 }
 if(argc!=3) {puts("declared test program");return 0;}
 char path[4096]; snprintf(path,sizeof(path),"%s/cache",argv[2]);
 FILE *f=fopen(path,"a"); if(!f){perror(path);return 1;}
 fprintf(f,"%s version=%s uid=%d\n",argv[1],getenv("CAL_VERSION"),getuid());fclose(f);
 return 0;
}
