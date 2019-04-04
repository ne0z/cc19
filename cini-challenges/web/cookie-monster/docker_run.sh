#!/bin/bash
docker run "$@" --rm -p "127.0.0.1:8082:80" --name "console" -it "zenhackteam/cookie-monster"
