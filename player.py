import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, hp):
        super().__init__()
        self.all_sprites = all_sprites

        self.sprite_sheet = pygame.image.load("img/Player.png").convert_alpha()

        # Ряды в спрайтшите для анимации
        self.ROWS = {
            "up": 8, "down": 10, "left": 9, "right": 11,
            "shoot_up": 16, "shoot_down": 18, "shoot_left": 17, "shoot_right": 19
        }

        # Создание списков кадров
        self.animations = {direction: [] for direction in self.ROWS}
        for direction, row in self.ROWS.items():
            for col in range(9):
                frame = self.sprite_sheet.subsurface(
                    pygame.Rect(col * 64, row * 64, 64, 64))
                self.animations[direction].append(frame)

        # Кадр стоячего игрока
        self.stop_cadr = self.sprite_sheet.subsurface(pygame.Rect(0, 2 * 64, 64, 64))

        # Константы
        self.image = self.stop_cadr
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3
        self.KEY = "down"
        self.is_moving = False
        self.is_shooting = False  # флаг стрельбы
        self.frame_index = 0
        self.frame_delay = 100
        self.last_update = pygame.time.get_ticks()
        self.afk_timer = 0
        self.hp = hp
        self.count = 0

    def collide(self, health_bar_player, enemy, aids):
        self.count += 1
        if self.rect.colliderect(enemy):
            self.hp -= 3
            health_bar_player.hp -= 3
        if self.hp <= 0:
            self.kill()

    def update(self):
        self.run()
        self.animation()
        self.check_afk()

    def run(self):
        if self.is_shooting:  # Если игрок стреляет, он не должен двигаться
            return

        keys = pygame.key.get_pressed()
        player_x, player_y = 0, 0
        # ходьба
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
        if self.is_shooting:  # Нельзя стрелять, пока не завершилась анимация предыдущего выстрела
            return

        bullet = Bullet(self.rect.centerx, self.rect.centery, mouse_x, mouse_y)
        self.all_sprites.add(bullet)

        # Определение направления стрельбы
        dx, dy = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        if abs(dx) > abs(dy):
            if dx > 0:
                self.KEY = "shoot_right"
            else:
                self.KEY = "shoot_left"
        else:
            if dy > 0:
                self.KEY = "shoot_down"
            else:
                self.KEY = "shoot_up"

        # Запуск анимации стрельбы
        self.is_shooting = True
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()

    def animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.frame_delay:
            self.last_update = current_time

            if self.is_shooting:
                # Анимация стрельбы (ограничена 5 кадрами, чтобы не зацикливалась)
                if self.frame_index < 5:
                    self.image = self.animations[self.KEY][self.frame_index]
                    self.frame_index += 1
                else:
                    self.is_shooting = False  # Останавливаем анимацию
                    self.frame_index = 0
                    self.image = self.stop_cadr  # Возвращаем обычное состояние

            elif self.is_moving:
                # Анимация движения
                self.frame_index = (self.frame_index + 1) % 9
                self.image = self.animations[self.KEY][self.frame_index]

    def check_afk(self):
        if not self.is_moving and pygame.time.get_ticks() - self.afk_timer > 10000:
            self.image = self.stop_cadr  # Если прошло 10 секунд без движения — ставим AFK-кадр



class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, mouse_x, mouse_y):
        super().__init__()

        self.image = pygame.image.load("img/bullet_img.png").convert_alpha()
        self.rect = self.image.get_rect(center=(player_x, player_y))

        # Вычисляем направление пули
        now_x, now_y = mouse_x - player_x, mouse_y - player_y
        distance = math.sqrt(now_x ** 2 + now_y ** 2)

        dx, dy = mouse_x - player_x, mouse_y - player_y
        self.degrees = math.degrees(math.atan2(-dy, dx))  # Угол в градусах
        self.image = pygame.transform.rotate(self.image, self.degrees)

        if distance != 0:
            self.velocity = (dx / distance * 10, dy / distance * 10)  # скорость полета
        else:
            self.velocity = (0, 0)  # На случай, если расстояние 0

    def update(self):
        if self.velocity != 0:
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
        # Удаление пули, если она вышла за границы экрана
        if self.rect.left < -10:
            self.kill()
        if self.rect.right > 660:
            self.kill()
        if self.rect.top < -10:
            self.kill()
        if self.rect.bottom > 640:
            self.kill()


class HealthBarPlayer(pygame.sprite.Sprite):
    def __init__(self, player, w, h, max_hp):
        super().__init__()
        self.player = player  # Связываем хп с игроком
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
        self.x = self.player.rect.centerx - self.w // 2  # Центрируем по х
        self.y = self.player.rect.top - self.h - 5  # Чуть выше игрока

    def hurt(self):
        self.hp -= 1

    def update(self):
        # координаты игрока
        self.x = self.player.rect.centerx - self.w // 2
        self.y = self.player.rect.top - self.h - 5

    def draw(self, surface):
        count_hp = self.hp / self.max_hp  # Рассчитываем % здоровья
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))  # Фон (красный)
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * count_hp, self.h))  # Текущий хп (зеленый)
