import logging
import math
import pygame.draw
import pygame.font
import pygame.rect
import pygame.sprite

PADDLE_LEFT = -1
PADDLE_RIGHT = 1
DEFAULT_FONT = "sourcecodepro"
SCORE_FONT = DEFAULT_FONT
# BUNDLED_FONT = "assets/Quantifier.ttf"
BUNDLED_FONT = "assets/ArcadeClassic.ttf"

######################################################################
black = (000, 000, 000)
white = (255, 255, 255)
red = (255, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
######################################################################


# Is this a wall?
def is_wall(rect):
    # Is the height greater than the width?
    return rect.h > rect.w


def score_digitize(score):
    # Returns a left-padded string if the score is only a single digit
    if len(str(score)) == 1:
        return " {}".format(str(score))
    else:
        return str(score)


######################################################################
class PongPaddle(pygame.sprite.Sprite):
    HEIGHT = 64
    WIDTH = 16
    # White
    COLOR = (255, 255, 255)
    # red
    # COLOR = (255, 0, 0)
    VELOCITY = 15

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, side, walls, surface):
        """Initialize a pong paddle. The ``side`` parameter is one of
``PADDLE_LEFT`` or ``PADDLE_RIGHT``
        """
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.log = logging.getLogger('pong')

        self.surface = surface

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        # self.image = pygame.Surface([self.WIDTH, self.HEIGHT])
        # self.image.fill(self.COLOR)
        self.image = pygame.image.load('assets/paddle.png')

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
            self.rect.move_ip(8 * 3, 0)
        elif self.side == PADDLE_RIGHT:
            self.rect.center = self.walls[1].midleft
            self.rect.move_ip(-8 * 3, 0)

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
class PongBall(pygame.sprite.Sprite):
    def __init__(self, walls, paddles, velocity=10, angle=0.0):
        self.log = logging.getLogger('pong')
        self.surface = pygame.display.get_surface()
        self.surface_rect = self.surface.get_rect()
        self.walls = walls
        self.paddles = paddles
        self.velocity = velocity
        self.angle = angle
        self.width = 10
        self.height = 10
        self.rect = self.surface_rect.inflate(-1 * (self.surface_rect.width - self.width), -1 * (self.surface_rect.height - self.height))
        self.image = pygame.image.load('assets/ball.png')

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
                # next_x = -1 * (self.velocity * math.cos(math.radians(self.angle)))
                self.log.debug("boundary: {}".format(boundary))
                return boundary
            else:
                next_y = -1 * (self.velocity * math.sin(math.radians(self.angle)))

        self.angle = math.degrees(math.atan2(next_y, next_x))
        self.rect.move_ip(next_x, next_y)
        self.surface.blit(self.image, self.rect)
        # pygame.draw.rect(self.surface, self.color, self.rect)
        return False


class PongScore(pygame.sprite.Sprite):
    """The basic Sprite class can draw the Sprites it contains to a
Surface. The 'Group.draw - blit the Sprite images' method requires:

* that each Sprite have a Surface.image attribute
* a Surface.rect.

The Group.clear - draw a background over the Sprites method requires
these same attributes, and can be used to erase all the Sprites with
background.
    """
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.score = 0


class AnnoyingSplashScreen(pygame.sprite.Sprite):
    """A classic annoying splash screen you are unable to bypass"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        splash_font = pygame.font.Font(BUNDLED_FONT, 64)
        instruct_font = pygame.font.Font(BUNDLED_FONT, 24)

        # Title
        self.banner = splash_font.render("TBLABLABONG", True, white)
        self.banner_rect = self.banner.get_rect(center=pygame.display.get_surface().get_rect().center)

        # Instructions
        self.instructions = instruct_font.render("[w] up;  [s] down;  [f]  full screen;  [q] quit", True, white)
        instructions_midtop = self.banner_rect.midbottom
        self.instructions_rect = self.instructions.get_rect(midtop=(instructions_midtop[0], instructions_midtop[1] + 24))

    def update(self):
        surface = pygame.display.get_surface()
        surface.blit(self.banner, self.banner_rect)
        surface.blit(self.instructions, self.instructions_rect)


class CourtDividingLine(pygame.sprite.Sprite):
    """A simple vertical line through the middle of the screen"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.log = logging.getLogger('pong')
        self.surface = pygame.display.get_surface()
        self.surface_rect = self.surface.get_rect()
        # self.image = pygame.surface.Surface([6, self.surface_rect.height])
        # self.image.fill(white)
        self.image = pygame.image.load('assets/dividing_line.png')
        self.rect = self.image.get_rect(center=self.surface_rect.center)
        self.top = self.rect.top
        self.log.info("Dividing line top at: %s" % self.top)

    def update(self):
        self.surface.blit(self.image, self.rect)
