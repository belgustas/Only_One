import pygame

from player import Player  # Импортируем класс игрока
from enemy import Enemy  # Импортируем класс врага
from bowbar import BowBar



def main():
    from begining import Begining
    from begining import But

    pygame.init()

    # Настройки окна
    WIDTH, HEIGHT = 650, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Only one!")
    background = pygame.image.load("img/arena_img.png").convert()
    # Создание группы спрайтов
    all_sprites = pygame.sprite.Group()
    menu_sprites = pygame.sprite.Group()

    player = Player(WIDTH // 2, HEIGHT // 2, all_sprites)
    enemy = Enemy(100, 100, player)
    all_sprites.add(player, enemy)
    running = True
    menuning = True
    counter = 0
    clock = pygame.time.Clock()
    bow = BowBar(0)
    all_sprites.add(bow)
    again = But(WIDTH // 2 - 35, HEIGHT // 3, 70, "return.png")
    menu_sprites.add(again)
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


        if menuning:
            menu_sprites.update()
            menu_sprites.draw(screen)
            player.speed = 0
            enemy.speed = 0
        else:
            player.speed = 3
            enemy.speed = 1.25
        player.collide(enemy.rect)
        # Обновление всех спрайтов
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # FPS

    pygame.quit()
