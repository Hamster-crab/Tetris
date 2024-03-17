import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tetris", "Tetris")
clock = pygame.time.Clock()
running = True

# ブロックの画像
block_img = pygame.image.load("block.png")

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill((255, 255, 255))
    pygame.display.flip()
    clock.tick(60)