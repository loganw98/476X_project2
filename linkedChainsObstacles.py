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
    

#working on this
def isCloseToObstacle(r1):
    ob1x = 320
    ob2x = 320
    ob1y = 240-125
    ob2y = 240+125

def distance(x1, x2, y1, y2):
    return math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))

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
        #draw2Links(centerx,centery, 100, 20, t2, screen, white);
        x, y = drawLink(centerx,centery, 100, 20, 180*(pi/180), screen, white);
        drawLink(x,y, 100, 20, 270*(pi/180), screen, white);
        # draw obstacles
        #pygame.draw.rect(screen, RED, [centerx, centery, 10, 10])
        pygame.draw.rect(screen, RED, [centerx, centery-125, 20, 20])
        pygame.draw.rect(screen, RED, [centerx, centery+125, 20, 20])
        pygame.display.update()
        pygame.time.wait(50)
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



