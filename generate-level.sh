#!/bin/bash

svg_file_name="$(./raster-to-vector.sh $1)"
echo "TODO: Remove 'echo' from the beginning of the following command after you edit your Python script so that it creates a polygon from SVG 'path' element values, instead of from SVG 'polygon' element values."
echo "python structure.py '$svg_file_name'"
