import pygame
from level import Level
from target import Target
from gun import Gun
from display import Display


class DuckHuntGame:
    def __init__(self, width, height):
        pygame.init()
        self.fps = 60
        self.timer = pygame.time.Clock()
        self.WIDTH = width
        self.HEIGHT = height
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
        self.load_assets()

    def load_levels(self):
        level_data = [
            (1, 0, 0, "../assets/bgs/bgs1.png", "../assets/banners/banner_1.png"),
            (1.5, 150, 0.03, "../assets/bgs/bgs2.png", "../assets/banners/banner_1.png"),
            (2, 200, 0.04, "../assets/bgs/bgs3.png", "../assets/banners/banner_2.png")
        ]
        self.levels = [Level(*data) for data in level_data]

    def load_assets(self):
        self.load_background()
        self.load_start_menu_images()
        self.load_levels()
        self.load_images()
        self.initialize_targets()
        self.load_sounds()
        self.load_paused_images()
        self.load_game_over_menu_images()
        self.load_gun_assets()
        self.banner_image()
        self.game_over_score_font = pygame.font.Font("../assets/fonts/AA_Magnum.ttf", 36)

    def load_gun_assets(self):
        self.gun = Gun("../assets/gun/Gun.png", (450, 600))

    def update_gun(self):
        self.gun.update()

    def load_images(self):
        self.bird_images = [
            pygame.transform.scale(
                pygame.image.load(f"../assets/targets/bird{i}.png").convert_alpha(),
                (50, 50)
            )
            for i in range(1, 5)
        ]

    def load_sounds(self):
        sound_files = ["shot.mp3", "bird1.mp3", "bird2.mp3", "bird3.mp3", "bird4.mp3"]
        self.sounds = {file.split(".")[0]: pygame.mixer.Sound(f"../assets/sounds/{file}") for file in sound_files}
        self.sounds["shot"].set_volume(0.08)
        pygame.mixer.music.load("../assets/sounds/background.mp3")
        pygame.mixer.music.play(-1)

    def load_background(self):
        current_level_background = f"../assets/bgs/bgs{self.current_level + 1}.png"
        self.background_image = pygame.transform.scale(
            pygame.image.load(current_level_background).convert(),
            (self.WIDTH, self.HEIGHT)
        )

    def banner_image(self):
        self.pause_button = pygame.image.load("../assets/banners/pause_button.png").convert_alpha()
        self.restart_button = pygame.image.load("../assets/banners/restart_button.png").convert_alpha()
        self.pause_button_rect = self.pause_button.get_rect(center=(723, 685))
        self.restart_button_rect = self.restart_button.get_rect(center=(750, 745))

    def load_paused_images(self):
        paused_background_image = pygame.image.load("../assets/menu/pause_menu/background.png").convert_alpha()
        self.paused_background_image = pygame.transform.scale(paused_background_image, (self.WIDTH, self.HEIGHT))
        self.main_menu_image = pygame.image.load("../assets/menu/pause_menu/Main_menu.png").convert_alpha()
        self.resume_image = pygame.image.load("../assets/menu/pause_menu/Resume.png").convert_alpha()

        self.main_menu_rect = self.main_menu_image.get_rect(center=(200, 450))
        self.resume_rect = self.resume_image.get_rect(center=(700, 450))

    def load_start_menu_images(self):
        start_menu_background = pygame.image.load("../assets/menu/start_menu/background.png").convert_alpha()
        self.start_menu_background = pygame.transform.scale(start_menu_background, (self.WIDTH, self.HEIGHT))
        self.free_play = pygame.image.load("../assets/menu/start_menu/free_play.png").convert_alpha()
        self.accuracy = pygame.image.load("../assets/menu/start_menu/accuracy.png").convert_alpha()
        self.countdown = pygame.image.load("../assets/menu/start_menu/countdown.png").convert_alpha()
        self.reset_scores = pygame.image.load("../assets/menu/start_menu/reset_scores.png").convert_alpha()
        self.free_play_rect = self.free_play.get_rect(center=(200, 400))
        self.accuracy_rect = self.accuracy.get_rect(center=(700, 400))
        self.countdown_rect = self.countdown.get_rect(center=(200, 600))
        self.reset_scores_rect = self.reset_scores.get_rect(center=(700, 600))

    def load_game_over_menu_images(self):
        game_over_menu_background = pygame.image.load("../assets/menu/game_over_menu/background.png").convert_alpha()
        self.game_over_menu_background = pygame.transform.scale(game_over_menu_background, (self.WIDTH, self.HEIGHT))
        self.game_over_main_menu = pygame.image.load("../assets/menu/game_over_menu/main_menu.png").convert_alpha()
        self.game_over_exit = pygame.image.load("../assets/menu/game_over_menu/exit.png").convert_alpha()
        self.game_over_main_menu_rect = self.game_over_main_menu.get_rect(center=(200, 450))
        self.game_over_exit_rect = self.game_over_exit.get_rect(center=(700, 450))

    def initialize_targets(self):
        level = self.levels[self.current_level]
        positions = [(100, 200), (300, 400), (500, 100), (700, 300), (800, 600)]
        speeds = [1, -1, 2, -1.5, 1.5]
        self.targets = [
            Target(pos[0], pos[1], 20, speed, level.amplitude_y, level.frequency_y, self.bird_images, self.WIDTH) for
            pos, speed in zip(positions, speeds)]
        self.load_background()

    def restart_level(self):
        self.current_level = 0
        self.score = 0
        self.shot_count = 0
        self.initialize_targets()
        if self.countdown_mode:
            self.countdown_timer = 15

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.check_button_clicked(self.pause_button_rect, self.pause_button, mouse_x, mouse_y):
                    self.toggle_pause()
                elif self.check_button_clicked(self.restart_button_rect, self.restart_button, mouse_x, mouse_y):
                    self.restart_level()
                else:
                    self.handle_shooting()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.toggle_pause()

    @staticmethod
    def check_button_clicked(button_rect, button_image, mouse_x, mouse_y):
        if button_rect.collidepoint(mouse_x, mouse_y):
            relative_x = mouse_x - button_rect.left
            relative_y = mouse_y - button_rect.top
            pixel = button_image.get_at((relative_x, relative_y))
            return pixel[3] > 0
        return False

    def handle_paused_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.check_button_clicked(self.main_menu_rect, self.main_menu_image, mouse_x, mouse_y):
                    self.paused = False
                    self.in_main_menu = True
                    self.run_main_menu()
                elif self.check_button_clicked(self.resume_rect, self.resume_image, mouse_x, mouse_y):
                    self.toggle_pause()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.toggle_pause()

    def handle_main_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.check_button_clicked(self.free_play_rect, self.free_play, mouse_x, mouse_y):
                    self.run_game()
                elif self.check_button_clicked(self.accuracy_rect, self.accuracy, mouse_x, mouse_y):
                    self.accuracy_mode = True
                    self.run_game()
                elif self.check_button_clicked(self.countdown_rect, self.countdown, mouse_x, mouse_y):
                    self.countdown_mode = True
                    self.run_game()
                elif self.check_button_clicked(self.reset_scores_rect, self.reset_scores, mouse_x, mouse_y):
                    self.run_main_menu()

    def handle_game_over_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.check_button_clicked(self.game_over_main_menu_rect, self.game_over_main_menu, mouse_x, mouse_y):
                    self.in_game_over_menu = False
                    self.run_main_menu()
                elif self.check_button_clicked(self.game_over_exit_rect, self.game_over_exit, mouse_x, mouse_y):
                    pygame.quit()
                    quit()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()

    def handle_shooting(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.sounds["shot"].play()
        self.shot_count += 1
        for target in self.targets:
            if (
                    target.x - target.radius <= mouse_x <= target.x + target.radius and
                    target.y - target.radius <= mouse_y <= target.y + target.radius
            ):
                self.targets.remove(target)
                bird_sounds = [self.sounds[f"bird{i + 1}"] for i in range(4)]
                bird_sound = bird_sounds[self.bird_images.index(target.current_bird_image)]
                bird_sound.play()
                self.score += 1

    def update_screen(self):
        # Modify this method to use methods from DisplayManager
        self.display.display_image(self.background_image, (0, 0))
        if self.paused:
            self.display.display_paused_menu(self.paused_background_image, self.main_menu_image,
                                             self.resume_image, self.main_menu_rect, self.resume_rect)
        else:
            if self.levels[self.current_level].banner_image is not None:
                self.shot_score()
                if self.countdown_mode:
                    font = pygame.font.Font("../assets/fonts/AA_Magnum.ttf", 30)
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
        banner = pygame.image.load(self.levels[self.current_level].banner_image).convert_alpha()
        banner_rect = banner.get_rect(midbottom=(self.WIDTH // 2, self.HEIGHT))
        self.screen.blit(banner, banner_rect)
        font = pygame.font.Font("../assets/fonts/AA_Magnum.ttf", 30)
        shot_text = font.render(f'Shot: {self.shot_count}', True, (0, 0, 0))
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(shot_text, (350, 680))
        self.screen.blit(score_text, (350, 720))
        self.screen.blit(self.gun.rotated_image, self.gun.rotated_rect)

    def check_game_status(self):
        if not self.targets:
            if self.current_level < len(self.levels) - 1:
                self.current_level += 1
                self.initialize_targets()
                print("Level completed! Proceeding to the next level...")
                return True
            else:
                print("Congratulations! You have completed all levels.")
                self.run_game_over_menu()
                return False
        return True

    def run_game(self):
        self.in_main_menu = False
        run = True
        while run:
            self.timer.tick(self.fps)
            if not self.paused:
                self.handle_events()
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
                self.handle_paused_events()
            run = self.check_game_status()

    def run_game_over_menu(self):
        self.in_game_over_menu = True
        # Calculate score text based on the game state
        score_text = self.game_over_score_font.render(f'Your Score: {self.score}', True, (255, 255, 255))
        while self.in_game_over_menu:
            self.display.display_game_over_menu(
                self.game_over_menu_background, self.game_over_main_menu,
                self.game_over_exit, self.game_over_main_menu_rect,
                self.game_over_exit_rect, score_text)
            self.handle_game_over_menu_events()
            pygame.display.flip()

    def run_main_menu(self):
        self.in_main_menu = True
        while self.in_main_menu:
            self.timer.tick(self.fps)
            self.handle_main_menu_events()
            self.display.display_start_menu(
                self.start_menu_background, self.free_play, self.accuracy,
                self.countdown, self.reset_scores, self.free_play_rect,
                self.accuracy_rect, self.countdown_rect,
                self.reset_scores_rect
            )
            pygame.display.flip()
