import pygame
from game_model import Block, BaseGameField, FastGame
from random import randint, choice
from high_score import LogRecords

pygame.init()


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font):
        super().__init__()
        self.color = (0, 0, 0)
        self.backcolor = (255, 255, 255)
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.backcolor, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft = self.pos)

    def update(self, event):
        if not event is None:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 10:
                        self.text += event.unicode
                self.render_text()

    def update_aktive(self, game):
        if game:
            self.active = (game.status == 0)


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, font, text):
        super().__init__()
        self.color = (0, 0, 0)
        self.backcolor = (255, 255, 255)
        self.pos = (x, y)
        self.font = font
        self.text = text
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color)
        self.image = pygame.Surface((t_surf.get_width()+10, t_surf.get_height()+10), pygame.SRCALPHA)
        self.image.blit(t_surf, (5, 5))
        self.rect = self.image.get_rect(center=self.pos)


class Game(pygame.sprite.Sprite):

    font_check_box = pygame.font.SysFont(None, 25)
    fn_menu = pygame.font.SysFont(None, 50)
    fn_rec = pygame.font.SysFont(None, 30)
    fn = pygame.font.SysFont(None, 30)
    text_input_box = TextInputBox(50, 150, 250, fn_menu)
    button1 = Button(175, 350, fn_menu, 'Долгая игра')
    button2 = Button(175, 450, fn_menu, 'Быстрая игра')
    all_sprites = pygame.sprite.Group(text_input_box, button2, button1)
    ch1 = pygame.mixer.Sound('sound/conect_blok.ogg')
    ch2 = pygame.mixer.Sound('sound/add_blok.ogg')
    path_backround = ['images/back_leto.jpg',
                      'images/back_osen.jpg',
                      'images/back_vesna.jpg',
                      'images/back_zima.jpg',
                      'images/back_more.jpg']

    def __init__(self, game=None):
        super().__init__()
        self.sc = pygame.image.load(choice(Game.path_backround))
        self.records = LogRecords()
        self.image = pygame.Surface((350, 600))
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.game = game
        self.new_block = Block(randint(1, 1))
        self.menu(None)

    def menu(self, event):
        sc = pygame.image.load('images/menu.jpg').convert()
        text = Game.fn_menu.render('Введите ваши имя', 1, (0, 0, 0))
        pos = text.get_rect(center=(175, 100))
        self.image.blit(sc, (0, 0))
        self.image.blit(text, pos)
        text1 = Game.fn_menu.render('выберите игру', 1, (0, 0, 0))
        pos = text1.get_rect(center=(175, 250))
        self.image.blit(text1, pos)
        if event:
            Game.all_sprites.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and Game.text_input_box.text:
                if Game.button1.rect.collidepoint(event.pos) or Game.button2.rect.collidepoint(event.pos):
                    if Game.button1.rect.collidepoint(event.pos):
                        self.game = BaseGameField()
                    else:
                        self.game = FastGame()
                    self.sc = pygame.image.load(choice(Game.path_backround))
                    self.game.next_status()
                    Game.text_input_box.update_aktive(self.game)
        Game.all_sprites.draw(self.image)


    def game_over(self):
        if self.records.record[self.game.name].get(Game.text_input_box.text, 0) <= self.game.score:
            self.records.add_result(Game.text_input_box.text, self.game.score, self.game.name)
        sc = pygame.image.load('images/menu.jpg').convert()
        self.image.blit(sc, (0, 0))
        bac_r = pygame.Surface((250, 500))
        bac_r.fill((200, 200, 200))
        bac_r.set_alpha(150)
        self.image.blit(bac_r, (50, 30))
        text = Game.fn_menu.render('рекорды:', 1, (255, 0, 0))
        pos = text.get_rect(center=(175, 50))
        self.image.blit(text, pos)
        for rec in enumerate(self.records.get_top(self.game.name)):
            text = Game.fn_rec.render(f'{rec[0] + 1}. {rec[1][0]}: {rec[1][1]}', 1, (255, 0, 0))
            pos = text.get_rect(center=(175, 50 + (rec[0] + 1) * 40))
            self.image.blit(text, pos)
        text = Game.fn_rec.render(
            f'Ваше текущее место: {self.records.get_now_place(Game.text_input_box.text, self.game.score, self.game.name)}', 1,
            (255, 0, 0))
        pos = text.get_rect(center=(175, 500))
        self.image.blit(text, pos)

    def grid(self, x, y):
        self.image.blit(self.sc, (0, 0))
        for i in range(0, 600, 50):
            pygame.draw.aaline(self.image, (255, 255, 255), (0, i), (350, i))
        for j in range(0, 350, 50):
            pygame.draw.aaline(self.image, (255, 255, 255), (j, 0), (j, 600))
        for i in range(12):
            for j in range(7):
                if self.game.field[i][j]:
                    pygame.draw.rect(self.image, self.game.field[i][j].color, (j * 50 + 1, i * 50 + 1, 48, 48))
                    text = Game.fn.render(self.game.field[i][j].text, 1, (0, 0, 0))
                    pos = text.get_rect(center=(j * 50 + 25, i * 50 + 25))
                    self.image.blit(text, pos)
        pygame.draw.rect(self.image, self.new_block.color, (x * 50 + 1, y * 50 + 1, 48, 48))
        text = Game.fn.render(self.new_block.text, 1, (0, 0, 0))
        pos = text.get_rect(center=(x * 50 + 25, y * 50 + 25))
        self.image.blit(text, pos)

    def perform_event(self, x, y, event):
        if self.game is None or self.game.status == 0:
            self.menu(event)
        elif event.type == pygame.KEYDOWN:
            if self.game.status == 1:
                if event.key == pygame.K_LEFT:
                    x = x - 1 if x else 0
                elif event.key == pygame.K_RIGHT:
                    x = x + 1 if x < 6 else 6
                elif event.key == pygame.K_UP:
                    a = self.game.get_free_cell(y, x)
                    f = self.game.add_block(self.new_block, a, x)
                    self.new_block = Block(randint(1, self.game.max_block))
                    x = 3
                    if f:
                        Game.ch1.play()
                    else:
                        Game.ch2.play()
            elif (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN) and self.game.status == 2:
                self.game.next_status()
        return x, y

    def update(self, x, y, event=None):
        if self.game:
            if self.game.status == 0:
                self.game.score = 0
                self.menu(event)
            elif self.game.status == 1:
                self.grid(x, y)
            else:
                self.game_over()
        else:
            self.menu(event)

if __name__ == '__main__':
    Game()