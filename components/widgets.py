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

        self.toggle_button_left = 0.75 * self.width
        self.toggle_button_top = 0.1 * self.height
        self.toggle_button = ToggleButton(
            screen=self.surface,
            left=self.toggle_button_left, top=self.toggle_button_top,
            font=self.font,
            initial_state=self.harmonic.is_on
        )

        self.sliders_left = 0.1 * self.width
        self.amplitude_slider_top = 0.35 * self.height
        self.omega_slider_top = 0.65 * self.height
        self.amplitude_slider = Slider(
            screen=self.surface,
            value=self.harmonic.amplitude, maximum_value=1, minimum_value=0,
            left=self.sliders_left, top=self.amplitude_slider_top,
            font=font
        )
        self.omega_slider = Slider(
            screen=self.surface,
            value=self.harmonic.omega, maximum_value=1, minimum_value=0,
            left=self.sliders_left, top=self.omega_slider_top,
            font=font
        )

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
        self.surface.blit(title_text, (0.1 * self.width, 0.07 * self.height))

        self.toggle_button.draw()

        amplitude_text = self.font.render("A", True, Colors.contrast_light_blue)
        self.surface.blit(amplitude_text, (0.04 * self.width, 0.35 * self.height))
        self.amplitude_slider.draw()

        omega_text = self.font.render("ω", True, Colors.contrast_light_blue)
        self.surface.blit(omega_text, (0.04 * self.width, 0.65 * self.height))
        self.omega_slider.draw()

    def handle_event(self, event):
        change_toggle, state = self.toggle_button.handle_event(event,
                                                               self.left + self.toggle_button_left,
                                                               self.top + self.toggle_button_top)
        if change_toggle:
            state = self.toggle_button.state
            self.harmonic.is_on = state
            if state is False and self.harmonic.sound is not None:
                self.harmonic.sound.stop()

        if self.harmonic.is_on:
            change_amplitude = self.amplitude_slider.handle_event(event,
                                                                  self.left + self.sliders_left,
                                                                  self.top + self.amplitude_slider_top)
            self.harmonic.amplitude = self.amplitude_slider.value

            change_omega = self.omega_slider.handle_event(event,
                                                          self.left + self.sliders_left,
                                                          self.top + self.omega_slider_top)
            if change_omega:
                self.harmonic.omega = self.omega_slider.value

            if (change_amplitude or change_omega) and self.harmonic.sound is not None:
                self.harmonic.sound.stop()
                self.harmonic.calculate_sound()
                self.harmonic.sound.play(loops=-1)


class Slider:
    def __init__(self, screen, value, maximum_value, minimum_value, left, top, font, thickness=3):
        self.screen = screen
        self.value = value
        self.maximum_value = maximum_value
        self.minimum_value = minimum_value
        self.left = left
        self.top = top
        self.font = font

        self.rect_margin_left = 10
        self.rect_margin_top = 8
        self.width = 150
        self.thickness = thickness

        self.surf = pg.surface.Surface((0.7 * control_rectangle_width, 0.25 * control_panels_height))
        self.hit = False
        self.button_surf = self.render()
        self.button_rect = None

    def render(self):
        pg.draw.rect(self.surf, Colors.white, [self.rect_margin_left, self.rect_margin_top, self.width, self.thickness])
        button_surf = pg.surface.Surface((20, 20))
        button_surf.set_colorkey(Colors.black)
        pg.draw.circle(button_surf, Colors.amp_orange, (10, 10), 8)
        return button_surf

    def draw(self):
        surf = self.surf.copy()
        pos = (
            self.rect_margin_left + int(
                (self.value - self.minimum_value) / (self.maximum_value - self.minimum_value) * self.width),
            self.rect_margin_top + 0.5 * self.thickness
        )
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)

        value_text = self.font.render(f"{self.value:.2f}", True, Colors.contrast_light)
        surf.blit(value_text, (self.width + 20, 0.5 * self.thickness - 5))

        self.button_rect.move_ip(self.left, self.top)
        self.screen.blit(surf, (self.left, self.top))

    def move(self, absolute_left):
        value_position = (pg.mouse.get_pos()[0] - absolute_left - self.rect_margin_left) / self.width
        scale = (self.maximum_value - self.minimum_value) + self.minimum_value
        self.value = value_position * scale
        if self.value < self.minimum_value:
            self.value = self.minimum_value
        if self.value > self.maximum_value:
            self.value = self.maximum_value

    def handle_event(self, event, absolute_left, absolute_top):
        mouse_absolute_position_x, mouse_absolute_position_y = pg.mouse.get_pos()
        mouse_relative_position = (
            mouse_absolute_position_x - absolute_left + self.left,
            mouse_absolute_position_y - absolute_top + self.top
        )

        if event.type == pg.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(mouse_relative_position):
                self.hit = True
            return False
        elif event.type == pg.MOUSEBUTTONUP:
            self.hit = False
            return True
        elif event.type == pg.MOUSEMOTION:
            if self.hit:
                self.move(absolute_left)
                return False
            return False
        return False


class ToggleButton:
    def __init__(self, screen, left, top, font, initial_state=True):
        background_rectangle = pg.Rect(0, 0, 10, 10)
        pg.draw.rect(screen, Colors.gray, background_rectangle)

        self.screen = screen
        self.left = left
        self.top = top
        self.font = font
        self.state = initial_state

        self.width = 0.2 * control_rectangle_width
        self.height = 0.2 * control_panels_height

        self.surface = pg.surface.Surface((self.width, self.height))
        self.background_rectangle = pg.Rect(0, 0, self.width, self.height)

    def draw(self):
        pg.draw.rect(self.surface, Colors.gray, self.background_rectangle)

        if self.state:
            rectangle = pg.Rect(0.4 * self.width, 0, 0.6 * self.width, self.height)
            pg.draw.rect(self.surface, Colors.green, rectangle)

            text = self.font.render("On", True, Colors.black)
            self.surface.blit(text, (0.55 * self.width, 0.05 * self.height))

        else:
            rectangle = pg.Rect(0, 0, 0.6 * self.width, self.height)
            pg.draw.rect(self.surface, Colors.red, rectangle)

            text = self.font.render("Off", True, Colors.white)
            self.surface.blit(text, (0.05 * self.width, 0.05 * self.height))

        self.screen.blit(self.surface, (self.left, self.top))

    def change_state(self):
        self.state = not self.state
        self.draw()

    def handle_event(self, event, absolute_left, absolute_top):
        mouse_absolute_position_x, mouse_absolute_position_y = pg.mouse.get_pos()
        mouse_relative_position = (
            mouse_absolute_position_x - absolute_left,
            mouse_absolute_position_y - absolute_top
        )

        if event.type == pg.MOUSEBUTTONDOWN:
            if self.background_rectangle.collidepoint(mouse_relative_position):
                self.change_state()
                return True, self.state
        return False, self.state
