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

show_splash = True
if '-q' in sys.argv or '--quick' in sys.argv:
    show_splash = False

show_debug = False
# D for debug
if '-d' in sys.argv or '--debug' in sys.argv:
    show_debug = True
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
paddles.add(pong.PongPaddleLeft(wall_list))
paddles.add(pong.PongPaddleRight(wall_list))


def new_ball():
    angle = float(random.randrange(0, 359))
    # angle = 25
    logging.getLogger('pong').debug("Projectile angle: %s" % angle)
    return pong.PongBall(wall_list, paddles, velocity=15, angle=angle)

######################################################################
dividing_line = pong.CourtDividingLine()
ball = new_ball()
game_start_time = time.time()
splash_screen = pong.AnnoyingSplashScreen()
court_skirt = pong.CourtSkirt()
debug_panel = pong.DebugPanel(show_debug)

left_score = pong.PongScoreLeft()
right_score = pong.PongScoreRight()

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

    # Create a surface (score) to blit onto the screen
    if dt <= 4:
        splash_screen.update()
        pygame.display.flip()
        # Press any key to skip the intro
        if 1 in kb_input:
            show_splash = False
        continue

    left_score.update()
    right_score.update()
    paddles.update()
    court_skirt.update()
    dividing_line.update()
    debug_str = "FPS: %s; Ball Theta: %s" % (int(clock.get_fps()), int(ball.angle))
    debug_panel.update(debug_str)

    ######################################################################

    ball_play = ball.update()
    # 1 and 3 are the indicie of the right and left walls
    if not ball_play:
        pass
    elif ball_play == 1:
        log.debug("hit right: %s" % ball_play)
        # Hitting the right wall is a point for the left player
        left_score.scored()
        ball = new_ball()
    elif ball_play == 3:
        log.debug("hit left")
        # And the left wall is a point for the right player
        right_score.scored()
        ball = new_ball()

    pygame.display.flip()
