import pytest
from src.display import (
    Display,
)  # Assuming your Display class is in a file named display.py
import pygame


# Fixture to initialize a Display object
@pytest.fixture
def display():
    pygame.init()
    display = Display(800, 600)
    yield display
    pygame.quit()


# Test display_image method
def test_display_image(display):
    # Assuming you have some test images
    test_image = pygame.Surface((100, 100))  # Mock test image
    rect = (0, 0, 100, 100)  # Mock rect
    display.display_image(test_image, rect)
    # Add assertions here to verify that the image was displayed correctly


# Test display_paused_menu method
def test_display_paused_menu(display):
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
