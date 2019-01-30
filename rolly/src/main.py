#!/usr/bin/env python
import pygame
import rospy
from std_msgs.msg import Bool
from std_srvs.srv import Trigger, TriggerResponse
from pygame.locals import *
import sys
import time
import os

print(1)
def update_img(request):
    if True:
        print("hoi")
        windowSurface.blit(img2, (0, 0))
        pygame.display.flip()
        pygame.mixer.music.play(0)
        time.sleep(3)
        windowSurface.blit(img, (0, 0))
        pygame.display.flip()
    return TriggerResponse(success = True, message=" ")

pygame.init()
src_dir = "~/catkin_ws/src/rolly/src"
rospy.init_node('GUI', anonymous=True)
rospy.Subscriber("trashTrownIn", Bool, update_img, queue_size=1)
pygame.init()
WIDTH = 1024
HEIGHT = 768
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.mixer.music.load(os.path.expanduser(src_dir + "/" + 'beep.ogg'))
# pygame.display.toggle_fullscreen()
print(2)
img = pygame.image.load(os.path.expanduser(src_dir + "/" + "Rolly/Rolly-1.jpg"))
img = pygame.transform.scale(img, (WIDTH, HEIGHT))
img2 = pygame.image.load(os.path.expanduser(src_dir + "/" + "Rolly/Rolly-2.jpg"))
img2 = pygame.transform.scale(img2, (WIDTH, HEIGHT))

windowSurface.blit(img, (0, 0)) #Replace (0, 0) with desired coordinates
pygame.display.flip()

s = rospy.Service("TrownIn", Trigger, update_img)
rospy.spin()

pygame.quit()
pygame.display.quit()
sys.exit()


