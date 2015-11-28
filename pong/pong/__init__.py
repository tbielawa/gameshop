import logging
import math
import pygame.draw
import pygame.font
import pygame.rect
import pygame.sprite

BUNDLED_FONT = "assets/ArcadeClassic.ttf"
pygame.font.init()

WALL_TOP = 0
WALL_RIGHT = 1
WALL_BOTTOM = 2
WALL_LEFT = 3

######################################################################
black = (000, 000, 000)
white = (255, 255, 255)
red = (255, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
######################################################################


def score_digitize(score):
    # Returns a left-padded string if the score is only a single digit
    if len(str(score)) == 1:
        return " {}".format(str(score))
    else:
        return str(score)


######################################################################
class PongPaddle(pygame.sprite.Sprite):
    velocity = 15
    pos = (0, 0)
    up = None
    down = None

    def __init__(self, h_walls=None):
        """Initialize a pong paddle. Don't forget the walls
        """
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.log = logging.getLogger('pong')

        self.surface = pygame.display.get_surface()
        self.image = pygame.image.load('assets/paddle.png')

        self.h_walls = h_walls

        # Initial position setting
        self.rect = self.image.get_rect(center=self.pos)

    def hit_border(self, dy):
        """Calculate using our dy (change in up/down) if we hit a
ceiling/floor.

If we are *already* in collission with something, allow movement away
from the object. Do not allow movement further into the object.

Return data:

* ``True`` if we need to shut this shit down (we hit something)
* ``False`` if we may continue moving
        """
        # Remember the current position
        initial_pos = self.rect.copy()
        # Temporarily move us to the next position
        self.rect.move_ip(0, dy)
        # Check if we would hit anything once moved
        h_collide = pygame.sprite.spritecollide(self, self.h_walls, False)
        # Reset our position to the initial position
        self.rect = initial_pos
        # Return True if we would hit something, else: False
        if h_collide:
            return True
        else:
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
            dy = -self.velocity
        elif kb_input[self.down] == 1:
            dy = self.velocity

        if not self.hit_border(dy):
            self.rect.move_ip(0, dy)
        else:
            pass
        self.surface.blit(self.image, self.rect)


class PongPaddleLeft(PongPaddle):
    pos = (78, 360)
    up = pygame.K_w
    down = pygame.K_s


class PongPaddleRight(PongPaddle):
    pos = (1202, 360)
    up = pygame.K_UP
    down = pygame.K_DOWN


######################################################################
class PongBall(pygame.sprite.Sprite):
    def __init__(self, paddles=None, velocity=10, angle=0.0, h_walls=None, v_walls=None):
        self.log = logging.getLogger('pong')
        self.surface = pygame.display.get_surface()
        self.surface_rect = self.surface.get_rect()
        self.h_walls = h_walls
        self.v_walls = v_walls
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
        """Check if the ball has struck a boundary. Returns:

* `None` - if no wall was hit
* impact - int - a constant the ``pong`` module's
  ``WALL_(TOP|BOTTOM|LEFT|RIGHT)`` list
        """
        # Was it a wall or ceiling?
        h_collide = pygame.sprite.spritecollide(self, self.h_walls, False)

        # Was it the left or right score zone?
        v_collide = pygame.sprite.spritecollide(self, self.v_walls, False)

        if h_collide:
            return h_collide[0].wall_type
        elif v_collide:
            return v_collide[0].wall_type
        else:
            return None

    def update(self):
        """Calculate the next ball position and account for wall/paddle
collisions. Returns:

 * `False` - When no other boundary or object was hit
 * An int from the ``pong`` module's constants: ``WALL_(LEFT|RIGHT)``
   indicating a score has landed and the side which was struck
        """
        next_x = self.velocity * math.cos(math.radians(self.angle))
        next_y = self.velocity * math.sin(math.radians(self.angle))
        paddle = self.hit_paddle()
        boundary = self.hit_boundary()

        # Our "collission free movement" case has been calculated in
        # the block above. Now we need to see if we are hitting
        # anything and how we need to adjust our path of movement

        if paddle:
            # TODO: Refactor to handle the ball impacting different
            # positions on a paddle
            next_x = -1 * (self.velocity * math.cos(math.radians(self.angle)))
        elif boundary is not None:
            # Left or right wall = A PLAYER HAS SCORED
            if boundary in [WALL_LEFT, WALL_RIGHT]:
                self.log.debug("wall: {}".format(boundary))
                return boundary
            # Not a score zone, just a reflection about the x axis to
            # flip the y component trajectory
            else:
                next_y = -1 * (self.velocity * math.sin(math.radians(self.angle)))

        self.angle = math.degrees(math.atan2(next_y, next_x))
        self.rect.move_ip(next_x, next_y)
        self.surface.blit(self.image, self.rect)
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
    pos = (0, 0)

    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.display.get_surface()
        self.score = 0
        self.score_font = pygame.font.Font(BUNDLED_FONT, 64)
        self.image = self.score_font.render(score_digitize(self.score), True, white)
        self.rect = self.image.get_rect(topleft=self.pos)

    def scored(self):
        """Increment the score for this side"""
        self.score += 1

    def update(self):
        _score = self.score_font.render(score_digitize(self.score), True, white)
        self.surface.blit(_score, self.rect)


class PongScoreLeft(PongScore):
    pos = (282, 44)


class PongScoreRight(PongScore):
    pos = (922, 44)


class AnnoyingSplashScreen(pygame.sprite.Sprite):
    """A classic annoying splash screen you are unable to bypass"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.display.get_surface()

        splash_font = pygame.font.Font(BUNDLED_FONT, 64)
        instruct_font = pygame.font.Font(BUNDLED_FONT, 24)
        skip_font = pygame.font.Font(BUNDLED_FONT, 18)

        # Title
        self.banner = splash_font.render("TBLABLABONG", True, white)
        self.banner_rect = self.banner.get_rect(center=self.surface.get_rect().center)

        # Instructions
        self.instructions = instruct_font.render("[w] up;  [s] down;  [f]  full screen;  [esc] quit", True, white)
        instructions_midtop = self.banner_rect.midbottom
        self.instructions_rect = self.instructions.get_rect(midtop=(instructions_midtop[0], instructions_midtop[1] + 24))

        # Skip msg
        self.skip_msg = skip_font.render("press a key at any time to skip this screen", True, white)
        screen_midbottom = self.surface.get_rect().midbottom
        self.skip_rect = self.skip_msg.get_rect(midbottom=screen_midbottom)
        self.skip_rect.move_ip(0, -self.skip_rect.height)

    def update(self):
        self.surface.blit(self.banner, self.banner_rect)
        self.surface.blit(self.instructions, self.instructions_rect)
        self.surface.blit(self.skip_msg, self.skip_rect)


class CourtDividingLine(pygame.sprite.Sprite):
    """A simple vertical line through the middle of the screen"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.log = logging.getLogger('pong')
        self.surface = pygame.display.get_surface()
        self.surface_rect = self.surface.get_rect()
        self.image = pygame.image.load('assets/dividing_line.png')
        self.rect = self.image.get_rect(center=self.surface_rect.center)
        self.top = self.rect.top
        self.log.info("Dividing line top at: %s" % self.top)

    def update(self):
        self.surface.blit(self.image, self.rect)


class CourtSkirt(pygame.sprite.Sprite):
    """"Skirt" because it's on the bottom and it hides only a little bit
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1280, 44))
        self.image.fill(black)
        self.rect = self.image.get_rect(topleft=(0, 676))
        self.surface = pygame.display.get_surface()

    def update(self):
        self.surface.blit(self.image, self.rect)


class DebugPanel(pygame.sprite.Sprite):
    """A simple panel for debug information"""

    def __init__(self, show_debug):
        pygame.sprite.Sprite.__init__(self)
        self.show_debug = show_debug
        self.surface = pygame.display.get_surface()
        self.debug_font = pygame.font.Font(BUNDLED_FONT, 14)
        self.image = self.debug_font.render("FPS: 32", True, red)
        self.rect = self.image.get_rect(center=self.surface.get_rect().center)

    def update(self, debug_str):
        """Update the debug panel with new information. You must pre-format
the debug string yourself. New lines are not acceptable!

* ``debug_str`` - The string to print in the debug panel

        """
        if self.show_debug:
            self.image = self.debug_font.render(debug_str, True, red)
            self.rect = self.image.get_rect(x=5, y=self.surface.get_rect().height - 30)
            self.surface.blit(self.image, self.rect)
        else:
            return


class Wall(pygame.sprite.Sprite):
    """Just a ball to bounce off of, or to score on"""
    def __init__(self, area, wall_type):
        # * `area` - A rect representing the area covered by this wall
        # * `wall_type` - a constant from the ``pong`` module in WALL_(LEFT|RIGHT|TOP|BOTTOM)
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.display.get_surface()
        self.wall_type = wall_type
        self.rect = area
        self.image = pygame.Surface(self.rect.size)

    def update(self):
        pass
