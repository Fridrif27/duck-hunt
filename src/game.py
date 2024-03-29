# pylint: disable=line-too-long
# pylint: disable=no-member
# pylint: disable=too-many-instance-attributes
# pylint: disable=R0904
# pylint: disable=E0401
"""
This module implements the DuckHuntGame class for the Duck Hunt game.
"""

import pygame
from level import Level
from target import Target
from gun import Gun
from display import Display
from menu_handler import MenuHandler


class DuckHuntGame:
    """
    This class implements the Duck Hunt game.
    """

    def __init__(self, width, height):
        """
        Initialize the DuckHuntGame instance.

        Args:
            width (int): The width of the game window.
            height (int): The height of the game window.
        """
        pygame.init()
        self.fps = 60
        self.timer = pygame.time.Clock()
        self.width = width
        self.height = height
        self.levels = []
        self.bird_images = []
        self.game_over_score_font = pygame.font.Font("assets/fonts/AA_Magnum.ttf", 36)
        self.sounds = {}
        self.background_image = []
        self.pause_button = None
        self.restart_button = None
        self.pause_button_rect = None
        self.restart_button_rect = None
        self.paused_background_image = None
        self.main_menu_image = None
        self.resume_image = None
        self.main_menu_rect = None
        self.resume_rect = None
        self.start_menu_background = None
        self.free_play = None
        self.accuracy = None
        self.countdown = None
        self.reset_scores = None
        self.free_play_rect = None
        self.accuracy_rect = None
        self.countdown_rect = None
        self.reset_scores_rect = None
        self.game_over_menu_background = None
        self.game_over_main_menu = None
        self.game_over_exit = None
        self.game_over_main_menu_rect = None
        self.game_over_exit_rect = None
        self.targets = []
        self.in_main_menu = True
        self.display = Display(width, height)
        self.screen = pygame.display.set_mode([width, height])
        self.current_level = 0
        self.in_game_over_menu = False
        self.paused = False
        self.accuracy_mode = False
        self.countdown_mode = False
        self.score = 0
        self.shot_count = 0
        self.countdown_timer = 15
        self.menu_handler = MenuHandler(self)
        self.load_assets()
        self.load_gun_assets()

    def load_assets(self):
        """
        Load game assets such as images, sounds, and menu items.
        """
        self.load_background()
        self.load_start_menu_images()
        self.load_levels()
        self.load_images()
        self.initialize_targets()
        self.load_sounds()
        self.load_game_over_menu_images()
        self.load_gun_assets()
        self.banner_image()
        self.load_paused_images()

    def load_levels(self):
        """
        Load levels of the game.

        The levels are loaded from predefined level data.

        Args:
            None

        Returns:
            None
        """
        level_data = [
            (1, 0, 0, "assets/bgs/bgs1.png", "assets/banners/banner_1.png"),
            (1.5, 150, 0.03, "assets/bgs/bgs2.png", "assets/banners/banner_1.png"),
            (2, 200, 0.04, "assets/bgs/bgs3.png", "assets/banners/banner_2.png")
        ]
        self.levels = [Level(*data) for data in level_data]

    def load_gun_assets(self):
        """
        Load assets related to the gun.

        The gun asset is loaded with its image and position.

        Args:
            None

        Returns:
            None
        """
        self.gun = Gun("assets/gun/Gun.png", (450, 600))

    def update_gun(self):
        """
        Update the gun position.

        The gun's position is updated based on user input.

        Args:
            None

        Returns:
            None
        """
        self.gun.update()

    def load_images(self):
        """
        Load images of the game.

        Bird images used in the game are loaded and scaled to a specific size.

        Args:
            None

        Returns:
            None
        """
        self.bird_images = [
            pygame.transform.scale(
                pygame.image.load(f"assets/targets/bird{i}.png").convert_alpha(),
                (50, 50)
            )
            for i in range(1, 5)
        ]

    def load_sounds(self):
        """
        Load sounds of the game.

        Sound files for shooting and bird sounds are loaded.

        Args:
            None

        Returns:
            None
        """
        sound_files = ["shot.mp3", "bird1.mp3", "bird2.mp3", "bird3.mp3", "bird4.mp3"]
        self.sounds = {
            file.split(".", maxsplit=1)[0]: pygame.mixer.Sound(
                f"assets/sounds/{file}"
            )
            for file in sound_files
        }
        self.sounds["shot"].set_volume(0.08)
        pygame.mixer.music.load("assets/sounds/background.mp3")
        pygame.mixer.music.play(-1)

    def load_background(self):
        """
        Load background image.

        The background image for the current level is loaded and scaled to fit the screen.

        Args:
            None

        Returns:
            None
        """
        current_level_background = f"assets/bgs/bgs{self.current_level + 1}.png"
        self.background_image = pygame.transform.scale(
            pygame.image.load(current_level_background).convert(),
            (self.width, self.height)
        )

    def banner_image(self):
        """
        Load pause and restart button images and their respective rectangles.

        Args:
            None

        Returns:
            None
        """
        self.pause_button = pygame.image.load("assets/banners/pause_button.png").convert_alpha()
        self.restart_button = pygame.image.load("assets/banners/restart_button.png").convert_alpha()
        self.pause_button_rect = self.pause_button.get_rect(center=(723, 685))
        self.restart_button_rect = self.restart_button.get_rect(center=(750, 745))

    def load_paused_images(self):
        """
        Load images for the paused menu.

        Args:
            None

        Returns:
            None
        """
        paused_background_image = pygame.image.load("assets/menu/pause_menu/background.png").convert_alpha()
        self.paused_background_image = pygame.transform.scale(paused_background_image, (self.width, self.height))
        self.main_menu_image = pygame.image.load("assets/menu/pause_menu/Main_menu.png").convert_alpha()
        self.resume_image = pygame.image.load("assets/menu/pause_menu/Resume.png").convert_alpha()

        self.main_menu_rect = self.main_menu_image.get_rect(center=(200, 450))
        self.resume_rect = self.resume_image.get_rect(center=(700, 450))

    def load_start_menu_images(self):
        """
        Load images for the start menu.

        Args:
            None

        Returns:
            None
        """
        start_menu_background = pygame.image.load("assets/menu/start_menu/background.png").convert_alpha()
        self.start_menu_background = pygame.transform.scale(start_menu_background, (self.width, self.height))
        self.free_play = pygame.image.load("assets/menu/start_menu/free_play.png").convert_alpha()
        self.accuracy = pygame.image.load("assets/menu/start_menu/accuracy.png").convert_alpha()
        self.countdown = pygame.image.load("assets/menu/start_menu/countdown.png").convert_alpha()
        self.reset_scores = pygame.image.load("assets/menu/start_menu/reset_scores.png").convert_alpha()
        self.free_play_rect = self.free_play.get_rect(center=(200, 400))
        self.accuracy_rect = self.accuracy.get_rect(center=(700, 400))
        self.countdown_rect = self.countdown.get_rect(center=(200, 600))
        self.reset_scores_rect = self.reset_scores.get_rect(center=(700, 600))

    def load_game_over_menu_images(self):
        """
        Load images for the game over menu.

        Args:
            None

        Returns:
            None
        """
        game_over_menu_background = pygame.image.load("assets/menu/game_over_menu/background.png").convert_alpha()
        self.game_over_menu_background = pygame.transform.scale(game_over_menu_background, (self.width, self.height))
        self.game_over_main_menu = pygame.image.load("assets/menu/game_over_menu/main_menu.png").convert_alpha()
        self.game_over_exit = pygame.image.load("assets/menu/game_over_menu/exit.png").convert_alpha()
        self.game_over_main_menu_rect = self.game_over_main_menu.get_rect(center=(200, 450))
        self.game_over_exit_rect = self.game_over_exit.get_rect(center=(700, 450))

    def initialize_targets(self):
        """
        Initialize target positions, speeds, and attributes.

        Args:
            None

        Returns:
            None
        """
        level = self.levels[self.current_level]
        positions = [(100, 200), (300, 400), (500, 100), (700, 300), (800, 600)]
        speeds = [1, -1, 2, -1.5, 1.5]
        self.targets = [
            Target(pos[0], pos[1], 20, speed, level.amplitude_y, level.frequency_y, self.bird_images, self.width) for
            pos, speed in zip(positions, speeds)]
        self.load_background()

    def restart_level(self):
        """
        Restart the current level.

        Args:
            None

        Returns:
            None
        """
        self.current_level = 0
        self.score = 0
        self.shot_count = 0
        self.initialize_targets()
        if self.countdown_mode:
            self.countdown_timer = 15

    @staticmethod
    def check_button_clicked(button_rect, button_image, mouse_x, mouse_y):
        """
        Check if a button is clicked.

        Args:
            button_rect (pygame.Rect): The rectangle area of the button.
            button_image (pygame.Surface): The image of the button.
            mouse_x (int): The x-coordinate of the mouse.
            mouse_y (int): The y-coordinate of the mouse.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        if not button_rect.collidepoint(mouse_x, mouse_y):
            return False

        relative_x = mouse_x - button_rect.left
        relative_y = mouse_y - button_rect.top
        pixel = button_image.get_at((relative_x, relative_y))
        return pixel[3] > 0

    def toggle_pause(self):
        """
        Toggle the pause state of the game.

        Args:
            None

        Returns:
            None
        """
        self.paused = not self.paused
        if self.paused:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()

    def handle_shooting(self):
        """
        Handle shooting events.

        Args:
            None

        Returns:
            None
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.sounds["shot"].play()
        self.shot_count += 1
        for target in self.targets:
            if (
                    target.x - target.radius <= mouse_x <= target.x + target.radius and target.y - target.radius <= mouse_y <= target.y + target.radius
            ):
                self.targets.remove(target)
                bird_sounds = [self.sounds[f"bird{i + 1}"] for i in range(4)]
                bird_sound = bird_sounds[self.bird_images.index(target.current_bird_image)]
                bird_sound.play()
                self.score += 1

    def update_screen(self):
        """
        Update the game screen.

        Args:
            None

        Returns:
            None
        """
        self.display.display_image(self.background_image, (0, 0))
        if self.paused:
            self.display.display_paused_menu(self.paused_background_image, self.main_menu_image,
                                             self.resume_image, self.main_menu_rect, self.resume_rect)
        else:
            if self.levels[self.current_level].banner_image is not None:
                self.shot_score()
                if self.countdown_mode:
                    font = pygame.font.Font("assets/fonts/AA_Magnum.ttf", 30)
                    countdown_text = font.render(f'Time: {int(self.countdown_timer)}', True, (0, 0, 0))
                    countdown_rect = countdown_text.get_rect(midright=(570, 700))
                    self.display.display_image(countdown_text, countdown_rect)
                    self.display.display_image(self.gun.rotated_image, self.gun.rotated_rect)
                self.display.display_image(self.pause_button, self.pause_button_rect)
                self.display.display_image(self.restart_button, self.restart_button_rect)
            for target in self.targets:
                target.move()
                if target.speed > 0:
                    image = pygame.transform.flip(target.current_bird_image, True, False)
                else:
                    image = target.current_bird_image
                self.display.display_image(image, image.get_rect(center=(int(target.x), int(target.y))))
        pygame.display.flip()

    def shot_score(self):
        """
        Display shot count and score on the screen.

        Args:
            None

        Returns:
            None
        """
        banner = pygame.image.load(self.levels[self.current_level].banner_image).convert_alpha()
        banner_rect = banner.get_rect(midbottom=(self.width // 2, self.height))
        self.screen.blit(banner, banner_rect)
        font = pygame.font.Font("assets/fonts/AA_Magnum.ttf", 30)
        shot_text = font.render(f'Shot: {self.shot_count}', True, (0, 0, 0))
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(shot_text, (350, 680))
        self.screen.blit(score_text, (350, 720))
        self.screen.blit(self.gun.rotated_image, self.gun.rotated_rect)

    def check_game_status(self):
        """
        Check the status of the game.

        Args:
            None

        Returns:
            bool: True if the game is still running, False otherwise.
        """

        if not self.targets:
            if self.current_level < len(self.levels) - 1:
                self.current_level += 1
                self.initialize_targets()
                print("Level completed! Proceeding to the next level...")
                return True
            print("Congratulations! You have completed all levels.")
            self.run_game_over_menu()
            return False
        return True

    def run_game(self):
        """
        Run the main game loop.

        Args:
            None

        Returns:
            None
        """
        self.in_main_menu = False
        run = True
        while run:
            self.timer.tick(self.fps)
            if not self.paused:
                self.menu_handler.handle_events()
                self.update_gun()
                self.update_screen()
                if self.accuracy_mode:
                    if self.shot_count >= 15:
                        self.run_game_over_menu()
                        return
                if self.countdown_mode:
                    self.countdown_timer -= 1 / self.fps
                    if self.countdown_timer <= 0:
                        self.run_game_over_menu()
                        return
            else:
                self.menu_handler.handle_paused_events()
            run = self.check_game_status()

    def run_game_over_menu(self):
        """
        Run the game over menu loop.

        Args:
            None

        Returns:
            None
        """

        self.accuracy_mode = False
        self.countdown_mode = False
        self.in_game_over_menu = True
        score_text = self.game_over_score_font.render(f'Your Score: {self.score}', True, (255, 255, 255))
        while self.in_game_over_menu:
            self.display.display_game_over_menu(
                self.game_over_menu_background, self.game_over_main_menu,
                self.game_over_exit, self.game_over_main_menu_rect,
                self.game_over_exit_rect, score_text)
            self.menu_handler.handle_game_over_menu_events()
            pygame.display.flip()

    def run_main_menu(self):
        """
        Run the main menu loop.

        Args:
            None

        Returns:
            None
        """
        self.in_main_menu = True
        while self.in_main_menu:
            self.timer.tick(self.fps)
            self.menu_handler.handle_main_menu_events()
            self.display.display_start_menu(
                self.start_menu_background, self.free_play, self.accuracy,
                self.countdown, self.reset_scores, self.free_play_rect,
                self.accuracy_rect, self.countdown_rect,
                self.reset_scores_rect
            )
            pygame.display.flip()
