import pygame
from pygame.locals import *
import sys

pygame.init()
WIDTH = 1920
HEIGHT = 1080
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
# pygame.display.toggle_fullscreen()

img = pygame.image.load("Rolly/Rolly-1.jpg")
running = True
while running:
        events = pygame.event.get()
        for event in pygame.event.get():
            print("jo", event.type)
            if event.type == QUIT:
               running = False
        windowSurface.blit(img, (0, 0)) #Replace (0, 0) with desired coordinates
        pygame.display.flip()

pygame.quit()
pygame.display.quit()
sys.exit()