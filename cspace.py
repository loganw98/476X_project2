#!/usr/bin/env python

import random, math, pygame
from pygame.locals import *
from pygame.sprite import *
from array import *
from math import sin, cos, pi

class Rect:
    def __init__(self, x, y, width, height, theta):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.theta = theta
        self.v0 = (width * cos(theta), width * sin(theta))
        self.v1 = (height/2 * cos(theta + pi/2), height/2 * sin(theta+pi/2))
        self.LL = (self.x+self.v1[0],self.y+self.v1[1])
        self.UL = (self.x-self.v1[0],self.y-self.v1[1])
        self.UR = (self.x-self.v1[0]+self.v0[0],self.y-self.v1[1]+self.v0[1])
        self.LR = (self.x+self.v1[0]+self.v0[0],self.y+self.v1[1]+self.v0[1])
    def setLL(self, LL):
        self.LL = LL
    def setLR(self, LR):
        self.LR = LR
    def setUL(self, UL):
        self.UL = UL
    def setUR(self, UR):
        self.UR = UR
    def recalcTheta(self, theta):
        self.theta = theta
        self.v0 = (width * cos(theta), width * sin(theta))
        self.v1 = (height/2 * cos(theta + pi/2), height/2 * sin(theta+pi/2))
        self.LL = (self.x+self.v1[0],self.y+self.v1[1])
        self.UL = (self.x-self.v1[0],self.y-self.v1[1])
        self.UR = (self.x-self.v1[0]+self.v0[0],self.y-self.v1[1]+self.v0[1])
        self.LR = (self.x+self.v1[0]+self.v0[0],self.y+self.v1[1]+self.v0[1])

class cell:
    value = 0
    timestamp = 0
    def setValue(self, val):
        self.value = val
    def setTimestamp(self, val):
        self.timestamp = val
    def getTimestamp(self):
        return self.timestamp
    def getValue(self):
        return self.value

#constants
SIZE = 360
cObstacles = [[cell() for i in range(SIZE)] for j in range(SIZE)]
cSpace = [[0 for i in range(SIZE)] for j in range(SIZE)]
WINSIZE = [640, 480]

def calcAxi(r1, r2):
    axis1 = (r1.UR[0] - r1.UL[0], r1.UR[1] - r1.UL[1])
    axis2 = (r1.UR[0] - r1.LR[0], r1.UR[1] - r1.LR[1])
    axis3 = (r2.UL[0] - r2.LL[0], r2.UL[1] - r2.LL[1])
    axis4 = (r2.UL[0] - r2.UR[0], r2.UL[1] - r2.UR[1])
    return [axis1, axis2, axis3, axis4]

def projectionUR(axis, r1):
    numerator = r1.UR[0] * axis[0] + r1.UR[1] * axis[1]
    denominator = math.pow(r1.UR[0], 2) + math.pow(r1.UR[1], 2)
    return ((numerator / denominator) * axis[0],(numerator / denominator) * axis[1])

def projectionUL(axis, r1):
    numerator = r1.UL[0] * axis[0] + r1.UL[1] * axis[1]
    denominator = math.pow(r1.UL[0], 2) + math.pow(r1.UL[1], 2)
    return ((numerator / denominator) * axis[0],(numerator / denominator) * axis[1])

def projectionLR(axis, r1):
    numerator = r1.LR[0] * axis[0] + r1.LR[1] * axis[1]
    denominator = math.pow(r1.LR[0], 2) + math.pow(r1.LR[1], 2)
    return ((numerator / denominator) * axis[0],(numerator / denominator) * axis[1])

def projectionLL(axis, r1):
    numerator = r1.LL[0] * axis[0] + r1.LL[1] * axis[1]
    denominator = math.pow(r1.LL[0], 2) + math.pow(r1.LL[1], 2)
    return ((numerator / denominator) * axis[0],(numerator / denominator) * axis[1])

def castProjectionToDotArray(UR, UL, LL, LR, axis):
    URdot = dotProd(UR[0], UR[1], axis[0], axis[1])
    ULdot = dotProd(UL[0], UL[1], axis[0], axis[1])
    LRdot = dotProd(LR[0], LR[1], axis[0], axis[1])
    LLdot = dotProd(LL[0], LL[1], axis[0], axis[1])
    return [URdot, ULdot, LRdot, LLdot]

def dotProd(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2

def isNotCollision(array1, array2):
    if(min(array2) <= max(array1) and max(array2) >= min(array1)):
        return False
    return True

def singleAxisCollisionDetection(r1, r2, axis):
    r1UL = projectionUL(axis, r1)
    r1UR = projectionUR(axis, r1)
    r1LL = projectionLL(axis, r1)
    r1LR = projectionLR(axis, r1)
    r1dot = castProjectionToDotArray(r1UR, r1UL, r1LL, r1LR, axis)

    r2UL = projectionUL(axis, r2)
    r2UR = projectionUR(axis, r2)
    r2LL = projectionLL(axis, r2)
    r2LR = projectionLR(axis, r2)
    r2dot = castProjectionToDotArray(r2UR, r2UL, r2LL, r2LR, axis)

    return isNotCollision(r1dot, r2dot)

def collisionDetection(r1, r2):
    collisionBool = False
    axisArr = calcAxi(r1, r2)
    for i in axisArr:
        collisionBool = singleAxisCollisionDetection(r1, r2, i)
        if(collisionBool):
            return False #no collision
    return True #collision
    

#working on this
def isCloseToObstacle(r1):
    ob1x = 320
    ob2x = 320
    ob1y = 240-125
    ob2y = 240+125

def distance(x1, x2, y1, y2):
    return math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))

def writeCObstaclesToFile():
    try:
        f = open("cObstacles", 'w')
        for row in range(len(cObstacles)):
            for col in range(len(cObstacles[row])):
                f.write("%d " % cObstacles[row][col].getValue())
            f.write("\n")
    finally:
        f.close()	

def main():

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
    theta2 = 0

    obstacle1 = Rect(centerx, centery-125, 20, 20, 0)
    x = centerx
    y = centery - 125
    obstacle1.setUL((x, y))
    obstacle1.setLL((x, y+20))
    obstacle1.setUR((x+20, y))
    obstacle1.setLR((x+20, y+20))
    obstacle2 = Rect(centerx, centery+125, 20, 20, 0)
    x = centerx
    y = centery + 125
    obstacle2.setUL((x, y))
    obstacle2.setLL((x, y+20))
    obstacle2.setUR((x+20, y))
    obstacle2.setLR((x+20, y+20))
    for i in range(len(cObstacles)):
        link1 = Rect(centerx, centery, 100, 20, theta)
        for j in range(len(cObstacles[i])):
            link2 = Rect(link1.x+link1.v0[0], link1.y+link1.v0[1], 100, 20, theta2)
            c1 = collisionDetection(link2, obstacle1)
            c2 = collisionDetection(link2, obstacle2)
            if(c1 == True or c2 == True):
                cObstacles[i][j].setValue(1)
                cSpace[i][j] = 1
            theta2 = theta2 + float(pi/180)
        theta2 = 0
        theta = theta + float(pi/180)
    writeCObstaclesToFile()

    for x in range(len(cSpace)):
        for y in range(len(cSpace[x])):
            if cSpace[x][y] == 1:
                pygame.draw.rect(screen, RED, [x, y, 1, 1])
            else:
                pygame.draw.rect(screen, white, [x, y, 1, 1])
    pygame.display.flip()

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




