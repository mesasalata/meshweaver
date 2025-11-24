#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1 ; pwd -P )
run_path=$( cd . ; pwd -P )

cd "$parent_path/tests" || exit 1
python -m unittest discover --pattern=test_*.py

cd "$run_path" || exit 1

exit 0
