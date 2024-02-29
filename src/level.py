"""
This module implements the Level class for the Duck Hunt game.
"""


class Level:
    """Class representing a level in the game."""

    def __init__(self, bird_speed, amplitude_y, frequency_y, background, banner_image):
        """
        Initialize a Level object with the specified parameters.
        
        Args:
            bird_speed (float): The speed of the birds in the level.
            amplitude_y (int): The amplitude of the bird's vertical oscillation.
            frequency_y (float): The frequency of the bird's vertical oscillation.
            background (str): The path to the background image for the level.
            banner_image (str): The path to the banner image for the level.
        """
        self.bird_speed = bird_speed
        self.amplitude_y = amplitude_y
        self.frequency_y = frequency_y
        self.background = background
        self.banner_image = banner_image
