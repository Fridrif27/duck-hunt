import pygame
import math


class Gun:
    def __init__(self, image_path, initial_position):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect(center=initial_position)

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        offset_x = mouse_x - self.rect.centerx
        offset_y = mouse_y - self.rect.centery
        angle = math.atan2(offset_y, offset_x)
        angle = math.degrees(angle)
        self.rotated_image = pygame.transform.rotate(self.image, -angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center)
