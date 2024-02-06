import pygame
import math

class Target:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.radius = 20
        self.speed = speed
        
    def move(self, dx):
        self.x += dx
        
class DuckHuntGame:
    def __init__(self, width, height):
        pygame.init()

        self.fps = 60
        self.timer = pygame.time.Clock()
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        target_coordinates_and_speed = [((100, 200), -1), ((300, 400), 1), ((500, 100), -2), ((700, 300), 1), ((800, 600), -3)]
        self.targets = [Target(x, y, speed) for (x, y), speed in target_coordinates_and_speed]
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
                target.move(target.speed)
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = DuckHuntGame(900, 800)
    game.run_game()
