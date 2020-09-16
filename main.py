import pygame as pg
import math
from settings import *
from playstore_maps import *
import cmath
from random import uniform

vec = pg.math.Vector2

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
clock = pg.time.Clock()
dt = clock.tick(FPS) / 1000

player_img = pg.image.load(PLAYER_IMAGE)

hand_image = pg.image.load(HAND_IMAGE)
width, height = hand_image.get_size()


def draw_text(text, font_name, size, color, x, y, align="nw"):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "nw":
        text_rect.topleft = (x, y)
    if align == "ne":
        text_rect.topright = (x, y)
    if align == "sw":
        text_rect.bottomleft = (x, y)
    if align == "se":
        text_rect.bottomright = (x, y)
    if align == "n":
        text_rect.midtop = (x, y)
    if align == "s":
        text_rect.midbottom = (x, y)
    if align == "e":
        text_rect.midright = (x, y)
    if align == "w":
        text_rect.midleft = (x, y)
    if align == "center":
        text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


# -----------------------------------------------PLAYER--------------------------------------------------------- #
class Player1(pg.sprite.Sprite):
    def __init__(self, x, y):
        self.groups = all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self._layer = PLAYER_LAYER
        self.image = player_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (int(WIDTH / 2), int(HEIGHT / 2))
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.last_shot = pg.time.get_ticks()
        self.shoot_delay = 250
        self.jumping = True
        print("player1:", self.pos)

    def update(self):
        self.acc = vec(0, GRAVITY)
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]:
            self.acc.x = -0.5
        if keystate[pg.K_d]:
            self.acc.x = 0.5

        self.acc.x += self.vel.x * FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos
        self.rect.center = (self.rect.midbottom[0], self.rect.midbottom[1] - 40)


# ----------------------------------------------BULLET---------------------------------------------------------- #
class Bullet(pg.sprite.Sprite):
    def __init__(self, bullet_rotation, bullet_pos, bullet_direction):
        # self._layer = BULLET_LAYER
        self.groups = all_sprites, bullets
        self._layer = BULLET_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.orig_image = pg.transform.scale(pg.image.load(BULLET_IMAGE), (2, 9))

        self.image = pg.transform.rotate(self.orig_image, bullet_rotation)
        self.rect = self.image.get_rect()
        self.pos = bullet_pos
        self.rect.center = self.pos
        # self.image.set_colorkey(BLACK)
        # spread = uniform(-GUN_SPREAD, GUN_SPREAD)

        # velocity of bullet  = Bullet speed * direction vector
        self.vel = bullet_direction * 200 * 1.1

        # spawn time of bullet after it get deleted
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * dt
        self.rect.center = self.pos

        # bullet collision with walls
        if pg.sprite.spritecollideany(self, grounds):
            self.kill()

        # bullet deletion
        if pg.time.get_ticks() - self.spawn_time > 5000:
            self.kill()


# ----------------------------------------------PLAYER_HAND----------------------------------------------------- #
class Hand(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self._layer = HAND_LAYER
        self.image = hand_image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.pos = pg.math.Vector2(int(player1.pos[0] + 6), int(player1.pos[1] - 20))
        self.rect.center = (int(WIDTH / 2), int(HEIGHT / 2))
        self.originPos = (width // 2, height // 2)
        self.surf = screen
        self.last_shot = pg.time.get_ticks()
        self.shoot_delay = 250

    def update(self):
        self.pos = pg.math.Vector2(int(player1.pos[0] + 6), int(player1.pos[1] - 20))
        self.rect.center = (player1.rect.center[0] + 3, player1.rect.center[1] + 4)
        # self.blitRotate(screen, self.image, (width // 2, height // 2))
        # calcaulate the axis aligned bounding box of the rotated image
        rel_x = mouse[0] - self.pos[0]
        rel_y = mouse[1] - self.pos[1]
        self.angle = math.atan2(rel_x, rel_y) * 180 // 3.14
        print("angle", self.angle)
        w, h = self.image.get_size()
        box = [pg.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(self.angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot
        # pivot        = pg.math.Vector2(originPos[0], -originPos[1])
        # pivot_rotate = pivot.rotate(-angle)
        # pivot_move   = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        self.origin = (self.pos[0] - self.originPos[0] + min_box[0], self.pos[1] - self.originPos[1] - max_box[1])
        # origin = pg.math.Vector2(int(mouse[0]), int(mouse[1]))
        # get a rotated image
        self.rotated_image = pg.transform.rotate(self.image, self.angle)
        if pg.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.last_shot = pg.time.get_ticks()
            self.shoot()
        # print("hand_center:", self.pos)

    def shoot(self):
        keys = pg.key.get_pressed()
        bullet_direction = vec(0, 1).rotate(-self.angle)
        if keys[pg.K_f]:
            Bullet(self.angle, self.rect.center, bullet_direction)

    def draw(self, surface):
        # rotate and blit the image
        surface.blit(self.rotated_image, self.origin)


# ----------------------------------------------GROUND---------------------------------------------------------- #
class Ground(pg.sprite.Sprite):
    def __init__(self, x, y, ground_width, ground_height):
        self.groups = all_sprites, grounds
        self._layer = PLATFORM_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        # self.image = pg.Surface((width, height))
        # self.image.fill(GREEN)
        # self.rect = self.image.get_rect()
        self.rect = pg.Rect(x, y, ground_width, ground_height)
        self.x = x
        self.y = y
        self.rect.center = self.x, self.y


def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGREY, (0, y), (WIDTH, y))


def first_interface():
    screen.blit(FIRST_INTERFACE_IMAGE, (0, 0))
    draw_text("WELCOME", GAME_FONT, 50, BLACK, WIDTH / 2, 50, align='center')
    menu_start_button.draw(screen, 45, (0, 0, 0))
    quit_button.draw(screen, 45, (0, 0, 0))
    pg.display.flip()
    # pg.event.wait()


def second_interface():
    screen.blit(SECOND_INTERFACE_IMAGE, (0, 0))
    play_button.draw(screen, 45, (0, 0, 0))
    weapon_button.draw(screen, 45, (0, 0, 0))
    map_settings_button.draw(screen, 45, (0, 0, 0))
    pg.display.flip()


def weapon_interface():
    screen.blit(WEAPON_INTERFACE_IMAGE, (0, 0))
    back_button.draw(screen, 45, (0, 0, 0))
    pg.display.flip()


def escape_interface():
    screen.blit(ESCAPE_INTERFACE_IMAGE, (0, 0))
    continue_button.draw(screen, 45, (0, 0, 0))
    quit_button.draw(screen, 45, (0, 0, 0))
    pg.display.flip()


def map_interface():
    screen.blit(MAP_INTERFACE_IMAGE, (0, 0))
    MAP1_button.draw(screen, 45, (0, 0, 0))
    MAP2_button.draw(screen, 45, (0, 0, 0))
    okay_button.draw(screen, 45, (0, 0, 0))
    pg.display.flip()


# ----------------------------------------------JUMP OF PLAYER-------------------------------------------------- #
def jump():
    hits = pg.sprite.spritecollide(player1, grounds, False)
    if hits:
        player1.vel.y = -20


# -------------------------------------------MAP_SETTINGS------------------------------------------------------ #
map = TiledMap(MAP1)
map_img = map.make_map()
map_rect = map_img.get_rect()

# ----------------------------------------------SPRITES--------------------------------------------------------- #
all_sprites = pg.sprite.LayeredUpdates()
grounds = pg.sprite.Group()
# for ground in GROUND_LIST:
#     Ground(*ground)
for tile_object in map.tmxdata.objects:
    obj_center = vec(tile_object.x + tile_object.width / 2,
                     tile_object.y + tile_object.height / 2)

    if tile_object.name == 'player':
        player1 = Player1(obj_center.x, obj_center.y)
    if tile_object.name == 'ground':
        Ground(obj_center.x, obj_center.y, tile_object.width, tile_object.height)
# player1 = Player1(400, 300)
bullets = pg.sprite.Group()
hand = Hand()

# ------------------------------------------ Camera ----------------------------------------------------------- #
# camera = Camera(map.width, map.height)
# ---------------------------------------- Weapons ------------------------------------------------------------ #

# -----------------------------------------Buttons------------------------------------------------------------- #
menu_start_button = Button(WHITE, WIDTH - 200, HEIGHT - 200, 100, 30, 'Start')
quit_button = Button(WHITE, 100, HEIGHT - 200, 100, 35, 'Quit')
play_button = Button(WHITE, WIDTH - 450, HEIGHT - 100, 100, 30, 'PLAY')
weapon_button = Button(WHITE, 100, HEIGHT - 200, 100, 30, 'WEAPON')
back_button = Button(WHITE, WIDTH - 200, 10, 100, 30, 'BACK')
continue_button = Button(WHITE, 300, 300, 100, 30, 'CONTINUE')
map_settings_button = Button(WHITE, 300, HEIGHT - 200, 100, 30, 'MAPS')
MAP1_button = Button(WHITE, 50, 200, 100, 30, 'MAP_1')
MAP2_button = Button(WHITE, 250, 200, 100, 30, 'MAP_2')
okay_button = Button(WHITE, WIDTH - 100, HEIGHT - 30, 100, 30, 'OKAY')
maps_button = [MAP1_button, MAP2_button]
all_button = [menu_start_button, play_button, quit_button, back_button, weapon_button, continue_button]

# ---------------------------------------------MAIN_GAME_LOOP--------------------------------------------------- #
first_interface_start = True
second_interface_start = True
weapon_interface_start = True
escape_interface_start = True
map_selected = False
last_interface = True
mouse_motion = True
done = False
while not done:
    if first_interface_start:
        first_interface()
    clock.tick(FPS)
    # keep loop running at the right speed

    # global direction
    # Process input (events)
    mouse = pg.mouse.get_pos()
    cursor = pg.mouse.get_pos()

    # print("mouse:", mouse)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            pg.quit()
        if not last_interface:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    escape_interface_start = True
                    if escape_interface_start:
                        last_interface = True
                        escape_interface()

                if event.key == pg.K_SPACE:
                    jump()
        # -------------------------------------------- Button Working------------------------------------------- #
        if event.type == pg.MOUSEBUTTONDOWN:
            if menu_start_button.isOver(mouse):
                first_interface_start = False
                second_interface()

            if play_button.isOver(mouse):
                last_interface = False

            if weapon_button.isOver(mouse):
                weapon_interface()

            if map_settings_button.isOver(mouse):
                map_interface()

            for selected_map in maps_button:
                if selected_map.isOver(mouse):
                    map_selected = True
                    if selected_map == MAP1_button:
                        map = TiledMap(MAP1)
                        map_img = map.make_map()
                        map_rect = map_img.get_rect()
                        # map.update(MAP1)
                        print('map1')
                    if selected_map == MAP2_button:
                        map = TiledMap(MAP2)
                        map_img = map.make_map()
                        map_rect = map_img.get_rect()
                        # map.update(MAP2)
                        print('map2')
                    print('map is selected')

            if okay_button.isOver(mouse):
                if not map_selected:
                    print('please select at least one map')

                if map_selected:
                    second_interface()

            if back_button.isOver(mouse):
                second_interface()

            if continue_button.isOver(mouse):
                last_interface = False
                escape_interface_start = False

            if quit_button.isOver(mouse):
                pg.quit()
                quit()
        if event.type == pg.MOUSEMOTION:
            for button in all_button:
                if button.isOver(mouse):
                    button.color = GRAY
                else:
                    button.color = WHITE
    # --------------------------------------------- Game starts ----------------------------------------------- #
    if not last_interface:
        screen.fill(WHITE)
        all_sprites.update()
        hand.update()
        if player1.vel.y > 0:
            hits = pg.sprite.spritecollide(player1, grounds, False)
            if hits:
                for hit in hits:
                    # if player1.pos.y - 5 < hit.rect.centery:
                    player1.pos.y = hit.rect.top
                    player1.vel.y = 0

        if player1.rect.top <= HEIGHT / 4:
            player1.pos.y += abs(player1.vel.y)
            for plat in grounds:
                plat.rect.y += abs(player1.vel.y)

        if player1.rect.top >= HEIGHT * 3 / 4:
            player1.pos.y -= abs(player1.vel.y)
            for plat in grounds:
                plat.rect.y -= abs(player1.vel.y)

        # camera.update(player1)
        screen.blit(map_img, map_rect)
        all_sprites.draw(screen)

        # pos = pg.math.Vector2(int(player1.pos[0] + 6), int(player1.pos[1] - 20))
        hand.draw(screen)
        # draw_grid()
        pg.display.flip()

pg.quit()
