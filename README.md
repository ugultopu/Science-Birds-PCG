# Science Birds PCG

Generate structures in Science Birds from a given image that represents a structure.

## Operation

python3 src/python/main.py [deeplab|gimp] [difficulty:1-4] [file-path]

## requirements

1.Download Science-Birds from https://aibirds.org/other-events/level-generation-competition/basic-instructions.html

2.Change directory in config.in to 'path_to_ScienceBirds/ScienceBirds_Data/StreamingAssets/Levels/'

3.Install tensorflow model : deeplab

4.Install Python3 package:   ImageMagick
							 Potrace
							 SciPy
			  				 Shapely
			  			     imageio
			  				 lxml
							 svgpathtools

## Notice

Deeplab demo only can identify those classes:

		'background',
		'aeroplane', 
		'bicycle', 
		'bird', 
		'boat', 
		'bottle', 
		'bus',
		'car', 
		'cat', 
		'chair', 
		'cow', 
		'diningtable', 
		'dog', 
		'horse', 
		'motorbike',
		'person', 
		'pottedplant', 
		'sheep', 
		'sofa', 
		'train', 
		'tv'

