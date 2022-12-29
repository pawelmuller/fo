from math import pi

import pygame as pg


class Colors:
    white = (255, 255, 255)
    black = (0, 0, 0)

    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    cyan = (0, 255, 255)
    magenta = (255, 0, 255)
    yellow = (255, 255, 0)

    gray = (128, 128, 128)

    # Backgrounds
    background_dark = (16, 23, 38)
    background_semi_dark = (38, 41, 61)
    background_semi_dark_off = (32, 34, 51)

    # Contrasting
    contrast_light = (234, 235, 252)
    contrast_light_blue = (162, 218, 240)
    contrast_blue = (78, 172, 210)

    # Special
    amp_orange = (236, 103, 37)
    transparent = (1, 1, 1)


POINTS_AMOUNT = 600
REFRESH_RATE = 60
SOUND_SAMPLING_RATE = 44100

SURFACE_WIDTH = 1280
SURFACE_HEIGHT = 720

control_rectangle_width = 360
control_rectangle_height = SURFACE_HEIGHT

animation_rectangle_width = SURFACE_WIDTH - control_rectangle_width
animation_rectangle_height = SURFACE_HEIGHT
animation_coordination_system_origin = (0.1 * animation_rectangle_width, 0.5 * animation_rectangle_height)

ANIMATION_RECTANGLE = pg.Rect(0, 0, animation_rectangle_width, animation_rectangle_height)
CONTROLS_RECTANGLE = pg.Rect(animation_rectangle_width, 0, control_rectangle_width, control_rectangle_height)

control_panels_height = 0.15 * control_rectangle_height
control_panels_header_height = control_panels_height * 1.5
control_panels_start_pos = (animation_rectangle_width, control_panels_header_height)
