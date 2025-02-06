import pygame
import sqlite3



def leaders():
    from begining import Begining
    from begining import But
    from db import leadtable
    pygame.init()

    WIDTH, HEIGHT = 650, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Leaders")
    background = pygame.image.load("background.jpg").convert()
    background = pygame.transform.scale(background, (750, 750))
    all_sprites = pygame.sprite.Group()

    running = True
    clock = pygame.time.Clock()
    but1 = But(0, 0, 70, "return.png")
    all_sprites.add(but1)

    intro_text = leadtable()

    screen.blit(background, (-50, -50))
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

    while running:


        # Обработчик событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                but1.clicked(mouse_x, mouse_y, Begining)

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # FPS

    pygame.quit()
