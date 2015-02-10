#!/bin/bash
vaurien --protocol http --proxy localhost:8002 --backend localhost:8001 \
    --behavior 100:delay --behavior-delay-sleep .1