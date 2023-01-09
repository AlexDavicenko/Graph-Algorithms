import pygame
import pygame.gfxdraw

class Render:
    def __init__(self, window: pygame.Surface):
        self.window = window

    def edge(self, line_points, color):
        pygame.gfxdraw.filled_polygon(self.window, line_points, color)
        pygame.gfxdraw.aapolygon(self.window, line_points, color)

    def arrow(self, points, color):
        pygame.gfxdraw.filled_polygon(self.window, points, color)
        pygame.gfxdraw.aapolygon(self.window, points, color)

#    def node(self, x, y, radius):
