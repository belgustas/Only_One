import pygame
from player import Player  # Импорт


pygame.init()

# Настройки окна
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Анимация персонажа")
background = pygame.image.load("img/arena.png").convert()

# Создание группы спрайтов
all_sprites = pygame.sprite.Group()
player = Player(WIDTH // 2, HEIGHT // 2)
all_sprites.add(player)
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background, (0, 0))

    # Обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление всех спрайтов
    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # FPS

pygame.quit()
