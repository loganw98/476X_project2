#!/usr/bin/env python

# Display a rectangle
# Guang Song

import random, math, pygame
from pygame.locals import *
from array import *
from math import sin, cos, pi

#constants
WINSIZE = [640, 480]
SIZE = 360
cObstacles = [[0 for i in range(SIZE)] for i in range(SIZE)]

class Rectangle:
    def __init__(x, y, width, height, theta):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.theta = theta
        self.v0 = (width * cos(theta), width * sin(theta))
        self.v1 = (height/2 * cos(theta + pi/2), height/2 * sin(theta+pi/2))
        self.LL = (x+v1[0],y+v1[1])
        self.UL = (x-v1[0],y-v1[1])
        self.UR = (x-v1[0]+v0[0],y-v1[1]+v0[1])
        self.LR = (x+v1[0]+v0[0],y+v1[1]+v0[1])

def calcAxi(r1, r2):
    axis1 = (r1.UR[0] - r1.UL[0], r1.UR[1] - r1.UL[1])
    axis2 = (r1.UR[0] - r1.LR[0], r1.UR[1] - r1.LR[1])
    axis3 = (r2.UL[0] - r2.LL[0], r2.UL[1] - r2.LL[1])
    axis4 = (r2.UL[0] - r2.UR[0], r2.UL[1] - r2.UR[1])
    return [axis1, axis2, axis3, axis4]

#projection onto above axi next

def drawLink(x, y, width, height, theta, screen, color):
    points = [] # start with an empty list
    v0 = (width * cos(theta), width * sin(theta))
    v1 = (height/2 * cos(theta + pi/2), height/2 * sin(theta+pi/2))
    points.append((x+v1[0],y+v1[1]))
    points.append((x-v1[0],y-v1[1]))
    points.append((x-v1[0]+v0[0],y-v1[1]+v0[1]))
    points.append((x+v1[0]+v0[0],y+v1[1]+v0[1]))
    points.append((x+v1[0],y+v1[1]))
    lineThickness = 2
    pygame.draw.lines(screen, color, False, points, lineThickness)
    pygame.display.update()
    return x+v0[0], y+v0[1]

def draw2Links(x, y, width, height, theta, screen, color):
    for t in theta:
        x, y = drawLink(x, y, width, height, t, screen, color)
    


def main():
    #initialize and prepare screen
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('Linked Chains with Obstacles: G. Song, 2019s')
    white = 255, 240, 200
    black = 20, 20, 40
    RED =   (255,   0,   0)
    screen.fill(black)

    centerx = 320
    centery = 240
    
    theta = 0
    while theta <= 4.*pi:
        t2 = (theta, theta+theta*0.5)
        screen.fill(black)
        draw2Links(centerx,centery, 100, 20, t2, screen, white);
        # draw obstacles
        pygame.draw.rect(screen, RED, [centerx, centery-125, 20, 20])
        pygame.draw.rect(screen, RED, [centerx, centery+125, 20, 20])
        pygame.display.update()
        pygame.time.wait(5)
        theta = theta + (pi/180)
   
    done = 0
    while not done:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
              print("\nLeaving because you said so\n")
              done = 1
              break
	

# if python says run, then we should run
if __name__ == '__main__':
    main()



