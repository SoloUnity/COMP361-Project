import pygame
from utils.paths import REGULAR

class Tab:
    def __init__(self, project, tab_id, position, width=125, height=30):
        self.project = project
        self.tab_id = tab_id
        self.position = position
        self.width = width
        self.height = height
        self.is_selected = False

        # Tab Rect
        self.rect = pygame.Rect((position * width) + 41, 33, width, height)

        # Colors
        self.COLOR_SELECTED = (70, 70, 70)
        self.COLOR_DEFAULT = (31, 30, 30)
        self.COLOR_TEXT = (255, 255, 255)

        # Font
        self.font = pygame.font.Font(REGULAR, 15)

    def draw(self, screen):
        color = self.COLOR_SELECTED if self.is_selected else self.COLOR_DEFAULT
        pygame.draw.rect(screen, color, self.rect)

        # Draw text
        text_surface = self.font.render("Tab" + str(self.tab_id), True, self.COLOR_TEXT)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

        # Draw a white border on the left side
        pygame.draw.line(screen, (255, 255, 255), (self.rect.right, self.rect.top), (self.rect.right, self.rect.bottom), 1)  # Adjust thickness if needed
        # Draw a white border on the right side
        pygame.draw.line(screen, (255, 255, 255), (self.rect.left, self.rect.top), (self.rect.left, self.rect.bottom), 1)  # Adjust thickness if needed
        

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
