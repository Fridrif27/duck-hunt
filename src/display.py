import pygame


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])
        self.game_over_score_font = pygame.font.Font("../assets/fonts/AA_Magnum.ttf", 36)

    def display_image(self, image, rect):
        self.screen.blit(image, rect)

    def display_paused_menu(self, paused_background_image, main_menu_image, resume_image, main_menu_rect, resume_rect):
        self.display_image(paused_background_image, (0, 0))
        self.display_image(main_menu_image, main_menu_rect)
        self.display_image(resume_image, resume_rect)

    def display_start_menu(self, start_menu_background, free_play, accuracy, countdown, reset_scores,
                           free_play_rect, accuracy_rect, countdown_rect, reset_scores_rect):
        self.display_image(start_menu_background, (0, 0))
        self.display_image(free_play, free_play_rect)
        self.display_image(accuracy, accuracy_rect)
        self.display_image(countdown, countdown_rect)
        self.display_image(reset_scores, reset_scores_rect)

    def display_game_over_menu(self, game_over_menu_background, game_over_main_menu, game_over_exit,
                               game_over_main_menu_rect, game_over_exit_rect, score_text):
        self.display_image(game_over_menu_background, (0, 0))
        self.display_image(game_over_main_menu, game_over_main_menu_rect)
        self.display_image(game_over_exit, game_over_exit_rect)
        self.display_image(score_text, (435, 300))
