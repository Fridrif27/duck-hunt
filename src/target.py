import math
import random


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
