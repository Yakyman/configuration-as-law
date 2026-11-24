import pathlib,os,json
out={'route':'current-open-descriptors-and-mapped-files','processes':0,'fd_links_read':0,'maps_read':0,'certificate_fd_links':0,'certificate_mapping_lines':0,'ssl_library_mapping_lines':0,'errors':0}
for p in pathlib.Path('/proc').glob('[0-9]*'):
 out['processes']+=1
 try:
  for fd in (p/'fd').iterdir():
   try:
    target=os.readlink(fd);out['fd_links_read']+=1
    out['certificate_fd_links']+=target.startswith(('/etc/ssl/certs','/usr/share/ca-certificates','/usr/local/share/ca-certificates'))
   except OSError:out['errors']+=1
  data=(p/'maps').read_text();out['maps_read']+=1
  out['certificate_mapping_lines']+=sum('/etc/ssl/certs' in x or '/share/ca-certificates' in x for x in data.splitlines())
  out['ssl_library_mapping_lines']+=sum('/libssl.so' in x or '/libgnutls.so' in x or '/libnss3.so' in x for x in data.splitlines())
 except OSError:out['errors']+=1
print(json.dumps(out,sort_keys=True))
