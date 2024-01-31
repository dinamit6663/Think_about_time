import sqlite3

import pygame
import os
import sys
from wires import wires
from dush import dush
from ruletka import rulet


# загрузка изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# загрузка изображений для ходьбы
def load_nin(name, colorkey=None):
    fullname = os.path.join('data/Running', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Think about time')
screen_size = (1400, 800)
screen = pygame.display.set_mode(screen_size)
FPS = 30

tile_width = tile_height = 50


# класс для создания объектов
class Landing(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, img1, img2):
        super().__init__(tiles_group, all_sprites)
        self.image = img1
        self.img1 = img1
        self.img2 = img2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.pos = (pos_x, pos_y)

    # проверяет нахождение игрока рядом и меняем картинку
    def update(self):
        if pygame.sprite.collide_mask(self, hero):
            self.image = self.img2
            return True
        else:
            self.image = self.img1


# класс для создания игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames = [load_nin(i) for i in os.listdir("data/Running")]

        self.cur_frame = 0
        self.turn = 2
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (250, 250))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.pos = (pos_x, pos_y)
        self.ifmo = False

    # передвижение игрока
    def move(self, x, y, turn):
        self.pos = (x, y)
        if turn == 1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            new_sprite = pygame.transform.scale(self.frames[self.cur_frame], (250, 250))
            self.image = pygame.transform.flip(new_sprite, True, False)
            self.turn = 1

        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (250, 250))
            self.turn = 0
        self.rect = self.image.get_rect().move(
            self.pos[0], self.pos[1])

    # поворот игрока
    def update(self):
        if self.turn == 1:
            self.image = pygame.transform.flip(pygame.transform.scale(load_image('0_Samurai_Idle_000.png'), (250, 250)),
                                               True, False)
        else:
            self.image = pygame.transform.scale(load_image('0_Samurai_Idle_000.png'), (250, 250))


player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


# загрузка списка лидеров из таблицы
def loaddata():
    world_place = 0
    connection = sqlite3.connect('rating.db')
    cur = connection.cursor()
    sqlquery = ('SELECT name, time '
                'FROM score')
    # выбираем столбцы имя пользователя и время активности (они связаны) и сортируем по убыванию времени
    number, nickname, time = [], [], []
    for row in cur.execute(sqlquery):
        world_place += 1
        number.append(f'{world_place}')
        nickname.append(f'{row[0]}')
        time.append(f'{(row[1] % 3600) // 60}мин {row[1] % 60}cек')
    connection.commit()
    connection.close()
    return number, nickname, time
    # в базе данных время для удобства выражено в секундах,
    # для удобного же восприятия пользователем в таблицу мы выводим время переводя его в стандартный вид


# выход из игры
def terminate():
    pygame.quit()
    sys.exit()


# передвижение игрока
def move(hero, movement):
    x, y = hero.pos
    if movement == 'left':
        if x > 0:
            hero.move(x - 15, y, 1)
    if movement == 'right':
        if x <= 1400:
            hero.move(x + 15, y, 0)
    if movement == 'down':
        hero.move(x, y + 400, 0)
    if movement == 'up':
        hero.move(x, y - 400, 0)
    if movement == 'tp':
        hero.move(0, 150, 0)


# показ списка лидеров на экране
def leaders():
    fon = pygame.transform.scale(load_image('rating_screen.png'), (1400, 800))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 200
    backbtn2 = pygame.Rect(90, 15, 240, 100)
    backbtn = pygame.transform.scale(load_image('back_buttom.png'), (400, 300))
    number, nickname, time = loaddata()
    # вывод в 3 строки номера, имени и времеени игрока
    for line in number:
        string = font.render(line, 1, pygame.Color('white'))
        intro_rect = string.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string, intro_rect)

    text_coord = 200
    for line in nickname:
        string = font.render(line, 1, pygame.Color('white'))
        intro_rect = string.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 550
        text_coord += intro_rect.height
        screen.blit(string, intro_rect)

    text_coord = 200
    for line in time:
        string = font.render(line, 1, pygame.Color('white'))
        intro_rect = string.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 1100
        text_coord += intro_rect.height
        screen.blit(string, intro_rect)
    text_coord = 205
    for line in range(len(time) + 1):
        pygame.draw.line(screen, pygame.Color('white'), (100, text_coord), (1300, text_coord), 1)
        text_coord += 30
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backbtn2.collidepoint(event.pos):
                    return

        pygame.display.flip()
        screen.blit(backbtn, (-20, -80))
        clock.tick(50)


# стартовый экран
def start_screen():
    pygame.mixer.music.set_volume(0.0)
    fon = pygame.transform.scale(load_image('fonk.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    input_box = pygame.Rect(830, 120, 400, 60)
    backbtn2 = pygame.Rect(40, 180, 340, 110)
    startbtn2 = pygame.Rect(40, 15, 340, 110)
    ratingbtn2 = pygame.Rect(40, 335, 340, 110)
    color_inactive = pygame.Color('black')
    color_active = pygame.Color('purple')
    color = color_inactive
    backbtn = pygame.transform.scale(load_image('exit_button.png'), (400, 300))
    startbtn = pygame.transform.scale(load_image('start_button.png'), (400, 300))
    ratingbtn = pygame.transform.scale(load_image('rating_button.png'), (400, 300))
    instruction = pygame.transform.scale(load_image('instruction.png'), (500, 300))
    active = False
    text = ''
    nicname = 'user'
    string = font.render('Введите имя:', 1, pygame.Color('purple'))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # Change the current color of the input box.
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                if startbtn2.collidepoint(event.pos):
                    return nicname
                if ratingbtn2.collidepoint(event.pos):
                    leaders()
                if backbtn2.collidepoint(event.pos):
                    return
            color = color_active if active else color_inactive
            # ввод имени
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        nicname = text
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        fon = pygame.transform.scale(load_image('fonk.png'), screen_size)

        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 50)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        screen.blit(startbtn, (10, -80))
        screen.blit(backbtn, (10, 80))
        screen.blit(ratingbtn, (10, 240))
        screen.blit(string, (800, 60))
        screen.blit(instruction, (10, 480))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(50)


# финальный экран
def final_screen(time, timef1, timef2, name):
    pygame.mixer.music.set_volume(0.0)
    # берём значения игрока
    intro_text = [f'{(timef1 % 3600) // 60} мин {timef1 % 60} cек',
                  f'{(timef2 % 3600) // 60} мин {timef2 % 60} cек',
                  f'{(time % 3600) // 60} мин {time % 60} cек']
    connection = sqlite3.connect('rating.db')
    cursor = connection.cursor()
    past_activity = cursor.execute(f"SELECT time "
                                   f"FROM score WHERE name = ?",
                                   (f'{name}',)).fetchall()

    best_time = int(past_activity[0][0])
    fon = pygame.transform.scale(load_image('result_screen.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 180
    for line in intro_text:
        string = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string.get_rect()
        text_coord += 105
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string, intro_rect)
    string = font.render(f'{(best_time % 3600) // 60} мин {best_time % 60} cек', 1, pygame.Color('yellow'))
    screen.blit(string, (900, 250))
    backbtn2 = pygame.Rect(90, 15, 240, 100)
    backbtn = pygame.transform.scale(load_image('back_buttom.png'), (400, 300))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backbtn2.collidepoint(event.pos):
                    return
        screen.blit(backbtn, (-20, -80))
        pygame.display.flip()
        clock.tick(50)


# прописываем предметы
hero = Player(0, 150)
tr1 = Landing(570, 50, pygame.transform.scale(load_image('lift-1down.png'), (250, 300)),
              pygame.transform.scale(load_image('lift-2down.png'), (250, 300)))
tr2 = Landing(570, 450, pygame.transform.scale(load_image('lift-1up.png'), (250, 300)),
              pygame.transform.scale(load_image('lift-2up.png'), (250, 300)))
elec = Landing(350, 80, pygame.transform.scale(load_image('elec1.png'), (160, 160)),
               pygame.transform.scale(load_image('elec2.png'), (140, 160)))
bag = Landing(1100, 200, pygame.transform.scale(load_image('bag.png'), (150, 200)),
              pygame.transform.scale(load_image('bag.png'), (150 * 1.1, 200 * 1.1)))
dux = Landing(280, 530, pygame.transform.scale(load_image('Duhovka_closed.png'), (180, 200)),
              pygame.transform.scale(load_image('Duhovka_opened.png'), (180, 200)))
exitd = Landing(1100, 450, pygame.transform.scale(load_image('door_closed_s.png'), (220, 320)),
                pygame.transform.scale(load_image('door_closed_a.png'), (220, 320)))
ded = Landing(800, 550, pygame.transform.scale(load_image('old_sleep.png'), (250, 250)),
              pygame.transform.scale(load_image('old_tell.png'), (250, 250)))
clock_orange = Landing(900, 140, pygame.transform.scale(load_image('clock_or.png'), (100, 100)),
                       pygame.transform.scale(load_image('clock_or_a.png'), (100, 100)))
clock_red = Landing(220, 250, pygame.transform.scale(load_image('clock_r.png'), (100, 70)),
                    pygame.transform.scale(load_image('clock_r_a.png'), (100, 70)))
clock_blue = Landing(60, 580, pygame.transform.scale(load_image('clock_bl.png'), (100, 100)),
                     pygame.transform.scale(load_image('clock_bl_a.png'), (100, 100)))
exitpos = (1100, 450)
# прописываем изображения
exit_op = pygame.transform.scale(load_image('door_closed_l.png'), (220, 320))
exit_f = pygame.transform.scale(load_image('door_opened.png'), (320, 330))
wantcake = pygame.transform.scale(load_image('waca.png'), (300, 250))
wantcake2 = wantcake
givekey = pygame.transform.scale(load_image('gike.png'), (300, 250))
clbag = pygame.transform.scale(load_image('clbag.png'), (300, 250))
instruction = pygame.transform.scale(load_image('instruction.png'), (500, 300))
h1 = pygame.transform.scale(load_image('h1.png'), (250, 50))
h2 = pygame.transform.scale(load_image('h2.png'), (250, 150))
h3 = pygame.transform.scale(load_image('h3.png'), (250, 50))
dl = pygame.transform.scale(load_image('dl.png'), (110, 110))
realyrun = True
# 1-ый цикл. В нем запускается вся играи можно её перепроходить, не перезапуская приложение
while realyrun:
    move(hero, 'tp')
    # прописываем значения переменных
    running = True
    nicname = start_screen()
    if nicname is None:
        running = False
        realyrun = False

    liftwork = False
    normform = False
    cakeisalie = False
    keykeykey = False
    infor = False
    h11 = False
    h21 = False
    h31 = False
    wantcake = wantcake2
    time = 0
    timer = 0
    timef1 = 0
    timef2 = 0
    font = pygame.font.Font(None, 30)

    fon = pygame.transform.scale(load_image('fon1.png'), screen_size)
    # запускаем музыку
    pygame.mixer.pre_init()
    pygame.mixer.init()
    pygame.init()
    pygame.mixer.music.load(os.path.join(os.getcwd(), 'sound', 'main_theme.mp3'))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/start_clock.mp3'))
    # 2-ой цикл. в нем работает сама игра
    while running:
        # проверка инпутов от игрока
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d] == 1:
                move(hero, 'right')
            if keys[pygame.K_a] == 1:
                move(hero, 'left')
            if keys[pygame.K_s] == 1 and tr1.update() and liftwork:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/lopen.mp3'))
                move(hero, 'down')
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/lclose.mp3'))
                timef1 = time
            if keys[pygame.K_w] == 1 and tr2.update() and liftwork:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/lopen.mp3'))
                move(hero, 'up')
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/lclose.mp3'))
            if keys[pygame.K_a] != 1 and keys[pygame.K_d] != 1:
                hero.update()
            if keys[pygame.K_i] == 1:
                infor = True
            else:
                infor = False
            if keys[pygame.K_1] == 1:
                h11 = True
            else:
                h11 = False
            if keys[pygame.K_2] == 1:
                h21 = True
            else:
                h21 = False
            if keys[pygame.K_3] == 1:
                h31 = True
            else:
                h31 = False
            if keys[pygame.K_e] == 1:
                if elec.update():
                    w = wires()
                    if w[1]:
                        liftwork = True
                    time += w[0]
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/elec.mp3'))
                    screen = pygame.display.set_mode(screen_size)

                if dux.update() and normform:
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/dush.mp3'), maxtime=20)
                    w = dush()
                    if w[1] == 'no':
                        normform = True
                    elif w[1]:
                        cakeisalie = True
                        normform = False
                    else:
                        normform = False
                    time += w[0]
                    screen = pygame.display.set_mode(screen_size)
                    timef2 = time - timef1
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/dush.mp3'), maxtime=20)
                if bag.update():
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/kunai.mp3'))
                    w = rulet()
                    if w[1]:
                        normform = True
                    time += w[0]
                    screen = pygame.display.set_mode(screen_size)
                if ded.update():
                    if cakeisalie:
                        wantcake = givekey
                        keykeykey = True
                if exitd.update():
                    if keykeykey:
                        activity_time_sec = time
                        connection = sqlite3.connect('rating.db')
                        cursor = connection.cursor()
                        c = cursor.execute(f"SELECT name "
                                           f"FROM score").fetchall()
                        USER = False
                        for i in c:
                            if i == (f'{nicname}',):
                                USER = True
                        # проверяем есть ли пользователь в базе данных и результат помещаем в флаг "USER"
                        if USER:
                            past_activity = cursor.execute(f"SELECT time "
                                                           f"FROM score WHERE name = ?",
                                                           (f'{nicname}',)).fetchall()
                            best_time = int(past_activity[0][0])
                            # получаем значение уже накопленной активности
                            if activity_time_sec < best_time:
                                cursor.execute(f"UPDATE score SET time = ?"
                                               f"WHERE name = ?",
                                               (activity_time_sec, nicname)).fetchall()
                        else:
                            cursor.execute(f"INSERT INTO score(name, time)"
                                           f" VALUES('{nicname}',{activity_time_sec})")
                            # если же пользователя не было в базе данных, мы его вносим вместе с новым временем
                        connection.commit()
                        connection.close()
                        running = False
                        final_screen(time, timef1, timef2, nicname)
        # проверка взаимодействия от игрока
        clock_orange.update()
        tr1.update()
        tr2.update()
        elec.update()
        dux.update()
        bag.update()
        clock_red.update()
        clock_blue.update()
        exitd.update()
        ded.update()
        # отоборажение на экран
        screen.blit(fon, (0, 0))
        tiles_group.draw(screen)
        if exitd.update():
            if keykeykey:
                screen.blit(exit_f, exitpos)
            else:
                screen.blit(exit_op, exitpos)

        player_group.draw(screen)
        screen.blit(font.render('Время:', 1, pygame.Color('white')), (1100, 10))
        screen.blit(font.render(str(time), 1, pygame.Color('white')), (1200, 10))
        if ded.update():
            screen.blit(wantcake, (860, 400))
        if infor:
            screen.blit(instruction, (400, 0))
        if h11:
            screen.blit(h1, (0, 0))
        if h21:
            screen.blit(h2, (0, 0))
        if h31:
            screen.blit(h3, (0, 50))
        if dux.update():
            if not normform:
                screen.blit(clbag, (310, 350))
        timer = (timer + 1) % 30
        if timer == 0:
            time += 1

        if timef1 == 0:
            pass
            pygame.draw.rect(screen, (0, 0, 0), (0, 400, 1500, 400), 0)
        screen.blit(dl, (1290, 0))
        pygame.display.flip()
        clock.tick(30)

pygame.quit()
