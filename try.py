import pygame as pg
import pytmx
from settings import *
from playstore_maps import *
from playstore_sprites import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.last_interface = True
        self.first_interface_start = True
        self.second_interface_start = True
        self.map_setting_interface = True
        self.weapon_interface_start = True
        self.escape_interface_start = True
        self.map_selected = True

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
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
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        self.player_img = pg.image.load(PLAYER_IMAGE)
        self.hand_image = pg.image.load(HAND_IMAGE)
        self.hand_width, self.hand_height = self.hand_image.get_size()

        # ----------------------------------------- BUTTONS ----------------------------------------------------- #
        self.menu_start_button = Button(WHITE, WIDTH - 200, HEIGHT - 200, 100, 30, 'Start')
        self.quit_button = Button(WHITE, 100, HEIGHT - 200, 100, 35, 'Quit')
        self.play_button = Button(WHITE, WIDTH - 450, HEIGHT - 100, 100, 30, 'PLAY')
        self.weapon_button = Button(WHITE, 100, HEIGHT - 200, 100, 30, 'WEAPON')
        self.back_button = Button(WHITE, WIDTH - 200, 10, 100, 30, 'BACK')
        self.continue_button = Button(WHITE, 300, 300, 100, 30, 'CONTINUE')
        self.map_settings_button = Button(WHITE, 300, HEIGHT - 200, 100, 30, 'MAPS')
        self.MAP1_button = Button(WHITE, 50, 200, 100, 30, 'MAP_1')
        self.MAP2_button = Button(WHITE, 250, 200, 100, 30, 'MAP_2')
        self.okay_button = Button(WHITE, WIDTH - 100, HEIGHT - 30, 100, 30, 'OKAY')
        self.maps_button = [self.MAP1_button, self.MAP2_button]
        self.all_button = [self.menu_start_button, self.play_button, self.quit_button, self.back_button,
                           self.weapon_button, self.continue_button]
        self.map_pos_y = 0

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.map = TiledMap(MAP1)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.grounds = pg.sprite.Group()
        # --------------------------------------------------------------------------------------------------------- #
        for tile_object in self.map.tmxdata.objects:
            # taking exact center of sprites as in Tiled map
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)

            if tile_object.name == 'ground':
                Platform(self, obj_center.x, obj_center.y, tile_object.width, tile_object.height)

        self.bullets = pg.sprite.Group()
        self.player1 = Player1(self, 300, 400)
        self.hand = Hand(self)
        # self.map_pos_y = self.player1.vel.y

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.last_interface:
                self.update()
                self.draw()

    def first_interface(self):
        self.screen.blit(FIRST_INTERFACE_IMAGE, (0, 0))
        self.draw_text("WELCOME", GAME_FONT, 50, BLACK, WIDTH / 2, 50, align='center')
        self.menu_start_button.draw(self.screen, 45, (0, 0, 0))
        self.quit_button.draw(self.screen, 45, (0, 0, 0))
        pg.display.flip()
        # pg.event.wait()

    def second_interface(self):
        self.screen.blit(SECOND_INTERFACE_IMAGE, (0, 0))
        self.play_button.draw(self.screen, 45, (0, 0, 0))
        self.weapon_button.draw(self.screen, 45, (0, 0, 0))
        self.map_settings_button.draw(self.screen, 45, (0, 0, 0))
        pg.display.flip()

    def weapon_interface(self):
        self.screen.blit(SECOND_INTERFACE_IMAGE, (0, 0))
        self.back_button.draw(self.screen, 45, (0, 0, 0))
        pg.display.flip()

    def escape_interface(self):
        self.screen.blit(ESCAPE_INTERFACE_IMAGE, (0, 0))
        self.continue_button.draw(self.screen, 45, (0, 0, 0))
        self.quit_button.draw(self.screen, 45, (0, 0, 0))
        pg.display.flip()

    def map_interface(self):
        self.screen.blit(MAP_INTERFACE_IMAGE, (0, 0))
        self.MAP1_button.draw(self.screen, 45, (0, 0, 0))
        self.MAP2_button.draw(self.screen, 45, (0, 0, 0))
        self.okay_button.draw(self.screen, 45, (0, 0, 0))
        pg.display.flip()

    def update(self):
        self.all_sprites.update()
        self.hand.update()
        if self.player1.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player1, self.grounds, False)
            if hits:
                for hit in hits:
                    # if player1.pos.y - 5 < hit.rect.centery:
                    self.player1.pos.y = hit.rect.top
                    self.player1.vel.y = 0

        if self.player1.rect.top <= HEIGHT / 4:
            self.player1.pos.y += max(abs(self.player1.vel.y), 2)
            # for plat in self.grounds:
            #     plat.rect.y += max(abs(self.player1.vel.y), 2)

            self.map_rect.y += max(abs(self.player1.vel.y), 2)

        if self.player1.rect.top >= HEIGHT * 3 / 4:
            self.player1.pos.y -= max(abs(self.player1.vel.y), 2)
            for plat in self.grounds:
                plat.rect.y -= max(abs(self.player1.vel.y), 2)
            self.map_rect.y -= max(abs(self.player1.vel.y), 2)

        # print("map_y", self.map_rect.y)
    def draw(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.map_img, self.map_rect)
        self.all_sprites.draw(self.screen)
        self.hand.draw(self.screen)
        pg.display.flip()

    def start_screen(self):
        if self.first_interface_start:
            self.first_interface()

    def events(self):
        self.mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player1.jump()

                if event.key == pg.K_ESCAPE:
                    pg.quit()

            # ----------------------------------------- buttons -------------------------------------------- #
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.menu_start_button.isOver(self.mouse):
                    self.first_interface_start = False
                    self.second_interface()

                if self.back_button.isOver(self.mouse):
                    self.second_interface()

                if self.play_button.isOver(self.mouse):
                    self.last_interface = False

                if self.map_settings_button.isOver(self.mouse):
                    self.map_interface()

                if self.weapon_button.isOver(self.mouse):
                    self.weapon_interface()

                if self.quit_button.isOver(self.mouse):
                    pg.quit()

                if self.okay_button.isOver(self.mouse):
                    if not self.map_selected:
                        print('please select at least one map')

                    if self.map_selected:
                        self.second_interface()

                for selected_map in self.maps_button:
                    if selected_map.isOver(self.mouse):
                        self.map_selected = True
                        if selected_map == self.MAP1_button:
                            self.map = TiledMap(MAP1)
                            self.map_img = self.map.make_map()
                            self.map_rect = self.map_img.get_rect()

                        if selected_map == self.MAP2_button:
                            self.map = TiledMap(MAP2)
                            self.map_img = self.map.make_map()
                            self.map_rect = self.map_img.get_rect()
g = Game()
g.start_screen()
while True:
    g.new()















