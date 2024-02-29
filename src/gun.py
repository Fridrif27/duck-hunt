"""
A module defining a Gun class for use in a game.

This module provides a Gun class that represents a gun object in a game. 
The Gun class allows for easy management of gun graphics and rotation.

Classes:
    Gun: A class representing a gun in a game.
"""
import math
import pygame


class Gun:
    """
    A class representing a gun in a game.

    Attributes:
        image_path (str): The path to the image file for the gun.
        initial_position (tuple): The initial position of the gun.
        image (pygame.Surface): The image of the gun.
        rect (pygame.Rect): The rectangular area of the gun's image.
        rotated_image (pygame.Surface): The rotated image of the gun.
        rotated_rect (pygame.Rect): The rectangular area of the rotated gun's image.
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
