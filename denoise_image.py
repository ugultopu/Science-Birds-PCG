from sys import argv

from imageio import imread, imwrite
from scipy.ndimage import gaussian_filter

imwrite(argv[2], gaussian_filter(imread(argv[1]), 10))
