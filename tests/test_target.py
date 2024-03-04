# pylint: disable=W0613
# pylint: disable=W0621
# pylint: disable=E0401

"""
This module provides tests for the Target class.
"""
import unittest.mock
import pytest
from src.target import (
    Target,
)  # Replace 'your_module' with the actual module name where Target class is defined


@pytest.fixture
def sample_target():
    """
            Fixture providing a sample Target instance for testing.

            Returns:
                Target: A Target instance with sample parameters.
            """
    bird_images = [
        "../assets/targets/bird1",
        "../assets/targets/bird2",
        "../assets/targets/bird3",
    ]
    return Target(
        x=0,
        y=0,
        radius=1,
        speed=1,
        amplitude_y=1,
        frequency_y=1,
        bird_images=bird_images,
        screen_width=100,
    )


def test_initialization(sample_target):
    """
           Test the initialization of the Target class.

           Args:
               sample_target: A fixture providing a sample Target instance.

           This test verifies that the Target instance is initialized with the correct attributes.
           """
    assert sample_target.x == 0
    assert sample_target.y == 0
    assert sample_target.radius == 1
    assert sample_target.speed == 1
    assert sample_target.amplitude_y == 1
    assert sample_target.frequency_y == 1
    assert sample_target.initial_y == 0
    assert sample_target.bird_images == [
        "../assets/targets/bird1",
        "../assets/targets/bird2",
        "../assets/targets/bird3",
    ]
    assert sample_target.screen_width == 100


def test_move_updates_position(sample_target, monkeypatch):
    """
            Test the move method of the Target class to ensure it updates the position.

            Args:
                sample_target: A fixture providing a sample Target instance.
                monkeypatch: A fixture provided by pytest for mocking objects.

            This test mocks the random.choice function to return a specific value
            and then checks if the move method
            correctly updates the position of the target.
            """
    with unittest.mock.patch("random.choice", return_value="bird_image"):
        sample_target.move()
    assert sample_target.x == 1
    assert sample_target.y != 0


def test_check_boundary_resets_position(sample_target):
    """
            Test the check_boundary method of the Target class to ensure
            it resets the position when it goes beyond the boundary.

            Args:
                sample_target: A fixture providing a sample Target instance.

            This test sets the target's x-coordinate beyond the boundary
            and then checks if the check_boundary method
            correctly resets the position of the target.
            """
    sample_target.x = sample_target.screen_width + sample_target.radius + 1
    sample_target.check_boundary()
    assert sample_target.x == -sample_target.radius


def test_check_boundary_does_nothing_within_boundary(sample_target):
    """
            Test the check_boundary method of the Target class
            when the target is within the boundary.

            Args:
                sample_target: A fixture providing a sample Target instance.

            This test sets the target's x-coordinate within the boundary
            and then checks if the check_boundary method
            does not modify the position of the target.
            """
    sample_target.x = 10
    sample_target.check_boundary()
    assert sample_target.x == 10


def test_move_check_boundary_integration(sample_target, monkeypatch):
    """
            Test the integration of move and check_boundary methods of the Target class.

            Args:
                sample_target: A fixture providing a sample Target instance.
                monkeypatch: A fixture provided by pytest for mocking objects.

            This test sets the target's x-coordinate beyond the boundary, calls the move method,
            and then checks if the position is correctly reset by the check_boundary method.
            """
    sample_target.x = sample_target.screen_width + sample_target.radius + 1
    with unittest.mock.patch("random.choice", return_value="bird_image"):
        sample_target.move()
    assert sample_target.x == -sample_target.radius
    assert sample_target.y != 0


def test_move_does_not_reset_position_within_boundary(sample_target, monkeypatch):
    """
            Test that the move method of the Target class
            does not reset the position when within the boundary.

            Args:
                sample_target: A fixture providing a sample Target instance.
                monkeypatch: A fixture provided by pytest for mocking objects.

            This test sets the target's x-coordinate within the boundary, calls the move method,
            and then checks if the position remains unchanged.
            """
    sample_target.x = 10
    with unittest.mock.patch("random.choice", return_value="bird_image"):
        sample_target.move()
    assert sample_target.x == 11
    assert sample_target.y != 0
