#!/usr/bin/env python

import sys
# http://www.pygame.org/docs/ref/pygame.html
import pygame
# http://www.pygame.org/docs/ref/draw.html
import pygame.draw
# http://www.pygame.org/docs/ref/time.html
import pygame.time

import os
os.environ["SDL_VIDEO_CENTERED"] = "TRUE"

# Reference stuff
# http://www.pygame.org/docs/ref/rect.html
# http://www.pygame.org/docs/ref/surface.html
# http://www.pygame.org/docs/ref/sprite.html
# http://www.pygame.org/docs/ref/font.html


court_margin = 8
court_width = 624
court_height = 464
court_rect = pygame.Rect(8, 8, court_width, court_height)

ball = pygame.Rect(0, 0, 16, 16)
paddle = pygame.Rect(0, 0, 64, 16)

screen_w = court_width + (court_margin * 2)
screen_h = court_height + (court_margin * 2)
screen_dim = (screen_w, screen_h)
black = (000, 000, 000)
white = (255, 255, 255)

# COLORS, BRO
red = (255, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


# the screen borders
#     Rect(left, top, width, height) -> Rect
screen_top    = pygame.Rect(court_rect.topleft, (court_rect.w, 2))
screen_right  = pygame.Rect(court_rect.topright, (2, court_rect.h+2))
screen_bottom = pygame.Rect(court_rect.bottomleft, (court_rect.w, 2))
screen_left   = pygame.Rect(court_rect.topleft, (2, court_rect.h))

pygame.init()
screen = pygame.display.set_mode(screen_dim)
pygame.display.set_caption("Pongu")
clock = pygame.time.Clock()

######################################################################

while 1:
    clock.tick(30)
    screen.fill(blue)
    # This is the court, it's black
    court_area = pygame.draw.rect(screen, black, court_rect)
    pygame.draw.rect(screen, green, screen_right)
    pygame.draw.rect(screen, green, screen_left)
    b = pygame.draw.rect(screen, green, screen_bottom)
    t = pygame.draw.rect(screen, green, screen_top)

    pygame.display.flip()


if __name__ == '__main__':
    update()
