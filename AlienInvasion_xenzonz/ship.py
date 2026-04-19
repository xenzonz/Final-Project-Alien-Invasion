"""
Docstring for ship.py
i. Final Project: Alien Invasion
ii. Sam Cocquyt
iii. Define the player-controlled ship for the game.

    This module contains the Ship class, which represents the player's
    spaceship in Alien Invasion. The ship is responsible for loading and
    drawing its sprite, tracking horizontal movement, staying within screen
    boundaries, managing its attached arsenal, firing bullets, and checking
    for collisions with other sprite groups.

iv. Starter code: https://github.com/xenzonz/Participation-Activity-Unit-12
v. 4/19/2026
"""

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal



class Ship:
    """
    Represent the player's ship.

    The Ship class manages the player-controlled spaceship. It stores
    references to the main game, screen, boundaries, and settings,
    loads and scales the ship image, tracks horizontal movement using
    a float-based x-coordinate, updates bullet state through its
    associated arsenal, draws itself to the screen, fires bullets,
    and checks for collisions with other sprites.

    Attributes:
        game (AlienInvasion): The main game instance that owns the ship.
        settings: The game settings object containing ship-related values.
        screen (pygame.Surface): The game screen where the ship is drawn.
        boundaries (pygame.Rect): The rectangular boundaries of the screen.
        image (pygame.Surface): The ship image loaded from disk and scaled.
        rect (pygame.Rect): The rectangle used for positioning and collision.
        x (float): The ship's horizontal position stored as a float for
            smoother movement updates.
        moving_right (bool): Whether the ship is currently moving right.
        moving_left (bool): Whether the ship is currently moving left.
        arsenal (Arsenal): The projectile manager attached to the ship.
    """
    
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
        """
        Initialize the player's ship.

        This constructor stores references to the game, settings, screen,
        and boundaries, loads and scales the ship image, positions the
        ship at the bottom-center of the screen, initializes movement
        flags, and attaches the provided arsenal.

        Args:
            game (AlienInvasion): The main game object that owns the ship.
            arsenal (Arsenal): The arsenal used to manage the ship's bullets.

        Returns:
            None
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.ship_w, self.settings.ship_h)
            )
        
        self.rect = self.image.get_rect()
        self._center_ship()

        self.moving_right = False
        self.moving_left = False

        self.arsenal = arsenal

    def _center_ship(self):
        """
        Center the ship along the bottom of the screen.

        This method places the ship at the horizontal center of the bottom
        edge of the screen and synchronizes the float-based x-position with
        the rectangle position.

        Returns:
            None
        """
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)


    def update(self):
        """
        Update the ship and its attached arsenal for the current frame.

        This method updates the ship's movement based on the current input
        state and then updates all active bullets managed by the arsenal.

        Returns:
            None
        """
        #updating the position of the ship
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """
        Update the ship's horizontal position.

        The ship moves left or right according to the current movement
        flags and the configured ship speed, while remaining within the
        screen boundaries. The final float position is copied back into
        the rectangle used for rendering and collision.

        Returns:
            None
        """
        temp_speed = self.settings.ship_speed
        
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed

        self.rect.x = self.x


    def draw(self):
        """
        Draw the ship and its bullets to the screen.

        This method first draws the ship's active bullets through the
        arsenal, then draws the ship sprite at its current position.

        Returns:
            None
        """
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    
    def fire(self):
        """
        Attempt to fire a bullet from the ship.

        This method delegates bullet creation to the attached arsenal.

        Returns:
            bool: True if a bullet was successfully fired, otherwise False.
        """
        return self.arsenal.fire_bullet()
    
    def check_collisions(self, other_group):
        """
        Check whether the ship collides with any sprite in another group.

        If a collision is detected, the ship is repositioned to the bottom
        center of the screen and the collision result is returned.

        Args:
            other_group (pygame.sprite.Group): The sprite group to test for
                collisions against the ship.

        Returns:
            bool: True if the ship collided with any sprite in the provided
                group, otherwise False.
        """
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False
    
