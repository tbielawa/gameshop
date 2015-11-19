import pygame.rect
import pygame.draw
import math

# Is this a wall?
def is_wall(rect):
    # Is the height greater than the width?
    return rect.h > rect.w


class Player(object):
    pass

######################################################################
class PongBall(object):
    white = (255, 255, 255)

    def __init__(self, surface, walls, paddles, velocity=8, angle=0.0, color=(255, 255, 255)):
        self.surface = surface
        # A dict of walls
        self.walls = walls
        self.paddles = paddles
        self.velocity = velocity
        self.angle = angle
        self.color = color
        self.center = self.surface.get_rect().center
        self.width = 10
        self.height = 10
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
        next_x = self.velocity * math.cos(math.radians(self.angle))
        next_y = self.velocity * math.sin(math.radians(self.angle))
        paddle = self.hit_paddle()
        boundary = self.hit_boundary()

        if paddle:
            # Hit a paddle, it's a wall shape by design
            next_x = -1 * (self.velocity * math.cos(math.radians(self.angle)))
        elif boundary is not None:
            # We hit a boundary, the boundary object is a Rect
            #
            # Is it vertical (a wall?), or horizontal (a floor/ceil)?
            if is_wall(self.walls[boundary]):
                next_x = -1 * (self.velocity * math.cos(math.radians(self.angle)))
            else:
                next_y = -1 * (self.velocity * math.sin(math.radians(self.angle)))

        self.angle = math.degrees(math.atan2(next_y, next_x))

        self.rect.move_ip(next_x, next_y)
        pygame.draw.rect(self.surface, self.color, self.rect)
