
import pygame
import os
import random
global menu1

game_started = True
menu1 = True
WIDTH = 1280
HEIGHT = 720
FPS = 30
timer = 0
choose_image = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

class Background(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('Background.png'), (1280, 720))

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Background.image

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)




class logos(pygame.sprite.Sprite):
    def __init__(self):
        super(logos, self).__init__()
        self.images = []
        self.images.append(load_image('not_blurred_name.png'))
        self.images.append(load_image('blurred_name.png'))


        self.timer = 0
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 3)

    def update(self):

        self.timer += 0.05
        if self.timer > 1:
            self.index += 1
            self.timer = 0
        if self.index >= len(self.images):
            self.index = 0

        self.image = self.images[self.index]





class Button(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('start_button.png'), (70, 70))
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = Button.image

        self.menu = menu1
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        self.hover = self.rect.collidepoint(mouse_pos) and any(mouse_buttons)

        if self.hover:
            print('BUTTON WORKS')

class Player_card(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        self.images.append(pygame.transform.scale(load_image('card_1.png'), (103, 144)))
        self.images.append(pygame.transform.scale(load_image('card_2.png'), (103, 144)))
        self.images.append(pygame.transform.scale(load_image('card_3.png'), (103, 144)))
        self.images.append(pygame.transform.scale(load_image('card_back.png'), (103, 144)))

        self.check = False
        self.timer = 0
        self.index = 3
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        #self.rect.center = (WIDTH / 12, HEIGHT / 2)
        self.rect.x = 106
        self.rect.y = 360
    def update(self):


        if self.rect.x < 560:
            self.rect = self.rect.move(+5, +2)

        if self.rect.x >= 560 and not self.check:
            self.index = random.randint(0,3)
            self.check = True

        self.image = self.images[self.index]

class Foe_card_1(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('card_back.png'), (103, 144))
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = Foe_card_1.image

        self.menu = menu1
        self.rect = self.image.get_rect()
        self.rect.center = (0, 360)
    def update(self):
        if self.rect.x < 280:
            self.rect = self.rect.move(+4, -3)

class Foe_card_2(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('card_back.png'), (103, 144))
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = Foe_card_2.image

        self.menu = menu1
        self.rect = self.image.get_rect()
        self.rect.center = (0, 360)
    def update(self):
        if self.rect.x < 560:
            self.rect = self.rect.move(+5, -2)

class Foe_card_3(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('card_back.png'), (103, 144))
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = Foe_card_2.image

        self.menu = menu1
        self.rect = self.image.get_rect()
        self.rect.center = (0, 360)
    def update(self):
        if self.rect.x < 840:
            self.rect = self.rect.move(+11, -3)



pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Resistance")
clock = pygame.time.Clock()
all_start = pygame.sprite.Group()
all_game = pygame.sprite.Group()
background = Background()
button = Button()
foe1 = Foe_card_1()
foe2 = Foe_card_2()
foe3 = Foe_card_3()
player_card = Player_card()
logos = logos()


all_start.add(background, button, logos)
all_game.add(background, player_card, foe1, foe2, foe3)

running = True
if not game_started:
    while running:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False


        all_start.update()

        
        screen.fill(BLACK)
        all_start.draw(screen)

        pygame.display.flip()
        #if not menu1:
        #    game_started = False
        #    break
if game_started:
    while running:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        all_game.update()

        screen.fill(BLACK)
        all_game.draw(screen)

        pygame.display.flip()


    pygame.quit()

pygame.quit()