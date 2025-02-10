import pygame


def choose(name, battle_music=None, sound_enabled=True):
    from main import main
    from db import input
    from New_level import main2
    from New_level2 import main3

    pygame.init()
    WIDTH, HEIGHT = 650, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("img/Auto")
    background = pygame.image.load("img/backgroundfor.jpg").convert()
    background = pygame.transform.scale(background, (750, 750))
    all_sprites = pygame.sprite.Group()
    font = pygame.font.Font(None, 30)
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.blit(background, (-50, -50))

        text_coord = 100
        string_rendered = font.render("1 Уровень", True, pygame.Color('white'))
        intro_rect1 = string_rendered.get_rect()
        intro_rect1.x = 10
        intro_rect1.top = text_coord
        screen.blit(string_rendered, intro_rect1)

        text_coord = 150
        string_rendered = font.render("2 Уровень", True, pygame.Color('white'))
        intro_rect2 = string_rendered.get_rect()
        intro_rect2.x = 10
        intro_rect2.top = text_coord
        screen.blit(string_rendered, intro_rect2)

        text_coord = 200
        string_rendered = font.render("3 Уровень", True, pygame.Color('white'))
        intro_rect3 = string_rendered.get_rect()
        intro_rect3.x = 10
        intro_rect3.top = text_coord
        screen.blit(string_rendered, intro_rect3)

        # Обработчик событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if intro_rect1.collidepoint(mouse_x, mouse_y):
                    main(battle_music, sound_enabled, name)
                if intro_rect2.collidepoint(mouse_x, mouse_y):
                    main2(battle_music, sound_enabled, name)
                if intro_rect3.collidepoint(mouse_x, mouse_y):
                    main3(battle_music, sound_enabled, name)








        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # FPS

    pygame.quit()