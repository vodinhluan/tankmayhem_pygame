import pygame

class Tank:
    def __init__(self, x, y, width, height, color, speed, controls):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.controls = controls
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, dx=0, dy=0):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.update(self.x, self.y, self.width, self.height)

    def handle_input(self, keys):
        dx, dy = 0, 0
        for control, pressed in self.controls.items():
            if keys[control]:
                if pressed:
                    if control == pygame.K_a or control == pygame.K_LEFT:
                        dx -= 2
                    elif control == pygame.K_d or control == pygame.K_RIGHT:
                        dx += 2
                    elif control == pygame.K_w or control == pygame.K_UP:
                        dy -= 2
                    elif control == pygame.K_s or control == pygame.K_DOWN:
                        dy += 2
        self.move(dx, dy)
