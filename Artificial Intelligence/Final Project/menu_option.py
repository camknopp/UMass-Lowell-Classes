# The class below is for a pygame menu option (e.g., "start game") which changes color when your mouse hovers over it
# most of the code is from https://gist.github.com/ohsqueezy/2802185 , though some small changes were made

import pygame

class Option:

    hovered = False
    
    def __init__(self, text, pos, screen):
        self.text = text
        self.pos = pos
        self.screen = screen
        self.set_rect()
        self.draw()
        
            
    def draw(self):
        self.set_rend()
        self.screen.blit(self.rend, self.rect)
        
    def set_rend(self):
        font = pygame.font.Font(None, 50)
        self.rend = font.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered:
            return (255, 255, 255)
        else:
            return (100, 100, 100)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        #self.rect.topleft = self.pos
        self.rect.center = self.pos
