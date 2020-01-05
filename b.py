import os
from PIL import Image
import pygame

pygame.init()

width = 600
height = 600
size = width, height
best_res = 0
s = 0
sch = 0

tim = 0

screen = pygame.display.set_mode(size)
running = True

W, H = 5, 10


class shot:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 2

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(self.x, self.y, W, H))


class button:
    def __init__(self, x, y, cliced=False, w=200, h=100):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cliced = cliced

    def draw(self, text, color=(255, 255, 0)):
        font = pygame.font.Font(None, 50)
        pygame.draw.rect(screen, color, (self.x, self.y,
                                         self.w, self.h))

        screen.blit(font.render(text, 1, (0, 0, 0)), (self.x, self.y))

        pygame.display.flip()

    def is_cliced(self):
        #global is_menu
        x_m, y_m = event.pos
        if (x_m <= (self.x + self.w) and (x_m >= self.x)) and (
                y_m <= (self.y + self.h) and (y_m >= self.y)): # and is_menu[1]:
            return True
        return False


def menu():
    global button_start
    screen.fill((0, 0, 0))
    button_start = button(width // 2 - 100, height // 2 - 200)

    button_start.draw('start')
    font1 = pygame.font.Font(None, 50)
    screen.blit(font1.render('Best result:', 1, (0, 255, 0)),
                (width // 2 - 100, height // 2 - 50))
    screen.blit(font1.render(str(best_res), 1, (0, 255, 0)),
                (width // 2 - 100, height // 2 - 20))
    pygame.display.flip()


class Heroo:
    def __init__(self, x, y, spd):
        self.x = x
        self.y = y
        self.spd = spd

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname).convert()

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

d = ['r1', 'r', 'd1', 'l1', 'l', 'd']
class Monster:
    def __init__(self, picture, x, y, a):
        self.name = picture
        self.x = x
        self.y = y


        self.a = a

    def pos(self, dir):
        global time
        if dir == 'r' or dir == 'r1':
            self.x += 25

        if dir == 'l' or dir == 'l1':
            self.x -= 25

        if dir == 'd' or dir == 'd1':
            self.y += 10





    def draw(self):
        fullname = os.path.join('data', self.name)
        image = pygame.image.load(fullname).convert()

        im = Image.open(fullname)
        self.w, self.h = im.size

        image = image.convert_alpha()
        return image


m = ['monster5.png', 'monster4.png', 'monster3.png', 'monster2.png', 'monster1.png']

bullets = []
monsters = []
is_menu = [True, True]
is_game = False
h = Heroo(width // 2 - 23, 525, 25)
dir = 'd'
clock = pygame.time.Clock()
time = pygame.time.Clock()

g_o = [False, False]

for i in m:
    for j in range(5):
        monsters.append(Monster(i, ((width // 5) * j) + 10, m.index(i) * 50, 2))

while running:

    for b in bullets:
        if b.y > 0:
            b.y -= b.vel
        else:
            bullets.pop(bullets.index(b))

    if g_o[0]:
        screen.fill((0, 0, 0))

        font1 = pygame.font.Font(None, 50)
        screen.blit(font1.render('GAME OVER', 1, (0, 255, 0)),
                    (width // 2 - 100, height // 2 - 100))

        b = button(width // 2 - 100, height // 2 +50, h=50)
        b.draw('restart', color=(255, 255, 0))

        b1 = button(width // 2 - 100, height // 2 +100, h=50)
        b1.draw('exit', color=(255, 0, 0))
        g_o[0] = False

    if is_menu[0]:
        screen.fill((0, 0, 0))
        menu()
        is_menu[0] = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_start.is_cliced():
                screen.fill((0, 0, 0))
                is_menu[1] = False
                pygame.display.flip()
                hero = h.load_image('hero.png')
            if g_o[1]:
                if b.is_cliced():
                    is_menu[0] = True
                    is_menu[1] = True
                    g_o[1] = False

                if b1.is_cliced():
                    running = False



        if event.type == pygame.KEYDOWN:

            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                h.x -= h.spd
            elif key[pygame.K_RIGHT]:
                h.x += h.spd
            elif key[pygame.K_UP]:
                h.y -= h.spd
            elif key[pygame.K_DOWN]:
                h.y += h.spd

            if key[pygame.K_SPACE]:
                bullet = shot(h.x + 20, h.y)

                if len(bullets) <= 7:
                    bullets.append(bullet)

    if not is_menu[1] and not g_o[1]:
        screen.fill((0, 0, 0))
        screen.blit(hero, (h.x, h.y))

        for bullet_ in bullets:
            bullet_.draw()

        for i in monsters:

            screen.blit(i.draw(), (i.x, i.y))
        s += clock.tick()
        if s // 1000 >= 1:
            dir = d[(d.index(dir) + 1) % 6]
            for i in monsters:
                i.pos(dir)
            s = 0

        for b in bullets:
            for mo in monsters:
                if (b.x >= mo.x and (b.x + W) <= (mo.x + mo.w)) and (b.y == (mo.y + mo.h)):
                    monsters.pop(monsters.index(mo))
                    bullets.pop(bullets.index(b))
                    sch += 20

                    break


        best_res = sch
        font = pygame.font.Font(None, 50)
        screen.blit(font.render(str(sch), 1, (0, 255, 0)), (20, 10))

        for m in monsters:
            if m.y >= 450:

                g_o[0], g_o[1] = True, True








    pygame.display.flip()

pygame.quit()
