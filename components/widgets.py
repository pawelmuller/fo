import pygame as pg
from components.constants import *


class ControlPanel:
    """
    This is a component that allows to control properties of a harmonic
    """
    color_circle_radius = 0.01 * SURFACE_HEIGHT

    def __init__(self, *, screen, harmonic, left, top, width, height, font, sub_header_font):
        self.screen = screen
        self.harmonic = harmonic
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.font = font
        self.sub_header_font = sub_header_font
        self.surface = pg.surface.Surface((self.width, self.height))

    def draw(self):
        color = Colors.background_semi_dark if self.harmonic.is_on else Colors.background_semi_dark_off
        self.surface.fill(color)
        pg.draw.circle(
            surface=self.surface,
            color=self.harmonic.color,
            center=(
                0.05 * self.width,
                0.2 * self.height
            ),
            radius=ControlPanel.color_circle_radius
        )
        title_text = self.sub_header_font.render(f"{self.harmonic.number}. harmoniczna", True, Colors.contrast_light)
        amplitude_text = self.font.render("A", True, Colors.contrast_light_blue)
        omega_text = self.font.render("w", True, Colors.contrast_light_blue)
        self.surface.blit(title_text, (0.1 * self.width, 0.07 * self.height))

        self.surface.blit(amplitude_text, (0.04 * self.width, 0.35 * self.height))
        self.surface.blit(omega_text, (0.04 * self.width, 0.65 * self.height))
