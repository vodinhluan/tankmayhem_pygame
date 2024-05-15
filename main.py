import pygame
from Setting import *
from os import path
import random



class Game:

    def __init__(self):
        pygame.init()  # initialize all imported pygame modules
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()  # create an object to help track time
        pygame.display.set_caption(TITLE)
        self.SCORE1 = 0
        self.SCORE2 = 0
        self.data()

    def data(self):
            folder_of_game = path.dirname(__file__)  # location of main.py
            image_folder = path.join(folder_of_game, 'imagefolder')
            Maps = path.join(folder_of_game, 'MAPS')
            sound_folder = path.join(folder_of_game, 'sound')
            self.map = []
            i = random.randint(1, 5)
            with open(path.join(Maps, 'MAP{}.txt'.format(i)), 'rt') as f:
                for line in f:
                    self.map.append(line)
            self.player_image = pygame.image.load(path.join(image_folder, PLAYER_IMAGE)).convert()
            self.player_image.set_colorkey(WHITE)
            self.enemy_image = pygame.image.load(path.join(image_folder, ENEMY_IMAGE)).convert()
            self.enemy_image.set_colorkey(WHITE)
            self.wall_image = pygame.image.load(path.join(image_folder, WALL_IMAGE)).convert()
            self.bullet_image = pygame.image.load(path.join(image_folder, BULLET_IMAGE)).convert()
            self.bullet_image.set_colorkey(WHITE)
            self.shoot_sound = pygame.mixer.Sound(path.join(sound_folder, 'shoot.wav'))
            self.explosion_sound = pygame.mixer.Sound(path.join(sound_folder, 'Explosion20.wav'))
            self.explosion_list = []
            for j in range(9):
                picture_name = 'regularExplosion0{}.png'.format(j)
                self.image_loading_of_explosion = pygame.image.load(path.join(image_folder, picture_name)).convert()
                self.image_loading_of_explosion.set_colorkey(BLACK)
                self.image = pygame.transform.scale(self.image_loading_of_explosion, (50, 50))
                self.explosion_list.append(self.image)
    def menu(self):
        pygame.font.init()  # you have to call this at the start,
        button_font = pygame.font.Font(None, 30)

        button_width = 200
        button_height = 50
        offline_button = pygame.Rect(WIDTH / 2 - button_width / 2, HEIGHT / 2 - button_height / 2, button_width, button_height)
        online_button = pygame.Rect(WIDTH / 2 - button_width / 2, HEIGHT / 2 + button_height, button_width, button_height)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if offline_button.collidepoint(mouse_pos):
                        self.new()
                        self.run()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if online_button.collidepoint(mouse_pos):
                        pass

            self.screen.fill(BGCOLOR)
            pygame.draw.rect(self.screen, (0, 255, 0), offline_button)
            pygame.draw.rect(self.screen, (0, 0, 255), online_button)

            offline_text = button_font.render("Offline", True, (0, 0, 0))  
            online_text = button_font.render("Online", True, (0, 0, 0))  
            self.screen.blit(offline_text, (offline_button.x + (offline_button.width - offline_text.get_width()) // 2, 
                                            offline_button.y + (offline_button.height - offline_text.get_height()) // 2))
            self.screen.blit(online_text, (online_button.x + (online_button.width - online_text.get_width()) // 2, 
                                           online_button.y + (online_button.height - online_text.get_height()) // 2))

            pygame.display.flip()  # update display

        self.quit()

# create game objects
g = Game()
while True:
    g.menu()
    g.new()
    g.run()


