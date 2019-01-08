#!/bin/bash

svg_file_name="$(./raster-to-vector.sh $1)"

python3 ../python/structure.py "$svg_file_name"
