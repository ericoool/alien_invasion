import pygame

class Settings():
    '''A class to store all settings for Alien Invasion.'''

    def __init__(self):
        '''
        Initialize the game's stats settings.

        white = (255, 255, 255)
        black = (0, 0, 0)
        gray = (128, 128, 128)
        red = (200, 0, 0)
        green = (0, 200, 0)
        bright_red = (255, 0, 0)
        bright_green = (0, 255, 0)
        blue = (0, 0, 255)

        '''
        # Screen settings
        self.screen = pygame.display.set_mode((1200, 800))

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)
        #self.background = pygame.image.load('images/star_bg.bmp')

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 5

        # Alien settings
        self.fleet_drop_speed = 5

        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        # How quickly the alien point values increase.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game.'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 5
        self.alien_speed_factor = 1
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        '''Increase speed settings and alien point values.'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)