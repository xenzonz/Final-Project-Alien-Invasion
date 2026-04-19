"""
Docstring for alien_fleet.py
i. Final Project: Alien Invasion
ii. Sam Cocquyt
iii. Defines the alien fleet manager for the game.

    This module contains the AlienFleet class, which is responsible for
    creating, positioning, updating, drawing, and managing the collection
    of alien enemies on the screen. The fleet handles group movement,
    edge detection, downward movement when changing direction, collision
    checks, bottom-of-screen detection, and destroyed-state checks.
    
iv. Starter code: https://github.com/xenzonz/Participation-Activity-Unit-12
v. 4/19/2026
"""

import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    


class AlienFleet:
    """
    Manage the collection of alien enemies in the game.

    The AlienFleet class creates a formation of Alien objects and stores
    them in a pygame sprite group. It controls fleet-wide behavior such as
    formation creation, horizontal movement, changing direction at screen
    edges, dropping the fleet downward, drawing all aliens, and checking
    game-relevant states like collisions or whether the fleet has been
    completely destroyed.

    Attributes:
        game (AlienInvasion): The main game instance that owns this fleet.
        settings: The game settings object containing fleet and screen values.
        fleet (pygame.sprite.Group): Group containing all Alien sprites.
        fleet_direction (int): Current horizontal movement direction for the
            fleet, typically 1 for right and -1 for left.
        fleet_drop_speed (int | float): Vertical distance the fleet moves
            downward after hitting a screen edge.
    """
    def __init__(self, game: 'AlienInvasion'):
        """
        Initialize the alien fleet and create its starting formation.

        This constructor stores references to the game and settings, creates
        the sprite group used to hold all aliens, initializes fleet movement
        properties, and immediately generates the fleet formation.

        Args:
            game (AlienInvasion): The main game object that owns this fleet.
        """
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        self.create_fleet()


    def create_fleet(self):
        """
        Create the alien formation using the current screen and alien sizes.

        This method reads alien and screen dimensions from the settings,
        calculates how many aliens can fit in the formation, determines
        offsets needed to center the fleet, and then builds the fleet in
        a triangular arrangement.

        Returns:
            None
        """
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)
        x_offset, y_offset = self.calculate_offsets(alien_w, alien_h, screen_w, fleet_w, fleet_h)

        self._create_triangle_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _create_triangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """
        Create a triangular alien formation.

        This method iterates through a rectangular grid space and only places
        aliens in positions that fall within a triangle shape centered in the
        formation. Each valid position is passed to the helper that creates
        an Alien instance.

        Args:
            alien_w (int | float): Width of a single alien sprite.
            alien_h (int | float): Height of a single alien sprite.
            fleet_w (int): Number of alien slots across the formation.
            fleet_h (int): Number of alien rows in the formation.
            x_offset (int): Horizontal offset used to center the formation.
            y_offset (int): Vertical offset used to position the formation.

        Returns:
            None
        """
        center = fleet_w // 2

        for row in range(fleet_h):
            for col in range(fleet_w):
                current_x = alien_w * col + x_offset
                current_y = alien_h * row + y_offset
                if abs(col - center) > (fleet_h - 1 - row):
                    continue
                self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_w, alien_h, screen_w, fleet_w, fleet_h):
        """
        Calculate offsets used to center the fleet on the screen.

        The horizontal offset centers the fleet within the screen width.
        The vertical offset centers the fleet within the top half of the
        screen so the formation begins higher on the display.

        Args:
            alien_w (int | float): Width of a single alien sprite.
            alien_h (int | float): Height of a single alien sprite.
            screen_w (int): Width of the game screen.
            fleet_w (int): Number of alien slots across the formation.
            fleet_h (int): Number of alien rows in the formation.

        Returns:
            tuple[int, int]: A tuple containing the horizontal and vertical
                offsets as `(x_offset, y_offset)`.
        """
        half_screen = self.settings.screen_h//2
        fleet_horizontal_space = fleet_w * alien_w
        fleet_vertical_space = fleet_h * alien_h
        x_offset = int((screen_w - fleet_horizontal_space)//2)
        y_offset = int((half_screen - fleet_vertical_space)//2)
        return x_offset,y_offset

    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h):
        """
        Calculate the width and height of the alien formation.

        The fleet size is derived from the available screen space and the
        dimensions of each alien sprite. The resulting width and height are
        adjusted to be odd numbers so the triangle formation has a clear
        horizontal center.

        Args:
            alien_w (int | float): Width of a single alien sprite.
            screen_w (int): Width of the game screen.
            alien_h (int | float): Height of a single alien sprite.
            screen_h (int): Height of the game screen.

        Returns:
            tuple[int, int]: A tuple containing the fleet width and fleet
                height as `(fleet_w, fleet_h)`.
        """
        fleet_w = (screen_w//alien_w)
        fleet_h = ((screen_h * 0.75)//alien_h)

        if fleet_w % 2 == 0 :
            fleet_w -= 1 
        else:
            fleet_w -= 2 

        if fleet_h % 2 == 0:
            fleet_h -= 1 
        else:
            fleet_h -= 2 


        return int(fleet_w), int(fleet_h)

        
    def _create_alien(self, current_x: int, current_y: int):
        """
        Create a single alien and add it to the fleet group.

        Args:
            current_x (int): The x-coordinate for the new alien.
            current_y (int): The y-coordinate for the new alien.

        Returns:
            None
        """
        new_alien = Alien(self, current_x, current_y)

        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """
        Check whether any alien in the fleet has reached a screen edge.

        If at least one alien touches the left or right boundary, the entire
        fleet is moved downward and its horizontal direction is reversed.

        Returns:
            None
        """
        alien: 'Alien'
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break
        
    
    def _drop_alien_fleet(self):
        """
        Move every alien in the fleet downward.

        This method is typically called when the fleet reaches a screen edge
        and needs to descend before reversing direction.

        Returns:
            None
        """
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed

    def update_fleet(self):
        """
        Update the fleet for the current frame.

        This method first checks for edge collisions that may require the
        fleet to drop and reverse direction, then updates every alien in the
        fleet.

        Returns:
            None
        """
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self):
        """
        Draw every alien in the fleet to the screen.

        Returns:
            None
        """
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group):
        """
        Check for collisions between the fleet and another sprite group.

        This method uses pygame's `groupcollide` function to detect overlaps
        between aliens in the fleet and sprites in the provided group. Any
        colliding sprites in both groups are removed.

        Args:
            other_group (pygame.sprite.Group): The other sprite group to test
                for collisions against the alien fleet.

        Returns:
            dict: A dictionary mapping collided aliens to lists of sprites
                they collided with.
        """
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    
    def check_fleet_bottom(self):
        """
        Check whether any alien has reached the bottom of the screen.

        Returns:
            bool: True if at least one alien's bottom edge has reached or
                passed the screen height, otherwise False.
        """
        alien: 'Alien'
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False
    
    def check_destroyed_status(self):
        """
        Check whether all aliens in the fleet have been destroyed.

        Returns:
            bool: True if the fleet is empty, otherwise False.
        """
        return not self.fleet
