#!/bin/bash
docker run "$@" --rm -p "127.0.0.1:31339:31339" --name "rsayyyy" -it "zenhackteam/rsayyyy"
