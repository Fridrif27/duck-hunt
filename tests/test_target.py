import math
import unittest.mock
import pytest
from src.target import (
    Target,
)  # Replace 'your_module' with the actual module name where Target class is defined


@pytest.fixture
def sample_target():
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
    with unittest.mock.patch("random.choice", return_value="bird_image"):
        sample_target.move()
    assert sample_target.x == 1
    assert sample_target.y != 0


def test_check_boundary_resets_position(sample_target):
    sample_target.x = sample_target.screen_width + sample_target.radius + 1
    sample_target.check_boundary()
    assert sample_target.x == -sample_target.radius


def test_check_boundary_does_nothing_within_boundary(sample_target):
    sample_target.x = 10
    sample_target.check_boundary()
    assert sample_target.x == 10


def test_move_check_boundary_integration(sample_target, monkeypatch):
    sample_target.x = sample_target.screen_width + sample_target.radius + 1
    with unittest.mock.patch("random.choice", return_value="bird_image"):
        sample_target.move()
    assert sample_target.x == -sample_target.radius
    assert sample_target.y != 0


def test_move_does_not_reset_position_within_boundary(sample_target, monkeypatch):
    sample_target.x = 10
    with unittest.mock.patch("random.choice", return_value="bird_image"):
        sample_target.move()
    assert sample_target.x == 11
    assert sample_target.y != 0
