#!/usr/bin/python2.7

import sys
from random import randint

from Crypto.Cipher import AES

def wrap(s, w):
    return [s[i:i + w] for i in range(0, len(s), w)]

def padding(data):
  length = 16 - (len(data) % 16)
  data += chr(length)*length
  return data

dic = "0123456789ABCDEF"

def randomString(size):
  return "".join([dic[randint(0, len(dic)-1)] for _ in range(size)])

key = 'supersecretkey!!'

cipher = AES.new(key, AES.MODE_ECB)

flag = 'flag{' + randomString(4) + '}'

assert(len(flag) == 10)

msg = cipher.encrypt(padding(flag)).encode("hex")
print (msg)

while True:
  msg = raw_input("> ")

  if msg == "exit":
    print "You loose, the flag was " + flag
    sys.exit(0)
    break

  if msg == flag:
    print "Nice, you've learned padding oracle attack!"
    break

  msg = msg + flag
  msg = cipher.encrypt(padding(msg)).encode("hex")
  print " ".join(wrap(msg, 32))
