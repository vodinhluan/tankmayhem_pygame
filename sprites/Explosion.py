import pygame
from Setting import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, center):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.explosion_list[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.picture = 0
        self.last_time_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):  # change the image when enough time has gone
        print(self.game.explosion_list)
        now = pygame.time.get_ticks()
        if now - self.last_time_update > self.frame_rate:
            self.last_time_update = now
            self.picture += 1
            if self.picture == len(self.game.explosion_list):
                self.kill()
            else:  # we should go to next new image
                center = self.rect.center  # next image on center
                self.image = self.game.explosion_list[self.picture]
                self.rect = self.image.get_rect()    # get the new rect for new picture
                self.rect.center = center