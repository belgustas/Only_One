import pygame
from random import uniform

from player import Player, HealthBarPlayer, Bullet
from enemy import Enemy, HealthBarEnemy
from bowbar import BowBar


def main(battle_music, sound_enabled, name):  # главная функция
    from begining import But
    from aid_ammo import Aid
    from begining import Begining
    pygame.init()
    aids = []
    enemys = []
    bars = []

    WIDTH, HEIGHT = 650, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Only one!")
    background = pygame.image.load("img/arena_img.png").convert()

    all_sprites = pygame.sprite.Group()
    bow = BowBar(0)
    player = Player(WIDTH // 2, HEIGHT // 2, all_sprites, 100, name)
    health_bar_player = HealthBarPlayer(player, 50, 5, player.hp)

    all_sprites.add(player, bow)

    running = True
    menuning = False
    clock = pygame.time.Clock()

    menu_sprites = pygame.sprite.Group()
    again = But(WIDTH // 2 - 30, HEIGHT // 2 - 60, 70, "img/return.png")
    home = But(WIDTH // 2 - 30, HEIGHT // 2 - 150, 70, "img/home.png")
    menu_sprites.add(again, home)

    font = pygame.font.Font(None, 30)

    while running:
        screen.blit(background, (0, 0))

        # обработка событий
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bow.update()
                    bow.count = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menuning = not menuning
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menuning:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    again.changes(mouse_x, mouse_y, lambda: main(battle_music, sound_enabled, name), name, player.point)
                    home.changes(mouse_x, mouse_y, lambda: Begining(battle_music, sound_enabled), name, player.point)

        if player.counte == 500:
            enemy = Enemy(uniform(0, WIDTH), uniform(0, HEIGHT), player, 100)
            health_bar_enemy = HealthBarEnemy(enemy, 50, 5, 100)
            all_sprites.add(enemy)
            enemys.append(enemy)
            bars.append(health_bar_enemy)
            player.counte = 0

        if menuning:
            player.speed = 0
            for enemy in enemys:
                enemy.speed = 0
            menu_sprites.draw(screen)
            menu_sprites.update()
        else:
            player.speed = 3
            for enemy in enemys:
                enemy.speed = 1.25

        if player.count == 1000:
            aid = Aid(uniform(0, 650), uniform(0, 650), "img/aid.png", all_sprites)
            all_sprites.add(aid)
            aids.append(aid)
            player.count = 0

        # Обновление всех спрайтов
        for enemy, health_bar_enemy in zip(enemys, bars):
            for bullet in [sprite for sprite in all_sprites if isinstance(sprite, Bullet)]:
                enemy.collide_with_bullet(bullet, health_bar_enemy, player)

        all_sprites.draw(screen)
        health_bar_player.update()
        for health_bar_enemy in bars:
            health_bar_enemy.update()
        all_sprites.update()

        for i in aids:
            i.collide(health_bar_player, player)

        for enemy, health_bar_enemy in zip(enemys, bars):
            if enemy.hp_enemy <= 0:
                enemy.kill()
                health_bar_enemy.kill()
            player.collide(health_bar_player, enemy)

        player.counter()
        screen.blit(font.render(f"Points:{player.point}", 1, pygame.Color('Red')), (550, 25))

        print(player.counte, player.count)
        health_bar_player.draw(screen)
        for health_bar_enemy in bars:
            health_bar_enemy.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
