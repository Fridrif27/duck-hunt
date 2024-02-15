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
            pygame.transform.scale(pygame.image.load("assets/targets/bird1.png").convert_alpha(), (40, 40)),
            pygame.transform.scale(pygame.image.load("assets/targets/bird2.png").convert_alpha(), (40, 40)),
            pygame.transform.scale(pygame.image.load("assets/targets/bird3.png").convert_alpha(), (40, 40)),
            pygame.transform.scale(pygame.image.load("assets/targets/bird4.png").convert_alpha(), (40, 40)),
        ]

    def load_sounds(self):
        self.sound_shot = pygame.mixer.Sound("assets/sounds/shot.mp3")
        self.sound_shot.set_volume(0.08)
        self.sound_bird1 = pygame.mixer.Sound("assets/sounds/bird1.mp3")
        self.sound_bird2 = pygame.mixer.Sound("assets/sounds/bird2.mp3")
        self.sound_bird3 = pygame.mixer.Sound("assets/sounds/bird3.mp3")
        self.sound_bird4 = pygame.mixer.Sound("assets/sounds/bird4.mp3")

    def load_background(self):
        self.background_image = pygame.transform.scale(pygame.image.load("assets/bgs/bgs1.PNG").convert(), (self.WIDTH, self.HEIGHT))

    def initialize_targets(self):
        level = self.levels[self.current_level]
        self.targets = [
            Target(100, 200, 20, 1, level.amplitude_y, level.frequency_y, self.bird_images, self.WIDTH),
            Target(300, 400, 20, -1, level.amplitude_y, level.frequency_y, self.bird_images, self.WIDTH),
            Target(500, 100, 20, 2, level.amplitude_y, level.frequency_y, self.bird_images, self.WIDTH),
            Target(700, 300, 20, -1.5, level.amplitude_y, level.frequency_y, self.bird_images, self.WIDTH),
            Target(800, 600, 20, 1.5, level.amplitude_y, level.frequency_y, self.bird_images, self.WIDTH)
        ]

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
        self.sound_shot.play()
        for target in self.targets:
            if (
                target.x - target.radius <= mouse_x <= target.x + target.radius and
                target.y - target.radius <= mouse_y <= target.y + target.radius
            ):
                self.targets.remove(target)
                self.handle_bird_sound(target)

    def handle_bird_sound(self, target):
        if target.current_bird_image == self.bird_images[0]:
            self.sound_bird1.play()
        elif target.current_bird_image == self.bird_images[1]:
            self.sound_bird2.play()
        elif target.current_bird_image == self.bird_images[2]:
            self.sound_bird3.play()
        elif target.current_bird_image == self.bird_images[3]:
            self.sound_bird4.play()

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
