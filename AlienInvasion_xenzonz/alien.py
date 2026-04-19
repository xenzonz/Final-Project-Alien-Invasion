"""
Docstring for alien.py
i. Final Project: Alien Invasion
ii. Sam Cocquyt
iii. Defines the Alien sprite used in the alien fleet.

    This module contains the Alien class, which represents a single enemy
    entity in the game. Each alien is created with a reference to its parent
    fleet and an initial position, and it is responsible for loading its own
    image, tracking its position, updating its movement, checking for screen
    edge collisions, and drawing itself to the screen.

iv. Starter code: https://github.com/xenzonz/Participation-Activity-Unit-12
v. 4/19/2026
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    """
    Represents a single alien enemy in the fleet.

    An Alien is a pygame sprite that belongs to an AlienFleet. It stores
    references to the game screen, screen boundaries, and settings through
    the fleet object. The alien loads and scales its image based on the
    configured settings, tracks its position using both rectangle-based and
    float-based coordinates, and supports movement, edge detection, and
    drawing.

    Attributes:
        fleet (AlienFleet): The fleet this alien belongs to.
        screen (pygame.Surface): The game screen where the alien is drawn.
        boundaries (pygame.Rect): The rectangular boundaries of the screen.
        settings: The game settings object containing alien configuration.
        image (pygame.Surface): The alien image loaded from disk and scaled.
        rect (pygame.Rect): The rectangle used for positioning and collision.
        x (float): The alien's horizontal position stored as a float.
        y (float): The alien's vertical position stored as a float.
    """
    def __init__(self, fleet: 'AlienFleet', x: float, y: float):
        """
        Initialize an alien at the given position.

        This constructor stores references to the fleet and game resources,
        loads and scales the alien image, initializes the alien's rectangle,
        and stores the starting position as both integer rect coordinates
        and float coordinates for smoother movement updates.

        Args:
            fleet (AlienFleet): The fleet that owns this alien.
            x (float): The initial x-coordinate of the alien.
            y (float): The initial y-coordinate of the alien.
        """
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.alien_w, self.settings.alien_h)
            )
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """
        Update the alien's position for the current frame.

        The alien moves horizontally according to the fleet speed and the
        fleet's current movement direction. The updated float position is
        then copied back into the sprite's rectangle so pygame can render
        and collide with it correctly.

        Returns:
            None
        """
        temp_speed = self.settings.fleet_speed

        #if self.check_edges():
            #self.settings.fleet_direction *= -1
            #self.y += self.settings.fleet_drop_speed

        self.x += temp_speed * self.fleet.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y
   

    def check_edges(self):
        """
        Check whether the alien has reached either horizontal screen edge.

        This method determines whether the alien's rectangle has moved past
        the left or right boundary of the screen.

        Returns:
            bool: True if the alien touches or crosses the left or right
                screen boundary, otherwise False.
        """
        return (self.rect.right >= self.boundaries.right or self.rect.left <= self.boundaries.left)

    def draw_alien(self):
        """
        Draw the alien onto the game screen.

        The alien image is drawn at its current rectangle position.

        Returns:
            None
        """
        self.screen.blit(self.image, self.rect)

