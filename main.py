import pygame
import math

class Target:
    def __init__(self, x, y, radius, speed, amplitude_y, frequency_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.amplitude_y = amplitude_y
        self.frequency_y = frequency_y
        self.initial_y = y
    def move(self):
        self.x += self.speed
        self.y = self.amplitude_y * math.sin(self.frequency_y * self.x) + self.initial_y
        if self.x - self.radius > self.width:
            self.x = -self.radius
        elif self.x + self.radius < 0:
            self.x = self.radius +self.width
class DuckHuntGame:
    def __init__(self, width, height):
        pygame.init()

        self.fps = 60
        self.timer = pygame.time.Clock()
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.targets = [
            Target(100, 200, 20, 1, 100, 0.02),
            Target(300, 400, 20, -1, 50, 0.03),
            Target(500, 100, 20, 2, 150, 0.01),
            Target(700, 300, 20, -1.5, 10, 0.015),
            Target(800, 600, 20, 1.5, 125, 0.025)
        ]
        for target in self.targets:
            target.width = self.WIDTH
        self.background_image = pygame.transform.scale(pygame.image.load("bgs1.png").convert(), (self.WIDTH, self.HEIGHT))

    def run_game(self):
        run = True
        while run:
            self.timer.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for target in self.targets:
                        if (
                            target.x - target.radius <= mouse_x <= target.x + target.radius and
                            target.y - target.radius <= mouse_y <= target.y + target.radius
                        ):
                            self.targets.remove(target)
            self.screen.blit(self.background_image, (0, 0))
            for target in self.targets:
                pygame.draw.circle(self.screen, (255, 0, 0), (target.x, target.y), target.radius)
                target.move()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = DuckHuntGame(900, 800)
    game.run_game()
