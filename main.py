import pygame
import math

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
class DuckHuntGame:
    def __init__(self, width, height):
        pygame.init()

        self.fps = 60
        self.timer = pygame.time.Clock()
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        target_coordinates = [(100, 200), (300, 400), (500, 100), (700, 300), (800, 600)]
        self.targets = [Target(x, y) for x, y in target_coordinates]
     
    def run_game(self):
        run = True
        while run:
            self.timer.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            for target in self.targets:
                pygame.draw.circle(self.screen, (255, 0, 0), (target.x, target.y), 20)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = DuckHuntGame(900, 800)
    game.run_game()
