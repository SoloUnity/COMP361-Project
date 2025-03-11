import pygame
from utils.paths import REGULAR, get_image
from src.util.dem_to_matrix import dem_to_matrix

pygame.init()

# Constants for UI
TEXT_COLOR = (0, 0, 0)
ERROR_COLOR = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
OFF_WHITE = (217,217,217)
WHITE = (255, 255, 255)
LOGIN_BLUE = (8, 158, 222)
# SCREENWIDTH, SCREENHEIGHT = 1440, 720
# 8536, 4268

class Test:
    def __init__(self, display, program_state_manager):
        # Setup display for the login window
        self.display = display
        self.program_state_manager = program_state_manager

        # GUI elements initialization
        self.font = pygame.font.Font(REGULAR, 18)

        icon = pygame.image.load("gui/images/icon_close.png")
        self.marker = pygame.transform.scale(icon, (10, 10))

        self.path = []

        # background = pygame.image.load('gui/images/mars.jpg')
        # background = pygame.transform.scale(background, (self.display.get_width(), self.display.get_height()))
        
        self.img_width, self.img_height = 1440, 720
        bg = self.draw_start_screen(self.img_width, self.img_height)
        
        # self.offset_x = (-760 / 1300 * self.img_width) + self.display.get_width() / 2
        # self.offset_y = (-130 / 650 * self.img_height) + self.display.get_height() / 2
        
        self.offset_x = 0
        self.offset_y = 0

        self.start_btn = pygame.Rect(0, 0, 100, 25)
        
        self.static_surface = pygame.Surface((self.display.get_width(), self.display.get_height()))
        self.static_surface.blit(bg, (self.offset_x, self.offset_y))
        
        self.start_btn = pygame.Rect(0, 0, 100, 25)
        pygame.draw.rect(self.display, GRAY, self.start_btn, border_radius=40)

    def draw_text(self, text, position, color=TEXT_COLOR):
        """Draw text on the screen at a given position with a specified color."""
        text_surface = self.font.render(text, True, color)
        self.display.blit(text_surface, position)

    def draw_start_screen(self, width, height):
        # Display bg image
        background = pygame.image.load('gui/images/mars.jpg')
        background = pygame.transform.scale(background, (width, height))
        return background
        # self.display.blit(background, (0,0))

    def on_click(self, mouse_pos, lon, lat):
        pos = (mouse_pos[0] - 5, mouse_pos[1] - 5)
        self.path.append(pos)

    def start_search(self):
        print(self.path)

    def run(self, events):
        # Draw background + start btn
        self.display.blit(self.static_surface, (0, 0))
        pygame.draw.rect(self.display, GRAY, self.start_btn, border_radius=40)

        # Draw markers in path
        for pos in self.path:
            self.display.blit(self.marker, pos)
        
        mouse_pos = pygame.mouse.get_pos()
        
        img_x = mouse_pos[0] - self.offset_x
        img_y = mouse_pos[1] - self.offset_y

        lat = 90 - (img_y / self.img_height) * 180
        lon = (img_x / self.img_width) * 360 - 180

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.start_btn.collidepoint(mouse_pos):
                    self.start_search()
                else:
                    self.on_click(mouse_pos, lon, lat)
                
        # Update coords text bottom right
        text_surface = self.font.render(f"{lat}, {lon}", True, OFF_WHITE, TEXT_COLOR)
        self.display.blit(text_surface, (self.display.get_width() - text_surface.get_width(), self.display.get_height() - text_surface.get_height()))