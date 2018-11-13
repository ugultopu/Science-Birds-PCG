#!/bin/bash
# USAGE: You need to provide the name of the input raster file as the first
# argument.

raster_image_name="$1"

if [ ! -e "$raster_image_name" ]; then
  echo "File $raster_image_name does not exist."
  exit 1
fi

export vector_image_name="${raster_image_name%.*}.svg"
export vector_image_path="$(pwd)/$vector_image_name"

raster_image_in_base64="$(base64 $raster_image_name)"
raster_image_width="$(identify -format %w $raster_image_name)"
raster_image_height="$(identify -format %h $raster_image_name)"

cat > "$vector_image_name" <<- END
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg
  xmlns="http://www.w3.org/2000/svg"
  xmlns:xlink="http://www.w3.org/1999/xlink">
  <image
    xlink:href="data:image/jpeg;base64,$raster_image_in_base64"
    width="$raster_image_width"
    height="$raster_image_height" />
</svg>
END

osascript open_svg_in_editor.applescript
python3 structure.py "$vector_image_name"
