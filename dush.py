import pygame
from random import randint
import os
import sys


rot1, rot2, rot3 = 9, 4, 11

# загрузка изображений
def load_image(name):
    q = os.path.abspath('data')
    fullname = os.path.join(q, name)
    image = pygame.image.load(fullname)
    return image


w = load_image('крутилка1.png')

# отображение уровня на экран
def update_level(screen, img):
    fon = pygame.transform.scale(load_image(img), (562, 650))
    screen.blit(fon, (0, 0))


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# класс для создания объектов
class Landing(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, img):
        self.image = img
        self.num = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.pos = (pos_x, pos_y)

    # поворот предмета на 30 градусов
    def turn(self, angle, x, y):
        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(center=(x, y)).center)
        self.num = (self.num + 1) % 12

        return rotated_image, new_rect

# запуск мини-игры
def dush():
    pygame.init()
    pygame.display.set_caption('Духовка')
    size = (562, 650)
    fps = 30
    img = 'Duhovka_closed.png'
    time = 0
    timer = 0
    clock = pygame.time.Clock()
    pygame.display.set_mode(size)
    screen = pygame.display.set_mode(size)
    background_image = pygame.Color('white')
    running = True
    win = False
    att = True
    angle1 = -30
    angle2 = -30
    angle3 = -30
    rit1 = Landing(43, 30, pygame.transform.scale(load_image('крутилка1.png'), (75, 75)))
    im1 = rit1.image
    de1 = (43, 30)
    rit2 = Landing(177, 30, pygame.transform.scale(load_image('крутилка2.png'), (75, 75)))
    im2 = rit2.image
    de2 = (177, 30)
    rit3 = Landing(318, 30, pygame.transform.scale(load_image('крутилка3.png'), (75, 75)))
    knbtn = pygame.transform.scale(load_image('31929.png'), (100, 100))

    im3 = rit3.image
    de3 = (318, 30)
    # цикл для мини-игры
    while running:
        # проверка инпутов от игрока
        for event in pygame.event.get():
            update_level(screen, img)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r] == 1:
                running = False
                if att:
                    win = 'no'
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos
                if att:
                    if 43 <= x1 <= 118 and 30 <= y1 <= 105:
                        rb1 = rit1.turn(angle1, 80, 68)
                        im1, de1 = rb1[0], rb1[1]
                        angle1 -= 30
                if att:
                    if 177 <= x1 <= 252 and 30 <= y1 <= 105:
                        rb2 = rit2.turn(angle2, 215, 68)
                        im2, de2 = rb2[0], rb2[1]
                        angle2 -= 30
                if att:
                    if 318 <= x1 <= 393 and 30 <= y1 <= 105:
                        rb3 = rit3.turn(angle3, 356, 68)
                        im3, de3 = rb3[0], rb3[1]
                        angle3 -= 30
                if att:
                    if 440 <= x1 <= 550 and 20 <= y1 <= 120:
                        att = False
                        if rit1.num == rot1 and rit2.num == rot2 and rit3.num == rot3:
                            win = True
                            img = 'Dush_win.png'
                        else:
                            img = 'Dush_lose.png'
        screen.blit(im1, de1)
        screen.blit(im2, de2)
        screen.blit(im3, de3)
        screen.blit(knbtn, (0, 550))
        pygame.display.flip()
        timer = (timer + 1) % 30
        if timer == 0:
            time += 1
        clock.tick(30)
    return [time, win]
    pygame.quit()


if __name__ == "__main__":
    print(dush())
