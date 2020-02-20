#!/usr/bin/env python

#Logan Williams
#Com S 476 Project 2

import random, math, pygame, collections
from pygame.locals import *
from collections import deque
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
    parent = None
    neighbors = []
    visited = 0 #0 for unvisited, 1 for visited, 2 for dead, 3 for goal, 4 for start
    def __init__(self, value):
        self.value = value
    def setParent(self, cell):
        self.parent = cell
    def getParent(self):
        return self.parent
    def setValue(self, val):
        self.value = val
    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)
    def getNeighbors(self):
        return self.neighbors
    def getValue(self):
        return self.value
    def getVisited(self):
        return self.visited
    def setVisited(self, visited):
        self.visited = visited
    def setXY(self, x, y):
        self.XY = (x, y)
    def getXY(self):
        return self.XY

#constants
SIZE = 360
cObstacles = [[None for i in range(SIZE)] for j in range(SIZE)]
cSpace = [[0 for i in range(SIZE)] for j in range(SIZE)]
WINSIZE = [640, 480]

#Calculate each and every axis to project the points onto
def calcAxi(r1, r2):
    axis1 = (r1.UR[0] - r1.UL[0], r1.UR[1] - r1.UL[1])
    axis2 = (r1.UR[0] - r1.LR[0], r1.UR[1] - r1.LR[1])
    axis3 = (r2.UL[0] - r2.LL[0], r2.UL[1] - r2.LL[1])
    axis4 = (r2.UL[0] - r2.UR[0], r2.UL[1] - r2.UR[1])
    return [axis1, axis2, axis3, axis4]

#project upper right onto an axis
def projectionUR(axis, r1):
    numerator = r1.UR[0] * axis[0] + r1.UR[1] * axis[1]
    denominator = math.pow(r1.UR[0], 2) + math.pow(r1.UR[1], 2)
    return ((numerator / denominator) * axis[0],(numerator / denominator) * axis[1])

#project upper left onto an axis
def projectionUL(axis, r1):
    numerator = r1.UL[0] * axis[0] + r1.UL[1] * axis[1]
    denominator = math.pow(r1.UL[0], 2) + math.pow(r1.UL[1], 2)
    return ((numerator / denominator) * axis[0],(numerator / denominator) * axis[1])

#project lower right onto an axis
def projectionLR(axis, r1):
    numerator = r1.LR[0] * axis[0] + r1.LR[1] * axis[1]
    denominator = math.pow(r1.LR[0], 2) + math.pow(r1.LR[1], 2)
    return ((numerator / denominator) * axis[0],(numerator / denominator) * axis[1])

#project lower left onto an axis
def projectionLL(axis, r1):
    numerator = r1.LL[0] * axis[0] + r1.LL[1] * axis[1]
    denominator = math.pow(r1.LL[0], 2) + math.pow(r1.LL[1], 2)
    return ((numerator / denominator) * axis[0],(numerator / denominator) * axis[1])

#takes each corner and dot product with the axis specified to get a scalar value
def castProjectionToDotArray(UR, UL, LL, LR, axis):
    URdot = dotProd(UR[0], UR[1], axis[0], axis[1])
    ULdot = dotProd(UL[0], UL[1], axis[0], axis[1])
    LRdot = dotProd(LR[0], LR[1], axis[0], axis[1])
    LLdot = dotProd(LL[0], LL[1], axis[0], axis[1])
    return [URdot, ULdot, LRdot, LLdot]

#returns the dot product of two coordinates
def dotProd(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2

#checks the scalar values to see if the projected boxes collide on an axis
def isNotCollision(array1, array2):
    if(min(array2) <= max(array1) and max(array2) >= min(array1)):
        return False
    return True

#checks if the two rectangles collide on an axis
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

#checks all four axi for collision. Note that according to the Separating Axis Theorem, if all four axi show collision, then there is a collision, otherwise there isn't collision
def collisionDetection(r1, r2):
    collisionBool = False
    axisArr = calcAxi(r1, r2)
    for i in axisArr:
        collisionBool = singleAxisCollisionDetection(r1, r2, i)
        if(collisionBool):
            return False #no collision
    return True #collision

#writes all obstacles to file
def writeCObstaclesToFile():
    try:
        f = open("cObstacles.txt", 'w')
        for row in range(len(cObstacles)):
            for col in range(len(cObstacles[row])):
                f.write("%d " % cObstacles[row][col].getValue())
            f.write("\n")
    finally:
        f.close()	

def main():

    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('C-Space and C-Obstacles: Logan Williams, 2019s')
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
                cObstacles[i][j] = cell(1)
                cSpace[i][j] = 1
            else:
                cObstacles[i][j] = cell(0)
                cSpace[i][j] = 0
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




