# tank_mayhem.py (main)
import pygame
from core.tank import Tank

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Mayhem")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Frame rate
FPS = 80
clock = pygame.time.Clock()

# Create tanks for player 1 and player 2
player1_tank = Tank(100, 100, 40, 60, GREEN, 5, {pygame.K_a: True, pygame.K_d: True, pygame.K_w: True, pygame.K_s: True})
player2_tank = Tank(600, 100, 40, 60, BLUE, 5, {pygame.K_LEFT: True, pygame.K_RIGHT: True, pygame.K_UP: True, pygame.K_DOWN: True})

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get currently pressed keys
    keys = pygame.key.get_pressed()
    
    # Handle input for player 1 and player 2
    player1_tank.handle_input(keys)
    player2_tank.handle_input(keys)
    
    # Clear screen
    screen.fill(BLACK)
    
    # Draw tanks
    player1_tank.draw(screen)
    player2_tank.draw(screen)
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
