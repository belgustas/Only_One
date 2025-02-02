import pygame
from player import Player  # Импортируем класс игрока
from enemy import Enemy  # Импортируем класс врага

pygame.init()

# Настройки окна
WIDTH, HEIGHT = 650, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Only one!")
background = pygame.image.load("img/arena.png").convert()

# Создание группы спрайтов
all_sprites = pygame.sprite.Group()


player = Player(WIDTH // 2, HEIGHT // 2, all_sprites)
enemy = Enemy(100, 100, player)

all_sprites.add(player, enemy)
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background, (0, 0))

    # Обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                player.shoot(mouse_x, mouse_y)

    # Обновление всех спрайтов
    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # FPS

pygame.quit()
