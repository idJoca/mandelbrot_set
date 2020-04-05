from __future__ import annotations
from pygame import Surface, Vector2, Color
from pygame.draw import line
from pygame.gfxdraw import aacircle


class Axis():
    AXIS_COLOR = Color(255, 255, 255)

    def __init__(self, screen_size: Vector2):
        self.center = screen_size / 2
        self.screen_size = screen_size

    def draw(self, canvas: Surface):
        # Horizontal axis line
        line(canvas, Axis.AXIS_COLOR, Vector2(0, self.center.y),
             Vector2(self.screen_size.x, self.center.y))
        # Vertical axis line
        line(canvas, Axis.AXIS_COLOR, Vector2(self.center.x, 0),
             Vector2(self.center.x, self.screen_size.y))

    def draw_unit_circle(self, canvas: Surface, scale: int):
        aacircle(canvas, int(self.center.x), int(self.center.y), scale, Axis.AXIS_COLOR)
