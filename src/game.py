import pygame
import math
from level import Level
from target import Target


class DuckHuntGame:
    def __init__(self, width, height):
        pygame.init()
        self.fps = 60
        self.timer = pygame.time.Clock()
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode([width, height])
        self.current_level = 0
        self.in_gameover_menu = False
        self.paused = False
        self.accuracy_mode = False
        self.score = 0
        self.shot_count = 0
        self.load_assets()

    def load_levels(self):
        self.levels = [
            Level(1, 0, 0, "assets/bgs/bgs1.png", "assets/banners/banner_1.PNG"),
            Level(1.5, 150, 0.03, "assets/bgs/bgs2.png", "assets/banners/banner_1.PNG"),
            Level(2, 200, 0.04, "assets/bgs/bgs3.png", "assets/banners/banner_2.PNG")
        ]

    def load_assets(self):
        self.load_background()
        self.load_start_menu_images()
        self.load_levels()
        self.load_images()
        self.initialize_targets()
        self.load_sounds()
        self.initialize_gun()
        self.load_paused_images()
        self.load_gameover_menu_images()
        self.gameover_score_font = pygame.font.SysFont('Arial', 36)
        
    def initialize_gun(self):
        self.gun_image = pygame.image.load("assets/gun/Gun.PNG").convert_alpha()
        self.gun_image = pygame.transform.scale(self.gun_image, (200, 200))
        self.gun_rect = self.gun_image.get_rect(center=(450, 600))

    def update_gun(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        offset_x = mouse_x - self.gun_rect.centerx
        offset_y = mouse_y - self.gun_rect.centery
        angle = math.atan2(offset_y, offset_x)
        angle = math.degrees(angle)
        self.rotated_gun_image = pygame.transform.rotate(self.gun_image, -angle)
        self.rotated_gun_rect = self.rotated_gun_image.get_rect(center=self.gun_rect.center)

    def load_images(self):
        self.bird_images = [
            pygame.transform.scale(
                pygame.image.load(f"assets/targets/bird{i}.png").convert_alpha(),
                (50, 50)
            )
            for i in range(1, 5)
        ]
    
    def load_sounds(self):
        sound_files = ["shot.mp3", "bird1.mp3", "bird2.mp3", "bird3.mp3", "bird4.mp3"]
        self.sounds = {file.split(".")[0]: pygame.mixer.Sound(f"assets/sounds/{file}") for file in sound_files}
        self.sounds["shot"].set_volume(0.08)
        pygame.mixer.music.load("assets/sounds/background.mp3")
        pygame.mixer.music.play(-1)

    def load_background(self):
        current_level_background = f"assets/bgs/bgs{self.current_level + 1}.png"
        self.background_image = pygame.transform.scale(
            pygame.image.load(current_level_background).convert(),
            (self.WIDTH, self.HEIGHT)
        )
    
    def load_paused_images(self):
        paused_background_image = pygame.image.load("assets/menu/pause_menu/background.png").convert_alpha()
        self.paused_background_image = pygame.transform.scale(paused_background_image, (self.WIDTH, self.HEIGHT))
        self.main_menu_image = pygame.image.load("assets/menu/pause_menu/Main_menu.png").convert_alpha()
        self.resume_image = pygame.image.load("assets/menu/pause_menu/Resume.png").convert_alpha()

        self.main_menu_rect = self.main_menu_image.get_rect(center=(200, 450))
        self.resume_rect = self.resume_image.get_rect(center=(700, 450))

    def display_image(self, image, rect):
        self.screen.blit(image, rect)

    def display_paused_menu(self):
        self.screen.blit(self.paused_background_image, (0, 0))
        self.screen.blit(self.main_menu_image, self.main_menu_rect)
        self.screen.blit(self.resume_image, self.resume_rect)

    def load_start_menu_images(self):
        start_menu_background = pygame.image.load("assets/menu/start_menu/background.PNG").convert_alpha()
        self.start_menu_background = pygame.transform.scale(start_menu_background, (self.WIDTH, self.HEIGHT))
        self.free_play = pygame.image.load("assets/menu/start_menu/free_play.png").convert_alpha()
        self.accuracy = pygame.image.load("assets/menu/start_menu/accuracy.png").convert_alpha()
        self.countdown = pygame.image.load("assets/menu/start_menu/countdown.png").convert_alpha()
        self.reset_scores = pygame.image.load("assets/menu/start_menu/reset_scores.png").convert_alpha()
        self.free_play_rect = self.free_play.get_rect(center=(200, 400))
        self.accuracy_rect = self.accuracy.get_rect(center=(700, 400))
        self.countdown_rect = self.countdown.get_rect(center=(200, 600))
        self.reset_scores_rect = self.reset_scores.get_rect(center=(700, 600))

    def display_start_menu(self):
        self.display_image(self.start_menu_background, (0, 0))
        self.display_image(self.free_play, self.free_play_rect)
        self.display_image(self.accuracy, self.accuracy_rect)
        self.display_image(self.countdown, self.countdown_rect)
        self.display_image(self.reset_scores, self.reset_scores_rect)

    def load_gameover_menu_images(self):
        gameover_menu_background = pygame.image.load("assets/menu/gameover_menu/background.PNG").convert_alpha()
        self.gameover_menu_background = pygame.transform.scale(gameover_menu_background, (self.WIDTH, self.HEIGHT))
        self.gameover_main_menu = pygame.image.load("assets/menu/gameover_menu/main_menu.png").convert_alpha()
        self.gameover_exit = pygame.image.load("assets/menu/gameover_menu/exit.png").convert_alpha()
        self.gameover_main_menu_rect = self.gameover_main_menu.get_rect(center=(200, 450))
        self.gameover_exit_rect = self.gameover_exit.get_rect(center=(700, 450))

    def display_gameover_menu(self):
        self.screen.blit(self.gameover_menu_background, (0, 0))
        self.screen.blit(self.gameover_main_menu, self.gameover_main_menu_rect)
        self.screen.blit(self.gameover_exit, self.gameover_exit_rect)
        score_text = self.gameover_score_font.render(f'{self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (435, 300))

        
    def initialize_targets(self):
        level = self.levels[self.current_level]
        positions = [(100, 200), (300, 400), (500, 100), (700, 300), (800, 600)]
        speeds = [1, -1, 2, -1.5, 1.5]
        self.targets = [Target(pos[0], pos[1], 20, speed, level.amplitude_y, level.frequency_y, self.bird_images, self.WIDTH) for pos, speed in zip(positions, speeds)]
        self.load_background()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_shooting()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.toggle_pause()

    def check_button_clicked(self, button_rect, button_image, mouse_x, mouse_y):
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
                    self.countdown = True
                    self.run_game()
                elif self.check_button_clicked(self.reset_scores_rect, self.reset_scores, mouse_x, mouse_y):
                    self.run_game()

    def handle_gameover_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.check_button_clicked(self.gameover_main_menu_rect, self.gameover_main_menu, mouse_x, mouse_y):
                    self.in_gameover_menu = False
                    self.run_main_menu() 
                elif self.check_button_clicked(self.gameover_exit_rect, self.gameover_exit, mouse_x, mouse_y):
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
        self.screen.blit(self.background_image, (0, 0))
        if self.paused:
            self.display_paused_menu()
        else:
            if self.levels[self.current_level].banner_image is not None:
                banner = pygame.image.load(self.levels[self.current_level].banner_image).convert_alpha()
                banner_rect = banner.get_rect(midbottom=(self.WIDTH // 2, self.HEIGHT))
                self.screen.blit(banner, banner_rect)
                font = pygame.font.SysFont('Arial', 30)
                shot_text = font.render(f'Shot: {self.shot_count}', True, (0, 0, 0))
                score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
                self.screen.blit(shot_text, (350, 680))
                self.screen.blit(score_text, (350, 720))  
                self.screen.blit(self.rotated_gun_image, self.rotated_gun_rect)
            for target in self.targets:
                target.move()
                if target.speed > 0:
                    image = pygame.transform.flip(target.current_bird_image, True, False)
                else:
                    image = target.current_bird_image
                self.screen.blit(image, image.get_rect(center=(int(target.x), int(target.y))))
        pygame.display.flip()

    def check_game_status(self):
        if not self.targets:
            if self.current_level < len(self.levels) - 1:
                self.current_level += 1
                self.initialize_targets()
                print("Level completed! Proceeding to the next level...")
                return True
            else:
                print("Congratulations! You have completed all levels.")
                self.run_gameover_menu()
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
                        self.run_gameover_menu()
                        return
            else:
                self.handle_paused_events()
            run = self.check_game_status()

    def run_gameover_menu(self):
        self.in_gameover_menu = True
        while self.in_gameover_menu:
            self.display_gameover_menu()
            self.handle_gameover_menu_events()
            pygame.display.flip()

    def run_main_menu(self):
        self.in_main_menu = True
        game = DuckHuntGame(900, 800)
        while self.in_main_menu:
            game.timer.tick(self.fps)
            game.handle_main_menu_events()
            game.display_start_menu()
            pygame.display.flip()

def main():
    game = DuckHuntGame(900, 800)
    game.run_main_menu()

if __name__ == "__main__":
    main()
