#!/bin/bash
vaurien --protocol http --proxy localhost:8000 --backend localhost:8080 \
        --behavior 50:error,50:delay --behavior-delay-sleep .5
