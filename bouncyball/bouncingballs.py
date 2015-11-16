import sys, pygame
import pygame.key
import pygame.draw
import os

# Allow keys to be pressed and held.
#
# Require 1/3 of a second before we consider a key to be 'held down',
# and then every 1/10 seconds after, emit another key-press event

accel_key = pygame.K_w
slow_key = pygame.K_s


import time
pygame.init()
pygame.key.set_repeat(300, 100)



size = width, height = 720, 450
base_speed = [3.14159, 2]
black = 255, 0, 255
os.environ["SDL_VIDEO_CENTERED"] = "TRUE"

screen = pygame.display.set_mode(size)
ball = pygame.image.load("ball.gif")
ballrect = ball.get_rect()

abox = pygame.draw.rect(screen, (100, 0, 100), (100,100,100,100))
print abox.center
print dir(abox)
res = screen.blit(screen, abox)
speed = base_speed
accel = 0
screen.fill(black)
pygame.display.flip()


while 1:
    abox.move(33,33)
    print abox.center
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    try:
        _pushers = pygame.key.get_pressed()
        i = _pushers.index(1)

        if i == pygame.K_w:
            print "You wanna go up: (%s)" % i
            print pygame.key.name(i)
            accel += 0.5
        elif i == pygame.K_s:
            print "You wanna go down: (%s)" % i
            print pygame.key.name(i)
            accel += -0.5
        else:
            pass
    except:
        pass

    print ballrect.center
    _speed = (speed[0] + accel, speed[1] + accel)
    ballrect = ballrect.move(_speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
        if speed[0] < 0:
            accel = accel * -1
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
        if speed[1] < 0:
            accel = accel * -1


    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    time.sleep(0.02)
