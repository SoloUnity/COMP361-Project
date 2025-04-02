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

        # Close Button Rect (small X button on the right side)
        self.x_size = 15  # Width & height of close button
        self.x_rect = pygame.Rect(self.rect.right - self.x_size - 5, self.rect.top + 9, self.x_size, self.x_size)

        # Colors
        self.COLOR_SELECTED = (70, 70, 70)
        self.COLOR_DEFAULT = (31, 30, 30)
        self.COLOR_TEXT = (255, 255, 255)
        self.COLOR_CLOSE = (200, 50, 50)  # Red for close button

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

        # Draw Close (X) Button
        pygame.draw.rect(screen, self.COLOR_CLOSE, self.x_rect, border_radius=3)  # Red button
        x_text = self.font.render("X", True, self.COLOR_TEXT)
        screen.blit(x_text, (self.x_rect.x + 2, self.x_rect.y - 1))  # Center the 'X'
        

    def check_click(self, mouse_pos):
        """Checks if the tab or close button was clicked"""
        if self.x_rect.collidepoint(mouse_pos):
            return "close"  # Close the tab
        elif self.rect.collidepoint(mouse_pos):
            return "select"  # Select the tab
        return None  # No interaction
        
