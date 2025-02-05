import pygame


def Settings():
    from begining import Begining
    from begining import But

    pygame.init()

    WIDTH, HEIGHT = 650, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Settings")
    background = pygame.image.load("backgroundset.png").convert()
    background = pygame.transform.scale(background, (750, 750))
    all_sprites = pygame.sprite.Group()

    running = True
    clock = pygame.time.Clock()
    but1 = But(0, 0, 70, "return.png")
    all_sprites.add(but1)

    while running:
        screen.blit(background, (-50, -50))

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
