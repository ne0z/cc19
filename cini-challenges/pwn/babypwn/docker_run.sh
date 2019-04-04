#!/bin/bash
docker run "$@" --rm -p "127.0.0.1:22230:22230" --name "babypwn" -it "zenhackteam/babypwn"
