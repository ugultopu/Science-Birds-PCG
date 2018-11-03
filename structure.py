from bisect import bisect_left
from configparser import ConfigParser

from shapely.geometry import Polygon

from constants import (BLOCK_REGISTRY,
                       MULTIPLIER,
                       GROUND_HEIGHT,
                       BLOCK_STRING,
                       PIG_STRING,
                       LEVEL_TEMPLATE)


class Structure:
    @staticmethod
    def get_shape_width(shape):
        bounds = shape.bounds
        return bounds[2] - bounds[0]


    @staticmethod
    def get_shape_height(shape):
        bounds = shape.bounds
        return bounds[3] - bounds[1]


    @staticmethod
    def get_number_of_instances_required_to_cover_distance(covered_distance, covering_distance):
        number_of_instances, remainder = divmod(int(covered_distance * MULTIPLIER),
                                                int(covering_distance * MULTIPLIER))
        if remainder:
            number_of_instances += 1
        return number_of_instances


    @staticmethod
    def transpose_and_invert_blocks(blocks):
        """
        The blocks start from top-left and go towards bottom-right. This is not
        practical when constructing a structure. We want to start from
        bottom-left and go towards top-right. Hence, we transpose and invert
        blocks.
        """
        return [column[::-1] for column in map(list, zip(*blocks))]


    def __init__(self,
                 level_path,
                 shape,
                 primary_block,
                 platform_block,
                 num_primary_blocks_on_x_axis):
        self.level_path = level_path
        self.shape = shape
        self.primary_block = primary_block
        self.platform_block = platform_block
        self.num_primary_blocks_on_x_axis = num_primary_blocks_on_x_axis
        self.primary_block_factor = self.get_primary_block_factor(num_primary_blocks_on_x_axis)
        self.factored_primary_block_width, self.factored_primary_block_height = self.get_factored_primary_block_dimensions()
        self.num_primary_blocks_on_y_axis = self.get_number_of_instances_required_to_cover_distance(self.get_shape_height(self.shape), self.factored_primary_block_height)
        self.original_blocks = self.get_blocks()
        self.blocks = self.transpose_and_invert_blocks(self.original_blocks)
        # This is to start from bottom row and go towards the top row, instead
        # of vice-versa.
        self.original_blocks = self.original_blocks[::-1]
        self.platforms = self.get_platforms()


    def get_primary_block_factor(self, num_primary_blocks):
        '''Normally every block has a width and height. However, since we want to
        decide on the number of primary blocks that will exist on an axis of the
        structure, we want to proportionate the primary block dimensions according
        to this number. Hence, we get the multiplier needed to get this number.'''
        shape_width = self.get_shape_width(self.shape)
        target_primary_block_width = shape_width / num_primary_blocks
        return target_primary_block_width / self.primary_block.width


    def get_factored_primary_block_dimensions(self):
        return (self.primary_block.width * self.primary_block_factor,
                self.primary_block.height * self.primary_block_factor)


    def is_tile_mostly_in_shape(self, tile):
        '''We designate an area for the structure and we partition it into small,
        equal tiles. The tiles can be of any size and shape but for simplicity, they
        are usually square. The tiles represent the "primary blocks" that are
        going to form the structure in the output.

        Then, in order to determine whether there should be a block present on a
        given tile or not, we find the intersection area of the tile with the
        structure SVG which is given as the input and if the intersection area is
        greater than half of the tile area, then we return true. Otherwise, we
        return false.
        '''
        return tile.intersection(self.shape).area > tile.area / 2


    def get_blocks(self):
        # Blocks is a boolean array indicating whether or not there is a block
        # in the indicated index.
        blocks = []
        for row in range(self.num_primary_blocks_on_y_axis):
            blocks_in_row = []
            y = self.shape.bounds[1] + row * self.factored_primary_block_height
            for column in range(self.num_primary_blocks_on_x_axis):
                x = self.shape.bounds[0] + column * self.factored_primary_block_width
                tile = Polygon([(x,y),
                                (x + self.factored_primary_block_width, y),
                                (x + self.factored_primary_block_width, y + self.factored_primary_block_height),
                                (x, y + self.factored_primary_block_height)])
                if self.is_tile_mostly_in_shape(tile):
                    blocks_in_row.append(True)
                else:
                    blocks_in_row.append(False)
            blocks.append(blocks_in_row)
        return blocks


    def get_platforms(self):
        '''In order to support blocks without anything underneath, we need to
        insert platforms.
        '''
        platforms = set()
        for column in self.blocks:
            last_element_is_a_gap = True
            for row, tile in reversed(list(enumerate(column))):
                if tile:
                    last_element_is_a_gap = False
                else:
                    if not last_element_is_a_gap:
                        platforms.add(row)
                    last_element_is_a_gap = True
        return platforms


    def get_block_height(self, block_type, index, platforms):
        number_of_platforms = bisect_left(sorted(self.platforms), index)
        total_platform_height = number_of_platforms * self.platform_block.height
        total_primary_block_height = index * self.primary_block.height
        if block_type is self.platform_block:
            total_primary_block_height += self.primary_block.height
        positioning_distance = block_type.height / 2
        return (GROUND_HEIGHT
              + total_platform_height
              + total_primary_block_height
              + positioning_distance)


    def get_lateral_distances_for_platform_blocks(self, index):
        lateral_distances = []
        # WARNING This method assumes that the empty blocks exists only on the
        # beginning and end of a row. If any empty block exists after a
        # non-empty block in the row, this calculation breaks down.
        number_of_empty_blocks_before_the_first_non_empty_block = self.original_blocks[index + 1].index(True)
        number_of_empty_blocks_after_the_last_non_empty_block = self.original_blocks[index + 1][::-1].index(True)
        number_of_primary_blocks_to_cover = (len(self.original_blocks[index + 1])
                                           - number_of_empty_blocks_before_the_first_non_empty_block
                                           - number_of_empty_blocks_after_the_last_non_empty_block)
        platform_center_distance = ((number_of_empty_blocks_before_the_first_non_empty_block
                                   + number_of_primary_blocks_to_cover / 2)) * self.primary_block.width
        distance_to_cover = number_of_primary_blocks_to_cover * self.primary_block.width
        number_of_platform_blocks = self.get_number_of_instances_required_to_cover_distance(distance_to_cover, self.platform_block.width)
        if number_of_platform_blocks % 2 is 0:
            lateral_distances.append(platform_center_distance - self.platform_block.width / 2)
            lateral_distances.append(platform_center_distance + self.platform_block.width / 2)
            number_of_platform_blocks -= 2
        else:
            lateral_distances.append(platform_center_distance)
            number_of_platform_blocks -= 1
        for i in range(int(number_of_platform_blocks / 2)):
            lateral_distances = [lateral_distances[0] - self.platform_block.width] + lateral_distances
            lateral_distances.append(lateral_distances[-1] + self.platform_block.width)
        return lateral_distances


    def get_xml_elements(self):
        primary_block_elements = ''
        for column in range(len(self.blocks)):
            for row in range(len(self.blocks[column])):
                if self.blocks[column][row]:
                    primary_block_elements += BLOCK_STRING.format(self.primary_block.xml_element_name,
                                                                  'stone',
                                                                  column * self.primary_block.width + self.primary_block.width / 2,
                                                                  self.get_block_height(self.primary_block, row, self.platforms),
                                                                  0)
        platform_block_elements = ''
        for platform in self.platforms:
            for lateral_distance in self.get_lateral_distances_for_platform_blocks(platform):
                platform_block_elements += BLOCK_STRING.format(self.platform_block.xml_element_name,
                                                               'stone',
                                                               lateral_distance,
                                                               self.get_block_height(self.platform_block, platform, self.platforms),
                                                               0)
        return primary_block_elements + platform_block_elements


    def construct_structure(self):
        with open(self.level_path, 'w') as level_file:
            level_file.write(LEVEL_TEMPLATE.strip().format(self.get_xml_elements()))


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini')

    structure = Structure(config.get('DEFAULT', 'LevelPath'),
                          Polygon([(0,0),(20,0),(10,20)]),
                          BLOCK_REGISTRY[config.get('DEFAULT', 'PrimaryBlock')],
                          BLOCK_REGISTRY['long_rectangle'],
                          int(config.get('DEFAULT', 'NumberOfPrimaryBlocksOnXAxis'))).construct_structure()
