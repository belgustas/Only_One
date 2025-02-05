import pygame


class BowBar(pygame.sprite.Sprite):
    def __init__(self, counter):
        pygame.sprite.Sprite.__init__(self)
        self.count = counter
        self.image = pygame.Surface((10, 50))
        self.image.fill("green")
        self.rect = self.image.get_rect()

    def update(self):
        if self.count > 150:
            self.rect.x = 150
        elif self.count != 0:
            self.rect.x += 5
            self.count += 5
        else:
            self.rect.x = 0

