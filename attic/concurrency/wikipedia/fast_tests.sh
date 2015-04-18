#!/bin/bash

# run tests skipping @pytest.mark.network
py.test test_daypicts.py -m 'not network' $1 $2 $3
