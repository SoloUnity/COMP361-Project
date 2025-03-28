import pygame
from utils.paths import REGULAR, get_image

## TODO handle no initial option list，for select rover

class DropDown():
    def __init__(self, name, options: list, color_main_inactive, color_main_active, color_option_inactive, color_option_active, font, text_color, border_radius: int, x: int, y: int, w: int, h: int, option_w: int, scroll_icon_actif = False):

        self.name = name
        self.options = options
        self.font = font
        self.color_main_active = color_main_active
        self.color_main_inactive = color_main_inactive
        self.color_option_active = color_option_active
        self.color_option_inactive = color_option_inactive
        self.rect = pygame.Rect(x,y,w,h)
        self.border_radius = border_radius
        self.text_color = text_color
        self.option_w = option_w

        self.menu_box_rect = pygame.Rect(x, y+h, option_w, len(options) * h + 6)
        self.option_toggled = False
        self.menu_active = False
        self.option_active = -1
        self.scroll_icon_actif = scroll_icon_actif

        
    def draw(self, display):
        pygame.draw.rect(display, self.color_main_active if self.menu_active else self.color_main_inactive, self.rect, 0, self.border_radius)
        name = self.font.render(self.name, 1, self.text_color) 
        display.blit(name, name.get_rect(center = self.rect.center))

        if self.scroll_icon_actif:
            arrow_icon = pygame.image.load(get_image('icon_arrow_down.png'))
            icon_size = (self.rect.height // 2, self.rect.height // 2)  # Resize based on dropdown height
            arrow_icon = pygame.transform.scale(arrow_icon, icon_size)

            icon_rect = arrow_icon.get_rect(midright=(self.rect.right - 10, self.rect.centery))
            display.blit(arrow_icon, icon_rect.topleft)
        
        if self.option_toggled:

            pygame.draw.rect(display, self.color_main_inactive, self.menu_box_rect, 0, self.border_radius)

            rect = self.rect.copy()
            for i, option in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height + 3
                rect.width = self.option_w - 5/100*self.option_w
                rect.centerx = self.menu_box_rect.centerx

                pygame.draw.rect(display, self.color_option_active if i == self.option_active else self.color_main_inactive, rect, 0, self.border_radius)
                option_text = self.font.render(option, True, self.text_color)

                text_rect = option_text.get_rect()
                text_rect.left = rect.left + 4  
                text_rect.centery = rect.centery  

                display.blit(option_text, text_rect.topleft)  
                
    def set_position(self, x, y):
        self.rect.topleft = (x, y)
        self.menu_box_rect.topleft = (x, y + self.rect.height)

    def update(self, events):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.option_active = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height + 3
            rect.width = self.option_w
            if rect.collidepoint(mpos):
                self.option_active = i
                break

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.option_toggled = not self.option_toggled
                elif self.option_toggled:
                    if self.option_active >= 0:
                        self.option_toggled = False
                        return self.option_active
                    elif not self.menu_box_rect.collidepoint(mpos) and not self.rect.collidepoint(mpos):
                        self.option_toggled = False

        return -1
    
