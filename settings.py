import pygame as pg
vec = pg.math.Vector2


# ------------------------------------------------GAME SETTINGS --------------------------------------------------- #
WIDTH = 1365
HEIGHT = 768
TITLE = 'Playstore_game'
TILESIZE = 21
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

FPS = 60
FRICTION = -0.12
GRAVITY = 0.8
TILESIZE = 32
GAME_FONT = 'GlueGun-GW8Z.ttf'
FIRST_INTERFACE_IMAGE  = pg.transform.scale(pg.image.load('white background.png'), (WIDTH, HEIGHT))
SECOND_INTERFACE_IMAGE = pg.transform.scale(pg.image.load('white background.png'), (WIDTH, HEIGHT))
WEAPON_INTERFACE_IMAGE = pg.transform.scale(pg.image.load('white background.png'), (WIDTH, HEIGHT))
ESCAPE_INTERFACE_IMAGE = pg.transform.scale(pg.image.load('white background.png'), (WIDTH, HEIGHT))
MAP_INTERFACE_IMAGE    = pg.transform.scale(pg.image.load('white background.png'), (WIDTH, HEIGHT))

# ----------------------------------------------------LAYERS ------------------------------------------------------- #
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
HAND_LAYER = 2
BULLET_LAYER = 2
MAP_LAYER = 0

# -------------------------------------------------- MAP SETTINGS ------------------------------------------------- #
MAP2 = 'dream_tile.tmx'
MAP1 = 'playstore_level1.tmx'

""" Add player name top of the game who is playing now"""
"""different seasons of maps and random choice among them"""
"""gun unlock at level ups"""
"""for different season there are special equipments which will be unlocked as level ups"""
"""after winning , winner will see some kind of face of his enemy"""
"""after sometime a crown or winning object will appear to win the match in short time"""
"""acid map, in which ground become acid and when player touches it it'll die"""
"""make different map unlock when player plays online and keep them lock when offline until level ups"""
"""curtain map"""
""" COLORS"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
GREEN1 = (45, 255, 0)
GREEN2 = (78, 255, 0)
GREEN3 = (126, 255, 0)
GREEN4 = (184, 255, 0)
YELLOW1 = (210, 255, 0)
YELLOW2 = (255, 255, 0)
YELLOW3 = (255, 200, 0)
YELLOW4 = (255, 159, 0)
ORANGE1 = (255, 123, 0)
ORANGE2 = (255, 89, 0)
RED1 = (255, 47, 0)
RED = (255, 0, 0)
LIGHTPINK = (255, 150, 190)
LIGHTGRAY = (203, 255, 255)
GRAY = (199, 197, 194)

# ----------------------------------------PLAYER SETTINGS---------------------------------------------------------- #
SPEEDX = 5
SPEEDY = 2
PLAYER_JUMP = 5
PLAYER_IMAGE = 'one_player4.png'

# ----------------------------------------BULLET SETTINGS --------------------------------------------------------- #
BULLET_IMAGE = 'laserGreen.png'

# ------------------------------------------Trampoline Settings---------------------------------------------------- #
TRAMPOLINE_IMAGE = 'trampoline_img.png'

# ----------------------------------------HAND_SETTINGS ----------------------------------------------------------- #
HAND_ROTATE_SPEED = 20
BARREL_OFFSET = vec(-20, -10)
HAND_IMAGE = 'player_hand.png'

# ----------------------------------------GROUND SETTINGS --------------------------------------------------------- #
GROUND_LIST = [(0, HEIGHT - 2, WIDTH * 2, TILESIZE),
               (int(375), int(HEIGHT-100), 100, TILESIZE),
                 (int(WIDTH / 2 - 50), int(HEIGHT * 3 / 4 - 50), 100, TILESIZE),
                 (125, HEIGHT - 350, 70, TILESIZE),
                 (350, 200, 100, TILESIZE),
                 (175, 100, 100, TILESIZE)]
