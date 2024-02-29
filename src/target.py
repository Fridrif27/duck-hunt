"""
This module implements the Target class for the Duck Hunt game.
"""
import math
import random


class Target:
    """
    Represents a target in the Duck Hunt game.

    Attributes:
        x (int): The x-coordinate of the target.
        y (int): The y-coordinate of the target.
        radius (int): The radius of the target.
        speed (float): The speed at which the target moves horizontally.
        amplitude_y (float): The amplitude of the vertical oscillation motion.
        frequency_y (float): The frequency of the vertical oscillation motion.
        initial_y (int): The initial y-coordinate of the target.
        bird_images (list): A list of images representing the target.
        screen_width (int): The width of the game screen.
    """
    def __init__(self, x, y, radius, speed, amplitude_y, frequency_y, bird_images, screen_width):
        """
        Initialize the Target object.

        Args:
            x (int): The x-coordinate of the target.
            y (int): The y-coordinate of the target.
            radius (int): The radius of the target.
            speed (float): The speed at which the target moves horizontally.
            amplitude_y (float): The amplitude of the vertical oscillation motion.
            frequency_y (float): The frequency of the vertical oscillation motion.
            bird_images (list): A list of images representing the target.
            screen_width (int): The width of the game screen.
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.amplitude_y = amplitude_y
        self.frequency_y = frequency_y
        self.initial_y = y
        self.bird_images = bird_images
        self.current_bird_image = random.choice(bird_images)
        self.screen_width = screen_width

    def move(self):
        """
        Move the target horizontally and update its vertical position based on oscillation motion.
        """
        self.x += self.speed
        self.y = self.amplitude_y * math.sin(self.frequency_y * self.x) + self.initial_y
        self.check_boundary()

    def check_boundary(self):
        """
        Check if the target has moved out of the game screen boundaries and adjust its position if necessary.
        """
        if self.x - self.radius > self.screen_width:
            self.x = -self.radius
        elif self.x + self.radius < 0:
            self.x = self.screen_width + self.radius
