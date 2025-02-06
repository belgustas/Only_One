import pygame
from begining import load_image
from random import uniform

class Aid(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT, name, all_sprites):
        pygame.sprite.Sprite.__init__(self)
        self.all_sprites = all_sprites
        self.image = load_image(name)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT

    def collide(self, health, player):
        if self.rect.colliderect(player):
            player.hp += 1
            health.hp += 1
            self.kill()


class Ammos():
    pass