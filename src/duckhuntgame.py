import pygame
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
        self.levels = [
            Level(1, 0, 0, "assets/bgs/bgs1.png"),
            Level(1.5, 150, 0.03, "assets/bgs/bgs2.png"),
            Level(2, 200, 0.04, "assets/bgs/bgs3.png")
        ]

        self.paused = False
        self.load_assets()
        self.load_background()
        self.initialize_targets()

    def load_assets(self):
        self.load_images()
        self.load_sounds()
        self.load_background()

    def load_images(self):
        self.bird_images = [pygame.transform.scale(pygame.image.load(f"assets/targets/bird{i}.png").convert_alpha(), (40, 40)) for i in range(1, 5)]
    
    def load_sounds(self):
        sound_files = ["shot.mp3", "bird1.mp3", "bird2.mp3", "bird3.mp3", "bird4.mp3"]
        self.sounds = {file.split(".")[0]: pygame.mixer.Sound(f"assets/sounds/{file}") for file in sound_files}
        self.sounds["shot"].set_volume(0.08)

    def load_background(self):
        current_level_background = f"assets/bgs/bgs{self.current_level + 1}.png"
        self.background_image = pygame.transform.scale(pygame.image.load(current_level_background).convert(), (self.WIDTH, self.HEIGHT))


    def initialize_targets(self):
        level = self.levels[self.current_level]
        positions = [(100, 200), (300, 400), (500, 100), (700, 300), (800, 600)]
        speeds = [1, -1, 2, -1.5, 1.5]
        self.targets = [Target(pos[0], pos[1], 20, speed, level.amplitude_y, level.frequency_y, self.bird_images, self.WIDTH) for pos, speed in zip(positions, speeds)]
        self.load_background()
    def run_game(self):
        run = True
        while run:
            self.timer.tick(self.fps)
            if not self.paused:
                self.handle_events()
                self.update_screen()
            else:
                self.handle_paused_events()
            run = self.check_game_status()

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

    def handle_paused_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.toggle_pause()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()

    def handle_shooting(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.sounds["shot"].play()
        for target in self.targets:
            if (
                target.x - target.radius <= mouse_x <= target.x + target.radius and
                target.y - target.radius <= mouse_y <= target.y + target.radius
            ):
                self.targets.remove(target)
                bird_sounds = [self.sounds[f"bird{i+1}"] for i in range(4)]
                bird_sound = bird_sounds[self.bird_images.index(target.current_bird_image)]
                bird_sound.play()

    def display_paused_menu(self):
        paused_background_image = pygame.image.load("assets/menu/pause_menu/background.png").convert_alpha()
        paused_background_rect = paused_background_image.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(paused_background_image, paused_background_rect)

        main_menu_image = pygame.image.load("assets/menu/pause_menu/Main_menu.png").convert_alpha()
        main_menu_rect = main_menu_image.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))
        self.screen.blit(main_menu_image, main_menu_rect)

        resume_image = pygame.image.load("assets/menu/pause_menu/Resume.png").convert_alpha()
        resume_rect = resume_image.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 50))
        self.screen.blit(resume_image, resume_rect)
    
    def update_screen(self):
        self.screen.blit(self.background_image, (0, 0))
        if self.paused:
            self.display_paused_menu()
            pygame.display.flip()
        else:
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
                pygame.time.delay(2000)
                return True
            else:
                print("Congratulations! You have completed all levels.")
                pygame.time.delay(1000)
                return False
        return True