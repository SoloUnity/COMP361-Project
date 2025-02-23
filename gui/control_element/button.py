import pygame


class Button:
    def __init__(self, name, color_main_inactive, color_main_active, font, text_color, border_radius, x, y, w, h, icon = None, icon_scaling = None):
        self.name = name
        self.color_main_inactive = color_main_inactive
        self.color_main_active = color_main_active
        self.font = font
        self.text_color = text_color
        self.rect = pygame.Rect(x, y, w, h)
        self.border_radius = border_radius
        self.icon = icon
        self.icon_scaling= icon_scaling

        self.is_hovered = False
        self.is_clicked = False
    
    def set_icon(self, icon):
        self.icon = icon

    def draw(self, display):
        color = self.color_main_active if self.is_hovered else self.color_main_inactive
        pygame.draw.rect(display, color, self.rect, 0, self.border_radius)

        if self.icon:
            # Resize icon to fit inside the button while maintaining aspect ratio
            icon_width, icon_height = self.icon.get_size()
            scale_factor = min(self.rect.width / icon_width, self.rect.height / icon_height)
            new_width = int(icon_width * scale_factor)
            new_height = int(icon_height * scale_factor)
            if self.icon_scaling:
                new_width = new_width * self.icon_scaling
                new_height = new_height * self.icon_scaling
            resized_icon = pygame.transform.scale(self.icon, (new_width, new_height))
            
            # Center the icon within the rectangle
            icon_rect = resized_icon.get_rect(center=self.rect.center)
            display.blit(resized_icon, icon_rect)
        else:
            # Render and center the text if no icon is provided
            text_surface = self.font.render(self.name, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            display.blit(text_surface, text_rect)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mpos)

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.is_hovered:
                    self.is_clicked = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.is_clicked = False

# Example usage:
# pygame.init()
# screen = pygame.display.set_mode((640, 480))
# clock = pygame.time.Clock()
# font = pygame.font.SysFont(None, 30)
# icon = pygame.image.load('path_to_icon.png')

# button = Button("Click Me", (100, 100, 100), (150, 150, 150), font, (255, 255, 255), 5, 200, 200, 150, 50, icon)

# running = True
# while running:
#     event_list = pygame.event.get()
#     for event in event_list:
#         if event.type == pygame.QUIT:
#             running = False

#     button.update(event_list)

#     screen.fill((0, 0, 0))
#     button.draw(screen)
#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()
