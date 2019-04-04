#!/bin/bash
docker run "$@" --rm -p "127.0.0.1:1341:12345" --name "giftwrapper2" -it "zenhackteam/giftwrapper2"
