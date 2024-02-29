"""
This module implements the Display class for the Duck Hunt game.
"""
import pygame


class Display:
    """Class to handle displaying images on the screen."""

    def __init__(self, width, height):
        """
        Initialize the Display with the given width and height.
        
        Args:
            width (int): The width of the display screen.
            height (int): The height of the display screen.
        """
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])
        self.game_over_score_font = pygame.font.Font("assets/fonts/AA_Magnum.ttf", 36)

    def display_image(self, image, rect):
        """
        Display the given image at the specified rectangle position on the screen.
        
        Args:
            image: The image to be displayed.
            rect: The rectangle position where the image will be displayed.
        """
        self.screen.blit(image, rect)

    def display_paused_menu(self, paused_background_image, main_menu_image, resume_image, main_menu_rect, resume_rect):
        """
        Display the paused menu on the screen.
        
        Args:
            paused_background_image: The background image for the paused menu.
            main_menu_image: The image for the main menu button.
            resume_image: The image for the resume button.
            main_menu_rect: The rectangle position for the main menu button.
            resume_rect: The rectangle position for the resume button.
        """
        if paused_background_image is not None:
            self.display_image(paused_background_image, (0, 0))
        if main_menu_image is not None:
            self.display_image(main_menu_image, main_menu_rect)
        if resume_image is not None:
            self.display_image(resume_image, resume_rect)

    def display_start_menu(self, start_menu_background, free_play, accuracy, countdown, reset_scores,
                           free_play_rect, accuracy_rect, countdown_rect, reset_scores_rect):
        """
        Display the start menu on the screen.
        
        Args:
            start_menu_background: The background image for the start menu.
            free_play: The image for the free play mode button.
            accuracy: The image for the accuracy mode button.
            countdown: The image for the countdown mode button.
            reset_scores: The image for the reset scores button.
            free_play_rect: The rectangle position for the free play mode button.
            accuracy_rect: The rectangle position for the accuracy mode button.
            countdown_rect: The rectangle position for the countdown mode button.
            reset_scores_rect: The rectangle position for the reset scores button.
        """
        if start_menu_background is not None:
            self.display_image(start_menu_background, (0, 0))
        if free_play is not None:
            self.display_image(free_play, free_play_rect)
        if accuracy is not None:
            self.display_image(accuracy, accuracy_rect)
        if countdown is not None:
            self.display_image(countdown, countdown_rect)
        if reset_scores is not None:
            self.display_image(reset_scores, reset_scores_rect)

    def display_game_over_menu(self, game_over_menu_background, game_over_main_menu, game_over_exit,
                               game_over_main_menu_rect, game_over_exit_rect, score_text):
        """
        Display the game over menu on the screen.
        
        Args:
            game_over_menu_background: The background image for the game over menu.
            game_over_main_menu: The image for the main menu button in game over menu.
            game_over_exit: The image for the exit button in game over menu.
            game_over_main_menu_rect: The rectangle position for the main menu button in game over menu.
            game_over_exit_rect: The rectangle position for the exit button in game over menu.
            score_text: The text displaying the player's score.
        """
        if game_over_menu_background is not None:
            self.display_image(game_over_menu_background, (0, 0))
        if game_over_main_menu is not None:
            self.display_image(game_over_main_menu, game_over_main_menu_rect)
        if game_over_exit is not None:
            self.display_image(game_over_exit, game_over_exit_rect)
        if score_text is not None:
            self.display_image(score_text, (350, 300))
