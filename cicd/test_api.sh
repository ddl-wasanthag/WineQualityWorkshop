#!/bin/bash
output=`python3 cicd/test_api.py`
echo $output
if [[ $output =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    if (( $(bc <<< "$output >= 1 && $output <= 10") )); then
        echo "Output is between 1 and 10: $output"
        exit 0  # Exit with success code
    else
        echo "Output is not between 1 and 10: $output"
        exit 1  # Exit with error code
    fi
else
    echo "Output is not a valid number: $output"
    exit 1  # Exit with error code
fi
