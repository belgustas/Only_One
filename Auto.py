import pygame

from Choose import choose


def Auto(battle_music, sound_enabled):  # авторизация
    from main import main
    from db import input
    from Choose import choose
    pygame.init()
    font = pygame.font.Font(None, 30)

    WIDTH, HEIGHT = 650, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("img/Auto")
    background = pygame.image.load("img/backgroundfor.jpg").convert()
    background = pygame.transform.scale(background, (750, 750))
    all_sprites = pygame.sprite.Group()

    running = True
    clock = pygame.time.Clock()
    need_inp = True
    input_text = ""
    while running:
        screen.blit(background, (-50, -50))

        # Обработчик событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if need_inp and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input(input_text)
                    print(battle_music, sound_enabled)
                    choose(battle_music, sound_enabled, input_text)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        string_rendered = font.render(input_text, 1, pygame.Color('Red'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = WIDTH // 2
        intro_rect.y = HEIGHT // 2
        screen.blit(string_rendered, intro_rect)

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # FPS

    pygame.quit()
