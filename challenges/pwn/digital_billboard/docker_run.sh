#!/bin/bash
docker run "$@" --rm -p "127.0.0.1:1337:12345" --name "digital_billboard" -it "zenhackteam/digital_billboard"
