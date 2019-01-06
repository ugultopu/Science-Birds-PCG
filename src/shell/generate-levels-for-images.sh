#!/bin/bash

# TODO Understand why we had to remove whitespace from file names.

find Images/Edited -name '.DS_Store' -delete
find Images/Edited -name '*-*' -delete
find Images/Edited -type f | while read image
do
    echo "$image"
    src/shell/generate-level.sh "$image"
done
