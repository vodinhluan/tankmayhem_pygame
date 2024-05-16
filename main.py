import pygame
from Setting import *
from os import path
import random

from sprites.Wall import Wall
from sprites.Player import Player
from sprites.Bullet import Bullet
from sprites.Enemy import Enemy
from sprites.Explosion import Explosion

Screen = pygame.display.set_mode((WIDTH,HEIGHT))
bgStart = pygame.image.load('imagefolder/bgS.png').convert_alpha()
bgWin = pygame.image.load('imagefolder/bgWin.png').convert_alpha()

btnStart = pygame.image.load('imagefolder/btnStart.png').convert_alpha()
btnOffline = pygame.image.load('imagefolder/btnOffline.png').convert_alpha()
btnExit = pygame.image.load('imagefolder/btnExit.png').convert_alpha()
nameGame = pygame.image.load('imagefolder/nameGame.png').convert_alpha()
cup = pygame.image.load('imagefolder/cup.png').convert_alpha()
textWin = pygame.image.load('imagefolder/textWin.png').convert_alpha()

btnSoundOn = pygame.image.load('imagefolder/sound-on.png').convert_alpha()
btnSoundOff = pygame.image.load('imagefolder/sound-off.png').convert_alpha()

class Game:

    def __init__(self):
        pygame.init()  # Initialize all imported pygame modules
        pygame.mixer.init()
        self.screen = Screen
        self.clock = pygame.time.Clock()  # Create an object to help track time
        pygame.display.set_caption(TITLE)
        self.SCORE1 = 0
        self.SCORE2 = 0
        self.sound_on = True
        pygame.mixer.music.load('sound/background_music.mp3')  # tải file nhạc
        pygame.mixer.music.play(-1)  # phát nhạc (lặp đi lặp lại với -1)
        self.data()

    def data(self):
        folder_of_game = path.dirname(__file__)  # Location of main.py
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

    def new(self):
        # initializing all variables and setup them for a new game
        self.walls = pygame.sprite.Group()  # created the walls group to hold them all
        self.bullets = pygame.sprite.Group()
        self.shields = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        for row, tiles in enumerate(self.map):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == '*':
                    self.player = Player(self, col, row)
                if tile == '-':
                    self.enemy = Enemy(self, col, row)
                # if tile == '@':
                #     ShieldItem(self, col, row)
                    
        self.game_over = False  # Đặt lại trạng thái game
        self.Score = False # reset score 

    def run(self):
            while not self.game_over:  # Thay đổi điều kiện dừng vòng lặp
                self.changing_time = self.clock.tick(FPS) / 1000
                self.events()
                self.update()
                self.draw()
                
            # Reset trạng thái điểm khi kết thúc màn chơi
            self.SCORE2 = 0
            self.SCORE1 = 0
            
            while self.playing:
                self.changing_time = self.clock.tick(FPS) / 1000
                self.events()
                self.update()
                self.draw()

                # Thêm kiểm tra để chuyển sang trạng thái chơi game khi điều kiện đạt được
                if self.Score:
                    self.SCORE2 = 0
                    self.SCORE1 = 0
                    self.new()
                    self.run()

    def grid(self):
        for x in range(0, WIDTH, SQSIZE):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, SQSIZE):
            pygame.draw.line(self.screen, WHITE, (0, y), (WIDTH, y))

    def menu(self):
        # Initialize buttons
        bgS = pygame.transform.scale(bgStart, (WIDTH, HEIGHT))
        button_width = btnStart.get_width()
        button_height = btnStart.get_height()
        online_button = pygame.Rect(WIDTH / 2 - button_width / 2, HEIGHT / 2 - button_height / 2, button_width, button_height)
        offline_button = pygame.Rect(WIDTH / 2 - button_width / 2, HEIGHT / 2 + button_height, button_width, button_height)
        exit_button = pygame.Rect(WIDTH / 2 - button_width / 2, HEIGHT / 2 + button_height * 2.5  , button_width, button_height)
        sound_button = pygame.Rect(0, 0, btnSoundOn.get_width(), btnSoundOn.get_height())
        
        running = True
        while running:
            self.screen.blit(bgS, (0, 0))  # Draw the background image first

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if offline_button.collidepoint(mouse_pos):
                        self.new()
                        self.run()
                    elif online_button.collidepoint(mouse_pos):
                        pass
                    elif sound_button.collidepoint(mouse_pos):
                        self.sound_on = not self.sound_on
                        if self.sound_on:
                            pygame.mixer.music.play(-1)  # Phát nhạc lặp lại
                        else:
                            pygame.mixer.music.stop()
                    
            # Draw the title image
            title_rect = nameGame.get_rect(center=(WIDTH / 2, HEIGHT / 8))
            self.screen.blit(nameGame, title_rect)
            
            # Draw button images
            self.screen.blit(btnStart, online_button.topleft)
            self.screen.blit(btnOffline, offline_button.topleft)
            self.screen.blit(btnExit, exit_button.topleft)
            
            if self.sound_on:
                self.screen.blit(btnSoundOn, sound_button.topleft)
            else:
                self.screen.blit(btnSoundOff, sound_button.topleft)
                
            pygame.display.flip()  # Update display

        self.quit()

    def quit(self):
        
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if self.game_over and event.type == pygame.KEYUP:
                self.new()
                self.run()
                
    def update(self):
        # keep track changing
        self.all_sprites.update()
        self.hit()

    def draw(self):
        # flip all the thing to screen
        self.screen.fill(BGCOLOR)
        self.grid()
        self.all_sprites.draw(self.screen)
        # kietbui
        # item_rect = self.threebullet.get_rect(center=self.screen.get_rect().center)
        # self.screen.blit(self.threebullet, item_rect)
        drawing_text(self.screen, str(self.SCORE1) + ':Green Tank', 25, 150, 710, GREEN)
        drawing_text(self.screen, 'Blue Tank:' + str(self.SCORE2), 25, 900, 710, BLUE)
        pygame.display.flip()

    def hit(self):
        self.hits1 = pygame.sprite.spritecollide(self.player, self.bullets, True, collide)
        if self.hits1:
            Explosion(self, self.player.rect.center)
            self.explosion_sound.play()
            self.player.kill()
            self.SCORE1 += 1
            self.playing = False
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(1000)
            self.new()
            self.data()
            
        if self.SCORE1 == 5:
            self.show_go_screen1()
                    
        self.hits2 = pygame.sprite.spritecollide(self.enemy, self.bullets, True, collide)
        if self.hits2:
            Explosion(self, self.enemy.rect.center)
            self.explosion_sound.play()
            self.enemy.kill()
            self.SCORE2 += 1
            self.playing = False
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(1000)
            self.new()
            self.data()
            
        if self.SCORE2 == 5:
            self.show_go_screen2()
                    
        # Draw all sprites after updating the explosions
        self.all_sprites.draw(self.screen)
        pygame.display.flip()  # Update the display after drawing

    def show_go_screen1(self):
        bgW = pygame.transform.scale(bgWin, (WIDTH, HEIGHT))
        self.screen.blit(bgW,(0,0))
        self.screen.blit(textWin,(120,0))
        # self.screen.blit(cup, (400,0))
        drawing_text(self.screen, 'Green Tank Win', 80, WIDTH / 2, HEIGHT / 3, GREEN)
        drawing_text(self.screen, 'SCORE:' + str(self.SCORE1) + '-' + str(self.SCORE2), 40, WIDTH / 2,  340, GREEN)
        drawing_text(self.screen, 'Press enter key to begin or escape key to quit', 20, WIDTH / 2, HEIGHT - 30 , RED)
       
        pygame.display.flip()
        self.wait_for_key()
        self.game_over = True
        
    def show_go_screen2(self):
        bgW = pygame.transform.scale(bgWin, (WIDTH, HEIGHT))
        self.screen.blit(bgW,(0,0))
        self.screen.blit(textWin,(120,0))
        # self.screen.blit(cup, (400,0))
        drawing_text(self.screen, 'Blue Tank Win', 80, WIDTH / 2, HEIGHT / 3, BLUE)
        drawing_text(self.screen, 'SCORE:' + str(self.SCORE2) + '-' + str(self.SCORE1) , 40, WIDTH / 2, 340, BLUE)
        drawing_text(self.screen, 'Press enter key to begin or escape key to quit', 20, WIDTH / 2, HEIGHT - 30, RED)
   
        pygame.display.flip()
        self.wait_for_key()
        self.game_over = True
        
    def wait_for_key(self):
        key_pressed = False
        while not key_pressed:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:  # Only break the loop if 'Enter' is pressed
                         key_pressed = True
        self.Score = False  # Đặt lại trạng thái chơi game

        
# Create game object
g = Game()
while True:
    g.menu()
    g.new()
    g.run()
