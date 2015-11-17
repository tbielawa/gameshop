#!/usr/bin/env python
import math
import random
# import sys
# http://www.pygame.org/docs/ref/pygame.html
import pygame
#
import pygame.event
#
import pygame.key
# http://www.pygame.org/docs/ref/draw.html
import pygame.draw
# http://www.pygame.org/docs/ref/time.html
import pygame.time

import os
import sys
os.environ["SDL_VIDEO_CENTERED"] = "TRUE"


######################################################################
# CONSTANTLY CONSTANT STUFF
PADDLE_LEFT = -1
PADDLE_RIGHT = 1


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
# Some funcs

# Alias math.radians() to just 'rads'
rads = math.radians
degs = math.degrees


# Is this a wall?
def is_wall(rect):
    # Is the height greater than the width?
    return rect.h > rect.w


######################################################################
class PongPaddle(pygame.sprite.Sprite):
    HEIGHT = 64
    WIDTH = 16
    # White
    # COLOR = (255, 255, 255)
    # red
    COLOR = (255, 0, 0)
    VELOCITY = 6

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, side, walls, surface):
        """Initialize a pong paddle. The ``side`` parameter is one of
``PADDLE_LEFT`` or ``PADDLE_RIGHT``
        """
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.surface = surface

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([self.WIDTH, self.HEIGHT])
        self.image.fill(self.COLOR)

        # Store our bounding walls and our paddle side
        self.side = side
        self.walls = walls

        # Paddles are left/right specific. Each paddle responds to a
        # different set of keyboard input codes.
        if self.side == PADDLE_LEFT:
            self.up = pygame.K_w
            self.down = pygame.K_s
        elif self.side == PADDLE_RIGHT:
            self.up = pygame.K_UP
            self.down = pygame.K_DOWN

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self._init_pos()

    def _init_pos(self):
        ######################################################################
        # Calculate initial positions for the paddles. Each init pos
        # is based off of the closest wall (vertical boundary rect)
        if self.side == PADDLE_LEFT:
            self.rect.center = self.walls[3].midright
            self.rect.move_ip(8*3, 0)
        elif self.side == PADDLE_RIGHT:
            self.rect.center = self.walls[1].midleft
            self.rect.move_ip(-8*3, 0)

    def hit_border(self, dy):
        """Calculate using our dy (change in up/down) if we hit a
ceiling/floor.

If we are *already* in collission with something, allow movement away
from the object. Do not allow movement further into the object.

Return data:

* ``True`` if we need to shut this shit down (we hit something)
* ``False`` if we may continue moving
        """
        # Just how far up and down we do want to allow the paddle to
        # go? I suppose we'd want to allow up to the bottom edge of
        # the top floor and the top edge of the bottom floor.

        # hitting the top floor. Then our rect.top (coordinate?) will
        # intersect with self.walls[0]
        #
        # hitting the bottom floor. Then out rect.bottom (coordinate?)
        # will intersect with self.walls[2]
        next_pos = self.rect.move(0, dy)
        hit_point = next_pos.collidelist(self.walls)

        # OK. We know if this was a floor/ceiling:
        # 0 and 2 are the top border and bottom border
        if hit_point in [0, 2]:
            return True
        return False

    def update(self):
        # Valid movement paths for paddles:
        #
        # rect.topleft going up until hitting a ceiling (wall[0])
        # rect.bottomleft going down until hitting a floor (wall[2])
        # No horizontal movement
        kb_input = pygame.key.get_pressed()
        dy = 0
        if kb_input[self.up] == 1:
            dy = -self.VELOCITY
        elif kb_input[self.down] == 1:
            dy = self.VELOCITY

        if not self.hit_border(dy):
            self.rect.move_ip(0, dy)
        else:
            pass

        self.surface.blit(self.image, self.rect)


######################################################################
class PongBall(object):
    white = (255, 255, 255)

    def __init__(self, surface, walls, paddles, velocity=5, angle=0.0, color=(255, 255, 255)):
        self.surface = surface
        # A dict of walls
        self.walls = walls
        self.paddles = paddles
        self.velocity = velocity
        self.angle = angle
        self.color = color
        self.center = self.surface.get_rect().center
        self.width = 16
        self.height = 16
        self.rect = pygame.Rect(self.center, (self.width, self.height))

    def hit_paddle(self):
        for paddle in self.paddles.sprites():
            if paddle.rect.colliderect(self.rect):
                return paddle
        return False

    def hit_boundary(self):
        # Check if the ball has struck a boundary
        impact = self.rect.collidelist(self.walls)
        if impact != -1:
            return impact
        else:
            return None

    def update(self):
        next_x = self.velocity * math.cos(rads(self.angle))
        next_y = self.velocity * math.sin(rads(self.angle))
        paddle = self.hit_paddle()
        boundary = self.hit_boundary()

        if paddle:
            # Hit a paddle, it's a wall shape by design
            next_x = -1 * (self.velocity * math.cos(rads(self.angle)))
        elif boundary is not None:
            # We hit a boundary, the boundary object is a Rect
            #
            # Is it vertical (a wall?), or horizontal (a floor/ceil)?
            if is_wall(self.walls[boundary]):
                next_x = -1 * (self.velocity * math.cos(rads(self.angle)))
            else:
                next_y = -1 * (self.velocity * math.sin(rads(self.angle)))

        self.angle = math.degrees(math.atan2(next_y, next_x))

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
screen_top = pygame.Rect(court_rect.topleft, (court_rect.w, 2))
screen_right = pygame.Rect(court_rect.topright, (2, court_rect.h + 2))
screen_bottom = pygame.Rect(court_rect.bottomleft, (court_rect.w, 2))
screen_left = pygame.Rect(court_rect.topleft, (2, court_rect.h))
wall_names = ["top", "right", "bottom", "left"]
wall_list = [screen_top, screen_right, screen_bottom, screen_left]

######################################################################
pygame.init()
screen = pygame.display.set_mode(screen_dim)
pygame.display.set_caption("Pongu")
clock = pygame.time.Clock()

######################################################################
# The pong ball
angle = random.randrange(0, 360)
paddles = pygame.sprite.Group()
paddles.add(PongPaddle(PADDLE_LEFT, wall_list, screen))
paddles.add(PongPaddle(PADDLE_RIGHT, wall_list, screen))
ball = PongBall(screen, wall_list, paddles, angle=float(angle))

while 1:
    for event in pygame.event.get():
        # Enable the 'close window' button
        if event.type == pygame.QUIT:
            sys.exit()
    kb_input = pygame.key.get_pressed()

    if kb_input[pygame.K_ESCAPE] == 1:
        sys.exit()

    clock.tick(30)
    screen.fill(white)
    # This is the court, it's black
    court_area = pygame.draw.rect(screen, black, court_rect)
    pygame.draw.rect(screen, white, screen_right)
    pygame.draw.rect(screen, white, screen_left)
    pygame.draw.rect(screen, white, screen_bottom)
    pygame.draw.rect(screen, white, screen_top)
    ball.update()
    paddles.update()
    pygame.display.flip()
