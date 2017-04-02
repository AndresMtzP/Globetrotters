#!/usr/bin/env python


import pygame
import sys
import math

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def is_long(val):
    try:
        int(round(float(val)))
    except (ValueError, TypeError) as e:
        return False
    return True

def control(command, rotVelocity, prevDestination):
    numOfFrames = 240
    newVel = rotVelocity
    rotateToDestination = 0
    swipeCount = 0
    if is_long(command):
        destination = float(command)
        destination = round(round(float(float(numOfFrames)/float(360))*destination)*float(float(360)/float(numOfFrames)))

        if destination <= 0 and destination > -181:
            destination = round((0 - destination)/float(float(360)/float(numOfFrames)))
            rotateToDestination = 1
        elif destination > 0 and destination < 180:
            destination = round((360 - destination)/float(float(360)/float(numOfFrames)))
            rotateToDestination = 1
        else:
            destination = prevDestination
    else:
        cmdStr = str(command).lower()
        destination = prevDestination
        if cmdStr == 'stop':
            newVel = 0
        elif cmdStr == 'left' or cmdStr == 'west':
            newVel = -1
        elif cmdStr == 'right' or cmdStr == 'east':
            newVel = 1
        elif cmdStr == 'fast':
            if rotVelocity >= 0:
                newVel = 2
            else:
                newVel = -2
        elif cmdStr == 'slow' or cmdStr == 'slowly':
            if rotVelocity >= 0:
                newVel = 1
            else:
                newVel = -1
        elif cmdStr == 'faster':
            if rotVelocity >= 0 and rotVelocity < 4:
                newVel += 1
            elif rotVelocity < 0 and rotVelocity > -4:
                newVel -= 1
        elif cmdStr == 'slower':
            if rotVelocity > 0:
                newVel -= 1
            elif rotVelocity < 0:
                newVel += 1
        elif cmdStr == 'swipel':
            swipeCount = 50
            newVel = 8
        elif cmdStr == 'swiper':
            swipeCount = 50
            newVel = -8
    return (newVel, destination, rotateToDestination, swipeCount)

def getNextFrame(imageList, frame):

    if frame >= len(imageList):
        return pygame.transform.flip(imageList[frame - len(imageList)], 1, 1)
    else:
        return imageList[frame]

pygame.init()
screen = pygame.display.set_mode((900,900))
done = False
clock = pygame.time.Clock()

origCenter = screen.get_rect().center
charImage = pygame.image.load('/home/pi/globe/Rotation/globe1.jpg')
charImage = pygame.transform.scale(charImage, screen.get_size())
charImage = charImage.convert()

screen_rect = screen.get_rect()
image_rect = charImage.get_rect()
image_rect.center = screen_rect.center
displayImage = pygame.transform.rotate(charImage, 0)
degree = 0

rotateToDestination = 0
rotationSpeed = 1  #idle speed
destination = 0
swipeCount = 0

stoppedCount = 0

numOfFrames = 120
imageList = []
for i in xrange(numOfFrames):
    imageList.append(rot_center(charImage, i*180/float(numOfFrames)))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    try:
        with open('/home/pi/globe/Rotation/commands', 'r+') as commandFile:
            command = commandFile.readline()
            if len(command) > 0:
                newState = control(command, rotationSpeed, destination)
                rotationSpeed = newState[0]
                destination = newState[1]
                rotateToDestination = newState[2]
                swipeCount = newState[3]
            commandFile.seek(0)
            commandFile.truncate()
    except IOError:
        pass

    ##################################
    # rotateToDestination takes shortest path to rotate towards a certain degree
    if rotateToDestination:
        if degree == destination:
            rotationSpeed = 0
        elif destination - degree > 0:
            if destination - degree < ((numOfFrames*2) - 1 + degree) - destination:
                degree += 1
                if degree >= numOfFrames * 2:
                    degree = 0
                displayImage = getNextFrame(imageList, degree)
            else:
                degree -= 1
                if degree < 0:
                    degree = (numOfFrames * 2) - 1
                displayImage = getNextFrame(imageList, degree)
        else:
            if degree - destination < ((numOfFrames*2) - 1 - degree) + destination:
                degree -= 1
                if degree < 0:
                    degree = (numOfFrames * 2) - 1
                displayImage = getNextFrame(imageList, degree)
            else:
                degree += 1
                if degree >= numOfFrames * 2:
                    degree = 0
                displayImage = getNextFrame(imageList, degree)
    else:
        degree += rotationSpeed
        if degree < 0:
            degree += (numOfFrames*2)
        elif degree >= numOfFrames*2:
            degree -= (numOfFrames*2)
        displayImage = getNextFrame(imageList, degree)

    if swipeCount > 0:
        if swipeCount == 47:
            if rotationSpeed > 0:
                rotationSpeed = 7
            else:
                rotationSpeed = -7
        elif swipeCount == 44:
            if rotationSpeed > 0:
                rotationSpeed = 6
            else:
                rotationSpeed = -6
        elif swipeCount == 41:
            if rotationSpeed > 0:
                rotationSpeed = 5
            else:
                rotationSpeed = -5
        elif swipeCount == 37:
            if rotationSpeed > 0:
                rotationSpeed = 4
            else:
                rotationSpeed = -4
        elif swipeCount == 32:
            if rotationSpeed > 0:
                rotationSpeed = 3
            else:
                rotationSpeed = -3
        elif swipeCount == 25:
            if rotationSpeed > 0:
                rotationSpeed = 2
            else:
                rotationSpeed = -2
        elif swipeCount == 15:
            if rotationSpeed > 0:
                rotationSpeed = 1
            else:
                rotationSpeed = -1
        elif swipeCount == 1:
            rotationSpeed = 0
        swipeCount -= 1

    # if globe is stopped for 4 seconds, rotate it at idle speed
    if stoppedCount > 40:
        stoppedCount = 0
        rotationSpeed = 1   #idle speed

    if rotationSpeed == 0:
        stoppedCount += 1
    else:
        stoppedCount = 0




    screen.fill((255,255,255))


    screen.blit(displayImage, (0,0))

    pygame.display.flip()
    clock.tick(10)
    #print clock.get_fps()


