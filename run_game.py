import time
from game_sprite import Game
from game_model import Block, BaseGameField, FastGame
import pygame

clock = pygame.time.Clock()

ch3 = pygame.mixer.Sound('sound/game_over.ogg')
ch4 = pygame.mixer.Sound('sound/pause.ogg')

FPS = 60
HEIGTH = 600
WIDTH = 700

screen = pygame.display.set_mode((WIDTH, HEIGTH))
b_sc = pygame.image.load('images/main_back1.jpg').convert()
screen.blit(b_sc, (0, 0))
pygame.display.set_caption('2048 merge block')
logo = pygame.image.load('images/logo.jpg')
logo = pygame.transform.scale(logo, (100, 100))
pygame.display.set_icon(logo)

fn_score = pygame.font.SysFont('Arial', 35)
font = pygame.font.Font('font/tetris.ttf', 40)
button3 = font.render("pause", 1, (255, 150, 150))
pos_bt3 = button3.get_rect(topleft=(375, 500))
button4 = font.render("stop", 1, (255, 150, 150))
pos_bt4 = button3.get_rect(topleft=(550, 500))

y, x = 11, 3
old_time = time.time()
old_status_game = 2
is_pause = False
path_music = ['sound/game_fon.mp3', 'sound/menu_end.mp3']

def update_base_screen(screen):
    screen.blit(b_sc, (0, 0))
    screen.blit(logo, (475, 200))
    if game.game:
        text = fn_score.render(f"Ваш Счет: {game.game.score}", 1, (0, 0, 0))
    else:
        text = fn_score.render("Ваш Счет: 0", 1, (0, 0, 0))
    pos = text.get_rect(topleft=(350, 100))
    screen.blit(text, pos)
    text = font.render("merge block", 1, (255, 150, 150))
    pos = text.get_rect(center=(525, 350))
    screen.blit(text, pos)
    text = fn_score.render("2048", 1, (255, 150, 150))
    pos = text.get_rect(center=(525, 420))
    screen.blit(text, pos)
    if game.game and game.game.status == 1:
        screen.blit(button3, pos_bt3)
        screen.blit(button4, pos_bt4)
        t = "Долгая игра" if game.game.name == 'long' else 'Быстрая игра'
        text = fn_score.render(t, 1, (0, 0, 0))
        pos = text.get_rect(center=(525, 50))
        screen.blit(text, pos)

def update_music(game):
    global old_status_game
    if game:
        if old_status_game != game.status:
            old_status_game = game.status
            pygame.mixer.music.load(path_music[old_status_game % 2])
            pygame.mixer.music.play(-1)
    elif old_status_game == 2:
        old_status_game = 0
        pygame.mixer.music.load(path_music[0])
        pygame.mixer.music.play(-1)

game = Game()
screen.blit(game.image, game.rect)

running = True
while running:
    update_music(game.game)

    if type(game.game) is FastGame:
        if game.game.status == 1 and time.time() - old_time >= 10:
            game.game.add_row()
            game.update(x, y)
            old_time = time.time()
        elif game.game.status != 1:
            old_time = time.time()
    else:
        old_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if game.game and game.game.status == 1:
                if event.type == pygame.MOUSEBUTTONDOWN and\
                        0 < event.pos[0] - 375 < button3.get_width() and\
                        0 < event.pos[1] - 500 < button3.get_height():
                    is_pause = not is_pause
                    ch4.play()
                elif event.type == pygame.MOUSEBUTTONDOWN and\
                        0 < event.pos[0] - 525 < button4.get_width() and\
                        0 < event.pos[1] - 500 < button4.get_height():
                    game.game.game_over()
                    game.new_block = Block(1)
                    is_pause = False
            if not is_pause:
                x, y = game.perform_event(x, y, event)
    update_base_screen(screen)
    game.update(x, y)
    screen.blit(game.image, game.rect)
    if is_pause:
        old_time = time.time()
        text = font.render("pause", 1, (0, 0, 0))
        pos = text.get_rect(center=(175, 300))
        screen.blit(text, pos)
    pygame.display.update()
    if game.game and game.game.check_last_field():
        game.game.game_over()
        game.new_block = Block(1)
        pygame.mixer.music.pause()
        ch3.play()
        pygame.time.delay(4 * 1000)
        game.update(x, y)

    clock.tick(FPS)