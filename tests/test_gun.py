# pylint: disable=W0621
# pylint: disable=E0401
# pylint: disable=C0301

"""
This module defines a Gun class for a simple game.
"""
import math
import pygame
import pytest
from src.gun import Gun

pygame.display.init()


# Define fixtures for common objects used in tests
@pytest.fixture
def gun_instance():
    """
            Fixture to provide an instance of the Gun class for testing.

            Returns:
                Gun: An instance of the Gun class.
            """
    pygame.display.set_mode((800, 600))
    initial_position = (400, 300)
    return Gun("assets/gun/Gun.png", initial_position)


# Define test cases for Gun class
def test_gun_initialization(gun_instance):
    """
            Test the initialization of the Gun class.

            Args:
                gun_instance: A fixture providing an instance of the Gun class.
            """
    assert isinstance(gun_instance.image, pygame.Surface)
    assert isinstance(gun_instance.rect, pygame.Rect)
    assert gun_instance.rect.center == (400, 300)
    assert isinstance(gun_instance.rotated_image, pygame.Surface)
    assert isinstance(gun_instance.rotated_rect, pygame.Rect)
    assert gun_instance.rotated_rect.center == (400, 300)


def test_gun_update_rotates_image(gun_instance, mocker):
    """
           Test the update method of the Gun class to ensure it rotates the image correctly.

           Args:
               gun_instance: A fixture providing an instance of the Gun class.
               mocker: A fixture provided by pytest for mocking objects.

           This test mocks the mouse position to simulate movement and then checks if the update method
           correctly rotates the gun image.
           """
    mocker.patch("pygame.mouse.get_pos", return_value=(500, 400))  # Mock mouse position
    gun_instance.update()

    # Check if the image has been rotated
    assert gun_instance.image != gun_instance.rotated_image

    # Check if the rotated image rect center remains the same
    assert gun_instance.rotated_rect.center == (400, 300)


def test_gun_update_rotates_image_correctly(gun_instance, mocker):
    """
            Test that the update method of the Gun class rotates the image correctly.

            Args:
                gun_instance: A fixture providing an instance of the Gun class.
                mocker: A fixture provided by pytest for mocking objects.

            This test mocks the mouse position to simulate movement and then checks if the update method
            correctly rotates the gun image. It also verifies that the rotation is performed correctly
            based on the mouse position.
            """
    mocker.patch("pygame.mouse.get_pos", return_value=(500, 300))  # Mock mouse position
    gun_instance.update()

    # Check if the rotated image is rotated correctly
    assert gun_instance.rotated_image != gun_instance.image
    assert math.isclose(gun_instance.rotated_rect.centerx, 400, abs_tol=1)
    assert (
        gun_instance.rotated_rect.centery <= 300
    )  # Assuming the gun rotates counterclockwise
