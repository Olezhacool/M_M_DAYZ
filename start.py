from random import sample, randint
import sys
import pygame
import os

FPS = 60
pygame.init()
hs = []
ds = []
rs = []
clock = pygame.time.Clock()

size = width, height = 900, 750
screen = pygame.display.set_mode((width, height))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f'Файл с изображением {fullname} не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_it((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(file):
    file = f'data/{file}'
    with open(file, 'r') as f:
        map_level = list(map(str.strip, f.readlines()))
    max_width = 110
    step = 20
    towns = 3
    # есть ошибки по длине
    level = list(map(lambda x: x.ljust(max_width - 15, '0'), map_level))
    level = list(map(lambda x: x.rjust(max_width, '1'), level))
    level[3] = level[3][:7] + '@' + level[3][8:]
    x = sample(range(15, 80, step), towns)
    y = sample(range(0, 80, step), towns)
    for i in y:
        for j in range(i, i + step):
            do = level[j][:x[y.index(i)]]
            posle = level[j][x[y.index(i)] + step:]
            level[j] = do + "22222222222222222222" + posle
    for i in y:
        hs.append(House1(x[y.index(i)] + 2, i))
        ds.append(Door1(x[y.index(i)] + 2, i))
    # print('\n'.join(level))
    return level


tile_images = {'wall': load_image('box.png'),
               'ground': load_image('ground.png'),
               'sand': load_image('sand.png'),
               'stone': load_image('stone.png'), }

player_image = load_image('gg.png')
tile_width = tile_height = 19


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def start_screen():
    screen = pygame.display.set_mode((width, height))
    screen.fill('black')
    fon = pygame.transform.scale(load_image('izmeneno1.png'), (450, 480))
    screen.blit(fon, (40, 180))
    font_title = pygame.font.Font('C:\\Users\max\PycharmProjects\M_M_DAYZ\data\DischargePro.ttf',
                                  150)
    font = pygame.font.Font('C:\\Users\max\PycharmProjects\M_M_DAYZ\data\DischargePro.ttf', 90)
    button_1 = pygame.Rect(460, 240, 300, 62)
    button_2 = pygame.Rect(460, 340, 437, 62)
    button_3 = pygame.Rect(460, 440, 360, 62)
    pygame.draw.rect(screen, '#827627', button_1)
    pygame.draw.rect(screen, '#827627', button_2)
    pygame.draw.rect(screen, '#827627', button_3)
    draw_text('M_M_DayZ', font_title, 'white', screen, 180, 10)
    draw_text('ИГРАТЬ', font, 'white', screen, 490, 224)
    draw_text('НАСТРОЙКИ', font, 'white', screen, 490, 324)
    draw_text('ПРАВИЛА', font, 'white', screen, 490, 424)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(pygame.mouse.get_pos()):
                    return
                if button_2.collidepoint(pygame.mouse.get_pos()):
                    settings()
                if button_3.collidepoint(pygame.mouse.get_pos()):
                    game_rules()
        pygame.display.flip()
        clock.tick(FPS)


def game_rules():
    font = pygame.font.Font('C:\\Users\max\PycharmProjects\M_M_DAYZ\data\DischargePro.ttf', 90)
    font_r = pygame.font.Font('C:\\Users\max\PycharmProjects\M_M_DAYZ\data\DischargePro.ttf', 27)
    rules_window = pygame.display.set_mode((900, 750))
    rules_window.fill('black')
    text = font.render("Правила игры", True, 'white')
    rules_window.blit(text, (100, 50))
    pygame.display.update()
    yr = 210
    rules = ['- Главныый герой должен премещаться по уровню,',
             '          собирать оружие, аптечки и еду.', ' ',
             '- Зомби будут атаковать героя,',
             '      поэтому герой должен использовать оружие для защиты', ' ',
             '- Герой может прятаться в домах,',
             '          восполнить свое здоровье и голод'
             ]
    for line in rules:
        draw_text(f'{line}', font_r, 'white', rules_window, 50, yr)
        yr += 45
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_screen()
                    return
            if event.type == pygame.QUIT:
                terminate()


def settings():
    font = pygame.font.Font('C:\\Users\max\PycharmProjects\M_M_DAYZ\data\DischargePro.ttf', 90)
    font_r = pygame.font.Font('C:\\Users\max\PycharmProjects\M_M_DAYZ\data\DischargePro.ttf', 45)
    rules_window = pygame.display.set_mode((900, 750))
    rules_window.fill('black')
    x1 = 380
    y1 = 260
    x2 = 480
    y2 = 260
    button_zv = pygame.Rect(x1, y1, 90, 40)
    pygame.draw.rect(screen, '#827627', button_zv)
    button_nzv = pygame.Rect(x2, y2, 120, 40)
    pygame.draw.rect(screen, 'black', button_nzv)
    text = font.render("Настройки", True, 'white')
    rules_window.blit(text, (100, 50))
    text = font_r.render("- Звук", True, 'white')
    rules_window.blit(text, (170, 260))
    text = font_r.render("ВКЛ", True, 'white')
    rules_window.blit(text, (390, 260))
    text = font_r.render("ВЫКЛ", True, 'white')
    rules_window.blit(text, (490, 260))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_screen()
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_zv.collidepoint(pygame.mouse.get_pos()):
                    x1, x2 = x2, x1
                if button_nzv.collidepoint(pygame.mouse.get_pos()):
                    x1, x2 = x2, x1
        pygame.display.flip()
        clock.tick(FPS)


class House1(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, house_group)
        self.frames = []
        self.sheet = load_image("lil house comb.png")
        self.cut_sheet(self.sheet, 2, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))


class Door1(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, door_group)
        self.frames = []
        self.open = 0
        self.sheet = load_image("lil house d.png")
        self.cut_sheet(self.sheet, 1, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))


def terminate():
    pygame.quit()
    sys.exit()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        self.x = tile_width * pos_x
        self.y = tile_width * pos_y
        self.move = True
        self.rifle = Nothing()
        self.rows = 0
        self.f_l = []
        self.frames = []
        self.sheet = load_image("gg.png")
        self.cut_sheet(12, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(load_image("ggm.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y

    def cut_sheet(self, columns, rows):
        self.rect = pygame.Rect(415, 340, self.sheet.get_width() // columns,
                                self.sheet.get_height() // (rows))
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.f_l.append(frame_location)
                self.frames.append(self.sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        ikey = False
        self.cur_frame = self.cur_frame % len(self.frames)
        self.image = self.frames[self.cur_frame]
        for h in hs:
            if not pygame.sprite.collide_mask(self, h):
                self.move = True
            else:
                self.move = False
                break
        for d in ds:
            if pygame.sprite.collide_mask(self, d):
                hs[ds.index(d)].image = load_image('lil house inside.png')
                hs[ds.index(d)].mask = pygame.mask.from_surface(load_image('lil house gr.png'))
                d.mask = pygame.mask.from_surface(load_image('lil house floor.png'))
            else:
                hs[ds.index(d)].image = load_image('lil house comb.png')
                hs[ds.index(d)].mask = pygame.mask.from_surface(load_image('lil house comb.png'))
        for r in rs:
            if pygame.sprite.collide_mask(self, r):
                r.rect.x, r.rect.y = player.rect.x + 2, player.rect.y - 7
                self.rifle = r
                self.frames = []
                self.sheet = load_image("gg with ak.png")
                self.cut_sheet(12, 1)


class Rifle(pygame.sprite.Sprite):
    def __init__(self, sheet, pos_x, pos_y, n=0):
        super().__init__(all_sprites, gun_group)
        self.frames = []
        self.sheet = sheet
        self.cut_sheet(self.sheet, 4, 1)
        self.mask = pygame.mask.from_surface(load_image("ak.png"))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y
        # self.rect.x, self.rect.y = player.rect.x - 10 + n, player.rect.y - 4

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class AK(Rifle):
    def __init__(self, pos_x, pos_y, n=0):
        super().__init__(load_image("kalash.png"), pos_x, pos_y, n=0)
        self.withrf = load_image("gg with ak.png")


class Nothing:
    def __init__(self):
        pass


def generate_level(level):
    np, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '0':
                Tile('ground', x, y)
            elif level[y][x] == '1':
                Tile('sand', x, y)
            elif level[y][x] == '2':
                Tile('stone', x, y)
            # elif level[y][x] == '3':
            #     hs.append(House1(x, y))
            #     ds.append(Door1(x, y))
            elif level[y][x] == '@':
                Tile('sand', x, y)
                np = Player(x, y)
                print(x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
    return np, x, y

all_sprites = pygame.sprite.Group()
start_screen()
door_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
gun_group = pygame.sprite.Group()
house_group = pygame.sprite.Group()
running = True
player, level_x, level_y = generate_level(load_level('level1.txt'))
# for i in range(3):
#     x = randint(0, 50)
#     y = randint(0, 50)
#     hs.append(House1(x, y))
#     ds.append(Door1(x, y))
rs.append(AK(0, 0, 0))
STEP = 4
e = 0
to_move = False
to_left = False
to_right = False
to_up = False
to_down = False
to_shoot = False
coord = [0, 0]
kx = 0
ky = 0
yy = 0
player_hp = 130
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, enemy_group)
        self.x = tile_width * pos_x
        self.y = tile_width * pos_y
        self.move = True
        self.rows = 0
        self.f_l = []
        self.frames = []
        self.sheet = load_image("zomb_og.png")
        self.cut_sheet(12, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(load_image("New Piskel.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y
        self.smotr()

    def cut_sheet(self, columns, rows):
        self.rect = pygame.Rect(415, 340, self.sheet.get_width() // columns,
                                self.sheet.get_height() // (rows))
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.f_l.append(frame_location)
                self.frames.append(self.sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global player_hp
        font = pygame.font.Font(None, 35)
        font_h = pygame.font.Font(None, 30)
        self.cur_frame = self.cur_frame % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.helth = pygame.Rect(60, 55, player_hp, 18)
        pygame.draw.rect(screen, 'red', self.helth)
        draw_text('HP', font, 'white', screen, 16, 52)
        draw_text(f"{player_hp}", font_h, 'white', screen, 110, 55)
        if pygame.sprite.collide_mask(self, player):
            player_hp -= 2
        if player_hp <= 0:
            died()



    def smotr(self):
        if player.x != self.x or player.y != self.y:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.xy = abs(player.x - self.x) + abs(player.y - self.y)
            self.xx = abs(player.x - self.x) / (self.xy + 0.000001)
            self.yy = abs(player.y - self.y) / (self.xy + 0.000001)
            if player.x < self.x:
                self.kx = -1
            else:
                self.kx = 1
            if player.y < self.y:
                self.ky = -1
            else:
                self.ky = 1
            self.rect.x += round(STEP * self.xx * self.kx)
            self.rect.y += round(STEP * self.yy * self.ky)
            self.x += round(STEP * self.xx * self.kx)
            self.y += round(STEP * self.yy * self.ky)



def died():
    global player
    font = pygame.font.Font('C:\\Users\max\PycharmProjects\M_M_DAYZ\data\DischargePro.ttf', 90)
    rules_window = pygame.display.set_mode((900, 750))
    rules_window.fill('black')
    text = font.render("YOU DIED", True, 'white')
    rules_window.blit(text, (400, 320))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen()






class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, object):
        object.rect = object.rect.move(self.dx, self.dy)

    def update(self, target):
        self.dx = width // 2 - target.rect.x - target.rect.w // 2
        self.dy = height // 2 - target.rect.y - target.rect.h // 2


en = Enemy(10, 50)
camera = Camera()
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # если произошло событие - нажатие клавиши
        if event.type == pygame.MOUSEMOTION:
            coord = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                to_shoot = True
            if event.key == pygame.K_d:
                to_move = True
        # если пользователь перестал нажимать клавишу
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                to_shoot = False
            if event.key == pygame.K_d:
                to_move = False
                player.cur_frame = 0
    # В зависимости от значений переменных направления
    # меняем значения координат
    if to_shoot and player.rifle.__class__.__name__ != 'Nothing':
        player.rifle.cur_frame = (player.rifle.cur_frame + 1) % len(player.rifle.frames)
    if to_right or to_left or to_down or to_up:
        player.cur_frame = (player.cur_frame + 1) % len(player.frames)
    if to_move and player.move:
        en.smotr()
        player.cur_frame = (player.cur_frame + 1) % len(player.frames)
        xy = abs(coord[0] - width // 2) + abs(coord[1] - height // 2)
        xx = abs(coord[0] - width // 2) / (xy + 0.000001)
        yy = abs(coord[1] - height // 2) / (xy + 0.000001)
        if coord[0] < width // 2:
            kx = -1
        else:
            kx = 1
        if coord[1] < height // 2:
            ky = -1
        else:
            ky = 1
        player.rect.x += round(STEP * xx * kx)
        player.rect.y += round(STEP * yy * ky)
        player.x += round(STEP * xx * kx)
        player.y += round(STEP * yy * ky)
    elif not player.move:
        xy = abs(coord[0] - width // 2) + abs(coord[1] - height // 2)
        xx = abs(coord[0] - width // 2) / xy
        yy = abs(coord[1] - height // 2) / xy
        if coord[0] < width // 2:
            jx = -1
        else:
            jx = 1
        if coord[1] < height // 2:
            jy = -1
        else:
            jy = 1
        if jy == -ky and jx == -kx:
            player.move = True
            player.rect.x -= round(STEP * xx * kx)
            player.rect.y -= round(STEP * yy * ky)
            player.x -= round(STEP * xx * kx)
            player.y -= round(STEP * yy * ky)

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    tiles_group.draw(screen)
    door_group.draw(screen)
    house_group.draw(screen)
    player_group.draw(screen)
    all_sprites.update()
    enemy_group.draw(screen)
    gun_group.draw(screen)
    clock.tick(30)
    pygame.display.flip()
