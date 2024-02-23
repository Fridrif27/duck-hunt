import pytest
from src.main import DuckHuntGame, Target


# Fixture to create a DuckHuntGame instance
@pytest.fixture
def duck_hunt_game():
    return DuckHuntGame(900, 800)


# Test the initialization of targets in DuckHuntGame
def test_initialize_targets(duck_hunt_game):
    duck_hunt_game.current_level = 0
    duck_hunt_game.initialize_targets()
    assert len(duck_hunt_game.targets) == 5
    assert all(isinstance(target, Target) for target in duck_hunt_game.targets)


# Test shooting functionality in DuckHuntGame
@pytest.mark.parametrize(
    "mouse_position, expected_targets_left",
    [
        ((150, 250), 2),
        ((350, 450), 2),
        ((550, 150), 1),
    ],
)
def test_handle_shooting(
    duck_hunt_game, monkeypatch, mouse_position, expected_targets_left
):
    duck_hunt_game.targets = [
        Target(100, 200, 20, 1, 0, 0, [], duck_hunt_game.WIDTH),
        Target(300, 400, 20, -1, 0, 0, [], duck_hunt_game.WIDTH),
        Target(500, 100, 20, 2, 0, 0, [], duck_hunt_game.WIDTH),
    ]
    monkeypatch.setattr("pygame.mouse.get_pos", lambda: mouse_position)
    duck_hunt_game.handle_shooting()
    assert len(duck_hunt_game.targets) == expected_targets_left


# Test game status after completing a level
def test_check_game_status_level_completion(duck_hunt_game, capsys):
    duck_hunt_game.current_level = 0
    duck_hunt_game.initialize_targets()
    duck_hunt_game.targets = []  # Simulate completing the level
    assert duck_hunt_game.check_game_status() is True
    captured = capsys.readouterr()
    assert "Level completed! Proceeding to the next level..." in captured.out


# Test game status after completing all levels
def test_check_game_status_game_completion(duck_hunt_game, capsys):
    duck_hunt_game.current_level = 2
    duck_hunt_game.initialize_targets()
    duck_hunt_game.targets = []  # Simulate completing the last level
    assert duck_hunt_game.check_game_status() is False
    captured = capsys.readouterr()
    assert "Congratulations! You have completed all levels." in captured.out
