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
from button import Button
from hud import HUD

class AlienInvasion:
    """
    Manage the main Alien Invasion game application.

    The class is responsible for setting up the game window, loading assets,
    creating game objects, running the main loop, handling events, updating
    gameplay state, checking collisions, and redrawing the screen.
    """
    def __init__(self):
        """
        Initialize the game, settings, assets, sounds, and main objects.

        Sets up Pygame, creates the display surface, loads the background image,
        initializes the score and HUD systems, loads sound effects, creates the
        player's ship, creates the alien fleet, and prepares the Play button.
        The game starts in an inactive state until the player clicks Play.
        """
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()
        

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
            )
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, 
            (self.settings.screen_w, self.settings.screen_h)
            )

        self.game_stats = GameStats(self)
        self.HUD = HUD(self)

        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.2)

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.2)

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()

        self.play_button = Button(self, 'Play')
        self.game_active = False
    
    def run_game(self):
        """
        Run the main game loop until the player quits.

        Each frame, this method checks user input, updates the ship and alien
        fleet while the game is active, checks for collisions, redraws the
        screen, and limits the frame rate using the configured FPS setting.
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
        Check and respond to collisions during active gameplay.

        Handles ship-alien collisions, aliens reaching the bottom of the screen,
        projectile-alien collisions, score updates, impact sounds, HUD updates,
        level resets, difficulty increases, and level display updates when the
        current fleet has been destroyed.
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
            self.game_stats.update(collisions)
            self.HUD.update_scores()

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()
            self.settings.increase_difficulty()
            #update game stats level
            self.game_stats.update_level()
            #update hud view
            self.HUD.update_level()

    def _check_game_status(self):
        """
        Update the game after the player loses a ship.

        If the player has ships remaining, subtracts one life, resets the level,
        and briefly pauses before play continues. If no ships remain, ends the
        active game so the Play button can be shown again.
        """
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False

        
    def _reset_level(self):
        """
        Clear current projectiles and aliens, then create a new fleet.

        This is used after the player loses a ship and after the player destroys
        the full alien fleet, allowing the game to continue with a fresh level.
        """
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def restart_game(self):
        """
        Reset the game state and begin a new active game.

        Restores dynamic settings, resets player statistics, refreshes score
        displays, creates a new level, centers the ship, starts active gameplay,
        and hides the mouse cursor during play.
        """
        self.settings.initialize_dynamic_settings()
        
        self.game_stats.reset_stats()
        self.HUD.update_scores()
        self._reset_level()
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        """
        Draw the current frame and display it on the screen.

        Draws the background, alien fleet, HUD, player ship, and Play button when
        the game is inactive. After drawing all visible objects, flips the
        display buffer so the newest frame appears on screen.
        """
        self.screen.blit(self.bg, (0,0))
        
        self.alien_fleet.draw()
        self.HUD.draw()
        self.ship.draw()
        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)


        pygame.display.flip()

    def _check_events(self):
        """
        Process all pending Pygame events.

        Handles quitting the game, key presses during active gameplay, key
        releases, and mouse clicks on the Play button. When quitting, the method
        saves high score data before closing Pygame and exiting the program.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_stats.save_scores()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        """
        Start a new game if the Play button is clicked.

        Gets the current mouse position, checks whether that position overlaps
        the Play button, and restarts the game when the button is selected.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()



    def _check_keyup_events(self, event):
        """
        Handle key release events for player movement.

        Args:
            event: The Pygame key release event to process.

        Stops horizontal ship movement when the player releases the right or left
        arrow key.
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_keydown_events(self, event):
        """
        Handle key press events for movement, firing, and quitting.

        Args:
            event: The Pygame key press event to process.

        Starts moving the ship when the player presses the arrow keys, fires a
        projectile when the spacebar is pressed, and saves scores before exiting
        when the player presses the Q key.
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
            self.game_stats.save_scores()
            pygame.quit()
            sys.exit()
        

if __name__ == '__main__':
    ai = AlienInvasion()
    
    ai.run_game()
