#!/usr/bin/env python
import math
import random
# import sys
# http://www.pygame.org/docs/ref/pygame.html
import pygame
#
import pygame.font
#
import pygame.event
#
import pygame.image
#
import pygame.key
# http://www.pygame.org/docs/ref/draw.html
import pygame.draw
# http://www.pygame.org/docs/ref/time.html
import pygame.time

import pong

import os
import sys
######################################################################
os.environ["SDL_VIDEO_CENTERED"] = "TRUE"
DISPLAY_ICON = "assets/icon.png"
DEFAULT_FONT = "sourcecodepro"
SCORE_FONT = DEFAULT_FONT
######################################################################
black = (000, 000, 000)
white = (255, 255, 255)
red = (255, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
######################################################################
court_margin = 8
court_width = 624
court_height = 464
court_rect = pygame.Rect(8, 8, court_width, court_height)

screen_w = court_width + (court_margin * 2)
screen_h = court_height + (court_margin * 2)
screen_dim = (screen_w, screen_h)

screen_top = pygame.Rect(court_rect.topleft, (court_rect.w, 2))
screen_right = pygame.Rect(court_rect.topright, (2, court_rect.h + 2))
screen_bottom = pygame.Rect(court_rect.bottomleft, (court_rect.w, 2))
screen_left = pygame.Rect(court_rect.topleft, (2, court_rect.h))
wall_names = ["top", "right", "bottom", "left"]
wall_list = [screen_top, screen_right, screen_bottom, screen_left]
######################################################################
pygame.init()
screen = pygame.display.set_mode(screen_dim)
icon = pygame.image.load(DISPLAY_ICON)
pygame.display.set_icon(icon)
pygame.display.set_caption("Pongu")
clock = pygame.time.Clock()
######################################################################
# Fonts
pygame.font.init()
fonts = pygame.font.get_fonts()
if DEFAULT_FONT not in fonts:
    DEFAULT_FONT = pygame.font.get_default_font()

score_font = pygame.font.SysFont(SCORE_FONT, 64)
# A test string so we can get some data positioning for later
score_size = score_font.render("10", True, white).get_size()
score_width = score_size[0]
score_height = score_size[1]
######################################################################
screen_rect = screen.get_rect()
s_rect_w = screen_rect.width
s_rect_h = screen_rect.height

score_width = 76


# centerx is the horizontal mid-point of the rectangle
# centery is the vertical mid-point of the rectangle
dividing_line = pygame.Rect(court_rect.centerx,
                            court_rect.top + 2,
                            8,
                            court_rect.height - 2)

score_region_l = pygame.Rect(dividing_line.left - score_width - 16,
                             dividing_line.top,
                             score_width,
                             score_height)
score_region_r = pygame.Rect(dividing_line.right + 16,
                             dividing_line.top,
                             score_width,
                             score_height)


while 1:
    for event in pygame.event.get():
        # Enable the 'close window' button
        if event.type == pygame.QUIT:
            sys.exit()
    kb_input = pygame.key.get_pressed()

    if kb_input[pygame.K_ESCAPE] == 1 or kb_input[pygame.K_q] == 1:
        sys.exit()

    if kb_input[pygame.K_f] == 1:
        pygame.display.toggle_fullscreen()

    ##################################################################
    clock.tick(30)
    screen.fill(white)
    court_area = pygame.draw.rect(screen, black, court_rect)
    pygame.draw.rect(screen, white, screen_right)
    pygame.draw.rect(screen, white, screen_left)
    pygame.draw.rect(screen, white, screen_bottom)
    pygame.draw.rect(screen, white, screen_top)
    ##################################################################
    # Font stuff, first, the white background
    pygame.draw.rect(screen, white, dividing_line)

    left_score = pong.score_digitize(10)
    right_score = pong.score_digitize(10)

    # # Create a surface (score) to blit onto the screen
    score_surface_l = score_font.render(left_score, True, white)
    screen.blit(score_surface_l, score_region_l)
    score_surface_r = score_font.render(right_score, True, white)
    screen.blit(score_surface_r, score_region_r)

    ##################################################################
    pygame.display.flip()
