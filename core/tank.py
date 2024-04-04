import pygame
import math

class Tank:
    def __init__(self, x, y, width, height, color, speed, direction, controls):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.direction = direction  # Initial direction (in degrees)
        self.controls = controls
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        # Draw tank body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # Draw turret (centered on body as a circle)
        turret_size = self.width // 2  # Define turret radius
        turret_center_x = self.x + self.width // 2
        turret_center_y = self.y + self.height // 3
        pygame.draw.circle(screen, pygame.Color('red'), (turret_center_x, turret_center_y), turret_size)

        # Draw barrel (fixed relative to turret)
        barrel_end_x = turret_center_x  # Fixed x-coordinate of the barrel end
        barrel_end_y = turret_center_y - self.width  # Fixed y-coordinate of the barrel end
        pygame.draw.line(screen, pygame.Color('yellow'), (turret_center_x, turret_center_y), (barrel_end_x, barrel_end_y), width=7)

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

        # Update tank direction based on barrel position
        barrel_end_x = self.x + self.width / 2  # x-coordinate of the barrel end
        barrel_end_y = self.y + self.height // 3 - self.width  # y-coordinate of the barrel end
        dx = barrel_end_x - self.x - self.width / 2  # distance from tank center to barrel end
        dy = barrel_end_y - self.y - self.height // 2  # distance from tank center to barrel end
        self.direction = math.degrees(math.atan2(dy, dx))

        self.rect.update(self.x, self.y, self.width, self.height)

    def handle_input(self, keys):
        dx, dy = 0, 0
        for control, pressed in self.controls.items():
            if keys[control]:
                if pressed:
                    if control == pygame.K_a or control == pygame.K_LEFT:
                        self.direction += 2 
                    elif control == pygame.K_d or control == pygame.K_RIGHT:
                        self.direction -= 2 
                    elif control == pygame.K_w or control == pygame.K_UP:
                        dx -= math.cos(math.radians(self.direction)) * self.speed  
                        dy += math.sin(math.radians(self.direction)) * self.speed
                    elif control == pygame.K_s or control == pygame.K_DOWN:
                        dx += math.cos(math.radians(self.direction)) * self.speed  
                        dy -= math.sin(math.radians(self.direction)) * self.speed
        self.move(dx, dy)
