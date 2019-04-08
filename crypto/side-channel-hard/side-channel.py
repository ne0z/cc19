#!/usr/bin/python2.7

import sys
import string
import time
from random import randint

dic = string.ascii_letters

def randomString(size):
  return "".join([dic[randint(0, len(dic)-1)] for _ in range(size)])

flag = 'flag{' + randomString(10) + '}'

assert len(flag) == 16

print(flag)

while True:
  msg = raw_input("> ")

  if msg == "exit":
    print "You loose, the flag was " + flag
    sys.exit(0)
    break

  if len(msg) > len(flag):
    print "Too long!"
    continue

  for i in range(len(msg)):
    if msg[i] == flag[i]:
      time.sleep(0.0005) # 0.5ms
    else:
      break

  if msg == flag:
    print "Nice, you've learned a time-base side-channel attack"
    break
  else:
    print "Wrong!"
