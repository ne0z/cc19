#!/bin/bash
docker run "$@" --rm -p "127.0.0.1:22227:22227" --name "1996" -it "zenhackteam/1996"
