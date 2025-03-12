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
# 8536, 4268
# 1440, 720

class MapView:
    def __init__(self, display, x, y, width, height):
        self.display = display
        self.font = pygame.font.Font(REGULAR, 18)
        self.display_offset_x, self.display_offset_y = x, y
        
        self.offset_x, self.offset_y = 0, 0
        self.display_w, self.display_h = width, height
        self.img_width, self.img_height = 1440, 720

        self.static_surface = pygame.Surface((self.display_w, self.display_h))
        self.draw_start_screen()

    def draw_text(self, text, position, color=TEXT_COLOR):
        """Draw text on the screen at a given position with a specified color."""
        text_surface = self.font.render(text, True, color)
        self.display.blit(text_surface, position)

    def draw_start_screen(self):
        bg = pygame.image.load('gui/images/mars.jpg')
        bg = pygame.transform.scale(bg, (self.img_width, self.img_height))
        self.static_surface.blit(bg, (self.offset_x, self.offset_y))

    def draw(self):
        self.display.blit(self.static_surface, (self.display_offset_x, self.display_offset_y))

        mouse_pos = pygame.mouse.get_pos()
        
        img_x = mouse_pos[0] - self.offset_x - self.display_offset_x
        img_y = mouse_pos[1] - self.offset_y - self.display_offset_y

        lat = 90 - (img_y / self.img_height) * 180
        lon = (img_x / self.img_width) * 360 - 180

        # Update coords text bottom right
        text_surface = self.font.render(f"{lat}, {lon}", True, OFF_WHITE, TEXT_COLOR)
        self.display.blit(text_surface, (self.display.get_width() - text_surface.get_width(), self.display.get_height() - text_surface.get_height()))

        return (float('%.3f'%lat), float('%.3f'%lon))
    
    # def update(self, top_left, bot_right):
    #     if bot_right is None:
    #         self.offset_x, self.offset_y = 0, 0
    #         self.img_width, self.img_height = 1440, 720
    #         self.draw_start_screen()
    #         return
        

    #     w, h = abs(bot_right[0] - top_left[0]), abs(bot_right[1] - top_left[1])
    #     center = (top_left[0] + w / 2, top_left[1] + h / 2)
            
    #     self.img_width, self.img_height = 8536, 4268
    #     self.offset_x = (-(center[0]) / self.display_w * self.img_width) + self.display_w / 2 + self.display_offset_x
    #     self.offset_y = (-(center[1]) / self.display_h * self.img_height) + self.display_h / 2 + self.display_offset_y

    #     self.draw_start_screen()

    def update(self, top_left, bot_right):
        if bot_right is None:
            # Reset to default view using an initial scale that fits the full image into the display area
            # initial_scale = min(self.display_w / 8536, self.display_h / 4268)
            self.offset_x, self.offset_y = 0, 0
            self.img_width, self.img_height = 1440, 720
            self.draw_start_screen()
            return

        # Compute the current scale factor (from original image to what's currently drawn)
        current_scale = self.img_width / 8536

        # Convert the bounding box coordinates (which are in MapView display space) back to original image coordinates
        top_left_orig = (top_left[0] / current_scale, top_left[1] / current_scale)
        bot_right_orig = (bot_right[0] / current_scale, bot_right[1] / current_scale)

        # Calculate the size of the bounding box in original image coordinates
        bbox_width_orig = abs(bot_right_orig[0] - top_left_orig[0])
        bbox_height_orig = abs(bot_right_orig[1] - top_left_orig[1])

        # Compute new scale so that the bounding box fills the MapView display area
        scale_x = self.display_w / bbox_width_orig
        scale_y = self.display_h / bbox_height_orig
        new_scale = min(scale_x, scale_y)

        # Update the full image dimensions using the new scale
        self.img_width = 8536 * new_scale
        self.img_height = 4268 * new_scale

        # Set the offsets so that the top-left of the bounding box aligns with the MapView's top-left corner
        self.offset_x = -top_left_orig[0] * new_scale + self.display_offset_x
        self.offset_y = -top_left_orig[1] * new_scale + self.display_offset_y

        self.draw_start_screen()
        
