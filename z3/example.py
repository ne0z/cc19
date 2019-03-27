#!/usr/bin/env python

from z3 import *

s = Solver()
x, y = Ints('x y')
s.add(x + y < 12)
s.add(x + y > 0)

# Check if the formulas are satisfiable
ret = s.check()
if ret != z3.sat:
    quit(1)

print(s.model())
print("A value for x is %s" % (s.model()[x]))


# A facebook-style problem
fb = Solver()
c = Int('c')
q = Int('q')
t = Int('t')
fb.add(c + c == 10)
fb.add(c * q + q == 12)
fb.add(c * q - t * c == c)
ret = fb.check()
if ret != z3.sat:
    quit(1)
print(fb.model())
