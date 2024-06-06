import sys

import pygame

GAME_WIDTH = 1000
GAME_HEIGHT = 700

pygame.init()
pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
logo = pygame.image.load('logo.png')
pygame.display.set_icon(logo)
pygame.display.set_caption('TetriX')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
