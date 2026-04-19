"""
Docstring for alien_invasion.py
i. Final Project: Alien Invasion
ii. Sam Cocquyt
iii. Run the main Alien Invasion game application.

    This module defines the AlienInvasion class, which initializes pygame,
    loads game resources, manages the main game loop, processes user input,
    updates game objects, checks win/loss conditions, handles collisions,
    and redraws the screen each frame. It also contains the script entry
    point used to launch the game directly.

iv. Starter code: https://github.com/xenzonz/Participation-Activity-Unit-12
v. 4/19/2026
"""

import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from arsenal import Arsenal
#from alien import Alien
from alien_fleet import AlienFleet
from time import sleep

class AlienInvasion:
    """
    Manage the overall game state and main execution loop.

    This class serves as the central controller for the game. It is
    responsible for initializing pygame and audio, creating the main
    display surface, loading settings and assets, creating the player
    ship and alien fleet, handling keyboard and quit events, updating
    game objects, checking collisions and game-over conditions, and
    rendering each frame to the screen.

    Attributes:
        settings (Settings): Configuration object containing screen,
            audio, sprite, and gameplay settings.
        game_stats (GameStats): Tracks game-related statistics such as
            the number of ships remaining.
        screen (pygame.Surface): The main display surface used to render
            the game.
        bg (pygame.Surface): The loaded and scaled background image.
        running (bool): Indicates whether the main loop should continue.
        clock (pygame.time.Clock): Controls the game's frame rate.
        laser_sound (pygame.mixer.Sound): Sound played when the ship
            fires a projectile.
        impact_sound (pygame.mixer.Sound): Sound played when a projectile
            collides with an alien.
        ship (Ship): The player-controlled ship.
        alien_fleet (AlienFleet): The fleet of enemy aliens.
        game_active (bool): Indicates whether gameplay is currently active
            or if the game has ended.
    """

    def __init__(self):
        """
        Initialize the game and load all required resources.

        This constructor initializes pygame, loads settings and game
        statistics, creates the display window, loads and scales the
        background image, initializes audio, loads sound effects,
        creates the player ship and alien fleet, and sets the initial
        game state.

        Returns:
            None
        """
        pygame.init()
        self.settings = Settings()
        self.game_stats = GameStats(self.settings.starting_ship_count)

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
            )
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, 
            (self.settings.screen_w, self.settings.screen_h)
            )



        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.2)

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.2)

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet() #<- bug, basically causes alien fleet to have 2 lives because it generates the fleet twice
        self.game_active = True
    
    def run_game(self):
        """
        Start and maintain the main game loop.

        The game loop continues while the application is running. During
        each frame it checks for input events, updates active game objects,
        checks for collisions, redraws the screen, and enforces the target
        frame rate.

        Returns:
            None
        """
        #game loop

        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

            
    def _check_collisions(self):
        """
        Check collisions and other game-state conditions.

        This method handles collisions between the ship and aliens,
        detects whether the alien fleet has reached the bottom of the
        screen, checks collisions between player projectiles and aliens,
        plays impact audio when needed, and resets the level when the
        fleet has been completely destroyed.

        Returns:
            None
        """
        #check collisions for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()

            #subract one life if possible

        #check collisions for aliens and bottom of screen
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()
        #check collision of projectiles and aliens
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()

    def _check_game_status(self):
        """
        Update the game state after the player loses a life.

        If the player still has ships remaining, one life is removed,
        the level is reset, and the game briefly pauses. If no ships
        remain, the game is marked inactive.

        Returns:
            None
        """
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False

        
        

    def _reset_level(self):
        """
        Reset the current level state.

        This clears all active projectiles, removes all aliens from the
        current fleet, and creates a new alien fleet for the next life
        or next wave.

        Returns:
            None
        """
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def _update_screen(self):
        """
        Redraw all visible game elements to the screen.

        This method draws the background, the player ship, and the alien
        fleet, then updates the display so the rendered frame appears
        on screen.

        Returns:
            None
        """
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        pygame.display.flip()

    def _check_events(self):
        """
        Process all pending pygame events.

        This method handles window close events as well as keyboard
        press and release events, routing input to the appropriate
        helper methods.

        Returns:
            None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keyup_events(self, event):
        """
        Handle key release events.

        This method stops ship movement when the left or right arrow
        key is released.

        Args:
            event (pygame.event.Event): The pygame event object
                representing the released key.

        Returns:
            None
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_keydown_events(self, event):
        """
        Handle key press events.

        This method starts ship movement when the left or right arrow
        key is pressed, attempts to fire a projectile when the spacebar
        is pressed, and exits the game when the Q key is pressed.

        Args:
            event (pygame.event.Event): The pygame event object
                representing the pressed key.

        Returns:
            None
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(500)
            
        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()
        

if __name__ == '__main__':
    """
    Launch the game when this file is run as a script.

    This block creates an AlienInvasion instance and starts the
    main game loop.
    """
    ai = AlienInvasion()
    
    ai.run_game()
