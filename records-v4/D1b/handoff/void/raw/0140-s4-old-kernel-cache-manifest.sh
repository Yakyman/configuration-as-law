python3 - /var/cache/xbps/linux-firmware-network-20260810_1.x86_64.xbps <<'S4_ARCHIVE_READER'

import ctypes as C, sys
a=C.CDLL('libarchive.so.13')
a.archive_read_new.restype=C.c_void_p
a.archive_read_support_filter_all.argtypes=[C.c_void_p]
a.archive_read_support_format_tar.argtypes=[C.c_void_p]
a.archive_read_open_filename.argtypes=[C.c_void_p,C.c_char_p,C.c_size_t]
a.archive_read_next_header.argtypes=[C.c_void_p,C.POINTER(C.c_void_p)]
a.archive_entry_pathname.argtypes=[C.c_void_p]; a.archive_entry_pathname.restype=C.c_char_p
a.archive_read_data.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t];a.archive_read_data.restype=C.c_ssize_t
a.archive_read_free.argtypes=[C.c_void_p]
a.archive_error_string.argtypes=[C.c_void_p];a.archive_error_string.restype=C.c_char_p
h=a.archive_read_new()
try:
 a.archive_read_support_filter_all(h);a.archive_read_support_format_tar(h)
 if a.archive_read_open_filename(h,sys.argv[1].encode(),65536)!=0:raise RuntimeError(a.archive_error_string(h))
 entry=C.c_void_p();found=False
 for index in range(100000):
  status=a.archive_read_next_header(h,C.byref(entry))
  if status==1:break
  if status<0:raise RuntimeError(a.archive_error_string(h))
  name=a.archive_entry_pathname(entry)
  if name not in (b'files.plist',b'./files.plist'):continue
  chunks=[];total=0;buffer=C.create_string_buffer(65536)
  while True:
   size=a.archive_read_data(h,buffer,len(buffer))
   if size<0:raise RuntimeError(a.archive_error_string(h))
   if size==0:break
   total+=size
   if total>16777216:raise RuntimeError('metadata size cap')
   chunks.append(buffer.raw[:size])
  sys.stdout.buffer.write(b''.join(chunks));found=True;break
 if not found:raise RuntimeError('manifest not present within header bound')
finally:a.archive_read_free(h)

S4_ARCHIVE_READER

