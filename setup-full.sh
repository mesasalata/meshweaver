#!/bin/bash
## IMPORTANT NOTE:
# This script should only be run if significant changes have been made to:
# 1. token-set.txt
# 2. the data set used to generate the token list

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1 ; pwd -P )
run_path=$( cd . ; pwd -P )

cd "$parent_path" || exit 1
python3 setup-full.py

cd "$run_path" || exit 1

exit 0
