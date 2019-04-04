#!/usr/bin/env python2

import frida
import sys
import time

pid = frida.spawn("./be-quick-or-be-dead-1")
print("pid =", pid)
session = frida.attach(pid)

script = session.create_script("""
'use strict';
Interceptor.replace(ptr('0x00400706'), new NativeCallback(function() {
	return 0xdfa8fc78;
},'int64', []));

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

