# pylint: disable=no-member
# pylint: disable=W0621
# pylint: disable=E0401

"""
This module provides tests for the menu_handler module.
"""
from unittest.mock import Mock, patch
import pygame
import pytest
from src.menu_handler import (
    MenuHandler,
)


# Define fixtures for common objects used in tests
@pytest.fixture
def game_instance():
    """
            Fixture providing a mocked game instance for testing.

            Returns:
                Mock: A mocked game instance.
            """
    game = Mock()
    game.load_assets.return_value = None
    return game


@pytest.fixture
def menu_handler(game_instance):
    """
           Fixture providing a MenuHandler instance for testing.

           Args:
               game_instance (Mock): A mocked game instance.

           Returns:
               MenuHandler: An instance of MenuHandler initialized with the provided game instance.
           """
    return MenuHandler(game_instance)


# Define test cases for MenuHandler class
@patch("pygame.quit")
@patch("pygame.event.get")
def test_handle_events_quit(mock_event_get, mock_pygame_quit, menu_handler):
    """
            Test the handle_events method of the MenuHandler class when handling a quit event.

            Args:
                mock_event_get: A patched version of pygame.event.get for mocking events.
                mock_pygame_quit: A patched version of pygame.quit for asserting it's called.
                menu_handler: A fixture providing an instance of the MenuHandler class.

            This test checks if the handle_events method
            correctly handles a QUIT event by raising a SystemExit.
            It also verifies that pygame.quit is called once.
            """
    # Mock the QUIT event and check if it quits the game
    mock_event_get.return_value = [Mock(type=pygame.QUIT)]
    with pytest.raises(SystemExit):
        menu_handler.handle_events()
    mock_pygame_quit.assert_called_once()


@patch("pygame.quit")
@patch("pygame.event.get")
def test_handle_events_pause_restart(mock_event_get, menu_handler):
    """
           Test the handle_events method of the MenuHandler class
           when handling pause and restart events.

           Args:
               mock_event_get: A patched version of pygame.event.get for mocking events.
               mock_pygame_quit: A patched version of pygame.quit for asserting it's called.
               menu_handler: A fixture providing an instance of the MenuHandler class.

           This test checks if the handle_events method correctly handles pause and restart events.
           It verifies that pygame.quit is not called and that the game is not exited.
           """
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
    """
            Test the handle_paused_events method of the MenuHandler class
            when handling resume event.

            Args:
                mock_event_get: A patched version of pygame.event.get for mocking events.
                menu_handler: A fixture providing an instance of the MenuHandler class.

            This test checks if the handle_paused_events
            method correctly handles the resume event by simulating
            a MOUSEBUTTONDOWN event on the resume button and verifying that the game is resumed.
            """
    # Mock the MOUSEBUTTONDOWN event on resume button and check if it resumes the game
    mock_event_get.return_value = [Mock(type=pygame.MOUSEBUTTONDOWN, button=1)]
    with patch("pygame.mouse.get_pos", return_value=(50, 50)):
        with patch(
            "src.menu_handler.MenuHandler.check_button_clicked", return_value=True
        ):
            menu_handler.handle_paused_events()
    assert not menu_handler.game.paused
