#!/bin/bash

svg_file_name="$(src/shell/raster-to-vector.sh $1)"
python3 src/python/structure.py "$svg_file_name"
