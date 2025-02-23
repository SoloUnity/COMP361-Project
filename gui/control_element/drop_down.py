import pygame

## TODO handle no initial option list，for select rover

class DropDown():
    def __init__(self, name, options: list, color_main_inactive, color_main_active, color_option_inactive, color_option_active, font, text_color, border_radius: int, x: int, y: int, w: int, h: int, option_w: int):

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
        
    def draw(self, display):
        pygame.draw.rect(display, self.color_main_active if self.menu_active else self.color_main_inactive, self.rect, 0, self.border_radius)
        name = self.font.render(self.name, 1, self.text_color) 
        display.blit(name, name.get_rect(center = self.rect.center))

        
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
    

# pygame.init()
# clock = pygame.time.Clock()
# screen = pygame.display.set_mode((640, 480))

# COLOR_INACTIVE = (40, 39, 44)
# COLOR_ACTIVE = (100, 200, 255)
# COLOR_LIST_INACTIVE = (255, 100, 100)
# COLOR_LIST_ACTIVE = (255, 150, 150)

# list1 = DropDown("File",["option 5", "option 1"], COLOR_INACTIVE, COLOR_ACTIVE, COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE, pygame.font.SysFont(None,18), "white", 3, 50, 50, 30, 20, 80)

# run = True
# while run:
#     clock.tick(30)

#     event_list = pygame.event.get()
#     for event in event_list:
#         if event.type == pygame.QUIT:
#             run = False

#     selected_option = list1.update(event_list)
#     if selected_option >= 0:
#         list1.main = list1.options[selected_option]

#     screen.fill((255, 255, 255))
#     list1.draw(screen)
#     pygame.display.flip()
    
# pygame.quit()
# exit()