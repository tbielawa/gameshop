#!/usr/bin/env python
import math

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

######################################################################
court_margin = 8
court_width = 624
court_height = 464
court_rect = pygame.Rect(8, 8, court_width, court_height)

######################################################################
# Alias math.radians() to just 'rads'
rads = math.radians

######################################################################
class PongBall(object):
    white = (255, 255, 255)

    def __init__(self, surface, velocity=5, angle=0, color=(255, 255, 255)):
        self.surface = surface
        self.velocity = velocity
        self.angle = angle
        self.color = color
        self.center = self.surface.get_rect().center
        self.width = 16
        self.height = 16
        self.rect = pygame.Rect(self.center, (self.width, self.height))

    def update(self):
        cur_x, cur_y = self.center
        next_x = self.velocity * math.cos(rads(self.angle))
        next_y = self.velocity * math.sin(rads(self.angle))
        self.rect.move_ip(next_x, next_y)
        pygame.draw.rect(self.surface, white, self.rect)

######################################################################
screen_w = court_width + (court_margin * 2)
screen_h = court_height + (court_margin * 2)
screen_dim = (screen_w, screen_h)

######################################################################
black = (000, 000, 000)
white = (255, 255, 255)
red = (255, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

######################################################################
# The screen borders
#     Rect(left, top, width, height) -> Rect
screen_top    = pygame.Rect(court_rect.topleft, (court_rect.w, 2))
screen_right  = pygame.Rect(court_rect.topright, (2, court_rect.h+2))
screen_bottom = pygame.Rect(court_rect.bottomleft, (court_rect.w, 2))
screen_left   = pygame.Rect(court_rect.topleft, (2, court_rect.h))
walls = [screen_top, screen_bottom, screen_right, screen_left]

######################################################################
pygame.init()
screen = pygame.display.set_mode(screen_dim)
pygame.display.set_caption("Pongu")
clock = pygame.time.Clock()

######################################################################
# DRAW THESE
ball = PongBall(screen, angle=0)


while 1:
    clock.tick(30)
    screen.fill(blue)
    # This is the court, it's black
    court_area = pygame.draw.rect(screen, black, court_rect)
    pygame.draw.rect(screen, green, screen_right)
    pygame.draw.rect(screen, green, screen_left)
    b = pygame.draw.rect(screen, green, screen_bottom)
    t = pygame.draw.rect(screen, green, screen_top)
    ball.update()

    pygame.display.flip()


if __name__ == '__main__':
    update()
