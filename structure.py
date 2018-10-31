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
                 p_block,
                 num_p_blocks_on_x_axis):
        self.level_path = level_path
        self.shape = shape
        self.p_block = p_block
        self.num_p_blocks_on_x_axis = num_p_blocks_on_x_axis
        self.p_block_factor = self.get_principal_block_factor(num_p_blocks_on_x_axis)
        self.factored_p_block_width, self.factored_p_block_height = self.get_factored_principal_block_dimensions()
        self.num_p_blocks_on_y_axis = self.get_number_of_instances_required_to_cover_distance(self.get_shape_height(self.shape), self.factored_p_block_height)
        self.blocks = self.transpose_and_invert_blocks(self.get_blocks())


    def get_principal_block_factor(self, num_p_blocks):
        '''Normally every block has a width and height. However, since we want to
        decide on the number of principal blocks that will exist on an axis of the
        structure, we want to proportionate the principal block dimensions according
        to this number. Hence, we get the multiplier needed to get this number.'''
        shape_width = self.get_shape_width(self.shape)
        target_p_block_width = shape_width / num_p_blocks
        return target_p_block_width / self.p_block.width


    def get_factored_principal_block_dimensions(self):
        return (self.p_block.width * self.p_block_factor,
                self.p_block.height * self.p_block_factor)


    def is_tile_mostly_in_shape(self, tile):
        '''We designate an area for the structure and we partition it into small,
        equal tiles. The tiles can be of any size and shape but for simplicity, they
        are usually square. The tiles represent the "principal blocks" that are
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
        for row in range(self.num_p_blocks_on_y_axis):
            blocks_in_row = []
            y = self.shape.bounds[1] + row * self.factored_p_block_height
            for column in range(self.num_p_blocks_on_x_axis):
                x = self.shape.bounds[0] + column * self.factored_p_block_width
                tile = Polygon([(x,y),
                                (x + self.factored_p_block_width, y),
                                (x + self.factored_p_block_width, y + self.factored_p_block_height),
                                (x, y + self.factored_p_block_height)])
                if self.is_tile_mostly_in_shape(tile):
                    blocks_in_row.append(True)
                else:
                    blocks_in_row.append(False)
            blocks.append(blocks_in_row)
        return blocks


    def get_xml_elements_for_primary_blocks(self):
        elements = ''
        for column in range(len(self.blocks)):
            for row in range(len(self.blocks[column])):
                if self.blocks[column][row]:
                    elements += BLOCK_STRING.format(self.p_block.xml_element_name,
                                                    'stone',
                                                    column * self.p_block.width + self.p_block.width / 2,
                                                    GROUND_HEIGHT + row * self.p_block.height + self.p_block.height / 2,
                                                    0)
        return elements


    def construct_structure(self):
        with open(self.level_path, 'w') as level_file:
            level_file.write(LEVEL_TEMPLATE.strip().format(self.get_xml_elements_for_primary_blocks()))


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini')

    structure = Structure(config.get('DEFAULT', 'LevelPath'),
                          Polygon([(0,0),(0,10),(10,10),(10,0)]),
                          BLOCK_REGISTRY[config.get('DEFAULT', 'PrimaryBlock')],
                          10).construct_structure()
