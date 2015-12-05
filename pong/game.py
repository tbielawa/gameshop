#!/usr/bin/env python
import pong
import pong.scene
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

    court_visual = pygame.Rect(78, 44, 1124, 632)


screen_rect = screen.get_rect()

######################################################################
# The screen borders
#     Rect(left, top, width, height) -> Rect
screen_top = pygame.Rect(0, 0, screen_w, 1)
screen_bottom = pygame.Rect(0, screen_h, screen_w, 1)
screen_right = pygame.Rect(screen_w, 0, 1, screen_h)
screen_left = pygame.Rect(0, 0, 1, screen_h)

v_walls = pygame.sprite.Group(pong.Wall(screen_left, pong.WALL_LEFT), pong.Wall(screen_right, pong.WALL_RIGHT))
h_walls = pygame.sprite.Group(pong.Wall(screen_top, pong.WALL_TOP), pong.Wall(screen_bottom, pong.WALL_BOTTOM))

######################################################################
# XXX: Future - use
paddles = pygame.sprite.Group()
paddles.add(pong.PongPaddleLeft(h_walls=h_walls))
paddles.add(pong.PongPaddleRight(h_walls=h_walls))

######################################################################
dividing_line = pong.CourtDividingLine()

game_start_time = time.time()
splash_screen = pong.AnnoyingSplashScreen()
court_skirt = pong.CourtSkirt()
debug_panel = pong.DebugPanel(show_debug)
left_score = pong.PongScoreLeft()
right_score = pong.PongScoreRight()

######################################################################

splash_scene = pong.scene.AnnoyingSplashScreenScene({'clock': clock}, active=True)

######################################################################
# The pong ball initializer
def new_ball(serve_to=None):
    if serve_to is None:
        # This is a new game, there is nobody specifically to serve to
        angle = random.choice(pong.serve_all)

    # This is a running game, select the side to serve to:
    elif serve_to == pong.PADDLE_LEFT:
        angle = random.choice(pong.serve_left)
    elif serve_to == pong.PADDLE_RIGHT:
        angle = random.choice(pong.serve_right)
    else:
        raise TypeError("Invalid argument type to new_ball. 'serve_to' must be pong.PADDLE_LEFT, pong.PADDLE_RIGHT, or None")

    logging.getLogger('pong').info("New ball angle: %s" % angle)
    return pong.PongBall(paddles, velocity=13, angle=angle, h_walls=h_walls, v_walls=v_walls, court_skirt=court_skirt)

ball = new_ball()

while splash_scene.active and show_splash:
    for event in pygame.event.get():
        # Enable the 'close window' button
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            kb_input = pygame.key.get_pressed()

            if kb_input[pygame.K_ESCAPE] == 1:
                sys.exit()

            # Break out of the splash as soon as someone presses a key
            show_splash = False
            splash_screen.active = False
            break
        else:
            splash_scene.run()

######################################################################
while 1:

    # Basic handlers and static assets
    clock.tick(45)

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

    if show_debug:
        pygame.draw.rect(screen, (000, 175, 000), court_visual, 2)

    ######################################################################
    left_score.update()
    right_score.update()
    paddles.update()
    court_skirt.update()
    dividing_line.update()
    debug_str = "FPS: %s; Ball Theta: %s" % (round(clock.get_fps(), 2), int(ball.angle))
    debug_panel.update(debug_str)

    ######################################################################

    ball_play = ball.update()
    if not ball_play:
        pass
    elif ball_play == pong.WALL_RIGHT:
        log.info("hit right wall")
        # Hitting the right wall is a point for the left player
        left_score.scored()
        ball = new_ball(serve_to=pong.PADDLE_RIGHT)
    elif ball_play == pong.WALL_LEFT:
        log.info("hit left wall")
        # And the left wall is a point for the right player
        right_score.scored()
        ball = new_ball(serve_to=pong.PADDLE_LEFT)

    pygame.display.flip()
