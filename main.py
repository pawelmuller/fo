from math import pi, sin, cos

import pygame as pg

from components.constants import Colors


POINTS_AMOUNT = 600


SURFACE_WIDTH = 1280
SURFACE_HEIGHT = 720

animation_rectangle_width = SURFACE_WIDTH
animation_rectangle_height = 420
animation_coordination_system_origin = (0.1 * animation_rectangle_width, 0.5 * animation_rectangle_height)

control_rectangle_width = SURFACE_WIDTH
control_rectangle_height = 300

ANIMATION_RECTANGLE = pg.Rect(0, 0, animation_rectangle_width, animation_rectangle_height)
CONTROLS_RECTANGLE = pg.Rect(0, 420, control_rectangle_width, control_rectangle_height)


def draw_main_components(screen):
    pg.draw.rect(screen, Colors.background_dark, ANIMATION_RECTANGLE)
    pg.draw.rect(screen, Colors.background_semi_dark, CONTROLS_RECTANGLE)


def draw_coordination_system(screen):
    pg.draw.line(surface=screen,
                 color=Colors.contrast_light,
                 start_pos=(animation_rectangle_width / 10, animation_rectangle_height / 10),
                 end_pos=(animation_rectangle_width / 10, animation_rectangle_height / 10 * 9),
                 width=3)
    pg.draw.line(surface=screen,
                 color=Colors.contrast_light,
                 start_pos=(animation_rectangle_width / 10, animation_rectangle_height / 10 * 5),
                 end_pos=(animation_rectangle_width / 10 * 9, animation_rectangle_height / 10 * 5),
                 width=3)


def translate_graph_to_global_coordinates(points: [(float, float)]) -> [(float, float)]:
    translated_points = []
    origin_x, origin_y = animation_coordination_system_origin
    for x, y in points:
        translated_point = (
            x * 0.8 * animation_rectangle_width / 2. / pi + origin_x,
            y * 0.8 * animation_rectangle_height / 4. + origin_y
        )
        translated_points.append(translated_point)
    return translated_points


def wave_equation(x, amplitude, wave_length, omega, time):
    k = 2 * pi / wave_length
    y = 2 * amplitude * sin(k * x) * cos(omega * time)
    return y


def main():
    pg.init()

    screen = pg.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))

    clock = pg.time.Clock()

    t = 0
    while True:
        t %= 120
        # Process player inputs.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit

        # Do logical updates here.
        points = []
        for i in range(POINTS_AMOUNT):
            x = i * 2. * pi / POINTS_AMOUNT
            amplitude = 0.25
            point = (x, wave_equation(x, amplitude, 1, 0.1, t))
            points.append(point)

        # Translate local coordinates to global system
        translated_points = translate_graph_to_global_coordinates(points)

        # Render the graphics here.
        draw_main_components(screen=screen)
        draw_coordination_system(screen=screen)
        # Temp grid
        for i in range(11):
            pg.draw.line(screen, (90, 90, 90), (animation_rectangle_width / 10 * i, 0),
                         (animation_rectangle_width / 10 * i, animation_rectangle_height))
            pg.draw.line(screen, (90, 90, 90), (0, animation_rectangle_height / 10 * i),
                         (animation_rectangle_width, animation_rectangle_height / 10 * i))

        pg.draw.lines(surface=screen, color=Colors.amp_orange, closed=False, points=translated_points, width=2)

        pg.display.flip()  # Refresh on-screen display
        clock.tick(60)  # wait until next frame (at 60 FPS)
        t += .1


if __name__ == "__main__":
    main()
