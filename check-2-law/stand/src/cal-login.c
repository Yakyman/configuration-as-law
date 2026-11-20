#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pwd.h>
#include <string.h>
int main(int argc,char **argv) {
 struct passwd *pw=getpwuid(getuid());
 if(!pw || (strcmp(pw->pw_name,"alice") && strcmp(pw->pw_name,"bob"))) return 125;
 char profile[64]; snprintf(profile,sizeof(profile),"cal-%s",pw->pw_name);
 char **args=calloc(argc+6,sizeof(char*));
 args[0]="aa-exec"; args[1]="-p"; args[2]=profile; args[3]="--"; args[4]="/bin/bash";
 for(int i=1;i<argc;i++) args[i+4]=argv[i];
 execv("/usr/bin/aa-exec",args); perror("cal-login");return 126;
}
