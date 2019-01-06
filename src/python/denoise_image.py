from sys import argv

from imageio import imread, imwrite
from scipy.ndimage import gaussian_filter, median_filter

imwrite(argv[2], gaussian_filter(median_filter(imread(argv[1]), 10), 10))
