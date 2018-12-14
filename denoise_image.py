from sys import argv

from imageio import imread, imwrite
from scipy.ndimage import median_filter

imwrite(argv[2], median_filter(imread(argv[1]), 10))
