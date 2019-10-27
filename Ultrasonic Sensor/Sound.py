import pygame
import time

pygame.mixer.init()

crash_sound = pygame.mixer.Sound("sample-20191026-2005.wav")
pygame.mixer.Sound.play(crash_sound)
time.sleep(2)
