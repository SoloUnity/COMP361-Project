import pygame
import sys
import pygame._sdl2
from gui.control_element.drop_down import DropDown
from gui.control_element.button import Button
from gui.control_element.popup_window import PopupWindow
from gui.control_element.bounding_box import BoundingBox
from gui.control_element.map_view import MapView
from utils.paths import REGULAR, get_image, get_text_file
from gui.states.tab_manager import TabManager
from gui.temp_project import Project
# from models.project import Project
#support resize

#constants for UI
WHITE = (255, 255, 255)
FONT = pygame.font.Font(REGULAR, 15) 
LIGHT_GRAY = (155, 155, 155)
TAB_COLOR = (31,30,30)
SIMULATION_SCREEN_COLOR = (48,48,49)

class Simulation:
    def __init__(self, display, program_state_manager):
        self.display = display
        self.program_state_manager = program_state_manager
        self.sdl2_window = pygame._sdl2.video.Window.from_display_module()
        self.tab_manager = TabManager()
        self.projects = [None] * 10  # max 10 projects/tabs
        self.active_project = None  # Currently selected project
        self.fullscreen = False  # Tracks fullscreen state

        # Initialize map area (x, y, width, height)
        self.map_x = 40
        self.map_y = 63
        self.map_width = self.display.get_width() - 40  # Default value (adjust based on UI)
        self.map_height = self.display.get_height() - 63 # Default value (adjust based on UI)

        # # Store previous values for resize calculations
        # self.prev_map_width = self.map_width
        # self.prev_map_height = self.map_height
        # self.prev_map_x = self.map_x
        # self.prev_map_y = self.map_y

        #MENU
        COLOR_MAIN_INACTIVE = (30,33,38)
        COLOR_MAIN_ACTIVE = (65, 71, 82)
        MENU_TEXT_COLOR = "white"
        MENU_BORDER_RADIUS = 3
        MENU_H = 25
        MENU_Y = 3
        FONT = pygame.font.Font(REGULAR, 15)   

        #DROP_DOWNS
        DROP_DOWN_COLOR_OPTION_ACTIVE = (65, 71, 82)
        DROP_DOWN_COLOR_OPTION_INACTIVE = (30,33,38)

        PROJECT_OPTIONS = ["New Project", "Load Project", "Save Project", "Delete Project"]

        #Temporary. TODO needs to upgrade button class
        TEMP_OPTION = [":D","ehehe", "》:O", "來財， 來"]

        self.project_drop_down = DropDown("Project", PROJECT_OPTIONS, COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, DROP_DOWN_COLOR_OPTION_INACTIVE, DROP_DOWN_COLOR_OPTION_ACTIVE,FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, 40, MENU_Y, 55, MENU_H, 150)

        self.select_rover_drop_down = DropDown("Select Rover", TEMP_OPTION, COLOR_MAIN_ACTIVE, (13, 59, 66), DROP_DOWN_COLOR_OPTION_ACTIVE, (21, 97, 109),FONT, MENU_TEXT_COLOR, 5, 483, MENU_Y, 342, MENU_H, 250)
        #display.get_width()/2 - 75

        #ICONS TOP
        ICON_W = 30
        CLOSE_ICON = pygame.image.load(get_image('icon_close.png'))
        RESTORE_ICON = pygame.image.load(get_image('icon_restore.png'))
        MINIMIZE_ICON = pygame.image.load(get_image('icon_minimize.png'))

        self.add_rover_button = Button("Add Rover", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, 100, MENU_Y, 75, MENU_H)

        self.help_button = Button("Help", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, 180, MENU_Y, 45, MENU_H)
        self.show_help_popup = False

        # Popup instance
        self.help_popup = PopupWindow(self.display, width=740, height=488, title="Documentation")

        self.close_window_button = Button("Close", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, display.get_width() - 40, MENU_Y, ICON_W, MENU_H, CLOSE_ICON, 0.8)

        self.restore_window_button = Button("Restore", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, display.get_width() - 75, MENU_Y, ICON_W, MENU_H, RESTORE_ICON, 0.7)

        self.minimize_window_button = Button("Minimize", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, display.get_width() - 110, MENU_Y, ICON_W, MENU_H, MINIMIZE_ICON, 0.8)

        #ICONS SIDE
        S_ICON_X = 3
        S_ICON_H = 25

        ERROR_ICON = pygame.image.load(get_image('icon_error.png'))
        SETTING_ICON = pygame.image.load(get_image('icon_setting.png'))
        VISIBILITY_ICON = pygame.image.load(get_image('icon_visibility.png'))

        self.error_button = Button("Error", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, S_ICON_X, display.get_height() - 110, ICON_W, S_ICON_H, ERROR_ICON, 0.8)

        self.view_data_button = Button("View", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, S_ICON_X, display.get_height() - 75, ICON_W, S_ICON_H, VISIBILITY_ICON, 0.8)

        self.setting_button = Button("Setting", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, S_ICON_X, display.get_height() - 40, ICON_W, S_ICON_H, SETTING_ICON, 0.8)

        
        self.drag = BoundingBox(self.display, self, 40, 63, self.display.get_width() - 40, self.display.get_height() - 63, 10000)
        self.confirm_bb = Button("Confirm", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, display.get_width()/2 - 80, display.get_height() - 100, 70, 50)
        self.reset_bb = Button("Reset", COLOR_MAIN_INACTIVE, COLOR_MAIN_ACTIVE, FONT, MENU_TEXT_COLOR, MENU_BORDER_RADIUS, display.get_width()/2 + 80, display.get_height() - 100, 70, 50)


    def draw_text(self, text, position, font, color=WHITE):
        """Draw text on the screen at a given position with a specified color."""
        text_surface = font.render(text, True, color)
        self.display.blit(text_surface, position)

    # def toggle_fullscreen(self):
    #     """Toggle fullscreen mode."""
    #     self.fullscreen = not self.fullscreen
    #     if self.fullscreen:
    #         self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    #     else:
    #         self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    #     self.update_ui_on_resize()
    #     self.draw_window()
    
    # def update_ui_on_resize(self):
    #     """Update UI elements dynamically after resizing."""
    #     width, height = self.display.get_size()

    #     # Update button positions dynamically
    #     self.close_window_button.rect.topleft = (width - 40, self.close_window_button.rect.y)
    #     self.restore_window_button.rect.topleft = (width - 75, self.restore_window_button.rect.y)
    #     self.minimize_window_button.rect.topleft = (width - 110, self.minimize_window_button.rect.y)

    #     self.error_button.rect.topleft = (self.error_button.rect.x, height - 110)
    #     self.view_data_button.rect.topleft = (self.view_data_button.rect.x, height - 75)
    #     self.setting_button.rect.topleft = (self.setting_button.rect.x, height - 40)

    #     self.drag = BoundingBox(self.display, self, 40, 63, width - 40, height - 63, 10000)
    #     self.active_project.map_view = MapView(self.display, 40, 63, width - 40, height - 63)

    #     self.confirm_bb.rect.topleft = (width // 2 - 80, height - 100)
    #     self.reset_bb.rect.topleft = (width // 2 + 80, height - 100)

    #     # Get new map area dimensions (adjust based on your layout)
    #     self.map_x = 40  # Example: Left padding for the map
    #     self.map_y = 63  # Example: Top padding for the map
    #     self.map_width = width - 40  # Example: Width excluding side padding
    #     self.map_height = height - 63  # Example: Height excluding top/bottom UI

    #     print("Resizing from w and h: " + str(self.prev_map_width) + " " + str(self.prev_map_height) + " to: " + str(self.map_width) + " " + str(self.map_height))

    #     # **Update the bounding box after resizing**
    #     if self.active_project and self.active_project.bounding_box:
    #         print("Updating bb after resize")

    #         if not self.active_project.relative_bounding_box:

    #             # Extract x1, y1, x2, y2 from bounding box
    #             x1, y1, x2, y2 = self.active_project.bounding_box

    #             # Store bounding box as relative values
    #             print("Storing bounding box relative values")
    #             self.active_project.relative_bounding_box = (
    #                 (x1 - self.prev_map_x) / self.prev_map_width,
    #                 (y1 - self.prev_map_y) / self.prev_map_height,
    #                 (x2 - self.prev_map_x) / self.prev_map_width,
    #                 (y2 - self.prev_map_y) / self.prev_map_height
    #             )

    #         rx1, ry1, rx2, ry2 = self.active_project.relative_bounding_box
    #         print("Relative values")
    #         print(self.active_project.relative_bounding_box)

    #         # Convert back to absolute coordinates
    #         new_x1 = int(rx1 * self.map_width) + self.map_x
    #         new_y1 = int(ry1 * self.map_height) + self.map_y
    #         new_x2 = int(rx2 * self.map_width) + self.map_x
    #         new_y2 = int(ry2 * self.map_height) + self.map_y

    #         # Reset bounding box selection
    #         self.drag.start_coord = None
    #         self.drag.end_coord = None
    #         self.drag.dragging = False

    #         self.active_project.bounding_box = (new_x1, new_y1, new_x2, new_y2)
    #         self.drag.start_coord = (new_x1, new_y1)
    #         self.drag.end_coord = (new_x2, new_y2)

    #         print("Resized to:", self.drag.start_coord, self.drag.end_coord)
        
    #     # Store previous map width & height
    #     self.prev_map_x, self.prev_map_y = self.map_x, self.map_y
    #     self.prev_map_width, self.prev_map_height = self.map_width, self.map_height

    #     if self.fullscreen:
    #         self.select_rover_drop_down.set_position(546,3)

    #     elif not self.fullscreen:
    #         self.select_rover_drop_down.set_position(483, 3)
        
    def reset_simulation_window(self):
        SIMULATION_WINDOW_X = 40
        SIMULATION_WINDOW_Y = 63
        SIMULATION_WINDOW_W = self.display.get_width() - 40
        SIMULATION_WINDOW_H = self.display.get_height() - 63
        simulation_window = pygame.Rect(SIMULATION_WINDOW_X,SIMULATION_WINDOW_Y,
        SIMULATION_WINDOW_W,SIMULATION_WINDOW_H)
        pygame.draw.rect(self.display, SIMULATION_SCREEN_COLOR, simulation_window)
        self.draw_text("Create new project to start simulation +", (499,342), FONT, LIGHT_GRAY)
        pygame.display.flip()  # Update the display

    def get_map_area(self):
        """Return the x, y, width, and height of the map section."""
        return (self.map_x, self.map_y, self.map_width, self.map_height)
    
    #tab methods
    def add_new_tab(self):
        # Find the first available position in the tab list
        existing_positions = {tab.position for tab in filter(None, self.tab_manager.tabs)}  # Set of occupied positions
        new_position = 0  # Start from index 0

        # Find the first available index
        while new_position in existing_positions:
            new_position += 1
                
        new_project = Project(project_id=new_position)  # Create a new project
        self.projects[new_position] = new_project
        self.tab_manager.add_tab(new_position, new_project)
        self.active_project = new_project  # Update active project reference

        SIMULATION_WINDOW_X = 40
        SIMULATION_WINDOW_Y = 63
        SIMULATION_WINDOW_W = self.display.get_width() - 40
        SIMULATION_WINDOW_H = self.display.get_height() - 63
        new_project.map_view = MapView(self.display, SIMULATION_WINDOW_X, SIMULATION_WINDOW_Y, SIMULATION_WINDOW_W, SIMULATION_WINDOW_H)

        print("Switched to project " + str(new_position) + "by adding new tab")

        # Reset bounding box selection
        self.drag.start_coord = None
        self.drag.end_coord = None
        self.drag.dragging = False


    def close_tab(self, tab_id):
        self.tab_manager.remove_tab(tab_id)

    def switch_tab(self, tab_id):
        self.tab_manager.select_tab(tab_id)
        self.active_project = self.projects[tab_id]
        print("Switched to project " + str(tab_id) + " by click")

        # Reset bounding box selection
        # print("Resetting bounding box coords after switching tabs")
        self.drag.start_coord = None
        self.drag.end_coord = None
        self.drag.dragging = False

        # If the new project has a saved bounding box, restore it
        if self.active_project.bounding_box:
            x1, y1, x2, y2 = self.active_project.bounding_box
            print(x1,y1,x2,y2)
            if (x1, y1) != (x2, y2):  # Ensure it's a valid box
                self.drag.start_coord = (x1, y1)
                self.drag.end_coord = (x2, y2)
                print("Restoring:", self.drag.start_coord, self.drag.end_coord)
            else:
                print("Warning: Stored bounding box has identical start and end coordinates.")
                self.drag.start_coord = None
                self.drag.end_coord = None

    def draw_tabs(self):
        for tab in filter(None, self.tab_manager.tabs):
            tab.draw(self.display)

    def draw_window(self):

        SIMULATION_WINDOW_X = 40
        SIMULATION_WINDOW_Y = 30
        SIMULATION_WINDOW_W = self.display.get_width() - 40
        SIMULATION_WINDOW_H = self.display.get_height() - 63
        SIMULATION_SCREEN_COLOR = (48,48,49)
        CREATE_PROJECT_X = 499
        # if self.fullscreen:
        #     prompt_x = 562
        # else: 
        #     prompt_x = 499
        simulation_window = pygame.Rect(SIMULATION_WINDOW_X,SIMULATION_WINDOW_Y,
        SIMULATION_WINDOW_W,SIMULATION_WINDOW_H)
        pygame.draw.rect(self.display, SIMULATION_SCREEN_COLOR, simulation_window)

        self.draw_text("Create new project to start simulation +", (CREATE_PROJECT_X,342), FONT, LIGHT_GRAY)
        pygame.draw.rect(self.display, TAB_COLOR, (40,32, SIMULATION_WINDOW_W,32)) #tab
        pygame.draw.rect(self.display, WHITE, (40,32, SIMULATION_WINDOW_W + 1,32), 1) #tab border
        self.draw_tabs()  # Draw tab bar

        self.display_mars_full_map()

        self.project_drop_down.draw(self.display)
        self.select_rover_drop_down.draw(self.display)
        self.add_rover_button.draw(self.display)
        self.help_button.draw(self.display)
        self.close_window_button.draw(self.display)
        self.restore_window_button.draw(self.display)
        self.minimize_window_button.draw(self.display)

        self.error_button.draw(self.display)
        self.view_data_button.draw(self.display)
        self.setting_button.draw(self.display)

        # Draw bounding box selection
        # self.drag.draw()

    def run(self, events):
        self.display.fill((30,33,38))

        # Project Dragdown Logic
        project_dragdown_option = self.project_drop_down.update(events)
        if project_dragdown_option >= 0:  # If a valid option was selected
            selected_option = self.project_drop_down.options[project_dragdown_option]
            if selected_option == "New Project":
                self.add_new_tab()
            
        current_project = self.active_project   

         # Process UI events
        rover_select_dragdown_option = self.select_rover_drop_down.update(events)
        self.add_rover_button.update(events)
        self.help_button.update(events)
        self.close_window_button.update(events)
        self.restore_window_button.update(events)
        self.minimize_window_button.update(events)
        self.setting_button.update(events)
        self.error_button.update(events)
        self.view_data_button.update(events) 
        # self.map_view.update()

        # Handle Window Control
        if self.close_window_button.is_clicked:
            pygame.quit()
            sys.exit()
        if self.minimize_window_button.is_clicked:
            self.sdl2_window.minimize()
        
        # Handle help button
        if self.help_button.is_clicked:
            self.show_help_popup = not self.show_help_popup  # Toggle the popup visibility
            if self.show_help_popup:
                self.help_popup.show(get_text_file("../text_files/help_desc.txt"))
            else:
                self.help_popup.hide()

        # if self.restore_window_button.is_clicked:
        #     self.toggle_fullscreen()
        #     self.restore_window_button.is_clicked = False  # Reset after toggle


        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if project_dragdown_option < 0: #prevents pressing tab0 when pressing dragdown
                    #modify
                    for tab in filter(None, self.tab_manager.tabs):
                        if tab.check_click(event.pos) == "select":   
                            self.switch_tab(tab.tab_id)
                        elif tab.check_click(event.pos) == "close":
                            self.close_tab(tab.tab_id)
                            print("Closed tab:", tab.tab_id)
                            if self.tab_manager.active_tab_index is not None:
                                print("Switching to this tab after closing tab", self.tab_manager.active_tab_index)
                                self.switch_tab(self.tab_manager.active_tab_index)
                            else:
                                print("no more tabs")
                                self.active_project = None
                                print(self.projects)
                                self.reset_simulation_window()


            # if event.type == pygame.VIDEORESIZE:  # Handle window resize properly
            #     self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            # If popup is open, let it handle events
            if self.help_popup.visible:
                self.help_popup.handle_event(event)

            if current_project and not current_project.bounding_box_selected:
                # print("Dragging mouse for bounding box is active")
                if not self.drag.dragging:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            current_project.map_view.handle_scroll(100) # Scroll left
                        if event.key == pygame.K_RIGHT:
                            current_project.map_view.handle_scroll(-100)  # Scroll right
                coords = current_project.map_view.draw()
                self.drag.update(events, coords)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Prevent new selection if finalized
                    # Ensure click is within the bounding box area
                    if self.drag.active and not current_project.selection_made:  
                        coords = self.drag.get_bounds()
                        if coords is not None:  # Prevent accidental None assignments
                            current_project.start_selection(coords)

                elif event.type == pygame.MOUSEMOTION and current_project.selecting_box:
                    # Prevent modification if finalized
                    if not current_project.selection_made:
                        coords = self.drag.get_bounds()
                        if coords is not None and coords != current_project.bounding_box:
                            current_project.update_selection(coords)

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # Prevent re-finalizing
                    if current_project.selecting_box and not current_project.selection_made:
                        if self.drag.start_coord != self.drag.end_coord:
                            current_project.selection_made = True
                        else:
                            print("Invalid selection: start and end coordinates are the same.")
        
        # Handle confirm and reset bounding box buttons
        self.confirm_bb.update(events)
        self.reset_bb.update(events)

        if self.confirm_bb.is_clicked and current_project.selection_made:
            current_project.finalize_selection()
            print(f"Bounding box set: {current_project.project_id, current_project.bounding_box}")
            current_project.selection_made = False

            offset = (40, 62)
            top_left, bot_right = self.drag.get_bounds()
            self.active_project.map_view.update(top_left, bot_right)
            self.drag.reset()

        elif self.reset_bb.is_clicked and current_project.selection_made:
            self.active_project.selection_made = False
            self.active_project.bounding_box = None  # Clear the stored bounding box
            self.drag.start_coord = None
            self.drag.end_coord = None
            self.drag.dragging = False
        
        # Draw UI elements
        self.draw_window()


        # Draw bounding box buttons if selection is made
        if current_project and current_project.selection_made:
            self.reset_bb.draw(self.display)
            self.confirm_bb.draw(self.display)

        # Display Help Popup Window
        if self.show_help_popup:
            self.help_popup.draw()

        
    def display_mars_full_map(self):
        # Mars Full Map
        #need to add condition for when no longer selecting area
        if self.active_project:
            self.active_project.map_view.draw_start_screen()
            coords = self.active_project.map_view.draw()
            if not self.active_project.bounding_box_selected:
                self.drag.draw(coords)

    def get_size(self):
        return self.width, self.height
    
    
        
