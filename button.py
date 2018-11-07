import pygame.font
from settings import Settings

class Button():

    def __init__(self, ai_settings, screen):
        '''Initialize button attributes.'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        # Set the dimensions and properties of the button.
        self.width, self.height = 250, 80
        self.button_color = (0, 200, 0)
        self.bright_button_color = (0, 255, 0)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.Font('Comic Sans MS.ttf', 50)

        # Build the button`s rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        #self.rect.center = self.screen_rect.center
        self.position1 = self.screen_rect.centerx*2/3, self.screen_rect.centery
        self.position2 = self.screen_rect.centerx*4/3, self.screen_rect.centery

        # The button message needs to be prepped only once.
        #self.prep_msg(msg)


    def prep_msg(self, msg, position):
        '''Turn msg into a rendered image and center text on the button.'''
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = position
    '''
    def draw_button(self,msg):
        self.prep_msg(msg)
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
    '''
    def button(self, msg, position):
        self.rect.center = position
        self.prep_msg(msg, position)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_clicked = self.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked:
            self.screen.fill(self.bright_button_color, self.rect)
        else:
            self.screen.fill(self.button_color, self.rect)

        self.msg_image_rect.center = position
        self.screen.blit(self.msg_image, self.msg_image_rect)
