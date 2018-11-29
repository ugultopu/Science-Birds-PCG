#!/bin/bash

svg_file_name="$(./raster-to-vector.sh $1)"
python3 structure.py "$svg_file_name"
