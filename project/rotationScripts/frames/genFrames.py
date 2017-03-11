import sys
import pygame

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

pygame.init()

charImage = pygame.image.load('globe1.jpg')

charImage = pygame.transform.scale(charImage, (900,900))


for i in xrange(360):
    pygame.image.save((rot_center(charImage, i)), str(i) + '.jpg')