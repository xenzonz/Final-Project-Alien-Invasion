"""
Docstring for game_stats.py
i. Final Project: Alien Invasion
ii. Sam Cocquyt
iii. Track, update, and save game statistics.

    This module defines the GameStats class, which stores the player's current
    score, high score, maximum score for the current session, remaining ships, and
    current level. 

iv. Starter code: https://github.com/xenzonz/Participation-Activity-Unit-12
v. 4/19/2026
"""

#from pathlib import Path
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats():
    """
    Store and manage statistics for an Alien Invasion game session.
    """
    def __init__(self, game: 'AlienInvasion'):
        """
        Initialize the game statistics object.

        Args:
            game: The main AlienInvasion game object that provides access to
                settings and score file information.
        """
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self):
        """
        Load the saved high score from the score file if it exists.

        If the score file does not exist or does not contain usable data, the
        high score is set to 0 and a new score file is saved.
        """
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat.__sizeof__() > 20:
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()
            #save the file

    def save_scores(self):
        """
        Save the current high score to the score file.
        """
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent = 4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f"File Not Found: {e}")

    def reset_stats(self):
        """
        Reset statistics that should start fresh when a new game begins.
        """
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1

    def update(self, collisions):
        """
        Update score values after projectile and alien collisions.

        Args:
            collisions: A dictionary-like collection of collision results
                returned by pygame's group collision check.
        """
        #update score
        self._update_score(collisions)
        #update max_score
        self._update_max_score()
        #update hi_score
        self._update_hi_score()


    def _update_max_score(self):
        """
        Update the current session's maximum score if the score increased.
        """
        if self.score > self.max_score:
            self.max_score = self.score
        #print(f"Max: {self.max_score}")

    def _update_hi_score(self):
        """
        Update the saved high score if the current score is higher.
        """
        if self.score > self.hi_score:
            self.hi_score = self.score
        #print(f"Hi: {self.hi_score}")
        
    def _update_score(self, collisions):
        """
        Increase the player's score based on the number of aliens hit.

        Args:
            collisions: A dictionary-like collection where each value represents
                aliens involved in a projectile collision.
        """
        for alien in collisions.values():
            self.score += self.settings.alien_points
        #print(f"Basic: {self.score}")

    def update_level(self):
        """
        Increase the current game level by one.
        """
        self.level += 1
        #print(self.level)
        



        
