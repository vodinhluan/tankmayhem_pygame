import pygame
from Setting import *
from sprites.Bullet import Bullet



vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_image
        self.rect = self.image.get_rect()
        self.hit_rect = player_box
        self.hit_rect.center = self.rect.center
        self.vel = vector(0, 0)
        self.position = vector(x, y) * SQSIZE
        self.rot = 0  # degree
        self.last_fire = 0
        self.last_key_state = pygame.key.get_pressed()
        self.rotation_speed = 0
        self.should_fire = False

    def keys(self):
        # get key for velocity every frame
        self.rotation_speed = 0  # not rotating
        self.vel = vector(0, 0)
        keys_state = pygame.key.get_pressed()
        if keys_state[pygame.K_a]:
            self.rotation_speed = +RotationSpeedOfPlayer
        if keys_state[pygame.K_d]:
            self.rotation_speed = -RotationSpeedOfPlayer
        if keys_state[pygame.K_w]:
            self.vel = vector(0, playerSpeed).rotate(-self.rot)
        if keys_state[pygame.K_s]:
            self.vel = vector(0, -playerSpeed/2).rotate(-self.rot)
        if keys_state[pygame.K_q]:
            now = pygame.time.get_ticks()
            if now - self.last_fire > bullet_rate:
                self.last_fire = now
                direction = vector(0, 1).rotate(-self.rot)
                position = self.position + turret.rotate(-self.rot)
                Bullet(self.game, position, direction)
                self.game.shoot_sound.play()

    def collide_with_walls(self, direction):
        if direction == 'x_direction':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False, collide)
            if hits:
                if self.vel.x > 0:
                    self.position.x = hits[0].rect.left - self.hit_rect.width/2
                    # because we use center of rectangle in update we have to devide it by 2
                if self.vel.x < 0:
                    self.position.x = hits[0].rect.right + self.hit_rect.width/2
                self.vel.x = 0
                self.hit_rect.centerx = self.position.x
        if direction == 'y_direction':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False, collide)
            if hits:
                if self.vel.y > 0:
                    self.position.y = hits[0].rect.top - self.hit_rect.height/2
                    # because we use center of rectangle in update we have to devide it by 2
                if self.vel.y < 0:
                    self.position.y = hits[0].rect.bottom + self.hit_rect.height/2
                self.vel.y = 0
                self.hit_rect.centery = self.position.y

    def update(self):
        # do whatever you want before this function in reality and this function change them into pixel
        self.keys()
        self.rot = (self.rot + self.rotation_speed * self.game.changing_time) % 360
        self.image = pygame.transform.rotate(self.game.player_image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.position += self.vel * self.game.changing_time
        self.hit_rect.centerx = self.position.x
        self.collide_with_walls('x_direction')
        self.hit_rect.centery = self.position.y
        self.collide_with_walls('y_direction')
        self.rect.center = self.hit_rect.center