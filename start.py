from random import sample
import sys

import pygame
import os

FPS = 60
pygame.init()
clock = pygame.time.Clock()

size = width, height = 600, 700
screen = pygame.display.set_mode((width, height))


def load_image(name, colorkey=None):
    fullname = os.path.join('../pythonProject1/m_m_dayz/data', name)

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


tile_images = {'wall': load_image('box.png'),
               'ground': load_image('ground.png'),
               'sand': load_image('sand.png'),
               'stone': load_image('stone.png')}

player_image = load_image('gg.png')
tile_width = tile_height = 19


def start_screen():
    text = ['ЗАСТАВКА', '', 'ПРАВИЛА ИГРЫ', 'Если в правилах много строк,',
            'выводи построчно']
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    coord_y = 50
    for line in text:
        draw_line = font.render(line, True, pygame.Color('black'))
        line_rect = draw_line.get_rect()
        coord_y += 1
        line_rect.top = coord_y
        line_rect.x = 20
        coord_y += line_rect.height
        screen.blit(draw_line, line_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def load_level(file):
    file = f'data/{file}'
    with open(file, 'r') as f:
        map_level = list(map(str.strip, f.readlines()))
    max_width = 110
    step = 10
    towns = 9
    level = list(map(lambda x: x.ljust(max_width - 15, '0'), map_level))
    level = list(map(lambda x: x.rjust(max_width, '1'), level))
    level[3] = level[3][:7] + '@' + level[3][8:]
    x = sample(range(15, 110, step), towns)
    y = sample(range(0, 90, step), towns)
    for i in y:
        for j in range(i, i + 10):
            print(j)
            do = level[j][:x[y.index(i)]]
            posle = level[j][x[y.index(i)] + 10:]
            level[j] = do + "2222222222" + posle
    print(level)
    return level


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        self.x = 270
        self.y = 320
        self.frames = []
        self.sheet = load_image("gg.png")
        self.cut_sheet(self.sheet, 12, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x + 13, tile_height * pos_x + 13

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


class Rifle(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, n=0):
        super().__init__(all_sprites, gun_group)
        self.frames = []
        self.sheet = sheet
        self.cut_sheet(self.sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect.x, self.rect.y = player.rect.x - 10 + n, player.rect.y - 4

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
    def __init__(self, sheet, columns, rows, n=0):
        super().__init__(load_image("AK-47l.png"), columns, rows, n=0)


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
            elif level[y][x] == '@':
                Tile('sand', x, y)
                np = Player(x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
    return np, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, object):
        object.rect = object.rect.move(self.dx, self.dy)

    def update(self, target):
        self.dx = width // 2 - target.rect.x - target.rect.w // 2
        self.dy = height // 2 - target.rect.y - target.rect.h // 2


all_sprites = pygame.sprite.Group()
start_screen()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
gun_group = pygame.sprite.Group()
running = True
camera = Camera()
player, level_x, level_y = generate_level(load_level('level1.txt'))
print("\n".join(load_level('level1.txt')))
rifle = Nothing()
STEP = 4
e = 0
to_move = False
to_left = False
to_right = False
to_up = False
to_down = False
to_shoot = False
coord = []
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # если произошло событие - нажатие клавиши
        if event.type == pygame.MOUSEMOTION:
            coord = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                to_shoot = True
            if event.key == pygame.K_d:
                to_move = True
        # если пользователь перестал нажимать клавишу
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                to_shoot = False
            if event.key == pygame.K_d:
                to_move = False
    # В зависимости от значений переменных направления
    # меняем значения координат
    if to_shoot and rifle.__class__.__name__ != 'Nothing':
        rifle.cur_frame = (rifle.cur_frame + 1) % len(rifle.frames)
    if to_right or to_left or to_down or to_up:
        player.cur_frame = (player.cur_frame + 1) % len(player.frames)
    if to_move:
        # доработать движение, только наискосок пока ходит
        player.cur_frame = (player.cur_frame + 1) % len(player.frames)
        xy = abs(coord[0] - width // 2) + abs(coord[1] - height // 2)
        xx = abs(coord[0] - width // 2) / xy
        yy = abs(coord[1] - height // 2) / xy
        if coord[0] < width // 2:
            kx = -1
        else:
            kx = 1
        if coord[1] < height // 2:
            ky = -1
        else:
            ky = 1
        player.rect.x += STEP * xx * kx
        player.rect.y += STEP * yy * ky
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    tiles_group.draw(screen)
    player_group.draw(screen)
    all_sprites.update()
    gun_group.draw(screen)
    clock.tick(30)
    pygame.display.flip()
