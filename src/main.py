import pygame
import math
import random

class Level:
    def __init__(self, bird_speed, amplitude_y, frequency_y):
        self.bird_speed = bird_speed
        self.amplitude_y = amplitude_y
        self.frequency_y = frequency_y


class Target:
    def __init__(self, x, y, radius, speed, amplitude_y, frequency_y, bird_images, screen_width):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.amplitude_y = amplitude_y
        self.frequency_y = frequency_y
        self.initial_y = y
        self.bird_images = bird_images
        self.current_bird_image = random.choice(bird_images)
        self.screen_width = screen_width

    def move(self):
        self.x += self.speed
        self.y = self.amplitude_y * math.sin(self.frequency_y * self.x) + self.initial_y
        self.check_boundary()

    def check_boundary(self):
        if self.x - self.radius > self.screen_width:
            self.x = -self.radius
        elif self.x + self.radius < 0:
            self.x = self.screen_width + self.radius

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
            Level(bird_speed=1, amplitude_y=0, frequency_y=0),
            Level(bird_speed=1.5, amplitude_y=150, frequency_y=0.03),
            Level(bird_speed=2, amplitude_y=200, frequency_y=0.04)
        ]
        self.load_assets()
        self.initialize_targets()

    def load_assets(self):
        self.load_images()
        self.load_sounds()
        self.load_background()

    def load_images(self):
        self.bird_images = [
            pygame.image.load("../assets/targets/bird1.png").convert_alpha(),
            pygame.image.load("../assets/targets/bird2.png").convert_alpha(),
            pygame.image.load("../assets/targets/bird3.png").convert_alpha(),
            pygame.image.load("../assets/targets/bird4.png").convert_alpha(),
        ]
        transparent_color = (0, 0, 0)
        for image in self.bird_images:
            image.set_colorkey(transparent_color)
        self.bird_images = [pygame.transform.scale(image, (40, 40)) for image in self.bird_images]

    def load_sounds(self):
        self.sound_shot = pygame.mixer.Sound("../assets/sounds/shot.mp3")
        self.sound_shot.set_volume(0.08)
        self.sound_bird1 = pygame.mixer.Sound("../assets/sounds/bird1.mp3")
        self.sound_bird2 = pygame.mixer.Sound("../assets/sounds/bird2.mp3")
        self.sound_bird3 = pygame.mixer.Sound("../assets/sounds/bird3.mp3")
        self.sound_bird4 = pygame.mixer.Sound("../assets/sounds/bird4.mp3")
        self.bird_images = [pygame.transform.scale(pygame.image.load(f"assets/targets/bird{i}.png").convert_alpha(), (40, 40)) for i in range(1, 5)]
    
    def load_sounds(self):
        sound_files = ["shot.mp3", "bird1.mp3", "bird2.mp3", "bird3.mp3", "bird4.mp3"]
        self.sounds = {file.split(".")[0]: pygame.mixer.Sound(f"assets/sounds/{file}") for file in sound_files}
        self.sounds["shot"].set_volume(0.08)


    def load_background(self):
        self.background_image = pygame.transform.scale(pygame.image.load("../assets/bgs/bgs1.png").convert(), (self.WIDTH, self.HEIGHT))

    def initialize_targets(self):
        level = self.levels[self.current_level]
        positions = [(100, 200), (300, 400), (500, 100), (700, 300), (800, 600)]
        speeds = [1, -1, 2, -1.5, 1.5]
        self.targets = [Target(pos[0], pos[1], 20, speed, level.amplitude_y, level.frequency_y, self.bird_images, self.WIDTH) for pos, speed in zip(positions, speeds)]

    def run_game(self):
        run = True
        while run:
            self.timer.tick(self.fps)
            self.handle_events()
            self.update_screen()
            run = self.check_game_status()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_shooting()

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


    def update_screen(self):
        self.screen.blit(self.background_image, (0, 0))
        for target in self.targets:
            target.move()
            self.screen.blit(target.current_bird_image, target.current_bird_image.get_rect(center=(int(target.x), int(target.y))))
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

if __name__ == "__main__":
    game = DuckHuntGame(900, 800)
    game.run_game()
