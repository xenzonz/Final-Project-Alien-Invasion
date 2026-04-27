"""
Docstring for hud.py
i. Final Project: Alien Invasion
ii. Sam Cocquyt
iii. Display and update the game's heads-up display.

    This module defines the HUD class, which is responsible for rendering the
    player's score, high score, maximum score, current level, and remaining lives
    on the game screen. 

iv. Starter code: https://github.com/xenzonz/Participation-Activity-Unit-12
v. 4/19/2026
"""

import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    

class HUD:
    """
    Manage the visual display of game statistics on the screen.
    """
    def __init__(self, game: 'AlienInvasion'):
        """
        Initialize the HUD using the main game instance.

        Args:
            game: The main AlienInvasion game object that provides access to
                settings, the screen, and game statistics.
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.game_stats = game.game_stats
        self.font = pygame.font.Font(self.settings.font_file,
            self.settings.HUD_font_size)
        self.padding = 10
        self.update_scores()
        self._setup_life_image()
        self.update_level()

    def _setup_life_image(self):
        """
        Load, scale, and prepare the ship image used to show remaining lives.
        """
        self.life_image = pygame.image.load(self.settings.ship_file)
        self.life_image = pygame.transform.scale(self.life_image, (
            self.settings.ship_w, self.settings.ship_h
            ))
        self.life_rect = self.life_image.get_rect()

    

    def update_scores(self):
        """
        Update all score-related images shown on the HUD.
        """
        self._update_score()
        self._update_hi_score()
        self._update_max_score()

    def _update_score(self):
        """
        Create and position the image for the player's current score.
        """
        score_str = f'Score: {self.game_stats.score: ,.0f}'
        self.score_image = self.font.render(score_str, True, 
            self.settings.text_color, None)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.boundaries.right - self.padding
        self.score_rect.bottom = self.boundaries.bottom - self.padding

    def _update_max_score(self):
        """
        Create and position the image for the maximum possible score.
        """
        max_score_str = f'Max Score: {self.game_stats.max_score: ,.0f}'
        self.max_score_image = self.font.render(max_score_str, True, 
            self.settings.text_color, None)
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.right = self.boundaries.right - self.padding
        self.max_score_rect.bottom = self.score_rect.top - self.padding

    def _update_hi_score(self):
        """
        Create and position the image for the saved high score.
        """
        hi_score_str = f'Hi-Score: {self.game_stats.hi_score: ,.0f}'
        self.hi_score_image = self.font.render(hi_score_str, True, 
            self.settings.text_color, None)
        self.hi_score_rect = self.hi_score_image.get_rect()
        self.hi_score_rect.midtop = (self.boundaries.centerx, self.padding)

    def update_level(self):
        """
        Create and position the image for the current game level.
        """
        level_str = f'Level: {self.game_stats.level: ,.0f}'
        self.level_image = self.font.render(level_str, True, 
            self.settings.text_color, None)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.padding
        self.level_rect.bottom = self.boundaries.bottom - self.padding
    
    def _draw_lives(self):
        """
        Draw one ship image for each remaining player life.
        """
        current_x = self.padding
        current_y = self.level_rect.top - self.life_rect.height - self.padding

        for _ in range(self.game_stats.ships_left):
            self.screen.blit(self.life_image, (current_x, current_y))
            current_x += self.life_rect.width + self.padding

    def draw(self):
        """
        Draw the complete HUD on the screen.
        """
        self.screen.blit(self.hi_score_image, self.hi_score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self._draw_lives()

        