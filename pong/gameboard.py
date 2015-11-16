#!/usr/bin/env python

import sys
# http://www.pygame.org/docs/ref/pygame.html
import pygame
# http://www.pygame.org/docs/ref/draw.html
import pygame.draw
# http://www.pygame.org/docs/ref/time.html
import pygame.time

# Reference stuff
# http://www.pygame.org/docs/ref/rect.html
# http://www.pygame.org/docs/ref/surface.html
# http://www.pygame.org/docs/ref/sprite.html
# http://www.pygame.org/docs/ref/font.html


court_margin = 8
court_border = 8
court_width = 624
court_height = 464

screen_w = (court_margin * 2) + (court_border * 2) + (court_width)
screen_h = (court_margin * 2) + (court_border * 2) + (court_height)
screen_dim = (screen_w, screen_h)

pygame.init()

screen = pygame.display.set_mode(screen_dim)
black = (000, 000, 000)
clock = pygame.time.Clock()
while 1:
    clock.tick(30)
    screen.fill(black)
    pygame.display.flip()


if __name__ == '__main__':
    update()
