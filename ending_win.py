import pygame  # импорт


def Ending_win(battle_music, sound_enabled, name, points):
    from begining import Begining
    from begining import But
    from main import main

    pygame.init()

    WIDTH, HEIGHT = 650, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("You are winner!")
    background = pygame.image.load("img/onemoretime.jpg").convert()
    background = pygame.transform.scale(background, (750, 750))
    all_sprites = pygame.sprite.Group()

    # Создаём кнопки
    but1 = But(WIDTH / 2 - 100, HEIGHT / 2, 70, "img/return.png")  # Сдвигаем кнопку влево
    but2 = But(WIDTH / 2 + 30, HEIGHT / 2, 70, "img/home.png")  # Сдвигаем кнопку вправо
    all_sprites.add(but1, but2)

    intro_text = ["YOU WIN!"]

    running = True
    clock = pygame.time.Clock()

    while running:
        # Обработчик событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                but1.changes(mouse_x, mouse_y, lambda: main(battle_music, sound_enabled, name), name, points)
                but2.clicked(mouse_x, mouse_y, lambda: Begining(battle_music, sound_enabled))

        # Отрисовка фона
        screen.blit(background, (-50, -50))

        # Отрисовка текста
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        # Отрисовка кнопок (после фона и текста)
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # FPS

    pygame.quit()
