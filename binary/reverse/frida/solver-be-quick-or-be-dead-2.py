#!/usr/bin/env python2

import frida
import sys
import time

pid = frida.spawn("./be-quick-or-be-dead-2")
print("pid =", pid)
session = frida.attach(pid)

# Replace the "calculate_key()" function with a function that directly
# returns Fibonacci(1026).
# We can use an online tool to get the 1026-th Fibonacci's number,
# and then use Python to compute the modulo 2^32:
# >>> 11798692818055232550147578884125865608089028544560913468519228968187430794620907976123201977895385245239705082830656904630178314159866370495211539023461052682811230321796555930907722724384131648527339458407317543768 % pow(2,32)
script = session.create_script("""
'use strict';
Interceptor.replace(ptr('0x40074b'), new NativeCallback(function(n) {
	return 0xf70a9b58;
},'int64', ['int64']));

""")

def on_message(message, data):
	print(message)
script.on('message', on_message)

done = False
def on_detached_with_reason(reason):
    global done
    assert reason == 'process-terminated'
    done = True
session.on('detached', on_detached_with_reason)

script.load()
frida.resume(pid)
while not done:
    time.sleep(1)

