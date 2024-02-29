"""
This module implements the MenuHandler class for the Duck Hunt game.
"""
import pygame


class MenuHandler:
    """Class to handle different types of events in the game menu."""

    def __init__(self, game):
        """
        Initialize MenuHandler with a reference to the main game instance.
        
        Args:
            game: The main game instance.
        """
        self.game = game
        self.game.load_assets()

    def handle_events(self):
        """
        Handle events during gameplay.
        
        - Quit the game.
        - Pause or restart the game.
        - Shoot targets.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.check_button_clicked(self.game.pause_button_rect, self.game.pause_button, mouse_x, mouse_y):
                    self.game.toggle_pause()
                elif self.check_button_clicked(self.game.restart_button_rect, self.game.restart_button, mouse_x, mouse_y):
                    self.game.restart_level()
                else:
                    self.game.handle_shooting()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game.toggle_pause()

    def handle_paused_events(self):
        """
        Handle events when the game is paused.
        
        - Quit the game.
        - Return to the main menu.
        - Resume the game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.check_button_clicked(self.game.main_menu_rect, self.game.main_menu_image, mouse_x, mouse_y):
                    self.game.paused = False
                    self.game.in_main_menu = True
                    self.game.restart_level()
                    self.game.run_main_menu()
                elif self.check_button_clicked(self.game.resume_rect, self.game.resume_image, mouse_x, mouse_y):
                    self.game.toggle_pause()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game.toggle_pause()

    def handle_main_menu_events(self):
        """
        Handle events when in the main menu.
        
        - Quit the game.
        - Start a new game.
        - Choose different game modes.
        - Reset scores.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.check_button_clicked(self.game.free_play_rect, self.game.free_play, mouse_x, mouse_y):
                    self.game.run_game()
                elif self.check_button_clicked(self.game.accuracy_rect, self.game.accuracy, mouse_x, mouse_y):
                    self.game.accuracy_mode = True
                    self.game.run_game()
                elif self.check_button_clicked(self.game.countdown_rect, self.game.countdown, mouse_x, mouse_y):
                    self.game.countdown_mode = True
                    self.game.run_game()
                elif self.check_button_clicked(self.game.reset_scores_rect, self.game.reset_scores, mouse_x, mouse_y):
                    self.game.run_main_menu()

    def handle_game_over_menu_events(self):
        """
        Handle events when in the game over menu.
        
        - Quit the game.
        - Return to the main menu.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.check_button_clicked(self.game.game_over_main_menu_rect, self.game.game_over_main_menu, mouse_x, mouse_y):
                    self.game.in_game_over_menu = False
                    self.game.restart_level()
                    self.game.run_main_menu()
                elif self.check_button_clicked(self.game.game_over_exit_rect, self.game.game_over_exit, mouse_x, mouse_y):
                    pygame.quit()
                    quit()

    def check_button_clicked(self, button_rect, button_image, mouse_x, mouse_y):
        """
        Check if a button is clicked based on its rectangle area, image, and mouse coordinates.
        
        Args:
            button_rect: The rectangle area of the button.
            button_image: The image of the button.
            mouse_x: The x-coordinate of the mouse position.
            mouse_y: The y-coordinate of the mouse position.
        
        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        if button_rect:
            if button_rect.collidepoint(mouse_x, mouse_y):
                relative_x = mouse_x - button_rect.left
                relative_y = mouse_y - button_rect.top
                pixel = button_image.get_at((relative_x, relative_y))
                return pixel[3] > 0
        return False
