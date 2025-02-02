import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, ):
        super().__init__()
        self.all_sprites = all_sprites
        self.sprite_sheet = pygame.image.load("img/Player.png").convert_alpha()

        # Ряды в спрайт шите для анимации хотьбы
        self.ROWS = {"up": 8, "down": 10, "left": 9, "right": 11, "shoot_up": 16, "shoot_down": 18, "shoot_left": 17,
                     "shoot_right": 19}

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
        self.KEY_2_dir = ""
        self.is_moving = False
        self.frame_index = 0
        self.frame_delay = 100
        self.last_update = pygame.time.get_ticks()
        self.afk_timer = 0

    def update(self):
        self.run()
        self.animation()
        self.check_afk()

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
        if self.rect.right > 672:
            self.rect.right = 672
        if self.rect.top < -20:
            self.rect.top = -20
        if self.rect.bottom > 650:
            self.rect.bottom = 650

        # Проверка диагонального движения
        if player_x != 0 and player_y != 0:
            player_x /= math.sqrt(2)  # уменьшаем скорость, чтобы игрок не летал по диагонали
            player_y /= math.sqrt(2)

        self.rect.x += player_x
        self.rect.y += player_y
        self.is_moving = player_x != 0 or player_y != 0

        if self.is_moving:
            self.afk_timer = pygame.time.get_ticks()

    def shoot(self, mouse_x, mouse_y):
        """ Создаем пулю и запускаем анимацию стрельбы """
        bullet = Bullet(self.rect.centerx, self.rect.centery, mouse_x, mouse_y)
        self.all_sprites.add(bullet)

        # Определение направления стрельбы
        dx, dy = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        if abs(dx) > abs(dy):
            self.KEY = "shoot_right" if dx > 0 else "shoot_left"
        else:
            self.KEY = "shoot_down" if dy > 0 else "shoot_up"

        # Устанавливаем начальный кадр анимации стрельбы
        self.frame_index = 0

    def animation(self):
        """ Обновляем кадры анимации """
        if self.is_moving or "shoot" in self.KEY:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update > self.frame_delay:
                self.frame_index = (self.frame_index + 1) % 9
                self.image = self.animations[self.KEY][self.frame_index]
                self.last_update = current_time

    def check_afk(self):
        if not self.is_moving and pygame.time.get_ticks() - self.afk_timer > 10000:
            self.image = self.stop_cadr  # Если прошло 10 секунд без движения — ставим AFK-кадр


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, mouse_x, mouse_y):
        super().__init__()

        self.image = pygame.image.load("img/bullet_img.png").convert_alpha()
        self.rect = self.image.get_rect(center=(player_x, player_y))

        # Вычисляем направление пули
        dx, dy = mouse_x - player_x, mouse_y - player_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx, dy = mouse_x - player_x, mouse_y - player_y
        self.degrees = math.degrees(math.atan2(-dy, dx))  # Угол в градусах
        self.image = pygame.transform.rotate(self.image, self.degrees)

        if distance != 0:
            self.velocity = (dx / distance * 10, dy / distance * 10)  # скорость полета
        else:
            self.velocity = (0, 0)  # На случай, если расстояние 0

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Удаление пули, если она вышла за границы экрана
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()

