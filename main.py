import os
import random
import pygame

pygame.init()
size = 500, 500
screen = pygame.display.set_mode(size)
w, h = 5, 10

class shot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = -8
    def draw(self):
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, w, h), 10)



def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


hero = load_image('hero0.png')
running = True
x, y = 210, 430
spd = 20
bullets = []
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for b in bullets:
            if b.y > 0:
                b.y += b.vel
            else:
                bullets.pop(bullets.index(b))
        if event.type == pygame.KEYDOWN :

            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                x -= spd
            elif key[pygame.K_RIGHT]:
                x += spd
            if key[pygame.K_SPACE]:
                if len(bullets) <= 7:
                    bullets.append(shot(x, y))


    for b in bullets:
        b.draw()



    screen.fill((0, 0, 0))
    screen.blit(hero, (x, y))




    pygame.display.flip()

pygame.quit()
