package main
import("syscall";"unsafe")
func snapshotInfo(fd int)bool{var b [504]byte;_,_,e:=syscall.Syscall(syscall.SYS_IOCTL,uintptr(fd),uintptr(0x81f8943c),uintptr(unsafe.Pointer(&b[0])));if e!=0{return true};for _,v:=range b[312:328]{if v!=0{return true}};return false}
