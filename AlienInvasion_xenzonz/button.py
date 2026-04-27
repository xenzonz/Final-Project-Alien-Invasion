import pygame.font
import math

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Button:
    def __init__(self, game: 'AlienInvasion', msg):
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
        self.rainbow_time += 0.05

        red = int((math.sin(self.rainbow_time) + 1) * 127.5)
        green = int((math.sin(self.rainbow_time + 2) + 1) * 127.5)
        blue = int((math.sin(self.rainbow_time + 4) + 1) * 127.5)
        
        return red, green, blue
        
    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = self.rect.centerx
        self.msg_image_rect.centery = self.rect.centery - 2

    def draw(self):
        rainbow_color = self._rainbow_color()

        pygame.draw.rect(self.screen, rainbow_color, self.rect, border_radius=12)

        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

