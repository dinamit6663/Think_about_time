import pygame
import random
import os

# генерация координат
e = [i for i in range(10, 290, 20)]
qa = []
for i in range(6):
    w = random.choice(e)
    qa.append(w)
    e.remove(w)
Y_RED, Y_RED_END, Y_GRE, Y_GRE_END, Y_BL, Y_BL_END = qa


# загрузка изображений
def load_image(name):
    q = os.path.abspath('data')
    fullname = os.path.join(q, name)
    image = pygame.image.load(fullname)
    return image


# отображение уровня на экран
def update_level(screen, pos_for_red, pos_for_gre, pos_for_bl):
    fon = pygame.transform.scale(load_image('wirfon.png'), (300, 300))
    screen.blit(fon, (0, 0))
    draw_wires(screen)
    if pos_for_red != (50, Y_RED):
        pygame.draw.line(screen, pygame.Color(255, 0, 0), (50, Y_RED), pos_for_red, 10)
    if pos_for_gre != (50, Y_GRE):
        pygame.draw.line(screen, pygame.Color(0, 100, 0), (50, Y_GRE), pos_for_gre, 10)
    if pos_for_bl != (50, Y_BL):
        pygame.draw.line(screen, pygame.Color(0, 0, 255), (50, Y_BL), pos_for_bl, 10)


# отображение проводов на экран
def draw_wires(scr):
    screen = scr
    pygame.draw.line(screen, pygame.Color(255, 0, 0), (0, Y_RED), (50, Y_RED), 10)  # start yellow
    pygame.draw.line(screen, pygame.Color(0, 150, 0), (0, Y_GRE), (50, Y_GRE), 10)  # start green
    pygame.draw.line(screen, pygame.Color(0, 0, 255), (0, Y_BL), (50, Y_BL), 10)  # start blue
    pygame.draw.line(screen, pygame.Color(255, 0, 0), (280, Y_RED_END), (300, Y_RED_END), 10)  # end yellow
    pygame.draw.line(screen, pygame.Color(0, 150, 0), (280, Y_GRE_END), (300, Y_GRE_END), 10)  # end green
    pygame.draw.line(screen, pygame.Color(0, 0, 255), (280, Y_BL_END), (300, Y_BL_END), 10)  # end blue


# запуск мини-игры
def wires():
    pygame.init()
    pygame.display.set_caption('Провода')
    size = (300, 300)
    fps = 60
    clock = pygame.time.Clock()
    pygame.display.set_mode(size)
    screen = pygame.display.set_mode(size)
    background_image = pygame.Color('white')
    running = True
    time = 0
    timer = 0
    win = False

    flag_for_red = False
    motion_for_red = True
    done_red = False
    red_pos = (50, Y_RED)

    flag_for_gre = False
    motion_for_gre = True
    done_gre = False
    green_pos = (50, Y_GRE)

    flag_for_bl = False
    motion_for_bl = True
    done_bl = False
    blue_pos = (50, Y_BL)
    draw_wires(screen)
    # цикл для мини-игры
    while running:
        # проверка инпутов от игрока
        for event in pygame.event.get():
            update_level(screen, red_pos, green_pos, blue_pos)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r] == 1:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # red:
                if 25 < event.pos[0] < 50 and Y_RED - 10 < event.pos[1] < Y_RED + 10:
                    flag_for_red = True
                    flag_for_bl = False
                    flag_for_gre = False
                # green:
                if 25 < event.pos[0] < 50 and Y_GRE - 10 < event.pos[1] < Y_GRE + 10:
                    flag_for_bl = False
                    flag_for_red = False
                    flag_for_gre = True
                # blue:
                if 25 < event.pos[0] < 50 and Y_BL - 10 < event.pos[1] < Y_BL + 10:
                    flag_for_gre = False
                    flag_for_red = False
                    flag_for_bl = True

            # проверка, подключены ли провода
            elif event.type == pygame.MOUSEMOTION and flag_for_red and motion_for_red:
                pygame.draw.line(screen, pygame.Color(255, 0, 0), (50, Y_RED), event.pos, 10)
                if event.pos[0] > 285 and Y_RED_END - 10 < event.pos[1] < Y_RED_END + 10:
                    flag_for_red = False
                    motion_for_red = False
                    done_red = True
                    red_pos = event.pos
            elif event.type == pygame.MOUSEMOTION and flag_for_gre and motion_for_gre:
                pygame.draw.line(screen, pygame.Color(0, 100, 0), (50, Y_GRE), event.pos, 10)
                if event.pos[0] > 285 and Y_GRE_END - 10 < event.pos[1] < Y_GRE_END + 10:
                    flag_for_gre = False
                    motion_for_gre = False
                    done_gre = True
                    green_pos = event.pos
            elif event.type == pygame.MOUSEMOTION and flag_for_bl and motion_for_bl:
                pygame.draw.line(screen, pygame.Color(0, 0, 255), (50, Y_BL), event.pos, 10)
                if event.pos[0] > 285 and Y_BL_END - 10 < event.pos[1] < Y_BL_END + 10:
                    flag_for_bl = False
                    motion_for_bl = False
                    done_bl = True
                    blue_pos = event.pos

            if done_red & done_gre & done_bl:
                win = True
                running = False

        timer = (timer + 1) % 30
        if timer == 0:
            time += 1
        pygame.display.flip()
        clock.tick(fps)
    return [time, win]
    pygame.quit()
