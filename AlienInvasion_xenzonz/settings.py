"""
Docstring for settings.py
i. Final Project: Alien Invasion
ii. Sam Cocquyt
iii. Define configuration values used throughout the game.

    This module contains the Settings class, which stores the core
    configuration for the Alien Invasion game. These settings include
    window properties, asset file paths, ship behavior, bullet behavior,
    alien behavior, and audio resources. Centralizing these values makes
    the game easier to configure and maintain.

iv. Starter code: https://github.com/xenzonz/Participation-Activity-Unit-12
v. 4/19/2026
"""

from pathlib import Path

class Settings:
    """
    Store all configurable settings for the game.

    The Settings class holds constants and configuration values used by
    multiple parts of the game. This includes screen size, frame rate,
    asset locations, ship attributes, bullet attributes, alien attributes,
    and sound file paths.

    Attributes:
        name (str): The title displayed in the game window.
        screen_w (int): Width of the game window in pixels.
        screen_h (int): Height of the game window in pixels.
        FPS (int): Target frames per second for the game loop.
        bg_file (Path): Path to the background image file.

        ship_file (Path): Path to the ship image file.
        ship_w (int): Width of the ship sprite in pixels.
        ship_h (int): Height of the ship sprite in pixels.
        ship_speed (int | float): Horizontal movement speed of the ship.
        starting_ship_count (int): Number of lives the player starts with.

        bullet_file (Path): Path to the bullet image file.
        laser_sound (Path): Path to the firing sound effect file.
        impact_sound (Path): Path to the collision sound effect file.
        bullet_speed (int | float): Upward movement speed of bullets.
        bullet_w (int): Width of the bullet sprite in pixels.
        bullet_h (int): Height of the bullet sprite in pixels.
        bullet_amount (int): Maximum number of bullets allowed on screen.

        alien_file (Path): Path to the alien image file.
        alien_w (int): Width of the alien sprite in pixels.
        alien_h (int): Height of the alien sprite in pixels.
        fleet_speed (int | float): Horizontal movement speed of the alien fleet.
        fleet_direction (int): Starting horizontal direction of the fleet,
            typically 1 for right and -1 for left.
        fleet_drop_speed (int | float): Vertical distance the fleet drops
            when it reaches a screen edge.
    """

    def __init__(self):
        """
        Initialize all game configuration values.

        This constructor sets the default values for the game window,
        asset paths, ship settings, bullet settings, alien settings,
        and sound resources.

        Returns:
            None
        """

        self.name: str = 'Alien Invasion'
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = Path.cwd() / 'AlienInvasion_xenzonz' / 'Assets' / 'images' / 'Starbasesnow.png'
        
        self.ship_file = Path.cwd() /'AlienInvasion_xenzonz' / 'Assets' / 'images' / 'ship2(no bg).png'
        self.ship_w = 40
        self.ship_h = 60
        self.ship_speed = 5
        self.starting_ship_count = 3

        self.bullet_file = Path.cwd() / 'AlienInvasion_xenzonz' / 'Assets' / 'images' / 'laserBlast.png'
        self.laser_sound = Path.cwd() / 'AlienInvasion_xenzonz' / 'Assets' / 'sound' / 'laser.mp3'
        self.impact_sound = Path.cwd() / 'AlienInvasion_xenzonz' / 'Assets' / 'sound' / 'impactSound.mp3'
        self.bullet_speed = 7
        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_amount = 5

        self.alien_file = Path.cwd() / 'AlienInvasion_xenzonz' / 'Assets' / 'images' / 'enemy_4.png'
        self.alien_w = 60
        self.alien_h = 60
        self.fleet_speed = 2
        self.fleet_direction = 1
        self.fleet_drop_speed = 40