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

        self.marker_icon = pygame.image.load("gui/images/icon_arrow_down.png")
        self.marker_icon = pygame.transform.scale(self.marker_icon, (15, 15))
        self.markers = []  
        
        self.static_surface = pygame.Surface((self.display_w, self.display_h))
        self.draw_start_screen()

    def draw_text(self, text, position, color=TEXT_COLOR):
        """Draw text on the screen at a given position with a specified color."""
        text_surface = self.font.render(text, True, color)
        self.display.blit(text_surface, position)

    def draw_start_screen(self):
        bg = pygame.image.load('gui/images/mars.jpg')
        # print(f"Offset X: {self.offset_x}, Offset Y: {self.offset_y}")
        # print(f"Image Size: {self.img_width}x{self.img_height}")


        # Scale the image based on the dynamically updated size
        bg = pygame.transform.scale(bg, (int(self.img_width), int(self.img_height)))

        # Clear the static surface
        self.static_surface.fill(BLACK)

        # Blit the scaled image with the current offset
        self.static_surface.blit(bg, (self.offset_x, self.offset_y))

    def is_within_map(self, pos):
        """Return True if pos is inside this MapView's displayed rectangle."""
        mx, my = pos
        return (
            self.display_offset_x <= mx < self.display_offset_x + self.display_w and
            self.display_offset_y <= my < self.display_offset_y + self.display_h
        )

    def handle_scroll(self, dx):
        new_offset_x = self.offset_x + dx

        if self.display_w - new_offset_x > self.img_width:
            self.offset_x = -(self.img_width - self.display_w)
        elif new_offset_x > 0:
            self.offset_x = 0
        else:
            self.offset_x = new_offset_x

        # Redraw after scrolling
        self.draw_start_screen()
    
    def add_marker(self, pos):
        x = pos[0] - self.marker_icon.get_width() / 2
        y = pos[1] - self.marker_icon.get_height()
        self.markers.append((x, y))

    def draw(self):
        self.display.blit(self.static_surface, (self.display_offset_x, self.display_offset_y))

        for marker_pos in self.markers:
            self.display.blit(self.marker_icon, marker_pos)

        mouse_pos = pygame.mouse.get_pos()
        
        img_x = mouse_pos[0] - self.offset_x - self.display_offset_x
        img_y = mouse_pos[1] - self.offset_y - self.display_offset_y

        lat = 90 - (img_y / self.img_height) * 180
        lon = (img_x / self.img_width) * 360 - 180

        # Update coords text bottom right
        text_surface = self.font.render(f"{lat}, {lon}", True, OFF_WHITE, TEXT_COLOR)
        self.display.blit(text_surface, (self.display.get_width() - text_surface.get_width(), self.display.get_height() - text_surface.get_height()))

        return (float('%.3f'%lat), float('%.3f'%lon))

    def calculate_zoom(self, start_lat_long, end_lat_long):
        start_lat, start_lon = start_lat_long
        end_lat, end_lon = end_lat_long
        print(f"Start: ({start_lat}, {start_lon}), End: ({end_lat}, {end_lon})")

        if end_lat is None or end_lon is None:
            # Reset to default view
            self.offset_x, self.offset_y = 0, 0
            self.img_width, self.img_height = 1440, 720  # Reset image size
            self.draw_start_screen()
            return

        # Convert lat/lon to pixel coordinates using full image resolution
        def latlon_to_pixels(lat, lon, img_width, img_height):
            x = ((lon + 180) / 360) * img_width
            y = ((90 - lat) / 180) * img_height
            return x, y

        top_left_x, top_left_y = latlon_to_pixels(start_lat, start_lon, 8536, 4268)
        bot_right_x, bot_right_y = latlon_to_pixels(end_lat, end_lon, 8536, 4268)

        # Calculate the size of the bounding box
        bbox_width_orig = abs(bot_right_x - top_left_x)
        bbox_height_orig = abs(bot_right_y - top_left_y)

        # Compute new scale so that the bounding box fills the MapView display area
        scale_x = self.display_w / bbox_width_orig
        scale_y = self.display_h / bbox_height_orig
        new_scale = min(scale_x, scale_y) # Keep the aspect ratio correct

        # Update the full image dimensions
        self.img_width = 8536 * new_scale
        self.img_height = 4268 * new_scale

        # Compute new bounding box positions in the scaled image
        new_top_left_x = top_left_x * new_scale
        new_top_left_y = top_left_y * new_scale
        new_bot_right_x = bot_right_x * new_scale
        new_bot_right_y = bot_right_y * new_scale

        # Compute offsets to center the bounding box correctly
        bbox_width_scaled = new_bot_right_x - new_top_left_x
        bbox_height_scaled = new_bot_right_y - new_top_left_y

        self.offset_x = (self.display_w - bbox_width_scaled) / 2 - new_top_left_x
        self.offset_y = (self.display_h - bbox_height_scaled) / 2 - new_top_left_y

        # # Set the offsets so that the top-left of the bounding box aligns with the MapView's top-left corner
        # self.offset_x = -top_left_x * new_scale + self.offset_x
        # self.offset_y = -top_left_y * new_scale + self.offset_y

        self.draw_start_screen()


    
        
