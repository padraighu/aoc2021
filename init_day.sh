#!/usr/bin/env bash

if [ ! -z "$1" ]
then
    day="$1";
    echo "Creating files for $day";
    touch "input/${day}t.txt"
    touch "input/${day}r.txt"
    touch "solution/${day}.py"
    echo "Done"
fi
