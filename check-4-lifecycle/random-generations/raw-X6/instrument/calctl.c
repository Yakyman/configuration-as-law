#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <errno.h>
int main(int argc, char **argv) {
    const char *action = argc > 1 ? argv[1] : "status";
    if (strcmp(action,"apply") && strcmp(action,"status") && strcmp(action,"gc") && strcmp(action,"rollback")) { fprintf(stderr,"usage: calctl [status|apply|gc GENERATION...|rollback GENERATION]\n"); return 2; }
    char request[65536];
    size_t pos = (size_t)snprintf(request,sizeof request,"{\"action\":\"%s\",\"generations\":[",action);
    for (int i=2; i<argc; i++) {
        size_t n=strlen(argv[i]);
        if (!n || n>40 || pos+n+5>=sizeof request) return 2;
        for (size_t j=0;j<n;j++) if (!isdigit((unsigned char)argv[i][j])) return 2;
        pos += (size_t)snprintf(request+pos,sizeof request-pos,"%s\"%s\"",i>2?",":"",argv[i]);
    }
    pos += (size_t)snprintf(request+pos,sizeof request-pos,"]}\n");
    int s=socket(AF_UNIX,SOCK_STREAM,0);
    struct sockaddr_un addr={.sun_family=AF_UNIX};
    strcpy(addr.sun_path,"/run/cal.sock");
    if (s<0 || connect(s,(struct sockaddr *)&addr,sizeof addr)<0) {perror("calctl connect");return 1;}
    size_t sent=0;
    while(sent<pos) {ssize_t n=write(s,request+sent,pos-sent);if(n<0){if(errno==EINTR)continue;perror("write");return 1;}sent+=(size_t)n;}
    char buf[4096], prefix[256]={0}; size_t used=0; ssize_t n;
    while((n=read(s,buf,sizeof buf))>0) {
        if(used<sizeof prefix-1){size_t take=(size_t)n; if(take>sizeof prefix-1-used)take=sizeof prefix-1-used;memcpy(prefix+used,buf,take);used+=take;}
        if(fwrite(buf,1,(size_t)n,stdout)!=(size_t)n)return 1;
    }
    close(s);
    if(n<0){perror("read");return 1;}
    /* Server sorts error first on failure; successful schema has no error key. */
    return strstr(prefix,"\"error\":") ? 1 : 0;
}
