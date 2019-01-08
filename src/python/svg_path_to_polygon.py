from sys import argv

from lxml import etree
from svgpathtools import parse_path

SVG_NAMESPACE = '{http://www.w3.org/2000/svg}'
index = argv[1].rfind('.')
file_name = argv[1][0:index]
extension = argv[1][index+1:]
root = etree.parse(file_name + '.' + extension).getroot()
group_element = root.find(f'{SVG_NAMESPACE}g')
path_element = group_element.find(f'{SVG_NAMESPACE}path')
path = parse_path(path_element.get('d'))

NUM_SAMPLES = 1024

polygon = []
for i in range(NUM_SAMPLES):
    polygon.append(path.point(i / (NUM_SAMPLES - 1)))

group_element.remove(path_element)
group_element.insert(0, etree.Element('polygon', points=' '.join(str(p[0]) + ',' + str(p[1]) for p in [(round(e.real, 2), round(e.imag, 2)) for e in polygon])))
etree.ElementTree(root).write(file_name + '-polygon.' + extension, pretty_print=True)
