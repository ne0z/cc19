#!/usr/bin/env python2

import binascii

def fmt(s):
	r=''
	for c in s:
		if 31<ord(c)<128:
			r+=c
		else:
			r+='?'
	return r


def binsearch(mn,mx,todo):
	print mx-mn
	print fmt(binascii.unhexlify(('0' if len(hex(mn)[2:].rstrip('L'))%2 else '')+hex(mn)[2:].rstrip('L'))),
	print fmt(binascii.unhexlify(('0' if len(hex(mx)[2:].rstrip('L'))%2 else '')+hex(mx)[2:].rstrip('L')))
	if mn==mx:
		return mn
	med=(mn+mx)/2
	cal=med**0x10001
	if cal<todo:
		return binsearch(med+1,mx,todo)
	elif cal>todo:
		return binsearch(mn,med-1,todo)
	return med


fi=open('rsa_16m')
ln=fi.readline().strip()
assert ln.startswith('n = 0x')
n=int(ln[6:],16)
print len(bin(n)[2:])
ln=fi.readline().strip()
assert ln.startswith('c = 0x')
c=int(ln[6:].strip(),16)
assert fi.readline().strip()=='e = 0x10001'
assert c<n/10000

print binsearch(0,100000000000000000000000000000000000000000000000000000000000000000000000,c)

