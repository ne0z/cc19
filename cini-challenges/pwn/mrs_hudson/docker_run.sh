#!/bin/bash
docker run "$@" --rm -p "127.0.0.1:31337:31337" --name "mrs_hudson" -it "zenhackteam/mrs_hudson"
