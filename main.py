from math import sin, cos

import pygame as pg

from components.constants import *
from components.widgets import ControlPanel


def draw_main_components(screen):
    pg.draw.rect(screen, Colors.background_dark, ANIMATION_RECTANGLE)
    pg.draw.rect(screen, Colors.background_semi_dark, CONTROLS_RECTANGLE)


def draw_control_panels(screen):
    surfaces = []
    for harmonic in available_harmonics:
        control_panel = ControlPanel(
            screen=screen,
            harmonic=harmonic,
            left=control_panels_start_pos[0],
            top=control_panels_start_pos[1] + control_panels_height * (harmonic.number - 1),
            width=control_rectangle_width,
            height=control_panels_height
        )
        control_panel.draw()
        surfaces.append((control_panel.surface, (control_panel.left, control_panel.top)))
    screen.blits(surfaces)


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


def draw_grid(screen):
    for i in range(1, 10):
        pg.draw.line(screen, Colors.background_semi_dark, (animation_rectangle_width / 10 * i, 0),
                     (animation_rectangle_width / 10 * i, animation_rectangle_height))
        pg.draw.line(screen, Colors.background_semi_dark, (0, animation_rectangle_height / 10 * i),
                     (animation_rectangle_width, animation_rectangle_height / 10 * i))


def translate_graph_to_global_coordinates(points: [(float, float)]) -> [(float, float)]:
    translated_points = []
    origin_x, origin_y = animation_coordination_system_origin
    for x, y in points:
        translated_point = (
            x * 0.8 * animation_rectangle_width / 2. / pi + origin_x,
            y * 0.8 * animation_rectangle_height / 16. + origin_y
        )
        translated_points.append(translated_point)
    return translated_points


def wave_equation(x: float, amplitude: float, wave_length: float, omega: float, time: float):
    k = 2 * pi / wave_length
    y = 2 * amplitude * sin(k * x) * cos(omega * time)
    return y


class Harmonic:
    def __init__(self, amplitude: float, omega: float, wave_length: float,
                 number: int, color: Colors, is_on: bool = True):
        self.number = number
        self.amplitude = amplitude
        self.omega = omega
        self.wave_length = wave_length
        self.color = color
        self.is_on = is_on

    def calculate(self, x, time) -> (float, float):
        y = wave_equation(
            x=x,
            amplitude=self.amplitude,
            wave_length=self.wave_length,
            omega=self.omega,
            time=time)
        return x, y


def main():
    pg.init()
    pg.display.set_caption('Fala stojąca w strunie')
    screen = pg.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    clock = pg.time.Clock()

    time = 0
    while True:
        # Process player inputs
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit

        draw_main_components(screen=screen)
        draw_grid(screen=screen)
        draw_coordination_system(screen=screen)

        chosen_harmonics = [0, 1, 2, 3, 4]

        lines = []
        for n in chosen_harmonics:
            harmonic = available_harmonics[n]
            points = []
            for i in range(POINTS_AMOUNT):
                x = i * 2. * pi / POINTS_AMOUNT
                point = harmonic.calculate(x, time)
                points.append(point)

            pg.draw.lines(
                surface=screen,
                color=harmonic.color,
                closed=False,
                points=translate_graph_to_global_coordinates(points))

            lines.append(points)

        summed_points = []
        for i in range(POINTS_AMOUNT):
            x = lines[0][i][0]
            y = 0
            for j in range(len(chosen_harmonics)):
                y += lines[j][i][1]
            summed_points.append((x, y))

        pg.draw.lines(
            surface=screen,
            color=Colors.amp_orange,
            closed=False,
            points=translate_graph_to_global_coordinates(summed_points),
            width=4)

        draw_control_panels(screen=screen)

        pg.display.flip()
        clock.tick(60)
        time += .1


if __name__ == "__main__":
    available_harmonics = [
        Harmonic(number=1, amplitude=1, omega=0.1, wave_length=2 * pi / 1, color=Colors.contrast_light),
        Harmonic(number=2, amplitude=1, omega=0.1, wave_length=2 * pi / 2, color=Colors.magenta),
        Harmonic(number=3, amplitude=1, omega=0.1, wave_length=2 * pi / 3, color=Colors.yellow, is_on=False),
        Harmonic(number=4, amplitude=1, omega=0.1, wave_length=2 * pi / 4, color=Colors.green),
        Harmonic(number=5, amplitude=1, omega=0.1, wave_length=2 * pi / 5, color=Colors.cyan),
    ]

    main()
