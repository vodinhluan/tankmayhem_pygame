import pygame
from Setting import *
from sprites.Bullet import Bullet



vector = pygame.math.Vector2

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites                     
        pygame.sprite.Sprite.__init__(self, self.groups)    
        self.game = game                                   
        self.image = game.enemy_image
        self.rect = self.image.get_rect()
        self.hit_rect = enemy_box
        self.hit_rect.center = self.rect.center
        self.vel = vector(0, 0)
        self.position = vector(x, y) * SQSIZE
        self.rot = 0  # degree
        self.last_fire = 0
        self.rotation_speed = 0
        self.last_key_state = pygame.key.get_pressed()
        self.should_fire = False

    def update_key_state(self):
        key_state = self.last_key_state

        self.rotation_speed = 0
        self.vel = vector(0, 0)

        if len(key_state) == 0:
            return
        
        # XỬ LÝ nếu Offline thì Enemy là WASD, còn Onl thì là mũi tên
        if  self.game.is_online and key_state[pygame.K_LEFT] or \
            not self.game.is_online and key_state[pygame.K_a]:

            self.rotation_speed = +RotationSpeedOfEnemy

        if  self.game.is_online and key_state[pygame.K_RIGHT] or \
            not self.game.is_online and key_state[pygame.K_d]:

            self.rotation_speed = -RotationSpeedOfEnemy
            
        if  self.game.is_online and key_state[pygame.K_UP] or \
            not self.game.is_online and key_state[pygame.K_w]:
            
            self.vel = vector(0, enemySpeed).rotate(-self.rot)

        if  self.game.is_online and key_state[pygame.K_DOWN] or \
            not self.game.is_online and key_state[pygame.K_s]:

            self.vel = vector(0, -enemySpeed/2).rotate(-self.rot)

        if  self.game.is_online and (key_state[pygame.K_m] or self.should_fire) or\
            not self.game.is_online and key_state[pygame.K_q]:
        
            now = pygame.time.get_ticks()
        
            if now - self.last_fire > bullet_rate:
                self.last_fire = now
                direction = vector(0, 1).rotate(-self.rot)
                position = self.position + turret.rotate(-self.rot)
                Bullet(self.game, position, direction)
                self.game.shoot_sound.play()
                self.should_fire = False

    def collide_with_walls(self, direction):

        if direction == 'x_direction':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False, collide)
            if hits:
                if self.vel.x > 0:
                    self.position.x = hits[0].rect.left - self.hit_rect.width/2
                    # because we use center of rectangle in update we have to devide it by 2
                if self.vel.x < 0:
                    self.position.x = hits[0].rect.right + self.hit_rect.width/2 # cause of centerize the rectangle why we centerize because we want to rotate around the center of our self
                self.vel.x = 0
                self.hit_rect.centerx = self.position.x   # cause of centerize the rectangle why we centerize because we want to rotate around the center of our self
        if direction == 'y_direction':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False, collide)
            if hits:
                if self.vel.y > 0:
                    self.position.y = hits[0].rect.top - self.hit_rect.height/2
                    # because we use center of rectangle in update we have to devide it by 2
                if self.vel.y < 0:
                    self.position.y = hits[0].rect.bottom + self.hit_rect.height/2  # cause of centerize the rectangle why we centerize because we want to rotate around the center of our self
                self.vel.y = 0
                self.hit_rect.centery = self.position.y   # cause of centerize the rectangle why we centerize because we want to rotate around the center of our self

    def push_key_states(self, key_state):
        self.key_state_stack.push(key_state)

    def update(self):
        # do whatever you want before this function in reality and this function change them into pixel
        self.update_key_state()
        self.rot = (self.rot + self.rotation_speed * self.game.changing_time) % 360
        self.image = pygame.transform.rotate(self.game.enemy_image, self.rot)  # after rotate we need to take our image and transform it.....rptate the original image
        self.rect = self.image.get_rect()
        self.rect.center = self.position        # centerize of rectangle to rotate depend on center
        self.position += self.vel * self.game.changing_time
        self.hit_rect.centerx = self.position.x     # centerize of rectangle to rotate depend on center
        self.collide_with_walls('x_direction')
        self.hit_rect.centery = self.position.y     # centerize of rectangle to rotate depend on center
        self.collide_with_walls('y_direction')
        self.rect.center = self.hit_rect.center
