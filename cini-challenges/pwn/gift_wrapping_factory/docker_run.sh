#!/bin/bash
docker run "$@" --rm -p "127.0.0.1:1338:12345" --name "giftwrapper" -it "zenhackteam/giftwrapper"
