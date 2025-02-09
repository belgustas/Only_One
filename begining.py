import pygame
import sys
import os

from db import change


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class But(pygame.sprite.Sprite):
    from db import change
    def __init__(self, WIDTH, HEIGHT, low, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(name)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT
        self.low = low

    def clicked(self, x, y, func):
        if self.rect.collidepoint(x, y):
            func()

    def changes(self, x, y, func, name, score):
        if self.rect.collidepoint(x, y):
            change(name, score)
            func()



def Begining(battle_music=None, sound_enabled=True):
    from Auto import Auto
    from main import main
    from leaders import leaders
    from settings import Settings
    pygame.init()

    WIDTH, HEIGHT = 650, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Begining")
    background = pygame.image.load("img/backgroundfor.jpg").convert()
    background = pygame.transform.scale(background, (750, 750))
    all_sprites = pygame.sprite.Group()

    running = True
    clock = pygame.time.Clock()
    but1 = But(WIDTH // 3 - 50, HEIGHT // 2 - 35, 70, "img/settings.png")
    but2 = But(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, "img/Play.png")
    but3 = But(WIDTH // 3 * 2 - 20, HEIGHT // 2 - 35, 70, "img/leaders.png")
    all_sprites.add(but1, but2, but3)

    while running:
        screen.blit(background, (-50, -50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                but1.clicked(mouse_x, mouse_y, lambda: Settings(battle_music, sound_enabled))
                but2.clicked(mouse_x, mouse_y, lambda: Auto(battle_music, sound_enabled))
                but3.clicked(mouse_x, mouse_y, lambda: leaders(battle_music, sound_enabled))

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    battle_music = pygame.mixer.Sound("sounds/battle_music.mp3")
    battle_music.set_volume(0.3)
    battle_music.play(-1)
    Begining(battle_music, True)
