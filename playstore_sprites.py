import pygame as pg
import math
from settings import *
from playstore_maps import *


# -----------------------------------------------PLAYER--------------------------------------------------------- #
class Player1(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self._layer = PLAYER_LAYER
        self.image = game.player_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (int(WIDTH / 2), int(HEIGHT / 2))
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.last_shot = pg.time.get_ticks()
        self.shoot_delay = 250
        self.jumping = True
        # print("player1:", self.pos)

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

    def jump(self):
        hits = pg.sprite.spritecollide(self.game.player1, self.game.grounds, False)
        if hits:
            self.game.player1.vel.y = -20


# ----------------------------------------------BULLET---------------------------------------------------------- #
class Bullet(pg.sprite.Sprite):
    def __init__(self, game, bullet_rotation, bullet_pos, bullet_direction):
        # self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        self._layer = BULLET_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
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
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        # bullet collision with walls
        if pg.sprite.spritecollideany(self, self.game.grounds):
            self.kill()

        # bullet deletion
        if pg.time.get_ticks() - self.spawn_time > 5000:
            self.kill()


# ----------------------------------------------PLAYER_HAND----------------------------------------------------- #
class Hand(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self._layer = HAND_LAYER
        self.game = game
        self.image = game.hand_image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.pos = pg.math.Vector2(int(game.player1.pos[0] + 6), int(game.player1.pos[1] - 20))
        self.rect.center = (int(WIDTH / 2), int(HEIGHT / 2))
        self.originPos = (game.hand_width // 2, game.hand_height // 2)
        self.surf = game.screen
        self.last_shot = pg.time.get_ticks()
        self.shoot_delay = 250

    def update(self):
        self.pos = pg.math.Vector2(int(self.game.player1.pos[0] + 6), int(self.game.player1.pos[1] - 20))
        self.rect.center = (self.game.player1.rect.center[0] + 3, self.game.player1.rect.center[1] + 4)
        # self.blitRotate(screen, self.image, (width // 2, height // 2))
        # calcaulate the axis aligned bounding box of the rotated image
        rel_x = self.game.mouse[0] - self.pos[0]
        rel_y = self.game.mouse[1] - self.pos[1]
        self.angle = math.atan2(rel_x, rel_y) * 180 // 3.14
        # print("angle", self.angle)
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
            Bullet(self.game, self.angle, self.rect.center, bullet_direction)

    def draw(self, surface):
        # rotate and blit the image
        surface.blit(self.rotated_image, self.origin)


# ----------------------------------------------GROUND---------------------------------------------------------- #
class Ground(pg.sprite.Sprite):
    def __init__(self, game, x, y, ground_width, ground_height):
        self.groups = game.all_sprites, game.grounds
        self._layer = PLATFORM_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((ground_width, ground_height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # self.rect = pg.Rect(x, y, ground_width, ground_height)
        self.x = x
        self.y = y
        self.rect.center = self.x, self.y


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, ground_width, ground_height):
        self.groups = game.grounds
        self._layer = PLATFORM_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((ground_width, ground_height))
        # self.image.fill(GREEN)
        # self.rect = self.image.get_rect()
        self.rect = pg.Rect(x, y, ground_width, ground_height)
        self.x = x
        self.y = y
        self.rect.center = self.x, self.y