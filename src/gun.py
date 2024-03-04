# pylint: disable=R0903
# pylint: disable=E0401

"""
This module provides mathematical functions and constants as well as
a library for creating games and multimedia applications.
"""
import math
import pygame


class Gun:
    """
        This class represents a gun in a game.

        The Gun class provides functionality to handle the appearance and behavior of a gun
        within a game. It allows for loading an image of the gun, updating its rotation based
        on the mouse position, and rendering it on the screen.

        Attributes:
            image: A pygame Surface object representing the image of the gun.
            rect: A pygame Rect object representing the position and dimensions of the gun's image.
            rotated_image: A pygame Surface object representing the rotated image of the gun.
            rotated_rect: A pygame Rect object representing the position
            and dimensions of the rotated gun image.
        """
    def __init__(self, image_path, initial_position):
        """
        Initialize the Gun object with its image and initial position.

        Args:
            image_path (str): The path to the image file for the gun.
            initial_position (tuple): The initial position of the gun.
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect(center=initial_position)
        self.rotated_image = self.image
        self.rotated_rect = self.rect

    def update(self):
        """
            Update the gun's rotation based on the mouse position.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        offset_x = mouse_x - self.rect.centerx
        offset_y = mouse_y - self.rect.centery
        angle = math.atan2(offset_y, offset_x)
        angle = math.degrees(angle)
        self.rotated_image = pygame.transform.rotate(self.image, -angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center)
