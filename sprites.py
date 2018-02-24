# import cocos
import pyglet

def getBearSprite():
    # load the example running.png as a pyglet image
    spritesheet = pyglet.image.load('assets/bear.png')

    # use ImageGrid to divide your sprite sheet into smaller regions
    grid = pyglet.image.ImageGrid(spritesheet, 2, 2, item_width=30, item_height=30)

    # convert to TextureGrid for memory efficiency
    textures = pyglet.image.TextureGrid(grid)

    # access the grid images as you would items in a list
    # this way you get a sequence for your animation
    bearUp = textures[:2]
    bearSide = textures[2:4]

    # create pyglet animation objects from the sequences
    movingUp = pyglet.image.Animation.from_image_sequence(bearUp, 0.2, loop=True)
    movingSide = pyglet.image.Animation.from_image_sequence(bearSide, 0.2, loop=True)
    return movingSide

