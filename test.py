
import pygame
import os
import random

game = 1

menu1 = True
WIDTH = 1280
HEIGHT = 720
FPS = 30
timer = 0
choose_image = True
pygame.init()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
font1 = pygame.font.SysFont('chalkduster.ttf', 32)
img1 = font1.render('ENTER NICKNAME:', True, BLUE)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        return image
    except pygame.error as message:
        print ('Cannot load image:', name)
        raise SystemExit(message)


class Background(pygame.sprite.Sprite):

    image = pygame.transform.scale(load_image('Background.png'), (1280,
                                   720))

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

    image = pygame.transform.scale(load_image('start_button.png'), (70,
                                   70))

    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = Button.image
        self.game = game
        self.menu = menu1
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        self.hover = self.rect.collidepoint(mouse_pos) \
            and any(mouse_buttons)

        if self.hover:
            print 'BUTTON WORKS'
            global game
            game = 2


class Player_card(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.images = []
        self.images.append(pygame.transform.scale(load_image('card_1.png'
                           ), (103, 144)))
        self.images.append(pygame.transform.scale(load_image('card_2.png'
                           ), (103, 144)))
        self.images.append(pygame.transform.scale(load_image('card_3.png'
                           ), (103, 144)))
        self.images.append(pygame.transform.scale(load_image('card_back.png'
                           ), (103, 144)))

        self.check = False
        self.timer = 0
        self.index = 3
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # self.rect.center = (WIDTH / 12, HEIGHT / 2)

        self.rect.x = 106
        self.rect.y = 360

    def update(self):

        if self.rect.x < 560:
            self.rect = self.rect.move(+5, +2)

        if self.rect.x >= 560 and not self.check:
            self.index = random.randint(0, 2)
            self.check = True

        self.image = self.images[self.index]


class Foe_card_1(pygame.sprite.Sprite):

    image = pygame.transform.scale(load_image('card_back.png'), (103,
                                   144))

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

    image = pygame.transform.scale(load_image('card_back.png'), (103,
                                   144))

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

    image = pygame.transform.scale(load_image('card_back.png'), (103,
                                   144))

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


class InputBox:

    def __init__(
        self,
        x,
        y,
        w,
        h,
        text='',
        ):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            # If the user clicked on the input_box rect.

            if self.rect.collidepoint(event.pos):

                # Toggle the active variable.

                self.active = not self.active
            else:
                self.active = False

            # Change the current color of the input box.

            self.color = \
                (COLOR_ACTIVE if self.active else COLOR_INACTIVE)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                # Re-render the text.

                self.txt_surface = FONT.render(self.text, True,
                        self.color)

    def update(self):

        # Resize the box if the text is too long.

        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):

        # Blit the text.

        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y
                    + 5))

        # Blit the rect.

        pygame.draw.rect(screen, self.color, self.rect, 2)


class BTN_YES_NO(object):

    """A fairly straight forward button class."""

    def __init__(
        self,
        rect,
        color,
        function,
        **kwargs
        ):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.function = function
        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self.process_kwargs(kwargs)
        self.render_text()

    def process_kwargs(self, kwargs):
        """Various optional customization you can change by passing kwargs."""

        settings = {
            'text': None,
            'font': pygame.font.Font(None, 16),
            'call_on_release': True,
            'hover_color': None,
            'clicked_color': None,
            'font_color': pygame.Color('white'),
            'hover_font_color': None,
            'clicked_font_color': None,
            'click_sound': None,
            'hover_sound': None,
            'border_color': pygame.Color('black'),
            'border_hover_color': pygame.Color('yellow'),
            'disabled': False,
            'disabled_color': pygame.Color('grey'),
            'radius': 5,
            }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError('{} has no keyword: {}'.format(self.__class__.__name__,
                        kwarg))
        self.__dict__.update(settings)

    def render_text(self):
        """Pre render the button text."""

        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text, True,
                        color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text, True,
                        color)
            self.text = self.font.render(self.text, True,
                    self.font_color)

    def check_event(self, event):
        """The button needs to be passed events from your program event loop."""

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                self.function()

    def on_release(self, event):
        if self.clicked and self.call_on_release:

            # if user is still within button rect upon mouse release

            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.function()
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def render(self, surface):
        """Update needs to be called every frame in the main loop."""

        color = self.color
        text = self.text
        border = self.border_color
        self.check_hover()
        if not self.disabled:
            if self.clicked and self.clicked_color:
                color = self.clicked_color
                if self.clicked_font_color:
                    text = self.clicked_text
            elif self.hovered and self.hover_color:
                color = self.hover_color
                if self.hover_font_color:
                    text = self.hover_text
            if self.hovered and not self.clicked:
                border = self.border_hover_color
        else:
            color = self.disabled_color

        # if not self.rounded:
        #    surface.fill(border,self.rect)
        #    surface.fill(color,self.rect.inflate(-4,-4))
        # else:

        if self.radius:
            rad = self.radius
        else:
            rad = 0
        self.round_rect(
            surface,
            self.rect,
            border,
            rad,
            1,
            color,
            )
        if self.text:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

    def round_rect(
        self,
        surface,
        rect,
        color,
        rad=20,
        border=0,
        inside=(0, 0, 0, 0),
        ):
        rect = pygame.Rect(rect)
        zeroed_rect = rect.copy()
        zeroed_rect.topleft = (0, 0)
        image = pygame.Surface(rect.size).convert_alpha()
        image.fill((0, 0, 0, 0))
        self._render_region(image, zeroed_rect, color, rad)
        if border:
            zeroed_rect.inflate_ip(-2 * border, -2 * border)
            self._render_region(image, zeroed_rect, inside, rad)
        surface.blit(image, rect)

    def _render_region(
        self,
        image,
        rect,
        color,
        rad,
        ):
        corners = rect.inflate(-2 * rad, -2 * rad)
        for attribute in ('topleft', 'topright', 'bottomleft',
                          'bottomright'):
            pygame.draw.circle(image, color, getattr(corners,
                               attribute), rad)
        image.fill(color, rect.inflate(-2 * rad, 0))
        image.fill(color, rect.inflate(0, -2 * rad))


def enter_nick():
    clock = pygame.time.Clock()
    input_box1 = InputBox(500, 328, 140, 32)
    input_boxes = [input_box1]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()
        nick_enter.update()

        screen.fill(BLACK)
        nick_enter.draw(screen)
        screen.blit(img1, (500, 300))
        for box in input_boxes:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def start_button():
    running = True
    while running:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        all_start.update()

        screen.fill(BLACK)
        all_start.draw(screen)
        if game == 2:
            break

        pygame.display.flip()


def cards_set():
    running = True

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


pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Resistance')
clock = pygame.time.Clock()
all_start = pygame.sprite.Group()
all_game = pygame.sprite.Group()
nick_enter = pygame.sprite.Group()
background = Background()
button = Button()
foe1 = Foe_card_1()
foe2 = Foe_card_2()
foe3 = Foe_card_3()
player_card = Player_card()
logos = logos()

nick_enter.add(background)
all_start.add(background, button, logos)
all_game.add(background, player_card, foe1, foe2, foe3)

if game == 1:
    start_button()

if game == 2:
    enter_nick()

if game == 3:
    cards_set()

pygame.quit()
