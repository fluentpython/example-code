#!/usr/bin/env bash

docker run -p 8002:8002 -p 8001:8001 -p 8003:8003 -it renzon/flupy-flags:run-servers ./run_servers.sh