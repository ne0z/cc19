#!/usr/bin/python2.7

import sys
import string
import random

from Crypto.Cipher import AES

def wrap(s, w):
    return [s[i:i + w] for i in range(0, len(s), w)]

def padding(data):
  length = 16 - (len(data) % 16)
  data += chr(length)*length
  return data

def randomString(size):
  s = ""
  for _ in range(size):
    s = s + string.ascii_letters[random.randint(0, len(string.ascii_letters)-1)]
  return s

key = 'supersecretkey!!'

cipher = AES.new(key, AES.MODE_ECB)

dim = random.randint(1, 1)*16 - 6
flag = 'flag{' + randomString(dim) + '}'

assert len(flag) == 16

msg = cipher.encrypt(flag).encode("hex")
print (msg)

while True:
  msg = raw_input("> ")

  if msg == "exit":
    print "You loose, the flag was " + flag
    sys.exit(0)

  if msg == flag:
    print "Nice, you've learned choosen-prefix attack!"
    sys.exit(0)

  msg = padding(msg + flag)
  msg = cipher.encrypt(msg).encode("hex")
  print " ".join(wrap(msg, 32))
