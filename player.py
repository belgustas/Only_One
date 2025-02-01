import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprite_sheet = pygame.image.load("img/Player.png").convert_alpha()

        # Параметры спрайтов
        self.SPRITE_WIDTH = 64
        self.SPRITE_HEIGHT = 64
        self.COLS = 9
        self.IDLE_ROW = 2
        self.IDLE_FRAME = 0

        # Ряды в спрайт шите для анимации хотьбы
        self.ROWS = {"UP": 8, "DOWN": 10, "LEFT": 9, "RIGHT": 11}

        # Создание списков кадров
        self.animations = {direction: [] for direction in self.ROWS}
        for direction, row in self.ROWS.items():
            for col in range(self.COLS):
                frame = self.sprite_sheet.subsurface(
                    pygame.Rect(col * self.SPRITE_WIDTH, row * self.SPRITE_HEIGHT, self.SPRITE_WIDTH,
                                self.SPRITE_HEIGHT)
                )
                self.animations[direction].append(frame)

        # Кадр покоя
        self.idle_frame = self.sprite_sheet.subsurface(
            pygame.Rect(self.IDLE_FRAME * self.SPRITE_WIDTH, self.IDLE_ROW * self.SPRITE_HEIGHT, self.SPRITE_WIDTH,
                        self.SPRITE_HEIGHT)
        )

        self.image = self.idle_frame  # Начальный спрайт
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 3
        self.current_direction = "DOWN"
        self.is_moving = False
        self.frame_index = 0
        self.frame_delay = 100
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.move()
        self.animate()

    def move(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_w]:
            dy -= self.speed
            self.current_direction = "UP"
        if keys[pygame.K_s]:
            dy += self.speed
            self.current_direction = "DOWN"
        if keys[pygame.K_a]:
            dx -= self.speed
            self.current_direction = "LEFT"
        if keys[pygame.K_d]:
            dx += self.speed
            self.current_direction = "RIGHT"

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
        if dx != 0 and dy != 0:
            dx /= math.sqrt(2)  # уменьшаем скорость, чтобы игрок не летал по диагонали
            dy /= math.sqrt(2)

        self.rect.x += dx
        self.rect.y += dy
        self.is_moving = dx != 0 or dy != 0

    # анимация
    def animate(self):
        if self.is_moving:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update > self.frame_delay:
                self.frame_index = (self.frame_index + 1) % self.COLS
                self.image = self.animations[self.current_direction][self.frame_index]
                self.last_update = current_time
        else:
            self.image = self.idle_frame
