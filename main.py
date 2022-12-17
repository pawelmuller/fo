from math import sin, cos

import pygame as pg

from components.constants import *
from components.widgets import ControlPanel


def draw_main_components(screen):
    pg.draw.rect(screen, Colors.background_dark, ANIMATION_RECTANGLE)
    pg.draw.rect(screen, Colors.background_semi_dark, CONTROLS_RECTANGLE)


def draw_control_panel_header(screen, text_font, header_font):
    header_surface = pg.surface.Surface((control_rectangle_width, control_panels_height))
    header_surface.set_colorkey(Colors.black)

    header = header_font.render("Właściwości fal i harmonicznych", True, Colors.white)
    text_1 = text_font.render("A - amplituda", True, Colors.contrast_light_blue)
    text_2 = text_font.render("w - częstość kołowa", True, Colors.contrast_light_blue)
    header_surface.blit(header, (0.05 * control_rectangle_width, 0.1 * control_panels_height))
    header_surface.blit(text_1, (0.05 * control_rectangle_width, 0.5 * control_panels_height))
    header_surface.blit(text_2, (0.05 * control_rectangle_width, 0.7 * control_panels_height))
    screen.blit(header_surface, (animation_rectangle_width, 0))


def draw_control_panel_footer(screen, sub_header_font):
    header_surface = pg.surface.Surface((control_rectangle_width, control_panels_height * 2 / 3))
    header_surface.set_colorkey(Colors.black)

    sub_header_font = sub_header_font.render("Superpozycja fal", True, Colors.white)
    header_surface.blit(sub_header_font, (0.05 * control_rectangle_width, 0.05 * control_panels_height))
    screen.blit(header_surface, (animation_rectangle_width, 0))


def draw_control_panels(screen, text_font, sub_header_font):
    surfaces = []
    for harmonic in available_harmonics:
        control_panel = ControlPanel(
            screen=screen,
            harmonic=harmonic,
            left=control_panels_start_pos[0],
            top=control_panels_start_pos[1] + control_panels_height * (harmonic.number - 1),
            width=control_rectangle_width,
            height=control_panels_height,
            font=text_font,
            sub_header_font=sub_header_font
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


def superpose_waves(wave_points: list[(float, float)]) -> [(float, float)]:
    superposed_wave_points = []
    for i in range(POINTS_AMOUNT):
        x = wave_points[0][i][0]
        y = 0
        for j in range(len(wave_points)):
            y += wave_points[j][i][1]
        superposed_wave_points.append((x, y))
    return superposed_wave_points


class Harmonic:
    def __init__(self, amplitude: float, omega: float, wave_length: float,
                 number: int, color: Colors, is_on: bool = True):
        self.number = number
        self.amplitude = amplitude
        self.omega = omega
        self.wave_length = wave_length
        self.color = color
        self.is_on = is_on
        self.points = []

    def calculate(self, x: float, time: float) -> (float, float):
        k = 2 * pi / self.wave_length
        y = 2 * self.amplitude * sin(k * x) * cos(self.omega * time)
        return x, y

    def calculate_wave_points(self, time) -> [(float, float)]:
        points = []
        for i in range(POINTS_AMOUNT):
            x = i * 2. * pi / POINTS_AMOUNT
            point = self.calculate(x, time)
            points.append(point)

        self.points = points
        return points


class Wave:
    def __init__(self, points, color, width: int = 1):
        self.points = points
        self.color = color
        self.width = width

    def __add__(self, other):
        if len(self.points) != len(other.points):
            raise ArithmeticError

        superposed_wave_points = []
        for self_point, other_point in zip(self.points, other.points):
            new_point = (self_point[0], self_point[1] + other_point[1])
            superposed_wave_points.append(new_point)

        return Wave(points=superposed_wave_points, color=self.color, width=self.width)

    def draw(self, screen):
        pg.draw.lines(
            surface=screen,
            color=self.color,
            closed=False,
            points=translate_graph_to_global_coordinates(self.points),
            width=self.width
        )


def main():
    pg.init()
    pg.display.set_caption('Fala stojąca w strunie')
    screen = pg.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    clock = pg.time.Clock()

    text_font = pg.font.SysFont("sourcesanspro", 16)
    header_font = pg.font.SysFont("sourcesanspro", 24)
    sub_header_font = pg.font.SysFont("sourcesanspro", 20)

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
        draw_control_panel_header(screen=screen, text_font=text_font, header_font=header_font)

        superposed_wave_initial_points = [(i * 2. * pi / POINTS_AMOUNT, 0) for i in range(POINTS_AMOUNT)]
        superposed_wave = Wave(points=superposed_wave_initial_points, color=Colors.amp_orange, width=4)
        for harmonic in available_harmonics:
            if harmonic.is_on is False:
                continue
            points = harmonic.calculate_wave_points(time=time)
            wave = Wave(points, harmonic.color)
            wave.draw(screen=screen)
            superposed_wave += wave

        superposed_wave.draw(screen=screen)
        draw_control_panels(screen=screen, text_font=text_font, sub_header_font=sub_header_font)

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
