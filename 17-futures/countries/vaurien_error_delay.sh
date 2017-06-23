#!/bin/bash
vaurien --protocol http --backend localhost:8001 \
        --proxy 0.0.0.0:8003  \
        --behavior 25:error,50:delay --behavior-delay-sleep .5