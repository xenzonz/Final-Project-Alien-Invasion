"""
Docstring for bullet.py
i. Final Project: Alien Invasion
ii. Sam Cocquyt
iii. Define the projectile used by the player's ship.

    This module contains the Bullet class, which represents a single
    projectile fired by the player. A bullet is implemented as a pygame
    sprite that loads its image from the game settings, positions itself
    at the ship's firing point, moves upward each frame, and draws itself
    to the screen.

iv. Starter code: https://github.com/xenzonz/Participation-Activity-Unit-12
v. 4/19/2026
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    """
    Represent a single bullet fired by the player's ship.

    The Bullet class is a pygame sprite that stores references to the
    game screen and settings, loads and scales its image, initializes
    its starting position at the ship's top-center point, updates its
    vertical movement, and draws itself during rendering.

    Attributes:
        screen (pygame.Surface): The game screen where the bullet is drawn.
        settings: The game settings object containing bullet configuration.
        image (pygame.Surface): The bullet image loaded from disk and scaled.
        rect (pygame.Rect): The rectangle used for positioning and collision.
        y (float): The bullet's vertical position stored as a float for
            smoother movement updates.
    """
    def __init__(self, game: 'AlienInvasion'):
        """
        Initialize a bullet at the ship's firing position.

        This constructor stores references to the screen and settings,
        loads and scales the bullet image, positions the bullet at the
        top-center of the player's ship, and stores its vertical position
        as a float to support smooth movement.

        Args:
            game (AlienInvasion): The main game object that created the
                bullet and provides access to the ship, screen, and settings.

        Returns:
            None
        """
        super().__init__()
        
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.bullet_w, self.settings.bullet_h)
            )
        
        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """
        Update the bullet's position for the current frame.

        The bullet moves upward by the configured bullet speed, and the
        updated float position is copied back into the sprite rectangle.

        Returns:
            None
        """
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """
        Draw the bullet on the game screen.

        The bullet image is rendered at its current rectangle position.

        Returns:
            None
        """
        self.screen.blit(self.image, self.rect)

