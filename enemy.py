import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, target, hp):
        super().__init__()
        self.sprite_sheet = pygame.image.load("img/Enemy.png").convert_alpha()
        self.ROWS = {"up": 8, "down": 10, "left": 9, "right": 11}

        # Загрузка анимации
        self.animations = {direction: [] for direction in self.ROWS}
        for direction, row in self.ROWS.items():
            for col in range(9):
                frame = self.sprite_sheet.subsurface(pygame.Rect(col * 64, row * 64, 64, 64))
                self.animations[direction].append(frame)

        self.image = self.animations["down"][0]  # Начальный спрайт
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)  # Создаем маску для врага

        self.target = target  # бегать за целью
        self.speed = 1.25  # Скорость врага
        self.frame_index = 0
        self.frame_delay = 100
        self.last_update = pygame.time.get_ticks()
        self.current_direction = "down"
        self.hp_enemy = hp

    def update(self):
        self.move_towards_player()
        self.animate()

    def move_towards_player(self):
        if self.rect.x < self.target.rect.x:
            self.rect.x += self.speed
            self.current_direction = "right"

        elif self.rect.x > self.target.rect.x:
            self.rect.x -= self.speed
            self.current_direction = "left"

        if self.rect.y < self.target.rect.y:
            self.rect.y += self.speed
            self.current_direction = "down"
        elif self.rect.y > self.target.rect.y:
            self.rect.y -= self.speed
            self.current_direction = "up"

    def animate(self):
        now_tick = pygame.time.get_ticks()
        if now_tick - self.last_update > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % 9
            self.image = self.animations[self.current_direction][self.frame_index]
            self.last_update = now_tick

    def collide_with_bullet(self, bullet, health_bar_enemy):
        if pygame.sprite.collide_mask(self, bullet):  # Проверяем столкновение по маскам
            self.hp_enemy -= 10
            health_bar_enemy.hp -= 10
            bullet.kill()  # Удаляем пулю
            if self.hp_enemy <= 0:
                self.kill()

    def distance_to_player(self):
        return abs(self.target.rect.x - self.rect.x) + abs(self.target.rect.y - self.rect.y)


class HealthBarEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy, w, h, max_hp):
        super().__init__()
        self.enemy = enemy  # Связываем хп с врага
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
        self.x = self.enemy.rect.centerx - self.w // 2  # Центрируем по х
        self.y = self.enemy.rect.top - self.h - 5  # Чуть выше игрока

    def update(self):
        # координаты игрока
        self.x = self.enemy.rect.centerx - self.w // 2
        self.y = self.enemy.rect.top - self.h - 5

    def draw(self, surface):
        count_hp = self.hp / self.max_hp  # Рассчитываем % здоровья
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))  # Фон (красный)
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * count_hp, self.h))  # Текущий хп (зеленый)