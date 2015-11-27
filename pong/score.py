#!/usr/bin/env python
import pong
import logging
import random
# import sys
# http://www.pygame.org/docs/ref/pygame.html
import pygame
#
import pygame.event
#
import pygame.image
#
import pygame.key
# http://www.pygame.org/docs/ref/draw.html
import pygame.draw
# http://www.pygame.org/docs/ref/time.html
import time
import pygame.time

import os
import sys
sys.path.insert(0, os.path.realpath('.'))
os.environ["SDL_VIDEO_CENTERED"] = "TRUE"

######################################################################

######################################################################
# CONSTANTLY CONSTANT STUFF
DISPLAY_ICON = "assets/icon.png"

# Reference stuff
# http://www.pygame.org/docs/ref/rect.html
# http://www.pygame.org/docs/ref/surface.html
# http://www.pygame.org/docs/ref/sprite.html
# http://www.pygame.org/docs/ref/font.html

######################################################################
court_margin = 8
court_width = 1124
court_height = 632
court_rect = pygame.Rect(78, 44, court_width, court_height)
# We'll make the actual court_rect once we have a screen

######################################################################
log = logging.getLogger("pong")
log.setLevel(logging.INFO)
log_stream_handler = logging.StreamHandler()
log_stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s  - %(message)s"))
log_stream_handler.setLevel(logging.INFO)
log.addHandler(log_stream_handler)
log.info("Logging initialized")

######################################################################
screen_w = 1280
screen_h = 720

######################################################################
pygame.init()
screen = pygame.display.set_mode((screen_w, screen_h))
icon = pygame.image.load(DISPLAY_ICON)
pygame.display.set_icon(icon)
pygame.display.set_caption("TBLABLABONG")
clock = pygame.time.Clock()
if '-f' in sys.argv or '--fullscreen' in sys.argv:
    pygame.display.toggle_fullscreen()
    pygame.mouse.set_visible(False)

show_splash = True
if '-q' in sys.argv or '--quick' in sys.argv:
    show_splash = False

# D for debug
if '-d' in sys.argv or '--debug' in sys.argv:
    show_fps = True
    log.setLevel(logging.DEBUG)
    log_stream_handler.setLevel(logging.DEBUG)

screen_rect = screen.get_rect()

######################################################################
# The screen borders
#     Rect(left, top, width, height) -> Rect
screen_top = pygame.Rect(0, 0, screen_w, 1)
screen_bottom = pygame.Rect(0, screen_h, screen_w, 1)
screen_right = pygame.Rect(screen_w, 0, 1, screen_h)
screen_left = pygame.Rect(0, 0, 1, screen_h)

wall_list = [screen_top, screen_right, screen_bottom, screen_left]

h_walls = pygame.sprite.Group()
v_walls = pygame.sprite.Group()

######################################################################
# The pong ball
paddles = pygame.sprite.Group()
paddles.add(pong.PongPaddle(pong.PADDLE_LEFT, wall_list, screen))
paddles.add(pong.PongPaddle(pong.PADDLE_RIGHT, wall_list, screen))


def new_ball():
    angle = float(random.randrange(0, 359))
    logging.getLogger('pong').debug("Projectile angle: %s" % angle)
    # return pong.PongBall(wall_list, paddles, angle=angle)
    return pong.PongBall(wall_list, paddles, velocity=15, angle=angle)

######################################################################
# Fonts
pygame.font.init()

# score_font = pygame.font.SysFont(pong.SCORE_FONT, 64)
score_font = pygame.font.Font(pong.BUNDLED_FONT, 64)
# A test string so we can get some data positioning for later
score_size = score_font.render("10", True, pong.white).get_size()
score_width = score_size[0]
score_height = score_size[1]
######################################################################

s_rect_w = screen_rect.width
s_rect_h = screen_rect.height

score_width = 76

dividing_line = pong.CourtDividingLine()
score_region_l = pygame.Rect((screen_rect.width * .25) - score_width * .5,
                             44,
                             score_width,
                             score_height)
score_region_r = pygame.Rect((screen_rect.width * .75 - score_width * .5,
                             44,
                             score_width,
                             score_height))

LEFT_SCORE = 0
RIGHT_SCORE = 0
ball = new_ball()
game_start_time = time.time()
splash_screen = pong.AnnoyingSplashScreen()
court_skirt = pong.CourtSkirt()

while 1:
    ######################################################################
    # Basic handlers and static assets
    clock.tick(45)
    # How long since we started the game (in seconds)
    if show_splash:
        dt = time.time() - game_start_time
    else:
        # Fake setting the time so we can skip the splash
        dt = 10

    for event in pygame.event.get():
        # Enable the 'close window' button
        if event.type == pygame.QUIT:
            sys.exit()
    kb_input = pygame.key.get_pressed()

    if kb_input[pygame.K_ESCAPE] == 1:
        sys.exit()

    if kb_input[pygame.K_f] == 1:
        pygame.display.toggle_fullscreen()

    # This clears out the trails left by moving objects
    screen.fill(pong.black)

    ######################################################################
    left_score = pong.score_digitize(LEFT_SCORE)
    right_score = pong.score_digitize(RIGHT_SCORE)

    # Create a surface (score) to blit onto the screen
    if dt <= 4:
        splash_screen.update()
        pygame.display.flip()
        # Press any key to skip the intro
        if 1 in kb_input:
            show_splash = False
        continue
    else:
        score_surface_l = score_font.render(left_score, True, pong.white)
        screen.blit(score_surface_l, score_region_l)
        score_surface_r = score_font.render(right_score, True, pong.white)
        screen.blit(score_surface_r, score_region_r)

    paddles.update()
    court_skirt.update()
    dividing_line.update()

    ######################################################################

    ball_play = ball.update()
    # 1 and 3 are the indicie of the right and left walls
    if not ball_play:
        pass
    elif ball_play == 1:
        log.debug("hit right: %s" % ball_play)
        # Hitting the right wall is a point for the left player
        LEFT_SCORE += 1
        ball = new_ball()
    elif ball_play == 3:
        log.debug("hit left")
        # And the left wall is a point for the right player
        ball = new_ball()
        RIGHT_SCORE += 1

    pygame.display.flip()
