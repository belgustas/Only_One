import pygame


def Settings(battle_music, sound_enabled):
    from begining import Begining
    from begining import But

    pygame.init()

    WIDTH, HEIGHT = 650, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Settings")
    background = pygame.image.load("img/backgroundset.png").convert()
    background = pygame.transform.scale(background, (750, 750))
    all_sprites = pygame.sprite.Group()

    but1 = But(0, 0, 70, "img/return.png")
    sound_button = But(WIDTH // 2 - 50, HEIGHT // 2 - 65, 100, "img/check_button.png")
    all_sprites.add(but1, sound_button)

    running = True
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)  # Шрифт для текста

    while running:
        screen.blit(background, (-50, -50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                but1.clicked(mouse_x, mouse_y, lambda: Begining(battle_music, sound_enabled))
                if sound_button.rect.collidepoint(mouse_x, mouse_y):
                    sound_enabled = not sound_enabled
                    battle_music.set_volume(0.3 if sound_enabled else 0)

        all_sprites.update()
        all_sprites.draw(screen)

        # Отображение состояния звука
        sound_status = "Sound: ON" if sound_enabled else "Sound: OFF"
        text = font.render(sound_status, True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - 60, HEIGHT // 2 + 50))  # Размещаем текст чуть ниже кнопки

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
