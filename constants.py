from block import Block

BLOCK_REGISTRY = {
    'square_with_hole': Block('SquareHole', 0.85, 0.85),
    'tiny_square': Block('SquareTiny', 0.22, 0.22),
    'long_rectangle': Block('RectBig', 2.06, 0.22),
    'pig': Block('BasicSmall', 0.5, 0.5),
}

# TODO Find a different solution for the following.
MULTIPLIER = 100
'''To convert the dimensions from floting point to integer
in order to avoid the peculiarities of floating point arithmetic.'''

GROUND_HEIGHT = -3.5

BLOCK_STRING = '<Block type="{}" material="{}" x="{}" y="{}" rotation="{}"/>\n'
PIG_STRING = '<Pig type="{}" material="{}" x="{}" y="{}" rotation="{}"/>\n'

# WARNING Science Birds is _very_ picky about its XML. For example, the game
# breaks (the level selection buttons are not rendered in level selection menu)
# if the leading newline in the level template is not trimmed. The same
# peculiarity happens if a <Block> elements start on the same line as the
# <GameObject> element.
LEVEL_TEMPLATE ='''
<?xml version="1.0" encoding="utf-16"?>
<Level width="2">
  <Camera x="0" y="2" minWidth="20" maxWidth="30">
    <Birds>
      <Bird type="BirdRed"/>
    </Birds>
    <Slingshot x="-8" y="-2.5">
      <GameObjects>
        {}
      </GameObjects>
    </Slingshot>
  </Camera>
</Level>
'''
