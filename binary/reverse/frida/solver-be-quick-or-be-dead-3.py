#!/usr/bin/env python2

import frida
import sys
import time

pid = frida.spawn("./be-quick-or-be-dead-3")
print("pid =", pid)
session = frida.attach(pid)

# Replace the "calculate_key()" function with a function that directly
# returns calc(0x11965).
script = session.create_script("""
'use strict';
Interceptor.replace(ptr('0x400792'), new NativeCallback(function(n) {
	return 0x9e22c98e;
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

