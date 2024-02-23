import pygame


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])
        self.gameover_score_font = pygame.font.Font("../assets/fonts/AA_Magnum.ttf", 36)

    def display_image(self, image, rect):
        self.screen.blit(image, rect)

    def display_paused_menu(self, paused_background_image, main_menu_image, resume_image, main_menu_rect, resume_rect):
        self.screen.blit(paused_background_image, (0, 0))
        self.screen.blit(main_menu_image, main_menu_rect)
        self.screen.blit(resume_image, resume_rect)

    def display_start_menu(self, start_menu_background, free_play, accuracy, countdown, reset_scores,
                           free_play_rect, accuracy_rect, countdown_rect, reset_scores_rect):
        self.display_image(start_menu_background, (0, 0))
        self.display_image(free_play, free_play_rect)
        self.display_image(accuracy, accuracy_rect)
        self.display_image(countdown, countdown_rect)
        self.display_image(reset_scores, reset_scores_rect)

    def display_gameover_menu(self, gameover_menu_background, gameover_main_menu, gameover_exit,
                              gameover_main_menu_rect, gameover_exit_rect, score_text):
        self.screen.blit(gameover_menu_background, (0, 0))
        self.screen.blit(gameover_main_menu, gameover_main_menu_rect)
        self.screen.blit(gameover_exit, gameover_exit_rect)
        self.screen.blit(score_text, (350, 300))
