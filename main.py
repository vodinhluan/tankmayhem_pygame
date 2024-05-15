import pygame
from Setting import *
from os import path
import random

class Game:

    def __init__(self):
        pygame.init()  # Initialize all imported pygame modules
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()  # Create an object to help track time
        pygame.display.set_caption(TITLE)
        self.SCORE1 = 0
        self.SCORE2 = 0
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

    def menu(self):
        folder_of_game = path.dirname(__file__)
        image_folder = path.join(folder_of_game, 'imagefolder')

        # Load background image with error handling
        try:
            self.bg_image = pygame.transform.scale(
                pygame.image.load(path.join(image_folder, "bgS.png")).convert(),
                (WIDTH, HEIGHT)
            )
        except pygame.error as e:
            print(f"Unable to load background image: {e}")
            return

        # Initialize font and buttons
        pygame.font.init()
        button_font = pygame.font.Font(None, 30)
        title_font = pygame.font.Font(None, 100)  # Define a larger font for the title
        button_width = 200
        button_height = 50
        offline_button = pygame.Rect(WIDTH / 2 - button_width / 2, HEIGHT / 2 - button_height / 2, button_width, button_height)
        online_button = pygame.Rect(WIDTH / 2 - button_width / 2, HEIGHT / 2 + button_height, button_width, button_height)

        running = True
        while running:
            self.screen.blit(self.bg_image, (0, 0))  # Draw the background image first

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

            # Draw the title text
            title_text = title_font.render("TANK MAYHEM", True, (197, 76, 0))
            title_rect = title_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
            self.screen.blit(title_text, title_rect)

            # Draw buttons
            pygame.draw.rect(self.screen, (192,192,192), offline_button)
            pygame.draw.rect(self.screen, ((255,255,0)) , online_button)

            offline_text = button_font.render("Offline", True, (0, 0, 0))
            online_text = button_font.render("Online", True, (0, 0, 0))
            self.screen.blit(offline_text, (offline_button.x + (offline_button.width - offline_text.get_width()) // 2,
                                            offline_button.y + (offline_button.height - offline_text.get_height()) // 2))
            self.screen.blit(online_text, (online_button.x + (online_button.width - online_text.get_width()) // 2,
                                           online_button.y + (online_button.height - online_text.get_height()) // 2))

            pygame.display.flip()  # Update display

        self.quit()

    def quit(self):
        pygame.quit()

# Create game object
g = Game()
while True:
    g.menu()
    g.new()
    g.run()
