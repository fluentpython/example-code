#!/bin/bash
vaurien --protocol http --backend localhost:8001 \
        --proxy 0.0.0.0:8002  \
        --behavior 100:delay --behavior-delay-sleep 1
