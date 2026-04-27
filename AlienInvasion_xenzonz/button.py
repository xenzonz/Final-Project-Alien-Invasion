"""
Docstring for button.py
i. Final Project: Alien Invasion
ii. Sam Cocquyt
iii. Create and display clickable buttons for the Alien Invasion game.

    This module defines the Button class, which is used to create interactive
    buttons such as the Play button. The button can display text, draw itself on
    the screen, use a rainbow color effect, and detect mouse clicks.

iv. Starter code: https://github.com/xenzonz/Participation-Activity-Unit-12
v. 4/19/2026
"""

import pygame.font
import math

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Button:
    """
    Represent a clickable button with text and a rainbow background.
    """
    def __init__(self, game: 'AlienInvasion', msg):
        """
        Initialize a button for the game screen.

        Args:
            game: The main AlienInvasion game object that provides access to
                the screen and settings.
            msg: The text displayed on the button.
        """
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings

        self.rainbow_time = 0

        self.font = pygame.font.Font(self.settings.font_file, 
            self.settings.button_font_size)
        self.rect = pygame.Rect(0, 0, self.settings.button_w, self.settings.button_h)
        self.rect.center = self.boundaries.center
        self._prep_msg(msg)

    def _rainbow_color(self):
        """
        Calculate and return the next color in the rainbow animation.

        Returns:
            A tuple containing the red, green, and blue color values.
        """
        self.rainbow_time += 0.05

        red = int((math.sin(self.rainbow_time) + 1) * 127.5)
        green = int((math.sin(self.rainbow_time + 2) + 1) * 127.5)
        blue = int((math.sin(self.rainbow_time + 4) + 1) * 127.5)
        
        return red, green, blue
        
    def _prep_msg(self, msg):
        """
        Create and position the button's text image.

        Args:
            msg: The text displayed on the button.
        """
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = self.rect.centerx
        self.msg_image_rect.centery = self.rect.centery - 2

    def draw(self):
        """
        Draw the button and its text on the screen.
        """
        rainbow_color = self._rainbow_color()

        pygame.draw.rect(self.screen, rainbow_color, self.rect, border_radius=12)

        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos):
        """
        Check whether the button was clicked.

        Args:
            mouse_pos: The current mouse position as an ``(x, y)`` tuple.

        Returns:
            True if the mouse position is inside the button, otherwise False.
        """
        return self.rect.collidepoint(mouse_pos)

