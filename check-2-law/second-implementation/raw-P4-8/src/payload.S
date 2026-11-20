/* Harmless static x86-64 ELF: prints unique marker and own executable path;
   bounded readlink of proc/self/exe, no data read/write besides stdout. */
.global _start
.section .text
_start:
    mov $1, %rax
    mov $1, %rdi
    lea marker(%rip), %rsi
    mov $marker_len, %rdx
    syscall
    mov $89, %rax
    lea self(%rip), %rdi
    lea buffer(%rip), %rsi
    mov $512, %rdx
    syscall
    test %rax, %rax
    js failed
    mov %rax, %rdx
    mov $1, %rax
    mov $1, %rdi
    lea buffer(%rip), %rsi
    syscall
    mov $1, %rax
    mov $1, %rdi
    lea newline(%rip), %rsi
    mov $1, %rdx
    syscall
    xor %rdi, %rdi
    jmp finish
failed:
    mov $3, %rdi
finish:
    mov $60, %rax
    syscall
.section .rodata
marker: .ascii "P48_NATIVE_4e8f39_OK\nEXE="
.set marker_len, .-marker
self: .asciz "/proc/self/exe"
newline: .ascii "\n"
.section .bss
.lcomm buffer,512
.section .note.GNU-stack,"",@progbits
