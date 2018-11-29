#!/bin/bash

file_name="$1"
base_name="${file_name%.*}"
extension="${file_name#*.}"
black_and_white_base_name="$base_name-black-and-white"
denoised_base_name="$black_and_white_base_name-denoised"

convert "$file_name" -negate -threshold 0 -negate "$black_and_white_base_name.$extension"
python3 denoise_image.py "$black_and_white_base_name.$extension" "$denoised_base_name.$extension"
mogrify -format bmp "$denoised_base_name.$extension"
potrace -b svg "$denoised_base_name.bmp"
python3 svg_path_to_polygon.py "$denoised_base_name.svg"

echo "$denoised_base_name-polygon.svg"
