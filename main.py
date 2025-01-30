import pygame
from Movement import Player
import values as v

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Мой мир")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
# Цикл игры
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                v.KEY = 'left'
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                v.KEY = 'right'
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                v.KEY = 'up'
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                v.KEY = 'down'
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
                    event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_a or \
                    event.key == pygame.K_s or event.key == pygame.K_w or event.key == pygame.K_d:
                v.KEY = 'stop'
    all_sprites.update()
    clock.tick(30)
    screen.fill(pygame.Color('black'))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
