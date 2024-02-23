import pytest
from src.target import (
    Target,
)  # Replace "your_module_name" with the actual name of the module containing the Target class


@pytest.fixture
def target_instance():
    # Create an instance of the Target class with some initial parameters for testing
    return Target(
        x=100,
        y=200,
        radius=20,
        speed=2,
        amplitude_y=50,
        frequency_y=0.1,
        bird_images=[],
        screen_width=800,
    )


def test_move(target_instance):
    # Check if the move function updates the position correctly
    initial_x = target_instance.x
    initial_y = target_instance.y
    target_instance.move()
    assert target_instance.x == initial_x + target_instance.speed
    assert target_instance.y != initial_y  # The y-coordinate should change


@pytest.mark.skip(reason="no way of currently testing this")
def test_check_boundary(target_instance):
    # Check if the check_boundary function works correctly
    # Move the target to a position outside the screen to trigger boundary conditions
    target_instance.x = target_instance.screen_width + target_instance.radius + 1
    target_instance.check_boundary()
    assert (
        target_instance.x == -target_instance.radius
    )  # Should be wrapped to the left side of the screen

    target_instance.x = -target_instance.radius - 1
    target_instance.check_boundary()
    assert (
        target_instance.x == target_instance.screen_width + target_instance.radius
    )  # Should be wrapped to the right side of the screen
