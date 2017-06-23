#!/bin/bash

#Start nginx on port 8001
nginx

#Start vaurien with delay in background on port 8002
vaurien --protocol http --backend localhost:8001 \
        --proxy 0.0.0.0:8002  \
        --behavior 100:delay --behavior-delay-sleep 1 &

#Start vaurien with delay and error on port 8003
vaurien --protocol http --backend localhost:8001 \
        --proxy 0.0.0.0:8003  \
        --behavior 25:error,50:delay --behavior-delay-sleep .5