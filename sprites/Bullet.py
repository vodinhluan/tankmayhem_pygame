import pygame
from Setting import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, position, direction):
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_image
        self.rect = self.image.get_rect()
        self.hit_rect = bullet_box
        self.hit_rect.center = self.rect.center
        self.position = vector(position)
        self.rect.center = position
        self.vel = direction * bulletSpeed
        self.product_bullet_time = pygame.time.get_ticks()

    def update(self):
        self.position += self.vel * self.game.changing_time
        self.rect.center = self.position  # update our rectangle to that location
        if pygame.sprite.spritecollide(self, self.game.walls, False):
            if self.vel.y > 0 and self.vel.x == 0:
                self.vel *= -1
            elif self.vel.y < 0 and self.vel.x == 0:
                self.vel *= -1
            elif self.vel.x > 0 and self.vel.y == 0:
                self.vel *= -1
            elif self.vel.x < 0 and self.vel.y == 0:
                self.vel *= -1
            elif self.vel.x > 0 and self.vel.y < 0:
                self.vel.x = -self.vel.x
            elif self.vel.x < 0 and self.vel.y < 0:
                self.vel.y = -self.vel.y
            elif self.vel.x < 0 and self.vel.y > 0:
                self.vel.x = -self.vel.x
            elif self.vel.x > 0 and self.vel.y > 0:
                self.vel.y = -self.vel.y
        if pygame.time.get_ticks() - self.product_bullet_time > Bullet_life_time:
            self.kill()