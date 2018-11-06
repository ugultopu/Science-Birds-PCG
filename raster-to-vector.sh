#!/bin/bash

file_name="$1"
file_name_without_extension="${file_name%.*}"
file_extension="${file_name#*.}"
monochrome_file_name_without_extension="$file_name_without_extension-monochrome"
monochrome_file_name="$monochrome_file_name_without_extension.$file_extension"
bitmap_file_name="$monochrome_file_name_without_extension.bmp"
svg_file_name="$monochrome_file_name_without_extension.svg"

convert "$file_name" -monochrome "$monochrome_file_name"
mogrify -format bmp "$monochrome_file_name"
potrace -b svg "$bitmap_file_name"

echo "$svg_file_name"
