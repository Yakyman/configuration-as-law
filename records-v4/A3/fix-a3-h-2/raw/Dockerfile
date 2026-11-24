FROM docker.io/library/busybox:stable
WORKDIR /www
COPY index.html /www/index.html
EXPOSE 8080
CMD ["httpd", "-f", "-p", "8080", "-h", "/www"]
