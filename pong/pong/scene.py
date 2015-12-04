# mode: -*- python -*-
import pygame
import pong
import sys
import time

class Scene(object):
    """A self-contained sequence of animation. Everything you need to know
to update a display is provided in the instance variable 'self.env'.

You must fill in the ``setup`` method. This method will be called
automatically once the class is initialized.

You must fill in the ``update`` method. This method will be called
    """
    def __init__(self, env, active=False):
        self.env = env
        self.active = active
        self.setup()

    def run(self):
        """Starts a scene, if it's active"""
        # kb_input = pygame.key.get_pressed()

        # if kb_input[pygame.K_ESCAPE] == 1:
        #     sys.exit()

        # if kb_input[pygame.K_f] == 1:
        #     pygame.display.toggle_fullscreen()

        if self.active:
            self.pre_run()
            result = self.update()
            self.post_run()
            return result

    def pre_run(self):
        self.env['clock'].tick(45)

    def post_run(self):
        pygame.display.flip()

    ######################################################################
    # Fill these in when you subclass this class
    ######################################################################
    def setup(self):
        """The stuff we need to do to prepare a scene"""
        raise NotImplementedError("A 'setup' method must be filled in")

    def update(self):
        raise NotImplementedError("An 'update' method must be filled in")

class AnnoyingSplashScreenScene(Scene):
    """The annoying splash screen with a logo and some instructions.
Displayed for a brief amount of time."""
    def setup(self):
        """Set up the scene with the basic objects we need to render.

* create the splash screen sprite

* initialize a timer set to a None value. Later on in our update we'll
check the timer to see if it needs to be initialized. Following that
we'll check it to see if enough time has elapsed for us to stop
displaying.
        """
        self.start_time = None
        self.splash = pong.AnnoyingSplashScreen()
        self.display_time = 4

    def update(self):
        if self.start_time is None:
            self.start_time = time.time()
        else:
            if time.time() - self.start_time > self.display_time:
                self.active = False
                self.start_time = None
                return

        self.splash.update()
