#!/bin/bash

# TODO Understand why we had to remove whitespace from file names.

find $2 -name '.DS_Store' -delete
find $2 -name '*-*' -delete
find $2 -type f | while read image
do
    echo "$image"
    $1/generate-level.sh $1 "$image" 
done
