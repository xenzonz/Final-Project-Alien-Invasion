"""
Docstring for arsenal.py
i. Final Project: Alien Invasion
ii. Sam Cocquyt
iii. Manage the collection of bullets fired by the player.

    This module defines the Arsenal class, which stores and manages the
    player's active projectiles. It is responsible for creating bullets,
    updating their positions, removing bullets that leave the screen, and
    drawing all active bullets during each frame of the game.

iv. Starter code: https://github.com/xenzonz/Participation-Activity-Unit-12
v. 4/19/2026
"""

import pygame
from typing import TYPE_CHECKING
from bullet import Bullet

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    


class Arsenal: 
    """
    Represent the player's active collection of bullets.

    The Arsenal class manages a pygame sprite group containing all bullets
    currently fired by the player's ship. It provides methods to update
    every bullet, clean up bullets that have moved offscreen, draw bullets
    to the screen, and create new bullets while respecting the configured
    firing limit.

    Attributes:
        game (AlienInvasion): The main game instance that owns this arsenal.
        settings: The game settings object containing bullet-related values.
        arsenal (pygame.sprite.Group): A sprite group containing all active
            Bullet objects currently in play.
    """
    def __init__(self, game: 'AlienInvasion'):
        """
        Initialize the arsenal for the current game.

        This constructor stores references to the game and settings, then
        creates the sprite group used to hold all active bullets.

        Args:
            game (AlienInvasion): The main game object that owns this arsenal.
        """
        self.game = game
        self.settings = game.settings

        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self):
        """
        Update all bullets and remove those that leave the screen.

        This method updates every bullet in the arsenal and then removes
        any bullets whose position has moved above the visible game area.

        Returns:
            None
        """
        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self):
        """
        Remove bullets that have moved off the top of the screen.

        This method safely iterates over a copy of the bullet group so
        bullets can be removed while iterating.

        Returns:
            None
        """
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)

    def draw(self):
        """
        Draw all active bullets to the screen.

        Returns:
            None
        """
        for bullet in self.arsenal:
            bullet.draw_bullet()

    def fire_bullet(self):
        """
        Create and add a new bullet if the bullet limit allows it.

        A new Bullet object is created and added to the arsenal only if
        the number of active bullets is below the configured maximum.

        Returns:
            bool: True if a bullet was successfully created and added,
                otherwise False.
        """
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False


         