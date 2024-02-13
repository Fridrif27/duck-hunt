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
        if self.x - self.radius > self.screen_width:
            self.x = -self.radius
        elif self.x + self.radius < 0:
            self.x = self.radius + self.screen_width
class DuckHuntGame:
    def __init__(self, width, height):
        pygame.init()
        self.fps = 60
        self.timer = pygame.time.Clock()
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode([width, height])
        self.bird_images = [
            pygame.transform.scale(pygame.image.load("assets/targets/bird1.jpg").convert(), (40, 40)),
            pygame.transform.scale(pygame.image.load("assets/targets/bird2.jpg").convert(), (40, 40)),
            pygame.transform.scale(pygame.image.load("assets/targets/bird3.jpg").convert(), (40, 40)),
            pygame.transform.scale(pygame.image.load("assets/targets/bird4.jpg").convert(), (40, 40)),
        ]
        self.targets = [
            Target(100, 200, 20, 1, 100, 0.02, self.bird_images, self.WIDTH),
            Target(300, 400, 20, -1, 50, 0.03, self.bird_images, self.WIDTH),
            Target(500, 100, 20, 2, 150, 0.01, self.bird_images, self.WIDTH),
            Target(700, 300, 20, -1.5, 10, 0.015, self.bird_images, self.WIDTH),
            Target(800, 600, 20, 1.5, 125, 0.025, self.bird_images, self.WIDTH)
        ]
        self.levels = [
            Level(bird_speed=1, amplitude_y=10, frequency_y=0.4),
            Level(bird_speed=1.5, amplitude_y=150, frequency_y=0.03),
            Level(bird_speed=1.5, amplitude_y=150, frequency_y=0.03),
        ]
        self.current_level = 0
        self.current_level_info = self.levels[self.current_level]
        self.sound_shot = pygame.mixer.Sound("assets/sounds/shot.mp3")
        self.sound_shot.set_volume(0.08)
        self.sound_bird1 = pygame.mixer.Sound("assets/sounds/bird1.mp3")
        self.sound_bird2 = pygame.mixer.Sound("assets/sounds/bird2.mp3")
        self.sound_bird3 = pygame.mixer.Sound("assets/sounds/bird3.mp3")
        self.sound_bird4 = pygame.mixer.Sound("assets/sounds/bird4.mp3")
        for target in self.targets:
            target.width = self.WIDTH
        self.background_image = pygame.transform.scale(pygame.image.load("assets/bgs/bgs1.PNG").convert(), (width, height))
    def run_game(self):
        run = True
        while run:
            self.timer.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.sound_shot.play()
                    for target in self.targets:
                        if (
                            target.x - target.radius <= mouse_x <= target.x + target.radius and
                            target.y - target.radius <= mouse_y <= target.y + target.radius
                        ):
                            self.targets.remove(target)
                            if target.current_bird_image == self.bird_images[0]:
                                self.sound_bird1.play()
                            elif target.current_bird_image == self.bird_images[1]:
                                self.sound_bird2.play()
                            elif target.current_bird_image == self.bird_images[2]:
                                self.sound_bird3.play()
                            elif target.current_bird_image == self.bird_images[3]:
                                self.sound_bird4.play()
            self.screen.blit(self.background_image, (0, 0))
            for target in self.targets:
                target.move()
                self.screen.blit(target.current_bird_image, target.current_bird_image.get_rect(center=(int(target.x), int(target.y))))
            pygame.display.flip()
            if not self.targets:
                if self.current_level < len(self.levels)-1:
                    self.current_level += 1
                    self.current_level_info = self.levels[self.current_level]
                    self.targets = [
                    Target(100, 200, 20, 1, 100, 0.02, self.bird_images, self.WIDTH),
                    Target(300, 400, 20, -1, 50, 0.03, self.bird_images, self.WIDTH),
                    Target(500, 100, 20, 2, 150, 0.01, self.bird_images, self.WIDTH),
                    Target(700, 300, 20, -1.5, 10, 0.015, self.bird_images, self.WIDTH),
                    Target(800, 600, 20, 1.5, 125, 0.025, self.bird_images, self.WIDTH)
                ]
                    for target in self.targets:
                        target.speed = self.current_level_info.bird_speed
                        target.amplitude_y = self.current_level_info.amplitude_y
                        target.frequency_y = self.current_level_info.frequency_y
                    print("Level completed! Proceeding to the next level...")
                    # Pause before next level
                    pygame.time.delay(2000)
                else:
                    # If all levels are completed, end the game
                    print("Congratulations! You have completed all levels.")
                    run = False
        pygame.quit()

if __name__ == "__main__":
    game = DuckHuntGame(900, 800)
    game.run_game()
