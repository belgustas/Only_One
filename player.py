import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprite_sheet = pygame.image.load("img/Player.png").convert_alpha()

        # Ряды в спрайт шите для анимации хотьбы
        self.ROWS = {"up": 8, "down": 10, "left": 9, "right": 11}

        # Создание списков кадров
        self.animations = {direction: [] for direction in self.ROWS}
        for direction, row in self.ROWS.items():
            for col in range(9):
                frame = self.sprite_sheet.subsurface(
                    pygame.Rect(col * 64, row * 64, 64, 64))
                self.animations[direction].append(frame)

        # Кадр стоячего
        self.stop_cadr = self.sprite_sheet.subsurface(pygame.Rect(0 * 64, 2 * 64, 64, 64))

        self.image = self.stop_cadr
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 3
        self.KEY = "down"
        self.is_moving = False
        self.frame_index = 0
        self.frame_delay = 100
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.run()
        self.animation()

    def run(self):
        keys = pygame.key.get_pressed()
        player_x, player_y = 0, 0

        if keys[pygame.K_w]:
            player_y -= self.speed
            self.KEY = "up"
        if keys[pygame.K_s]:
            player_y += self.speed
            self.KEY = "down"
        if keys[pygame.K_a]:
            player_x -= self.speed
            self.KEY = "left"
        if keys[pygame.K_d]:
            player_x += self.speed
            self.KEY = "right"

        # проверка, что человек не выбежал за поле
        if self.rect.left < -20:
            self.rect.left = -20
        if self.rect.right > 522:
            self.rect.right = 522
        if self.rect.top < -20:
            self.rect.top = -20
        if self.rect.bottom > 500:
            self.rect.bottom = 500

        # Проверка диагонального движения
        if player_x != 0 and player_y != 0:
            player_x /= math.sqrt(2)  # уменьшаем скорость, чтобы игрок не летал по диагонали
            player_y /= math.sqrt(2)

        self.rect.x += player_x
        self.rect.y += player_y
        self.is_moving = player_x != 0 or player_y != 0

    # анимация
    def animation(self):
        if self.is_moving:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update > self.frame_delay:
                self.frame_index = (self.frame_index + 1) % 9
                self.image = self.animations[self.KEY][self.frame_index]
                self.last_update = current_time
        else:
            self.image = self.stop_cadr
