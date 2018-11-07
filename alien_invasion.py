'''
In Alien Invasion, the player controls a ship that appears
at the bottom center of the screen.The player can move the
ship right and left using the arrow key and shoot bullets
using the spacebar. When the game begins,a fleet of aliens
fills the sky and moves across and down the screen.The player
shoots and destroys the aliens.If the player shoots all the
aliens,a new fleet appears that moves faster than the previous
fleet.If any alien hits the player's ship or reaches the
bottom of screen,the player loses a ship.If the player loses
three ships,the game ends.
'''

import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    # Initialize pygame,settings, and screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion Game")

    # Make the Play button.
    play_button = Button(ai_settings, screen)
    continue_button = Button(ai_settings, screen)
    quit_button = Button(ai_settings, screen)


    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, a group bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button,ship, aliens, bullets, quit_button)

        if stats.game_active and not stats.game_pause:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, continue_button, quit_button)

run_game()

