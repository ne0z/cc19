#!/bin/bash
docker run "$@" --rm -p "127.0.0.1:31337:31337" --name "smashme" -it "zenhackteam/smashme"
