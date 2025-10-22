import pygame
import sys
import os

pygame.init()
FPS = 50
size = width, height = 1500, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
sprite1 = pygame.sprite.Sprite()
sprite2 = pygame.sprite.Sprite()
sprite3 = pygame.sprite.Sprite()


def load_image(name, color_key=-1, fon=False):
    if fon:
        fullname = os.path.join('fon', name)
    else:
        fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        raise SystemExit(message)
    if name == 'sword.png':
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    elif name == 'buddha.png':
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = pygame.transform.scale(image, (250, 250))
    elif name == 'dead.png' or name == 'win.png' or name == 'pause.png' or name == 'retur.png':
        pass
    elif color_key == -1 and name == "master_list.png":
        image = pygame.transform.scale(image, (3000, 150))
    elif name == "j2.jpg":
        image = pygame.transform.scale(image, (2100, 1500))
    elif name == "mont.jpg":
        image = pygame.transform.scale(image, (3000, 2000))
    elif name == "fon.jpg":
        image = pygame.transform.scale(image, (3000, 2000))
    elif name == "zz.jpg":
        image = pygame.transform.scale(image, (3000, 2000))
    elif name == 'ninja.png':
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = pygame.transform.scale(image, (3500, 225))
    elif name == 'ded.png':
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = pygame.transform.scale(image, (700, 225))
    elif name == 'wall.png':
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = pygame.transform.scale(image, (25, 200))
    elif name == 'platform1.png' or name == 'platform2.png' or name == 'bad.png':
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = pygame.transform.scale(image, (200, 25))
    elif name == 'matat.png':
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
        image = pygame.transform.scale(image, (3000, 500))
    return image


def terminate():
    pygame.quit()
    sys.exit()



def start_screen():
    intro_text = [""]
    fon_list = [load_image('fon.jpg')]
    for i in range(78):
        fon_list.append(load_image(str(i) + '.gif', -1, True))
    fon = pygame.transform.scale(fon_list[0], (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text_coord = 50
    text_1 = font.render("НАЧАТЬ ИГРУ", 1, (0, 250, 154))
    text_x = width // 2 - text_1.get_width() // 2
    text_y = height // 4 - text_1.get_height() // 4
    text_w = text_1.get_width()
    text_h = text_1.get_height()
    screen.blit(text_1, (text_x, text_y))
    text_2 = font.render("ВЫХОД", 1, (0, 250, 154))
    text_x2 = width // 2 - text_2.get_width() // 2
    text_y2 = height // 2 - text_2.get_height() // 2
    text_w2 = text_2.get_width()
    text_h2 = text_2.get_height()
    screen.blit(text_2, (text_x2, text_y2))
    rect_start = pygame.Rect((text_x - 10, text_y - 10, text_w + 20, text_h + 20))
    rect_exit = pygame.Rect((text_x2 - 10, text_y2 - 10, text_w2 + 20, text_h2 + 20))
    pygame.draw.rect(screen, (255, 100, 102), rect_start, 5)
    t = 0
    fon_n = 0
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and rect_start.collidepoint(event.pos):
                return
            if event.type == pygame.MOUSEBUTTONDOWN and rect_exit.collidepoint(event.pos):
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pass
        if t % 5 == 0:
            fon = pygame.transform.scale(fon_list[fon_n % 77], (width, height))
            fon_n += 1
        t += 1
        screen.blit(fon, (0, 0))
        screen.blit(text_1, (text_x, text_y))
        screen.blit(text_2, (text_x2, text_y2))
        pygame.display.flip()
        clock.tick(FPS)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, img):
        super().__init__(all_sprites)
        self.image = load_image(img)
        self.rect = pygame.Rect(pos, (200, 25))
        self.add(platform)


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.life = True
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect.x = 100
        self.rect.y = 100
        self.lst = []
        self.x = 0
        self.y = 4
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 300)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, key=None):
        if self.life is True:
            if key == 'right':
                self.cur_frame = (self.cur_frame + 1) % 6
                self.image = self.frames[self.cur_frame]
            if key == 'down':
                self.cur_frame = (self.cur_frame + 1) % 4
                self.image = self.frames[self.cur_frame + 6]
                sword = Sword(self.rect.x + 200, self.rect.y)
                all_sprites.add(sword)
                attack.add(sword)

            if key == 'up':
                self.image = self.frames[10]
            if key == 'left':
                self.cur_frame = (self.cur_frame + 1) % 6
                self.image = self.frames[self.cur_frame]
            if key == 'static':
                self.image = self.frames[6]

    def moving(self, key=None):
        if self.life is True:
            if key == 'up':
                self.rect.y -= 8
            if key == 'right':
                self.rect.x += 3
            if key == 'left':
                self.rect.x -= 3

    def physics(self):
        if self.life is True:
            self.rect = self.rect.move(self.x, self.y)
            if pygame.sprite.spritecollideany(self, platform):
                self.y = 0
            else:
                self.y = 2
            if pygame.sprite.spritecollideany(self, wall_1):
                self.x += 1
            elif pygame.sprite.spritecollideany(self, wall_2):
                self.x -= 1
            else:
                self.x = 0

    def death(self):
        self.life = False
        self.image = self.frames[11]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.life = True
        if self.life is False:
            self.image = self.frames[8]
        else:
            self.life = True
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.rect.move(x, y)
            self.c = 0
            self.add(enemy_1)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.image = self.frames[9]
        if pygame.sprite.collide_mask(self, master):
            if self.life is True:
                if self.c <= 6:
                    self.cur_frame = (self.cur_frame + 1) % 6
                    self.image = self.frames[self.cur_frame + 9]
                    self.c += 1
                master.death()
            else:
                pass
        if pygame.sprite.spritecollideany(self, attack):
            self.image = self.frames[8]
            self.life = False
        if self.life is False:
            self.rect.y += 3
            self.image = self.frames[8]


class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image('sword.png')
        self.rect = pygame.Rect(x, y, 1, 1)
        self.mask = pygame.mask.from_surface(self.image)
        self.kill()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image('matat.png')
        self.rect = self.image.get_rect()
        self.rect.x = x - 10
        self.rect.y = y - 30
        self.speed = 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.kill()
        if pygame.sprite.collide_mask(self, master):
            master.death()
            pass
        if pygame.sprite.spritecollideany(self, wall_1) or pygame.sprite.spritecollideany(self, wall_2):
            self.kill()


class Metatel(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.life = True
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(x, y)
        self.c = 0
        self.add(enemy_2)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def shoot(self):
        if self.life is True:
            suriken = Projectile(self.rect.centerx - 20, self.rect.centery)
            all_sprites.add(suriken)
            projectiles.add(suriken)

    def update(self):
        if self.life is True:
            self.image = self.frames[0]
            if pygame.sprite.spritecollideany(self, attack):
                self.image = self.frames[0]
            self.cur_frame = (self.cur_frame + 1) % 3
            self.image = self.frames[self.cur_frame]

    def check(self):
        if pygame.sprite.spritecollideany(self, attack):
            self.image = self.frames[3]
            self.life = False
        if self.life is False:
            self.rect.y += 2
            self.image = self.frames[3]


class Wallleft(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = load_image('wall.png')
        self.rect = pygame.Rect(pos, (25, 200))
        self.add(wall_1)
        self.mask = pygame.mask.from_surface(self.image)


class Wallright(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = load_image('wall.png')
        self.rect = pygame.Rect(pos, (25, 200))
        self.add(wall_2)
        self.mask = pygame.mask.from_surface(self.image)


class Bad(pygame.sprite.Sprite):
    def __init__(self, pos, img):
        super().__init__(all_sprites)
        self.image = load_image(img)
        self.rect = pygame.Rect(pos, (200, 25))
        self.mask = pygame.mask.from_surface(self.image)
        self.add(bad)

    def update(self):
        if pygame.sprite.collide_mask(self, master):
            master.death()


class Fin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = load_image('buddha.png')
        self.rect = pygame.Rect(pos, (200, 200))
        self.mask = pygame.mask.from_surface(self.image)
        self.add(all_sprites)


running = True
t = 0
v = 200
c = 0
j = 0
u = 0
upp = False
clock = pygame.time.Clock()
up = down = block = right = left = False
player = None
camera = Camera()
game_end = True
over = pygame.sprite.Sprite(all_sprites)
over.image = load_image("dead.png")
over.rect = over.image.get_rect()
over.rect.x = 5
over.rect.y = 20
win = pygame.sprite.Sprite(all_sprites)
win.image = load_image("win.png")
win.rect = over.image.get_rect()
win.rect.x = 5
win.rect.y = 20
retur = pygame.sprite.Sprite(all_sprites)
retur.image = load_image("retur.png")
retur.rect = over.image.get_rect()
retur.rect.x = 550
retur.rect.y = 20
paused = pygame.sprite.Sprite(all_sprites)
paused.image = load_image("pause.png")
paused.rect = over.image.get_rect()
paused.rect.x = 5
paused.rect.y = 20
pause = False
while running:
    if game_end:
        all_sprites.empty()
        sprite1.image = load_image('j2.jpg')
        sprite1.rect = sprite1.image.get_rect()
        sprite1.rect.x = -650
        sprite1.rect.y = -600
        sprite2.image = load_image('mont.jpg')
        sprite2.rect = sprite2.image.get_rect()
        sprite2.rect.x = 1300
        sprite2.rect.y = -620
        sprite3.image = load_image('zz.jpg')
        sprite3.rect = sprite2.image.get_rect()
        sprite3.rect.x = 4300
        sprite3.rect.y = -620
        over.kill()
        start_screen()
        game_end = False
        right = False
        left = False
        platform = pygame.sprite.Group()
        bad = pygame.sprite.Group()
        wall_1 = pygame.sprite.Group()
        wall_2 = pygame.sprite.Group()
        all_sprites.add(sprite1)
        all_sprites.add(sprite2)
        all_sprites.add(sprite3)
        attack = pygame.sprite.Group()
        enemy_1 = pygame.sprite.Group()
        enemy_2 = pygame.sprite.Group()
        projectiles = pygame.sprite.Group()
        master = Player(load_image('master_list.png'), 12, 1, 60, 67)
        master.life = True
        plat1 = Platform((0, 550), 'platform1.png')
        plat2 = Platform((200, 550), 'platform1.png')
        plat3 = Platform((400, 550), 'platform1.png')
        plat4 = Platform((600, 350), 'platform2.png')
        plat5 = Bad((800, 350), 'bad.png')
        plat6 = Bad((1000, 350), 'bad.png')
        plat11 = Bad((1200, 350), 'bad.png')
        plat7 = Platform((1200, 550), 'platform1.png')
        plat8 = Platform((1400, 550), 'platform1.png')
        plat16 = Platform((800, 150), 'platform2.png')
        plat17 = Platform((1000, 150), 'platform2.png')
        plat9 = Platform((1600, 550), 'platform1.png')
        plat10 = Platform((1800, 550), 'platform1.png')
        wall001 = Wallleft((2000, 600))
        wall002 = Wallleft((2000, 800))
        plat91 = Platform((2000, 1000), 'platform1.png')
        plat92 = Platform((2200, 1000), 'platform1.png')
        plat93 = Platform((2400, 1000), 'platform1.png')
        plat94 = Platform((2600, 1000), 'platform1.png')
        bad11 = Bad((2800, 1000), 'bad.png')
        mirror15 = Enemy(load_image('ninja.png'), 19, 1, 2600, 830)
        mirror16 = Enemy(load_image('ninja.png'), 19, 1, 2400, 830)
        bad12 = Bad((2400, 550), 'bad.png')
        plat0141 = Platform((3000, 850), 'platform2.png')
        bad13 = Bad((3200, 850), 'bad.png')
        plat12 = Platform((3400, 650), 'platform2.png')
        plat13 = Platform((3600, 650), 'platform2.png')
        bad13 = Bad((3800, 650), 'bad.png')
        plat0142 = Platform((3800, 450), 'platform2.png')
        bad13 = Bad((4000, 450), 'bad.png')
        plat142 = Platform((4000, 250), 'platform2.png')
        plat143 = Platform((4300, 650), 'platform2.png')
        plat144 = Platform((4500, 450), 'platform2.png')
        plat145 = Platform((4300, 450), 'platform2.png')
        plat146 = Platform((4500, 650), 'platform2.png')
        plat0143 = Platform((4200, 250), 'platform2.png')
        plat1433 = Platform((4400, 250), 'platform2.png')
        plat147 = Platform((-200, 550), 'platform1.png')
        wall11 = Wallleft((4700, 250))
        wall12 = Wallleft((4700, 450))
        wall13 = Wallleft((4700, 650))
        wall14 = Wallleft((4700, 850))
        # final
        plat21 = Platform((4700, 1050), 'platform1.png')
        plat22 = Platform((4900, 1050), 'platform1.png')
        bad21 = Bad((5100, 1050), 'bad.png')
        bad22 = Bad((5300, 1050), 'bad.png')
        bad1 = Bad((600, 540), 'bad.png')
        plat23 = Platform((5300, 850), 'platform2.png')
        plat24 = Platform((5500, 850), 'platform2.png')
        plat25 = Platform((5700, 850), 'platform2.png')
        plat26 = Platform((5900, 850), 'platform2.png')
        plat27 = Platform((6100, 850), 'platform2.png')
        plat28 = Platform((6300, 850), 'platform2.png')
        plat29 = Platform((6500, 850), 'platform2.png')
        mirror12 = Enemy(load_image('ninja.png'), 19, 1, 5550, 685)
        mirror13 = Enemy(load_image('ninja.png'), 19, 1, 5750, 685)
        mirror14 = Enemy(load_image('ninja.png'), 19, 1, 5950, 685)
        mirror155 = Enemy(load_image('ninja.png'), 19, 1, 6150, 685)
        metatel4 = Metatel(load_image('ded.png'), 4, 1, 6350, 665)
        wall1 = Wallleft((-200, 350))
        wall2 = Wallleft((-200, 150))
        wall3 = Wallleft((-200, -50))
        wall4 = Wallright((2600, 350))
        wall5 = Wallright((2600, 150))
        wall01 = Wallright((6700, 650))
        wall02 = Wallright((6700, 450))
        wall03 = Wallright((6700, 250))
        mirror1 = Enemy(load_image('ninja.png'), 19, 1, 450, 385)
        mirror3 = Enemy(load_image('ninja.png'), 19, 1, 1850, 375)
        metatel1 = Metatel(load_image('ded.png'), 4, 1, 700, 160)
        metatel2 = Metatel(load_image('ded.png'), 4, 1, 4300, 250)
        metatel3 = Metatel(load_image('ded.png'), 4, 1, 4500, 450)
        mirror101 = Enemy(load_image('ninja.png'), 19, 1, 4400, 85)
        fin = Fin((6500, 650))
    if pygame.sprite.collide_mask(fin, master):
        all_sprites.add(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                over.kill()
                master.life = True
                game_end = True
    if master.life is False:
        all_sprites.add(over)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                over.kill()
                master.life = True
                game_end = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if retur.rect.collidepoint(event.pos):
                game_end = True
                pause = False
        if event.type == pygame.KEYDOWN:
            pause = False
            if event.key == pygame.K_UP and u == 0:
                up = True
                upp = True
            if event.key == pygame.K_DOWN:
                down = True
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_TAB:
                pause = True
                all_sprites.add(paused)
                all_sprites.add(retur)
                all_sprites.draw(screen)
                pygame.display.flip()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_LEFT:
                left = False
    if not pause:
        if paused in all_sprites:
            all_sprites.remove(paused)
        if up:
            master.moving('up')
        if down:
            master.moving('down')
        if right:
            master.moving('right')
        if left:
            master.moving('left')
        screen.fill((0, 0, 0))
        if t % 10 == 0 and right is True:
            master.update('right')
        if t % 10 == 0 and down is True:
            master.update('down')
            c += 1
            if c == 5:
                down = False
                c = 0
        if t % 10 == 0 and up is True:
            master.update('up')
            j += 1
            if j == 4:
                up = False
                j = 0
        if t % 10 == 0 and left is True:
            master.update('left')
        if left is False and right is False and up is False and down is False:
            master.update('static')
        master.physics()
        if t % 10 == 0:
            enemy_1.update()
        if t % 100 == 0:
            enemy_2.update()
        if t % 300 == 0:
            metatel1.shoot()
            metatel2.shoot()
            metatel3.shoot()
            metatel4.shoot()
        metatel1.check()
        metatel2.check()
        metatel3.check()
        metatel4.check()
        projectiles.update()
        fin.update()
        camera.update(master)
        bad.update()
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        pygame.display.flip()
        if upp:
            u += 1
        t += 1
        if u == 145:
            u = 0
            upp = False
terminate()

