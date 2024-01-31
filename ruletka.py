import pygame
from random import randint
import os
import random
import sys

# загрузка изображений
def load_image(name):
    q = os.path.abspath('data')
    fullname = os.path.join(q, name)
    image = pygame.image.load(fullname)
    return image

# отображение уровня на экран
def update_level(screen):
    fon = pygame.transform.scale(load_image('fon.png'), (500, 500))
    screen.blit(fon, (0, 0))


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
screen_rect = (0, 0, 500, 500)

# класс для круга
class Landing(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, img):
        self.image = img
        self.num = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.pos = (pos_x, pos_y)
    # поворот круга
    def turn(self, angle, x, y):
        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(center=(x, y)).center)
        self.num = (self.num + 4) % 360

        return rotated_image, new_rect

# класс для создания объектов
class obje(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, img):
        self.image = img
        self.num = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.pos = (pos_x, pos_y)
    # поворот предметов
    def turn(self, angle, x, y):
        w, h = self.image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        origin = (x + min_box[0], y - max_box[1])
        rotated_image = pygame.transform.rotate(self.image, angle)

        return rotated_image, origin

# генерация партиклов
class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, img):
        super().__init__(all_sprites)
        self.fire = [pygame.transform.scale(load_image(img), (25, 25))]
        # сгенерируем частицы разного размера
        for scale in (5, 10, 20):
            self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.2

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position, img):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), img)

# запуск мини-игры
def rulet():
    pygame.init()
    pygame.display.set_caption('блюдо')
    size = (500, 500)
    fps = 30
    clock = pygame.time.Clock()
    pygame.display.set_mode(size)
    screen = pygame.display.set_mode(size)
    # прописываем значения переменных
    running = True
    pr1 = True
    pr2 = True
    pr3 = True
    pr4 = True
    win = False
    angle0 = 0
    angle1 = 0
    angle2 = 90
    angle3 = 180
    angle4 = 270
    time = 0
    timer = 0
    objfall = 0
    kumai = True
    # прописываем изображения
    kn = pygame.transform.scale(load_image('kn.png'), (100, 100))
    knbtn = pygame.transform.scale(load_image('32262.png'), (100, 100))
    kn = pygame.transform.rotate(kn, -120)
    # прописываем предметы
    rit1 = Landing(250, 250, pygame.transform.scale(load_image('latest.png'), (245, 245)))
    rit2 = Landing(150, 300, pygame.transform.scale(load_image('bag.png'), (200, 200)))
    obj1 = obje(200, 200, pygame.transform.scale(load_image('myka.png'), (85, 85)))
    obj2 = obje(100, 100, pygame.transform.scale(load_image('milk.png'), (90, 90)))
    obj3 = obje(100, 100, pygame.transform.scale(load_image('egg.png'), (100, 100)))
    obj4 = obje(100, 100, pygame.transform.scale(load_image('other.png'), (100, 100)))
    # цикл для мини-игры
    while running:
        # проверка инпутов от игрока
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r] == 1:
                running = False
            if keys[pygame.K_q] == 1:
                kumai = False
                if 350 <= rit1.num or rit1.num <= 10:
                    if pr1:
                        create_particles((250, 350), 'myka.png')
                    pr1 = False
                if 80 <= rit1.num <= 100:
                    if pr2:
                        create_particles((250, 350), 'milk.png')
                    pr2 = False
                if 170 <= rit1.num <= 190:
                    if pr3:
                        create_particles((250, 350), 'egg.png')
                    pr3 = False
                if 260 <= rit1.num <= 280:
                    if pr4:
                        create_particles((250, 350), 'other.png')
                    pr4 = False
            else:
                kumai = True

        # поворот предметов
        rb1 = rit1.turn(angle0, 250, 130)
        im1, de1 = rb1[0], rb1[1]
        angle0 -= 4
        or1 = obj1.turn(angle1, 250, 130)
        om1, od1 = or1[0], or1[1]
        angle1 -= 4
        or2 = obj2.turn(angle2, 250, 130)
        om2, od2 = or2[0], or2[1]
        angle2 -= 4
        or3 = obj3.turn(angle3, 250, 130)
        om3, od3 = or3[0], or3[1]
        angle3 -= 4
        or4 = obj4.turn(angle4, 250, 130)
        om4, od4 = or4[0], or4[1]
        angle4 -= 4

        all_sprites.update()
        update_level(screen)
        all_sprites.draw(screen)
        screen.blit(im1, de1)
        screen.blit(knbtn, (400, 300))
        screen.blit(rit2.image, rit2.pos)
        # проверка, какие предметы сбиты
        if pr1:
            screen.blit(om1, od1)
        else:
            objfall += 1
        if pr2:
            screen.blit(om2, od2)
        else:
            objfall += 1
        if pr3:
            screen.blit(om3, od3)
        else:
            objfall += 1
        if pr4:
            screen.blit(om4, od4)
        else:
            objfall += 1

        if kumai:
            poskn = (300, 350)
            screen.blit(kn, poskn)
        else:
            poskn = (260, 220)
            screen.blit(kn, poskn)
        pygame.display.flip()
        timer = (timer + 1) % 30
        if timer == 0:
            time += 1
        clock.tick(30)
        if objfall == 4:
            win = True
            running = False
        else:
            objfall = 0
    return [time, win]
    pygame.quit()
