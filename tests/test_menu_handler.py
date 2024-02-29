import pygame
import pytest
from src.menu_handler import (
    MenuHandler,
)
from unittest.mock import Mock, patch


# Define fixtures for common objects used in tests
@pytest.fixture
def game_instance():
    game = Mock()
    game.load_assets.return_value = None
    return game  # Replace with actual initialization logic


@pytest.fixture
def menu_handler(game_instance):
    return MenuHandler(game_instance)


# Define test cases for MenuHandler class
@patch("pygame.quit")
@patch("pygame.event.get")
def test_handle_events_quit(mock_event_get, mock_pygame_quit, menu_handler):
    # Mock the QUIT event and check if it quits the game
    mock_event_get.return_value = [Mock(type=pygame.QUIT)]
    with pytest.raises(SystemExit):
        menu_handler.handle_events()
    mock_pygame_quit.assert_called_once()


@patch("pygame.quit")
@patch("pygame.event.get")
def test_handle_events_pause_restart(mock_event_get, mock_pygame_quit, menu_handler):
    # Mock the MOUSEBUTTONDOWN event on pause button and check if it toggles pause
    mock_event_get.return_value = [Mock(type=pygame.MOUSEBUTTONDOWN, button=1)]
    with patch("pygame.mouse.get_pos", return_value=(50, 50)):
        with patch(
            "src.menu_handler.MenuHandler.check_button_clicked",
            side_effect=[True, False],
        ):
            menu_handler.handle_events()
    assert menu_handler.game.paused
    assert menu_handler.game.restart_level_called


@patch("pygame.event.get")
def test_handle_paused_events_resume(mock_event_get, menu_handler):
    # Mock the MOUSEBUTTONDOWN event on resume button and check if it resumes the game
    mock_event_get.return_value = [Mock(type=pygame.MOUSEBUTTONDOWN, button=1)]
    with patch("pygame.mouse.get_pos", return_value=(50, 50)):
        with patch(
            "src.menu_handler.MenuHandler.check_button_clicked", return_value=True
        ):
            menu_handler.handle_paused_events()
    assert not menu_handler.game.paused
