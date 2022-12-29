from math import sin, cos

import pygame as pg
import numpy as np

from components.constants import *
from components.widgets import ControlPanel


def draw_main_components(screen):
    pg.draw.rect(screen, Colors.background_dark, ANIMATION_RECTANGLE)
    pg.draw.rect(screen, Colors.background_semi_dark, CONTROLS_RECTANGLE)


def draw_control_panel_header(screen, header_font, sub_header_font):
    header_surface = pg.surface.Surface((control_rectangle_width, control_panels_header_height))
    header_surface.set_colorkey(Colors.black)

    header = header_font.render("Właściwości harmonicznych", True, Colors.white)
    header_surface.blit(header, (0.05 * control_rectangle_width, 0.1 * control_panels_header_height))

    sub_header_font = sub_header_font.render("Superpozycja harmonicznych", True, Colors.white)
    header_surface.blit(sub_header_font, (0.1 * control_rectangle_width, 0.42 * control_panels_header_height))

    pg.draw.circle(
        surface=header_surface,
        color=Colors.amp_orange,
        center=(
            0.05 * control_rectangle_width,
            0.5 * control_panels_header_height
        ),
        radius=ControlPanel.color_circle_radius
    )

    screen.blit(header_surface, (animation_rectangle_width, 0))


def draw_control_panels(screen, control_panels: list[ControlPanel]):
    surfaces = []
    for control_panel in control_panels:
        control_panel.draw()
        surfaces.append((control_panel.surface, (control_panel.left, control_panel.top)))
    screen.blits(surfaces)


def create_control_panels(screen, text_font, sub_header_font) -> [ControlPanel]:
    control_panels = []
    for harmonic in available_harmonics:
        control_panel = ControlPanel(
            screen=screen,
            harmonic=harmonic,
            left=control_panels_start_pos[0],
            top=control_panels_start_pos[1] + int(control_panels_height * (harmonic.number - 1)),
            width=control_rectangle_width,
            height=control_panels_height,
            font=text_font,
            sub_header_font=sub_header_font
        )
        control_panels.append(control_panel)
    return control_panels


def draw_coordination_system(screen, header_font):
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
    text = header_font.render(f"A", True, Colors.contrast_light)
    text_position = (
        0.06 * animation_rectangle_width,
        0.08 * animation_rectangle_height
    )
    screen.blit(text, text_position)


def draw_grid(screen):
    for i in range(1, 10):
        pg.draw.line(screen, Colors.background_semi_dark, (animation_rectangle_width / 10 * i, 0),
                     (animation_rectangle_width / 10 * i, animation_rectangle_height))
        pg.draw.line(screen, Colors.background_semi_dark, (0, animation_rectangle_height / 10 * i),
                     (animation_rectangle_width, animation_rectangle_height / 10 * i))


def draw_scale(screen, sub_header_font):
    left_ratio = 0.07
    descriptions = (
        (3, (left_ratio, 0.2)),
        (2, (left_ratio, 0.3)),
        (1, (left_ratio, 0.4)),
        (0, (left_ratio, 0.5)),
        (-1, (left_ratio, 0.6)),
        (-2, (left_ratio, 0.7)),
        (-3, (left_ratio, 0.8)),
    )

    to_blit = []
    for name, position_ratio in descriptions:
        text = sub_header_font.render(f"{name}", True, Colors.contrast_light)
        text_position = (
            position_ratio[0] * animation_rectangle_width,
            (position_ratio[1] - 0.02) * animation_rectangle_height
        )
        to_blit.append((text, text_position))
    screen.blits(to_blit)


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


class Harmonic:
    def __init__(self, amplitude: float, base_frequency: float,
                 number: int, color: Colors, string_length: float = 2 * pi, is_on: bool = True):
        self.number = number
        self.amplitude = amplitude
        self.base_frequency = base_frequency
        self.string_length = string_length
        self.color = color
        self.is_on = is_on

        self.frequency = base_frequency * self.number
        self.omega = 2 * pi * self.frequency
        self.wave_length = 2 * string_length / number
        self.velocity = self.frequency * self.wave_length

        self.points = []
        self.sound = None

    def calculate(self, x: float, time: float) -> (float, float):
        k = self.number * pi / self.string_length
        y = 2 * self.amplitude * sin(k * x) * cos(self.omega / graph_slow_factor * time)
        return x, y

    def calculate_wave_points(self, time, points_amount=POINTS_AMOUNT) -> [(float, float)]:
        points = []
        for i in range(points_amount):
            x = i * 2. * pi / POINTS_AMOUNT
            point = self.calculate(x, time)
            points.append(point)

        self.points = points
        return points

    def calculate_sound(self):
        buffer = np.sin(
            2 * np.pi * self.frequency * np.arange(SOUND_SAMPLING_RATE * 60) / SOUND_SAMPLING_RATE
        ).astype(np.float32)
        self.sound = pg.mixer.Sound(buffer)
        self.sound.set_volume(self.amplitude)


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
    pg.mixer.pre_init(size=32)
    pg.init()
    pg.display.set_caption('Fala stojąca w strunie')
    screen = pg.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    clock = pg.time.Clock()

    text_font = pg.font.SysFont("sourcesanspro", 16)
    header_font = pg.font.SysFont("sourcesanspro", 24)
    sub_header_font = pg.font.SysFont("sourcesanspro", 20)

    control_panels = create_control_panels(screen=screen, text_font=text_font, sub_header_font=sub_header_font)

    for harmonic in available_harmonics:
        if harmonic.is_on is False:
            continue
        harmonic.calculate_sound()
        harmonic.sound.play(loops=-1)

    time = 0
    while True:
        # Handling events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            for control_panel in control_panels:
                control_panel.handle_event(event=event)

        # Drawing main components
        draw_main_components(screen=screen)
        draw_grid(screen=screen)
        draw_coordination_system(screen=screen, header_font=header_font)
        draw_scale(screen=screen, sub_header_font=sub_header_font)
        draw_control_panel_header(screen=screen, text_font=text_font, header_font=header_font)
        draw_control_panels(screen=screen, control_panels=control_panels)

        # Wave physics and superposition
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

        # Refreshing screen
        pg.display.flip()
        clock.tick(REFRESH_RATE)
        time += .1


if __name__ == "__main__":
    graph_slow_factor = 10000
    base_frequency = 110
    available_harmonics = [
        Harmonic(number=1, amplitude=0, base_frequency=base_frequency, color=Colors.contrast_light),
        Harmonic(number=2, amplitude=0, base_frequency=base_frequency, color=Colors.magenta),
        Harmonic(number=3, amplitude=0, base_frequency=base_frequency, color=Colors.yellow),
        Harmonic(number=4, amplitude=0, base_frequency=base_frequency, color=Colors.green),
        Harmonic(number=5, amplitude=0, base_frequency=base_frequency, color=Colors.cyan),
    ]

    main()
