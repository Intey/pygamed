from cocos.layer import Layer
from cocos.text import Label
from cocos.layer.util_layers import ColorLayer

class HUD(Layer):
    """ Game HUD """
    def __init__(self, player, width, height):
        Layer.__init__(self)
        self.width = width
        self.height = height
        self.player = player.domain
        msg = Label('health %s, sticks: %s' % (self.player.health,
                                               self.player.inventory.get('sticks', 0)),
                    font_name='somebitch',
                    anchor_x='left',
                    anchor_y='bottom',  # really - it's top of screen
                    width=width,
                    height=25,
                    x=5,
                    y=-3,
                    )

        color = (73, 106, 44, 255)
        hudBackground = ColorLayer(*color, width=self.width, height=25)
        hudBackground.position= (0, 0)
        self.add(hudBackground)
        self.add(msg, name='msg')
        self.schedule(self.update)

    def update(self, dt):
        p = self.player
        hp = p.health
        label = self.get('msg').element
        label.begin_update()
        label.text = 'health {}, sticks: {}'.format(hp,
                                                    p.inventory.get('sticks', 0))
        label.end_update()

