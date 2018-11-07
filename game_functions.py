import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
import random

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, quit_button):
    '''Respond to keypresses and mouse events.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, bullets, play_button, quit_button)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
            check_quit_button(quit_button, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''Start a new game when the player clicks Play.'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_keydown_events(event, ai_settings, screen, stats, ship, bullets, pause_button, quit_button):
    '''Respond to keypresses.'''
    if event.key == pygame.K_d:
        ship.moving_right = True
    if event.key == pygame.K_a:
        ship.moving_left = True
    if event.key == pygame.K_w:
        ship.moving_up = True
    if event.key == pygame.K_s:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p:
        sys.exit()
    # set a key for pause the game.
    elif event.key == pygame.K_l:
        stats.game_pause = True
        paused(ai_settings, stats, pause_button, quit_button)

def check_keyup_events(event, ship):
    '''Respond to key releases.'''
    if event.key == pygame.K_d:
        ship.moving_right = False
    if event.key == pygame.K_a:
        ship.moving_left = False
    if event.key == pygame.K_w:
        ship.moving_up = False
    if event.key == pygame.K_s:
        ship.moving_down = False


def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()
def paused(ai_settings, stats, pause_button, quit_button):
    pygame.mouse.set_visible(True)
    largeText = pygame.font.Font('Comic Sans MS.ttf', 100)
    TextSurf, TextRect = text_objects('Paused', largeText)
    TextRect.center = ((ai_settings.screen_width / 2), (ai_settings.screen_height / 3))
    ai_settings.screen.blit(TextSurf, TextRect)
    while stats.game_pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_pause_button(stats, pause_button, mouse_x, mouse_y)
                check_quit_button(quit_button, mouse_x, mouse_y)

        pause_button.button("Continue", pause_button.position1)
        quit_button.button("Quit", pause_button.position2)
        pygame.display.update()
        pygame.time.Clock().tick(15)

def check_pause_button(stats, pause_button, mouse_x, mouse_y):
    """pause game when the player clicks Play."""
    button_clicked = pause_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and stats.game_pause:
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statistics.
        stats.game_pause = False

def check_quit_button(quit_button, mouse_x, mouse_y):
    """pause game when the player clicks Play."""
    button_clicked = quit_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        #quit_button.screen.fill(quit_button.bright_button_color, quit_button.rect)
        pygame.quit()
        quit()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, pause_button, quit_button):
    '''Update images on the screen and flip to the new screen.'''
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    #screen.blit(ai_settings.background,(0,0))
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.button("Play", play_button.position1)
        quit_button.button("Quit", pause_button.position2)
    elif stats.game_pause:
        pause_button.button("Continue", pause_button.position1)
        quit_button.button("Quit", pause_button.position2)

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Update position of bullets and get rid of old bullets.'''
    # Update bullet position.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Respond to bullet-alien collisions.'''
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # Destroy existing bullets, speed up game and create new fleet, and start a new level.
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        stats.level += 1
        sb.prep_level()

def fire_bullet(ai_settings, screen, ship, bullets):
    '''Fire a bullet if limit not reached yet.'''
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_alien_x(ai_settings, alien_width):
    '''Determine the number of aliens that fit in a row.'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''Determine the number of rows of aliens that fit on the screen.'''
    available_space_y = (ai_settings.screen_height - 3 * alien_height - ship_height)
    number_rows = int(available_space_y / (4 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''Create an alien and place it in the row.'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height * 2 + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    '''Create a full fleet of aliens.'''
    # Create an alien and find the number of aliens in a raw.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    '''Respond appropriately if any aliens have reached an edge.'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''Drop the entire fleet and change the fleet's direction.'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''Respond to ship being hit by alien.'''
    # Decrement ships_left.
    if stats.ships_left > 0:
        # Decrement ship_left
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Check if any aliens have reached the bottom of the screen.'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if  the ship got hit.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''
    Check if the fleet is at an edge,
    and then update the positions of all aliens in the fleet.
    '''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    '''Check to see if there`s a new high score.'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

    with open("high_score.txt", "w+") as f:
        f.write(str(stats.high_score))
