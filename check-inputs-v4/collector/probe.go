// Bounded filesystem probe; Linux, no dependencies outside the standard library.
package main

import (
 "bufio"
 "crypto/md5"
 "crypto/sha1"
 "crypto/sha256"
 "crypto/sha512"
 "encoding/base64"
 "encoding/hex"
 "encoding/json"
 "fmt"
 "hash"
 "io"
 "os"
 "os/exec"
 "path/filepath"
 "strconv"
 "strings"
 "syscall"
 "time"
)
const maxEntries=1000000
var enc=json.NewEncoder(os.Stdout)
var pseudo=map[int64]bool{0x9fa0:true,0x62656572:true,0x1cd1:true,0x64626720:true,0x74726163:true,0x73636673:true,0x62656570:true}
func denied(p string) bool { p=filepath.Clean(p);for _,r:=range []string{"/proc","/sys","/dev"} {if p==r||strings.HasPrefix(p,r+"/"){return true}};return false }
// Resolve components with openat/O_NOFOLLOW: neither an intermediate symlink nor
// a symlink swapped into the final component can redirect a content read.
func openSafe(p string)(*os.File,error){
 p=filepath.Clean(p);if !filepath.IsAbs(p)||denied(p){return nil,fmt.Errorf("forbidden-path")}
 fd,e:=syscall.Open("/",syscall.O_RDONLY|syscall.O_DIRECTORY|syscall.O_CLOEXEC,0);if e!=nil{return nil,e}
 parts:=strings.Split(strings.TrimPrefix(p,"/"),"/")
 for i,s:=range parts {flags:=syscall.O_RDONLY|syscall.O_NOFOLLOW|syscall.O_NONBLOCK|syscall.O_CLOEXEC;if i<len(parts)-1 {flags|=syscall.O_DIRECTORY};next,er:=syscall.Openat(fd,s,flags,0);syscall.Close(fd);if er!=nil{return nil,er};fd=next}
 f:=os.NewFile(uintptr(fd),p);st,e:=f.Stat();if e!=nil||!st.Mode().IsRegular(){f.Close();return nil,fmt.Errorf("not-regular")}
 var fs syscall.Statfs_t;if e=syscall.Fstatfs(fd,&fs);e!=nil||pseudo[fs.Type]{f.Close();return nil,fmt.Errorf("forbidden-filesystem")};return f,nil
}
func read(p string,n int64)([]byte,error){f,e:=openSafe(p);if e!=nil{return nil,e};defer f.Close();s,e:=f.Stat();if e!=nil{return nil,e};if s.Size()>n{return nil,fmt.Errorf("size-cap")};b,e:=io.ReadAll(io.LimitReader(f,n+1));if int64(len(b))>n{return nil,fmt.Errorf("size-cap")};return b,e}
func fsinfo(p string)(int64,string,bool){var fs syscall.Statfs_t;if syscall.Statfs(p,&fs)!=nil{return 0,"unknown",false};persistent:="persistent";switch fs.Type{case 0x01021994,0x858458f6:persistent="runtime";case 0x794c7630:persistent="unknown"};if pseudo[fs.Type]{persistent="runtime"};return fs.Type,persistent,fs.Flags&1!=0}
func snapshot(p string,st os.FileInfo,fs int64) bool {
 if fs!=0x9123683e||st.Sys().(*syscall.Stat_t).Ino!=256||p=="/" {return false}
 // BTRFS_IOC_GET_SUBVOL_INFO: parent_uuid at offset 312 indicates snapshot.
 fd,e:=syscall.Open(p,syscall.O_RDONLY|syscall.O_DIRECTORY|syscall.O_NOFOLLOW,0);if e!=nil{return false};defer syscall.Close(fd)
 // See snapshotInfo in the platform helper below.
 return snapshotInfo(fd)
}
func atom(p string,st os.FileInfo) string {
 if st.IsDir(){for _,s:=range []string{"/var/lib/containers/storage","/.local/share/containers/storage","/var/lib/docker","/var/lib/containerd","/var/lib/rancher/k3s/agent/containerd","/var/lib/rancher/k3s/agent/cri-dockerd","/run/k3s/containerd","/run/k3s/cri-dockerd","/var/lib/kubelet/pods","/var/lib/flatpak","/.local/share/flatpak","/snap","/var/lib/snapd/snaps"}{if p==s||strings.HasSuffix(p,s){return "image-container-store"}};if strings.Contains(p,"/.zfs/snapshot/"){return "snapshot"}}
 if st.Mode().IsRegular(){switch strings.ToLower(filepath.Ext(p)){case ".qcow2",".qcow",".iso",".vmdk",".vdi",".squashfs",".img",".raw":return "image"}}
 return ""
}
func startup(p string)bool {b:=filepath.Base(p);for _,s:=range []string{".bashrc",".bash_profile",".bash_login",".bash_logout",".profile",".zshrc",".zshenv",".zprofile",".zlogin",".zlogout",".kshrc",".cshrc",".tcshrc",".login",".logout",".xsession",".xinitrc","config.fish"}{if b==s{return true}};for _,s:=range []string{"/etc/profile","/etc/bash.bashrc","/etc/bashrc","/etc/profile.d/","/etc/zsh/","/fish/conf.d/"}{if p==s||strings.Contains(p,s){return true}};return false}
func scan(){count:=0;errors:=0;seen:=map[[2]uint64]string{};start:=time.Now();root:="/";if len(os.Args)>2 {root=os.Args[2]};if !filepath.IsAbs(root)||denied(root){os.Exit(64)}
 var walk func(string)
 walk=func(p string){if count>=maxEntries||time.Since(start)>600*time.Second{return};if denied(p)||(p=="/run/c1-collector"||p=="/tmp/c1-collector"||p=="/var/tmp/c1-collector"){return}
 // The documented portal and GVFS namespaces are virtual alias views. Represent
 // this boundary without following it (root may lack access to its FUSE mount).
 parts:=strings.Split(strings.TrimPrefix(p,"/"),"/")
 if len(parts)==4&&parts[0]=="run"&&parts[1]=="user"&&(parts[3]=="doc"||parts[3]=="gvfs") {if _,er:=strconv.ParseUint(parts[2],10,32);er==nil {kind:="document-portal";if parts[3]=="gvfs"{kind="gvfs-alias"};_,ps,_:=fsinfo(filepath.Dir(p));enc.Encode(map[string]any{"path":p,"type":"directory","mode":"unknown","uid":"unknown","gid":"unknown","size":"unknown","mtime":"unknown","ctime":"unknown","executable":false,"signature":"not-read","persistence":ps,"readonly":"unknown","atomic":kind,"metadata":"documented virtual alias boundary; contents not collected"});count++;return}}
 st,e:=os.Lstat(p);if e!=nil{enc.Encode(map[string]any{"error":p,"detail":e.Error()});fmt.Fprintln(os.Stderr,"filesystem traversal:",e);errors++;return};s:=st.Sys().(*syscall.Stat_t);fsPath:=p;if st.Mode()&os.ModeSymlink!=0{fsPath=filepath.Dir(p)};ft,ps,ro:=fsinfo(fsPath);if pseudo[ft]{return}
 typ:="other";switch{case st.Mode().IsRegular():typ="file";case st.IsDir():typ="directory";case st.Mode()&os.ModeSymlink!=0:typ="symlink";case st.Mode()&os.ModeNamedPipe!=0:typ="fifo";case st.Mode()&os.ModeSocket!=0:typ="socket";case st.Mode()&os.ModeDevice!=0:typ="device"}
 rec:=map[string]any{"path":p,"type":typ,"mode":fmt.Sprintf("%04o",s.Mode&07777),"uid":s.Uid,"gid":s.Gid,"size":st.Size(),"mtime":st.ModTime().UTC().Format(time.RFC3339Nano),"ctime":time.Unix(s.Ctim.Sec,s.Ctim.Nsec).UTC().Format(time.RFC3339Nano),"executable":s.Mode&0111!=0,"signature":"not-regular","persistence":ps,"filesystem":fmt.Sprintf("0x%x",ft),"readonly":ro,"inode":s.Ino,"device":s.Dev}
 atomic:=atom(p,st);if st.IsDir()&&snapshot(p,st,ft){atomic="snapshot"};if atomic!=""{rec["atomic"]=atomic}
 if typ=="symlink"{target,er:=os.Readlink(p);if er==nil{rec["target"]=target}else{rec["target_error"]=er.Error()}}
 if typ=="file"{rec["startup"]=startup(p);f,er:=openSafe(p);if er==nil {buf:=make([]byte,4096);n,er:=f.Read(buf);f.Close();if er==nil||er==io.EOF{sum:=sha256.Sum256(buf[:n]);rec["signature"]="sha256-prefix4096:"+hex.EncodeToString(sum[:]);rec["signature_bytes"]=n;rec["shebang"]=n>=2&&string(buf[:2])=="#!"}else{rec["signature"]="unknown";rec["read_error"]=er.Error()}}else{rec["signature"]="unknown";rec["read_error"]=er.Error()}}
 count++;enc.Encode(rec);if !st.IsDir()||atomic!=""{return};key:=[2]uint64{uint64(s.Dev),s.Ino};if old,ok:=seen[key];ok{enc.Encode(map[string]any{"alias":p,"target":old});return};seen[key]=p
 fd,e:=syscall.Open(p,syscall.O_RDONLY|syscall.O_DIRECTORY|syscall.O_NOFOLLOW|syscall.O_CLOEXEC,0);f:=os.NewFile(uintptr(fd),p);if e!=nil{enc.Encode(map[string]any{"error":p,"detail":e.Error()});fmt.Fprintln(os.Stderr,"filesystem traversal:",e);errors++;return};defer f.Close();for {names,e:=f.Readdirnames(128);for _,name:=range names{walk(filepath.Join(p,name));if count>=maxEntries||time.Since(start)>600*time.Second{return}};if e==io.EOF{break};if e!=nil{enc.Encode(map[string]any{"error":p,"detail":e.Error()});fmt.Fprintln(os.Stderr,"filesystem traversal:",e);errors++;break}}
 };walk(root);complete:=count<maxEntries&&time.Since(start)<=600*time.Second&&errors==0;enc.Encode(map[string]any{"summary":true,"complete":complete,"count":count,"errors":errors,"duration":time.Since(start).Seconds()});if !complete{os.Exit(75)}
}
func digests(){scanner:=bufio.NewScanner(io.LimitReader(os.Stdin,16*1024*1024));scanner.Buffer(make([]byte,4096),1024*1024);for scanner.Scan(){var a struct{Path string `json:"path"`;Algorithm string `json:"algorithm"`;Limit int64 `json:"limit"`};if json.Unmarshal(scanner.Bytes(),&a)!=nil{os.Exit(65)};if a.Limit<=0||a.Limit>16777216{a.Limit=16777216};r:=map[string]any{"path":a.Path,"algorithm":a.Algorithm,"status":"unknown"};f,e:=openSafe(a.Path);if e==nil{st,_:=f.Stat();if st.Size()<=a.Limit{var h hash.Hash;switch a.Algorithm{case "md5":h=md5.New();case "sha1":h=sha1.New();case "sha256":h=sha256.New();case "sha384":h=sha512.New384();case "sha512":h=sha512.New()};if h!=nil{n,er:=io.Copy(h,io.LimitReader(f,a.Limit+1));if er==nil&&n<=a.Limit{r["digest"]=hex.EncodeToString(h.Sum(nil));r["status"]="ok"}}};f.Close()}else if os.IsNotExist(e){r["status"]="missing"};enc.Encode(r)}}
func run(){seconds,_:=strconv.Atoi(os.Args[2]);if seconds<1||seconds>700{os.Exit(64)};cmd:=exec.Command(os.Args[3],os.Args[4:]...);cmd.SysProcAttr=&syscall.SysProcAttr{Setpgid:true};cmd.Stdin=os.Stdin;cmd.Stdout=os.Stdout;cmd.Stderr=os.Stderr;if cmd.Start()!=nil{os.Exit(127)};timer:=time.AfterFunc(time.Duration(seconds)*time.Second,func(){syscall.Kill(-cmd.Process.Pid,syscall.SIGKILL)});e:=cmd.Wait();timed:=!timer.Stop();if timed{os.Exit(124)};if e!=nil{if ee,ok:=e.(*exec.ExitError);ok {os.Exit(ee.ExitCode())};os.Exit(1)}}
func main(){if len(os.Args)<2{os.Exit(64)};switch os.Args[1]{case "reads":reads();case "scan":scan();case "read":n,e:=strconv.ParseInt(os.Args[3],10,64);if e!=nil||n>16777216||n<0{os.Exit(64)};b,e:=read(os.Args[2],n);if e!=nil{fmt.Fprintln(os.Stderr,e);os.Exit(75)};os.Stdout.Write(b);case "digests":digests();case "run":run();case "b64":b,e:=io.ReadAll(io.LimitReader(os.Stdin,16777217));if e!=nil||len(b)>16777216{os.Exit(75)};fmt.Print(base64.StdEncoding.EncodeToString(b));default:os.Exit(64)}}

func reads(){scanner:=bufio.NewScanner(io.LimitReader(os.Stdin,16777216));scanner.Buffer(make([]byte,4096),1048576);for scanner.Scan(){var a struct{Path string `json:"path"`;Limit int64 `json:"limit"`};if json.Unmarshal(scanner.Bytes(),&a)!=nil{os.Exit(65)};if a.Limit<0||a.Limit>16777216{os.Exit(64)};b,e:=read(a.Path,a.Limit);r:=map[string]any{"path":a.Path,"status":"unknown"};if e==nil{r["status"]="ok";r["data"]=base64.StdEncoding.EncodeToString(b)}else{r["error"]=e.Error()};enc.Encode(r)}}
