import pathlib,json,re
out={'route':'running-process-trust-path-overrides','processes_read':0,'environment_overrides':0,'command_line_references':0,'errors':0,'trust_policy_files':0,'trust_policy_directives':0}
keys=[b'SSL_CERT_FILE=',b'SSL_CERT_DIR=',b'SSL_CA_CERT_FILE=',b'SSL_CA_CERT_PATH=',b'CURL_CA_BUNDLE=',b'REQUESTS_CA_BUNDLE=',b'NODE_EXTRA_CA_CERTS=']
for p in pathlib.Path('/proc').glob('[0-9]*'):
 try:
  env=(p/'environ').read_bytes();cmd=(p/'cmdline').read_bytes();out['processes_read']+=1
  out['environment_overrides']+=sum(x.startswith(tuple(keys)) for x in env.split(b'\0'))
  out['command_line_references']+=len(re.findall(rb'/etc/ssl/certs|--cacert|--capath|--ca-certificate',cmd))
 except OSError:out['errors']+=1
for s in ['/etc/ca-certificates.conf','/etc/ssl/openssl.cnf']:
 p=pathlib.Path(s)
 if p.is_file():
  out['trust_policy_files']+=1;out['trust_policy_directives']+=sum(bool(x.strip()) and not x.lstrip().startswith(b'#') for x in p.read_bytes().splitlines())
print(json.dumps(out,sort_keys=True))
