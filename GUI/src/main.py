#!/usr/bin/env python
import pygame
import rospy
from std_msgs.msg import Bool
from pygame.locals import *
import sys
import time

print(1)
def update_img(data):
    print(data)
    if data.data:
        print("hoi")
        windowSurface.blit(img2, (0, 0))
        pygame.display.flip()
        pygame.mixer.music.play(0)
        time.sleep(3)
        windowSurface.blit(img, (0, 0))
        pygame.display.flip()
    return


rospy.init_node('GUI', anonymous=True)
rospy.Subscriber("trashTrownIn", Bool, update_img, queue_size=1)
pygame.init()
WIDTH = 1920
HEIGHT = 1080
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.mixer.music.load('beep.ogg')
# pygame.display.toggle_fullscreen()
print(2)
img = pygame.image.load("Rolly/Rolly-1.jpg")
img2 = pygame.image.load("Rolly/Rolly-2.jpg")

windowSurface.blit(img, (0, 0)) #Replace (0, 0) with desired coordinates
pygame.display.flip()

rospy.spin()

pygame.quit()
pygame.display.quit()
sys.exit()


