#!/bin/bash
docker run "$@" --rm -p "127.0.0.1:1234:80" --name "flags" -it "zenhackteam/flags"

