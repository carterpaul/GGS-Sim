import pyglet
from pyglet.gl import *

window = pyglet.window.Window(500, 500)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        print("left click at", x, y)

def draw_hexagon(x, y, scale):
    pyglet.graphics.draw_indexed(6, pyglet.gl.GL_TRIANGLES,
        [0, 1, 2, 0, 2, 3, 0, 3, 5, 5, 3, 4],
        ('v2i', (x+0*scale, y+12*scale,
                 x+7*scale, y+16*scale,
                 x+14*scale, y+12*scale,
                 x+14*scale, y+4*scale,
                 x+7*scale, y+0*scale,
                 x+0*scale, y+4*scale))
    )

def draw_hexagons(scale):
    for i in range(10):
        for j in range(10):
            draw_hexagon(14*i*scale, 24*j*scale, scale)
            draw_hexagon(14*i*scale+(7*scale), 24*j*scale+(12*scale), scale)
@window.event
def on_draw():
    draw_hexagons(3)

pyglet.app.run()
