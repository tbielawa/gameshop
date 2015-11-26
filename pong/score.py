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

import random
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
court_width = 624
court_height = 464
court_rect = pygame.Rect(8, 8, court_width, court_height)

######################################################################
log = logging.getLogger("pong")
log.setLevel(logging.DEBUG)
log_stream_handler = logging.StreamHandler()
log_stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s  - %(message)s"))
log_stream_handler.setLevel(logging.DEBUG)
log.addHandler(log_stream_handler)
log.info("Logging initialized")

######################################################################
screen_w = court_width + (court_margin * 2)
screen_h = court_height + (court_margin * 2)
screen_dim = (screen_w, screen_h)


######################################################################
# The screen borders
#     Rect(left, top, width, height) -> Rect
screen_top = pygame.Rect(court_rect.topleft, (court_rect.w, 2))
screen_right = pygame.Rect(court_rect.topright, (2, court_rect.h + 2))
screen_bottom = pygame.Rect(court_rect.bottomleft, (court_rect.w, 2))
screen_left = pygame.Rect(court_rect.topleft, (2, court_rect.h))
# wall_names = ["top", "right", "bottom", "left"]
wall_list = [screen_top, screen_right, screen_bottom, screen_left]

h_walls = pygame.sprite.Group()
v_walls = pygame.sprite.Group()


######################################################################
pygame.init()
screen = pygame.display.set_mode(screen_dim)
icon = pygame.image.load(DISPLAY_ICON)
pygame.display.set_icon(icon)
pygame.display.set_caption("TBLABLABONG")
clock = pygame.time.Clock()
if '-f' in sys.argv or '--fullscreen' in sys.argv:
    pygame.display.toggle_fullscreen()
    pygame.mouse.set_visible(False)


######################################################################
# The pong ball
paddles = pygame.sprite.Group()
paddles.add(pong.PongPaddle(pong.PADDLE_LEFT, wall_list, screen))
paddles.add(pong.PongPaddle(pong.PADDLE_RIGHT, wall_list, screen))

def new_ball():
    angle = float(random.randrange(0,359))
    logging.getLogger('pong').debug("Projectile angle: %s" % angle)
    # return pong.PongBall(wall_list, paddles, angle=angle)
    return pong.PongBall(wall_list, paddles, angle=15)

######################################################################
# Fonts
pygame.font.init()
# fonts = pygame.font.get_fonts()
# if pong.DEFAULT_FONT not in fonts:
#     pong.DEFAULT_FONT = pygame.font.get_default_font()

# score_font = pygame.font.SysFont(pong.SCORE_FONT, 64)
score_font = pygame.font.Font(pong.BUNDLED_FONT, 64)
# A test string so we can get some data positioning for later
score_size = score_font.render("10", True, pong.white).get_size()
score_width = score_size[0]
score_height = score_size[1]
######################################################################
screen_rect = screen.get_rect()
s_rect_w = screen_rect.width
s_rect_h = screen_rect.height

score_width = 76


# centerx is the horizontal mid-point of the rectangle
# centery is the vertical mid-point of the rectangle
dividing_line = pygame.Rect(court_rect.centerx - 4,
                            court_rect.top + 2,
                            6,
                            court_rect.height - 2)

score_region_l = pygame.Rect((screen_rect.width * .25) - score_width * .5,
                             dividing_line.top + 10,
                             score_width,
                             score_height)
score_region_r = pygame.Rect((screen_rect.width * .75  - score_width * .5,
                             dividing_line.top + 10,
                             score_width,
                             score_height))


LEFT_SCORE = 0
RIGHT_SCORE = 0

ball = new_ball()

game_start_time = time.time()

while 1:
    ######################################################################
    # Basic handlers and static assets
    clock.tick(30)
    # How long since we started the game (in seconds)
    dt = time.time() - game_start_time

    for event in pygame.event.get():
        # Enable the 'close window' button
        if event.type == pygame.QUIT:
            sys.exit()
    kb_input = pygame.key.get_pressed()

    if kb_input[pygame.K_ESCAPE] == 1 or kb_input[pygame.K_q] == 1:
        sys.exit()

    if kb_input[pygame.K_f] == 1:
        pygame.display.toggle_fullscreen()

    # This clears out the trails left by moving objects
    screen.fill(pong.black)

    # These are the bounding walls of the court.
    #
    # These silly screen_<DIR> vars are Rect()s. They're defined above
    pygame.draw.rect(screen, pong.white, screen_right)
    pygame.draw.rect(screen, pong.white, screen_left)
    pygame.draw.rect(screen, pong.white, screen_bottom)
    pygame.draw.rect(screen, pong.white, screen_top)
    ######################################################################

    ######################################################################
    left_score = pong.score_digitize(LEFT_SCORE)
    right_score = pong.score_digitize(RIGHT_SCORE)

    # Create a surface (score) to blit onto the screen
    if dt <= 3:
        banner = score_font.render("TBLABLABONG", True, pong.white)
        banner_rect = banner.get_rect(center=screen_rect.center)
        screen.blit(banner, banner_rect)
        pygame.display.flip()
        continue
    else:
        score_surface_l = score_font.render(left_score, True, pong.white)
        screen.blit(score_surface_l, score_region_l)
        score_surface_r = score_font.render(right_score, True, pong.white)
        screen.blit(score_surface_r, score_region_r)

    pygame.draw.rect(screen, pong.white, dividing_line)

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

    paddles.update()
    pygame.display.flip()
