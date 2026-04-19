"""
Docstring for game_stats.py
i. Final Project: Alien Invasion
ii. Sam Cocquyt
iii. Store and manage game statistics.

    This module defines the GameStats class, which is responsible for holding
    basic gameplay state values that need to persist while the game is running.
    At the moment, it tracks how many ships the player has left.

iv. Starter code: https://github.com/xenzonz/Participation-Activity-Unit-12
v. 4/19/2026
"""


class GameStats():
    """
    Store gameplay statistics for the current session.

    The GameStats class is a simple container for values that describe
    the current progress or status of the game. In its current form,
    it tracks the number of player ships remaining.

    Attributes:
        ships_left (int): The number of ships the player has remaining.
    """
    def __init__(self, ship_limit):
        """
        Initialize the game statistics.

        This constructor sets the starting number of ships available to
        the player for the current game session.

        Args:
            ship_limit (int): The number of ships the player starts with.

        Returns:
            None
        """
        self.ships_left = ship_limit
        