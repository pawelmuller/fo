import pygame as pg
from components.constants import *


class ControlPanel:
    """
    This is a component that allows to control properties of a harmonic
    """
    color_circle_radius = 0.01 * SURFACE_HEIGHT

    def __init__(self, *, screen, harmonic, left, top, width, height):
        self.screen = screen
        self.harmonic = harmonic
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.surface = pg.surface.Surface((self.width, self.height))

    def draw(self):
        color = Colors.background_semi_dark if self.harmonic.is_on else Colors.background_semi_dark_off
        self.surface.fill(color)
        pg.draw.circle(
            surface=self.surface,
            color=self.harmonic.color,
            center=(
                0.05 * self.width,
                0.15 * self.height
            ),
            radius=ControlPanel.color_circle_radius
        )
