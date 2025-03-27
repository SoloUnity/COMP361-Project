import pygame
from gui.control_element.button import Button
from gui.control_element.drop_down import DropDown
from models import rover
from utils.paths import REGULAR, get_image, get_text_file

class EditRover:
    def __init__(self, display, rover=None):
        self.display = display
        self.rover = rover
        self.active = True  # Whether the popup is active
        self.font = pygame.font.Font(None, 30)  # Font for text

        # Box dimensions
        thick_width = 600
        lean_width = 300
        box_height = 500
        spacing = 10  # Space between the boxes
        total_width = thick_width + lean_width + spacing

        # Calculate x positions to center both boxes
        start_x = (display.get_width() - total_width) // 2

        # Define rectangles for the two boxes
        self.algorithm_rect = pygame.Rect(start_x, (display.get_height() - box_height) // 2, thick_width, box_height)
        self.rover_rect = pygame.Rect(start_x + thick_width + spacing, (display.get_height() - box_height) // 2, lean_width, box_height)

        COLOR_MAIN_INACTIVE = (30,33,38)
        COLOR_MAIN_ACTIVE = (65, 71, 82)
        MENU_TEXT_COLOR = "white"
        MENU_BORDER_RADIUS = 3
        MENU_H = 20
        FONT = pygame.font.Font(REGULAR, 15)   
        CLOSE_ICON = pygame.image.load(get_image('icon_close.png'))
        ICON_W = 25
        UI_W = 150

        self.close_button = Button("Close", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, self.algorithm_rect.x + self.algorithm_rect.width - 70, self.algorithm_rect.y + 5, ICON_W, MENU_H, CLOSE_ICON, 0.8)

        self.confirm_button = Button("Confirm", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, self.algorithm_rect.x + self.algorithm_rect.width - 40, self.algorithm_rect.y + 5, ICON_W, MENU_H, CLOSE_ICON, 0.8)

        ROVER_OPTIONS = ["Curiosity","Perseverance", "Lunokhod1", "Lunokhod2", "Custom"]

        self.rover_drop_down = DropDown("Rover", ROVER_OPTIONS, COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE,FONT, MENU_TEXT_COLOR, 5, self.algorithm_rect.x + 30, self.algorithm_rect.y + 40, UI_W, MENU_H, 150)


        self.astar_button = Button("A*", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, self.algorithm_rect.x + 30, self.algorithm_rect.y + 200, UI_W, MENU_H)

        self.bfs_button = Button("BFS", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, self.algorithm_rect.x + 30, self.algorithm_rect.y + 230, UI_W, MENU_H)

        self.dfs_button = Button("DFS", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, self.algorithm_rect.x + 30, self.algorithm_rect.y + 260, UI_W, MENU_H)

        self.selected_attr = None  # Track selected input field
        self.input_fields = {}

        if self.rover:
            for attr, value in vars(self.rover).items():
                self.input_fields[attr] = str(value)  # Store as strings

    def toggle_popup(self):
        self.active = not self.active

    def update(self, events):
        if not self.active:
            return
        
        self.close_button.update(events)
        self.confirm_button.update(events)
        self.rover_drop_down.update(events)

        self.astar_button.update(events)
        self.bfs_button.update(events)
        self.dfs_button.update(events)


        if self.close_button.is_clicked:
            print("Close button was clicked!")  # Debugging print
            self.active = False

        if self.confirm_button.is_clicked:
            print("Close button was clicked!")  # Debugging print
            self.active = False

    def draw(self, display):
        """Draws the popup window with both boxes."""
        if not self.active:
            return

        # Draw thick main popup box
        pygame.draw.rect(display, (200, 200, 200), self.algorithm_rect)  
        pygame.draw.rect(display, (0, 0, 0), self.algorithm_rect, 2)

        # Draw lean side box
        pygame.draw.rect(display, (180, 180, 180), self.rover_rect)
        pygame.draw.rect(display, (0, 0, 0), self.rover_rect, 2)

        # Draw input fields inside thick box
        y_offset = self.algorithm_rect.y + 20
        for attr, value in self.input_fields.items():
            text_surf = self.font.render(f"{attr}: {value}", True, (0, 0, 0))
            display.blit(text_surf, (self.algorithm_rect.x + 20, y_offset))
            y_offset += 40

        # Draw close button
        self.close_button.draw(self.display)
        self.confirm_button.draw(self.display)
        self.rover_drop_down.draw(self.display)

        self.astar_button.draw(self.display)
        self.bfs_button.draw(self.display)
        self.dfs_button.draw(self.display)


