import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
title = pygame.display.set_caption("Tank Mayhem Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Frame rate
FPS = 60
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Game logic goes here
    
    # Clear screen
    screen.fill(BLACK)
    
    # Draw everything here
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
