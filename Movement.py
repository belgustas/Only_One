import pygame
from os import path
import values as v


class Player(pygame.sprite.Sprite):
    pl_pos_x = 0
    pl_pos_y = 0
    frame = -1
    img_dir = path.join(path.dirname(__file__), 'img')

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.strip = pygame.image.load(path.join(self.img_dir, 'Player.png')).convert()
        self.image = pygame.Surface((64, 64))
        self.image.set_colorkey(pygame.Color('black'))
        self.image.blit(self.strip, (0, 0), (0, 128, 64, 64))
        self.original_image = self.image
        self.last_tick = pygame.time.get_ticks()  # начало отсчета тиков - задает промежуток времени между кадрами спрайтшита
        self.rect = self.image.get_rect()
        self.rect.center = (500 / 2, 500 / 2)
        self.speed = 3

    def update(self):
        self.animation()
        self.rect.x += self.pl_pos_x
        self.rect.y += self.pl_pos_y

    def animation(self):
        now_tick = pygame.time.get_ticks()
        now_speed = self.speed
        if now_tick - self.last_tick > 100: #для смены кадра
            self.frame += 1
            if v.KEY == 'left':
                self.image.blit(self.strip, (0, 0), ((self.frame % 9) * 64, 9 * 64, 64, 64)) # смена кадра
                self.rect.x -= now_speed
            if v.KEY == 'right':
                self.image.blit(self.strip, (0, 0), ((self.frame % 9) * 64, 11 * 64, 64, 64))
                self.rect.x += now_speed
            if v.KEY == 'up':
                self.image.blit(self.strip, (0, 0), ((self.frame % 9) * 64, 8 * 64, 64, 64))
                self.rect.y -= now_speed
            if v.KEY == 'down':
                self.image.blit(self.strip, (0, 0), ((self.frame % 9) * 64, 10 * 64, 64, 64))
                self.rect.y += now_speed
            if v.KEY == 'stop':
                self.image.blit(self.strip, (0, 0), ((self.frame % 1) * 64, 2 * 64, 64, 64))
                self.pl_pos_x = self.pl_pos_y = 0
            self.last_tick = pygame.time.get_ticks()
