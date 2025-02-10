import pygame


def leaders(battle_music, sound_enabled):  # лидеры
    from begining import Begining
    from begining import But
    from db import leadtable  # Функция для загрузки данных из БД

    pygame.init()

    WIDTH, HEIGHT = 650, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Leaders")
    background = pygame.image.load("img/background.jpg").convert()
    background = pygame.transform.scale(background, (750, 750))
    all_sprites = pygame.sprite.Group()

    running = True
    clock = pygame.time.Clock()
    but1 = But(0, 0, 70, "img/return.png")
    all_sprites.add(but1)

    font = pygame.font.Font(None, 30)

    while running:
        screen.blit(background, (-50, -50))

        # таблица лидеров
        intro_text = leadtable()

        # Отрисовка таблицы лидеров
        text_coord = 100
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 10
            intro_rect.top = text_coord
            text_coord += intro_rect.height + 5
            screen.blit(string_rendered, intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if but1.rect.collidepoint(mouse_x, mouse_y):
                    Begining(battle_music, sound_enabled)  # Возврат в меню
                    return

        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
