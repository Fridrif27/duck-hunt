# pylint: disable=no-member
# pylint: disable=W0621
# pylint: disable=E0401

"""
Test cases for the Display class.
"""
import pytest
import pygame
from src.display import (
    Display,
)  # Assuming your Display class is in a file named display.py


# Fixture to initialize a Display object
@pytest.fixture
def display():
    """
           Fixture for initializing and cleaning up a Display instance.

           This fixture initializes a Display instance with a width of 800 and a height of 600
           before each test and cleans up pygame after each test.

           Returns:
               Display: An instance of the Display class.
           """
    pygame.init()
    display = Display(800, 600)
    yield display
    pygame.quit()


# Test display_image method
def test_display_image(display):
    """
            Test the display_image method of the Display class.

            This test function verifies that the display_image method correctly displays
            an image on the display with the specified rectangle coordinates.

            Args:
                display (Display): An instance of the Display class.

            Note:
                This test requires a mock test image and rectangle coordinates.
                Add assertions to verify that the image was displayed correctly.
            """
    # Assuming you have some test images
    test_image = pygame.Surface((100, 100))  # Mock test image
    rect = (0, 0, 100, 100)  # Mock rect
    display.display_image(test_image, rect)
    # Add assertions here to verify that the image was displayed correctly


# Test display_paused_menu method
def test_display_paused_menu(display):
    """
            Test the display_paused_menu method of the Display class.

            This test function verifies that the display_paused_menu method correctly displays
            the paused menu with the specified background image, main menu button image, resume
            button image, main menu button rectangle, and resume button rectangle.

            Args:
                display (Display): An instance of the Display class.

            Note:
                This test requires mock images and rectangles for the paused menu components.
                Add assertions to verify that the paused menu is displayed correctly.
            """
    # Assuming you have mock images and rects for the paused menu
    paused_background_image = pygame.Surface((800, 600))  # Mock background image
    main_menu_image = pygame.Surface((100, 50))  # Mock main menu button image
    resume_image = pygame.Surface((100, 50))  # Mock resume button image
    main_menu_rect = (100, 100, 100, 50)  # Mock main menu button rect
    resume_rect = (300, 100, 100, 50)  # Mock resume button rect
    display.display_paused_menu(
        paused_background_image,
        main_menu_image,
        resume_image,
        main_menu_rect,
        resume_rect,
    )
