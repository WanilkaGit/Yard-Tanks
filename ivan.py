"""------------------------------------Імпорта----------------------------------------"""
import time
from maxym import is_edge_touched
from random import choices, choice
from pygame import*# імпорт пайгейма
import pygame as pg
from typing import Union
score = 0

init()# ініціалізуєм пайгейм

"""------------------------------------Map--------------------------------------"""
map_lvl1 = [                               #Unbreakeble - u
    "   gggge gggg    bb           gggg",#breakeable - b
    "   bbbb  bbbb    db bbbbb bbbbhbdg",#green_hide - g
    "   b  b  bgg   e du b  be b  b bdg",#dark_white_hide - d
    " e bbbb  bbbb    db bbbb  b  b bdg",#enemy - e
    "   b  b   ggb    db e  b  b  b bdg",#player1 - p
    "   bbbb  bbbb    db bbbb  bbbb bdg",#lose - l
    "  u              du          e bdg",#win - w
    "    bbbbbbbbbbb  db  bbgbbgbb  bdg",#кожен елемент цього
    "            gg   db    bbbb    bdg",#є частиню карти окрім
    "  bbbg gg         gggggggggggggggg",#пробілів
    "  gggg     buub        b  b     ug",#що вони означають написано вище
    "       bub gggg  g  b  bbbb  b bgg",#теж зі знаком коментаря
    "  bub  ggg       gb b  b  b  b bgg",
    "  ggg       bub  b bu      ub bg g",
    "       bbb  ggg  gb b  bbb   b bgg",
    "      pblbf     bdddb  blb ggggggg"
]


""" ----------------------------------ЗМІННІ-------------------------------------"""
#window = pg.display.set_mode((0, 0), pg.FULLSCREEN)
player_lives = 2
move_player1 = 1
beginers = [0, 70]
tile_size = [32, 32]
player_size = [28, 28]
friend_is_on = False

# це те скільки вийде блоків на екрані 40 кількість пікселів на оин силвол
level1_width = len(map_lvl1[0]) * tile_size[0]
level1_height = len(map_lvl1) * tile_size[1] + beginers[1]


""" ----------------------------------ГРУПИ-------------------------------------"""
blocks = sprite.Group()#  створюємо тусу
hides_blocks = sprite.Group()
players = sprite.Group()
bullets = sprite.Group()
loozes = sprite.Group()

"""----------------Картинки щоб швидше вставляти бо по іншому довго-------------------"""
player1 = "assets/textures/player/player11.png"
player1_moves = "assets/textures/player/player12.png"
players_image = [player1, player1_moves]

player2 = "assets/textures/player/player21.png"
player2_moves = "assets/textures/player/player22.png"
players2_image = [player2, player2_moves]

breakables = [
                "assets/textures/blocks/derevaskawitch4uglblenia.png",
                "assets/textures/blocks/derevaskawitchuglblenie.png",
                "assets/textures/blocks/derewaska.png",
                "assets/textures/blocks/oboi.png",
                "assets/textures/blocks/seno.png"]

unbreakable = choice([
                "assets/textures/blocks/obsidian1.png",
                "assets/textures/blocks/obsidian2.png"])

green_hide = "assets/textures/blocks/kuvsinka.png"


""" ----------------------------------ШРИФТИ-------------------------------------"""
font1 = font.SysFont("Arial", 35)
font2 = font.SysFont(('font/ariblk.ttf'), 60)
font_path = r"assets//textures//fonts//Blazma-Regular.otf"
font_size = 36
font3 = font.Font(font_path, font_size)

score_txt = font3.render('score: ' + str(score), True, (0, 0, 0))

""" ----------------------------------Кнопки-------------------------------------"""

# створюєм вікно
#window = pg.display.set_mode((0, 0), pg.FULLSCREEN)
#W, H = pg.display.Info().current_w, pg.display.Info().current_h


"""-------------------------------------Класи---------------------------------------"""
""" ----------------------------------Клас блоків-------------------------------------"""
class Blocks(sprite.Sprite):# основний клас тут основні параметри
    def __init__(self, coordinates, size, speed, img, breaking_ables: bool):
        super().__init__()
        self.width, self.height = size
        self.speed = speed
        self.image = transform.scale(image.load(img), (self.width, self.height))
        self.breaking_ables = breaking_ables
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coordinates


""" ----------------------------------клас пулі-------------------------------------"""
class PlayerBullet(sprite.Sprite):
    def __init__(self, x, y, width, height, speed, img, zone = (0, 70, 1000, 1000), rotate: str = "u"):
        super().__init__()
        self.width = width
        self.height = height
        self.speed = speed
        self.image = transform.scale(image.load(img), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.min_x, self.min_y, self.max_x, self.max_y = zone
        self.rotate = rotate
        if self.rotate == "u":
            self.image = transform.rotate(self.image, 0)
        if self.rotate == "d":
            self.image = transform.rotate(self.image, 180)
        if self.rotate == "l":
            self.image = transform.rotate(self.image, 270)
        if self.rotate == "r":
            self.image = transform.rotate(self.image, 90)

    def colides(self, blocks_colide, enemys):
        global score
        collides_blocks = sprite.spritecollide(self, blocks_colide, False)
        for block in collides_blocks:
            if block.breaking_ables:
                block.kill()
            self.kill()
        collides_enemy = sprite.spritecollide(self, enemys, False)
        for enemy in collides_enemy:
            if enemy.health <= 1:
                score += enemy.score
            enemy.take_damage(1)
            self.kill()

        if is_edge_touched(self, self.min_x, self.min_y, self.max_x, self.max_y):
            self.kill()


    def update(self, blocks, enemys):
        self.colides(blocks, enemys)
        if self.rotate == "u":
            # self.speed = 0
            # self.speed += 1 if self.speed != 10 else None
            self.rect.y -= self.speed
        if self.rotate == "d":
            # self.speed = 0
            # self.speed += 1 if self.speed != 10 else None
            self.rect.y += self.speed

        if self.rotate == "l":
            self.rect.x -= self.speed
        if self.rotate == "r":
            self.rect.x += self.speed

""" ----------------------------------клас гравця-------------------------------------"""
class Player(sprite.Sprite):# клас гравця з супер класом сетінгс
    def __init__(self, coordainates, start_coordinates, size, imgs, speed, k_u, k_d, k_l, k_r, k_shoot, lives, life_y, zone = (0, 0, 1000, 1000), rotate = 0, agle = "u"):
        super().__init__()
        self.width, self.height = size
        self.image = transform.scale(image.load(imgs[0]), (self.width, self.height))
        self.image_move1 = transform.scale(image.load(imgs[0]), (self.width, self.height))
        self.image_move2 = transform.scale(image.load(imgs[1]), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coordainates
        self.start_coordinates = start_coordinates
        self.speed = speed
        self.key_up = k_u
        self.key_down = k_d
        self.key_left = k_l
        self.key_right = k_r
        self.key_shoot = k_shoot
        self.lives = lives
        self.lifes_y = life_y
        self.zone = zone
        self.min_x, self.min_y, self.max_x, self.max_y = zone
        self.move = 1
        self.rotate = rotate # which need
        self.agle = agle# which has
        self.last_shot_time = 0  # час останнього пострілу
        self.shoot_delay = 300  # затримка між пострілами в мілісекундах

# тут анімація руху гравця
    def animate(self):
        if self.move % 2 == 0:
            self.image = transform.scale(self.image_move1, (self.width, self.height))# підсьтавляєм фотку
            self.move += 1
        else:
            self.image = transform.scale(self.image_move2, (self.width, self.height))# підсьтавляєм фотку
            self.move += 1

# тут повороти гравця
    def rotating(self, angage):
        if self.rotate is not angage:
            if self.rotate > angage:
                self.image_move2 = transform.rotate(self.image_move2, -90)
                self.image_move1 = transform.rotate(self.image_move1, -90)
                self.rotate -= 90
            elif self.rotate < angage:
                self.image_move2 = transform.rotate(self.image_move2, 90)
                self.image_move1 = transform.rotate(self.image_move1, 90)
                self.rotate += 90

    def colides(self, blocks):
        collided_blocks = pg.sprite.spritecollide(self, blocks, False)
        if collided_blocks:
            block = collided_blocks[0] #нам вистачає тільки першого блока зі списку
            if self.agle == "u":
                self.rect.top = block.rect.bottom
            elif self.agle == "d":
                self.rect.bottom = block.rect.top
            elif self.agle == "l":
                self.rect.left = block.rect.right 
            elif self.agle == "r":
                self.rect.right = block.rect.left

        if self.rect.right > self.max_x:
            self.rect.x = self.max_x - self.rect.width
        elif self.rect.left < self.min_x:
            self.rect.x = self.min_x
        if self.rect.bottom > self.max_y:
            self.rect.y = self.max_y - self.rect.height
        elif self.rect.top < self.min_y:
            self.rect.y = self.min_y

    def new_live(self):
        self.rect.x, self.rect.y = self.start_coordinates
        self.lives -= 1

    def blit_lives(self, window):
        life_txt = font3.render('Життя: ' + str(self.lives), True, (0, 0, 0))
        window.blit(life_txt, (1100, self.lifes_y))
    
    def death(self):
        if self.lives <= 0:
            self.kill()

# функція що відповідає за натискання кнопок та переміщення 
    def update(self, window, blocks, enemys):# тут буде переміщення в право ліво
        #записуємо всі блоки з якими стикнувся танк в змінну collided_blocks якщо список не пустий перевіряємо колізію

        self.colides(blocks)
        self.blit_lives(window)
        self.death()
        key_pressed = key.get_pressed()# задаєм в зміну значення

        if key_pressed[self.key_up]:# якщо в верх то віднімаєм піднімаємось
            self.agle = "u"
            self.rotating(angage=0)
            self.rect.y -= self.speed#
            self.animate()

        elif key_pressed[self.key_down]:# перевіряєм чи нажата кнопка це а
            self.agle = "d"
            self.rotating(angage=180)
            self.rect.y += self.speed# якщо так той демо в лівоdef move_animation():
            self.animate()

        elif key_pressed[self.key_left]:# якщо в верх то віднімаєм піднімаємось
            self.agle = "l"
            self.rotating(angage=90)
            self.rect.x -= self.speed#
            self.animate()

        elif key_pressed[self.key_right]:# перевіряєм чи нажата кнопка це а
            self.agle = "r"
            self.rotating(angage=270)
            self.rect.x += self.speed# якщо так той демо в лівоdef move_animation():
            self.animate()

        current_time = pg.time.get_ticks()
        if key_pressed[self.key_shoot] and current_time - self.last_shot_time >= self.shoot_delay:
            bullet = PlayerBullet(self.rect.x + self.width // 2 - 1, self.rect.y + self.height // 2 - 1, 3, 5, 3, 'assets/textures/bullet.png',self.zone , self.agle)
            bullets.add(bullet)
            self.last_shot_time = current_time

        bullets.update(blocks, enemys)

"""----------------------------------ФУНКЦІЇ------------------------------------------"""
# створення списків можливий через цю функцію
def creating_lists_coordinate(list, x, y):
    list.append((x, y))
    return list

# створення карти
def create_map(map: Union[ list , str , tuple], tile_size: int, begin_x: int = 0, begin_y: int = 70):# стартова позиція
    global blocks, hides_blocks, players, unbreakables, breakables, green_hides, dark_white_hides, enemy_coordinates, empty_coordinates
    breakables_lst = list()
    unbreakables = list()
    green_hides = list()
    dark_white_hides = list()
    enemy_coordinates = list()
    empty_coordinates = list()

    map_size_x = len(map[0]) * tile_size[0] + begin_x
    map_size_y = len(map) * tile_size[1] + begin_y

    # всі списки дивіться в кінотеатрах(коді)
    x = begin_x#  координати для обєктів
    y = begin_y
    for r in map:# фор як раб почав ходити по списками перевіряєм індекси
        for c in r:#  стучим в двері перевіряєм чи
            if c == " ":
                empty_coordinates = creating_lists_coordinate(empty_coordinates, x, y)
            if c == "b":# дім полу
                b = Blocks((x,y), tile_size, 0, choice(breakables), True)# створюєм раба платформа
                breakables_lst.append(b)
                blocks.add(b)
            if c == "u":
                u = Blocks((x,y), tile_size, 0, unbreakable, False)
                unbreakables.append(u)
                blocks.add(u)
            if c == "g":
                g = Blocks((x,y), tile_size, 0, green_hide, False)
                green_hides.append(g)
                hides_blocks.add(g)
            if c == "d":
                d = Blocks((x,y), tile_size, 0, green_hide, False)
                dark_white_hides.append(d)
                hides_blocks.add(d)
            if c == "e":
                enemy_coordinates = creating_lists_coordinate(enemy_coordinates, x, y)
            if c == "p":
                player = Player((x, y), (x, y), player_size, players_image, 2, K_w, K_s, K_a, K_d, K_e, player_lives, 60, (begin_x, begin_y, map_size_x, map_size_y))
                players.add(player)
            if c == "f" and friend_is_on:
                friend = Player((x, y), (x,y), player_size, players2_image, 2, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RCTRL, player_lives, 120, (begin_x, begin_y, map_size_x, map_size_y))
                players.add(friend)
            if c == "l":
                l = Blocks((x,y), tile_size, 0, 'assets/textures/blocks/base.png', False)
                loozes.add(l)
            x += tile_size[0]#  ікси плюс tile_size
        y += tile_size[1]#  перміщаємось в низ на tile_size
        x = begin_x#  ікси begin_x
    return blocks, hides_blocks, loozes, players, enemy_coordinates



# функція що 
def reset_map():
    global blocks, hides_blocks, loozes, players, bullets
    blocks.empty()#  створюємо тусу
    hides_blocks.empty()
    loozes.empty()
    players.empty()
    bullets.empty()