 def load_images(self):
        self.bird_images = [
            pygame.image.load("assets/targets/bird1.png").convert_alpha(),
            pygame.image.load("assets/targets/bird2.png").convert_alpha(),
            pygame.image.load("assets/targets/bird3.png").convert_alpha(),
            pygame.image.load("assets/targets/bird4.png").convert_alpha(),
        ]
        transparent_color = (0, 0, 0)
        for image in self.bird_images:
            image.set_colorkey(transparent_color)
        self.bird_images = [pygame.transform.scale(image, (40, 40)) for image in self.bird_images]