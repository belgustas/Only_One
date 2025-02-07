import pygame
from random import uniform

from player import Player, HealthBarPlayer, Bullet  # Импортируем класс игрока
from enemy import Enemy, HealthBarEnemy  # Импортируем класс врага
from bowbar import BowBar  # Импортируем тетиву


def main():
    from begining import But
    from aid_ammo import Aid
    from begining import Begining
    pygame.init()
    aids = []

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
    enemy = Enemy(100, 100, player, 100)
    health_bar_enemy = HealthBarEnemy(enemy, 50, 5, 10)

    all_sprites.add(player, enemy, bow)

    running = True
    menuning = False
    clock = pygame.time.Clock()

    # меню
    menu_sprites = pygame.sprite.Group()
    again = But(WIDTH // 2 - 30, HEIGHT // 2 - 60, 70, "return.png")
    home = But(WIDTH // 2 - 30, HEIGHT // 2 - 150, 70, "home.png")
    menu_sprites.add(again, home)

    # музыка
    battle_music = pygame.mixer.Sound("sounds/battle_music.mp3")
    battle_music.set_volume(0.3)

    while running:
        # запускаем музыку
        screen.blit(background, (0, 0))
        battle_music.play(-1)

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
                    if menuning:
                        menuning = False
                    else:
                        menuning = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menuning:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    again.clicked(mouse_x, mouse_y, main)
                    home.clicked(mouse_x, mouse_y, Begining)

        if menuning:
            player.speed = 0
            enemy.speed = 0
            menu_sprites.draw(screen)
            menu_sprites.update()
        else:
            player.speed = 3
            enemy.speed = 1.25

        if player.count == 1000:
            aid = Aid(uniform(0, 650), uniform(0, 650), "aid.png", all_sprites)
            all_sprites.add(aid)
            aids.append(aid)
            player.count = 0

        if enemy.hp_enemy <= 0:
            enemy.kill()
            health_bar_enemy.kill()

        # Обновление всех спрайтов
        for bullet in [sprite for sprite in all_sprites if isinstance(sprite, Bullet)]:
            enemy.collide_with_bullet(bullet)

        all_sprites.draw(screen)
        health_bar_player.update()
        health_bar_enemy.update()
        all_sprites.update()

        player.collide(health_bar_player, enemy)

        for i in aids:
            i.collide(health_bar_player, player)

        health_bar_player.draw(screen)
        health_bar_enemy.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # FPS

    pygame.quit()
