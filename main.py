import pygame

from player import Player, HealthBarPlayer  # Импортируем класс игрока
from enemy import Enemy, HealthBarEnemy  # Импортируем класс врага
from bowbar import BowBar  # Импортируем тетиву


def main():
    from begining import Begining
    pygame.init()

    # Настройки окна
    WIDTH, HEIGHT = 650, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Only one!")
    background = pygame.image.load("img/arena_img.png").convert()
    # Создание группы спрайтов
    all_sprites = pygame.sprite.Group()
    bow = BowBar(0)
    player = Player(WIDTH // 2, HEIGHT // 2, all_sprites, 100)
    health_bar_player = HealthBarPlayer(player, 50, 5, player.hp)
    enemy = Enemy(100, 100, player)
    health_bar_enemy = HealthBarEnemy(enemy, 50, 5, 10)
    all_sprites.add(player, enemy, bow)
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.blit(background, (0, 0))

        # Обработчик событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    bow.update()
                    if bow.rect.x == 150:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        player.shoot(mouse_x, mouse_y)
                    bow.count = 0
                    print(health_bar_player.hp)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bow.update()
                    bow.count = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Begining()

        # Обновление всех спрайтов
        all_sprites.draw(screen)
        health_bar_player.update()
        health_bar_enemy.update()
        all_sprites.update()

        player.collide(health_bar_player, enemy)
        health_bar_player.draw(screen)
        health_bar_enemy.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # FPS

    pygame.quit()
