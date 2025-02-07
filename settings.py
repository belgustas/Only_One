import pygame

def Settings():
    from begining import Begining
    from begining import But
    from main import main

    pygame.init()

    WIDTH, HEIGHT = 650, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Settings")
    background = pygame.image.load("backgroundset.png").convert()
    background = pygame.transform.scale(background, (750, 750))
    all_sprites = pygame.sprite.Group()

    # Переменная для управления звуком
    sound_enabled = True

    # Загрузка звука (пример)
    pygame.mixer.music.load("sounds/battle_music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)  # Зацикливаем музыку

    running = True
    clock = pygame.time.Clock()

    # Кнопка возврата
    but1 = But(0, 0, 70, "return.png")
    # Кнопка для включения/выключения звука
    sound_button = But(WIDTH // 2 - 100, HEIGHT // 2 - 65, 100, "img/check_button.png")  # Замените "check_button.png" на ваше изображение кнопки
    all_sprites.add(but1, sound_button)

    while running:
        screen.blit(background, (-50, -50))

        # Обработчик событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                but1.clicked(mouse_x, mouse_y, Begining)
                # Проверка нажатия на кнопку звука
                if sound_button.rect.collidepoint(mouse_x, mouse_y):
                    sound_enabled = not sound_enabled  # Переключаем состояние звука
                    if sound_enabled:
                        pygame.mixer.music.set_volume(0.3)  # Включаем звук
                    else:
                        pygame.mixer.music.set_volume(0)  # Выключаем звук

        all_sprites.update()
        all_sprites.draw(screen)

        # Отображение состояния звука на экране
        font = pygame.font.Font(None, 36)
        sound_status = "Sound: ON" if sound_enabled else "Sound: OFF"
        text = font.render(sound_status, True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(60)  # FPS

    pygame.quit()