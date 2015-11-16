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
court_border = 8
court_width = 624
court_height = 464
court_rect = pygame.Rect(court_margin * 2, court_margin * 2, court_width, court_height)

screen_w = (court_margin * 2) + (court_border * 2) + (court_width)
screen_h = (court_margin * 2) + (court_border * 2) + (court_height)
screen_dim = (screen_w, screen_h)
black = (000, 000, 000)

pygame.init()
screen = pygame.display.set_mode(screen_dim)
clock = pygame.time.Clock()

######################################################################

while 1:
    clock.tick(30)
    screen.fill(black)
    pygame.draw.rect(screen, (255,255,255), court_rect, court_border)
    pygame.display.flip()


if __name__ == '__main__':
    update()
