import pygame
from gui.control_element.button import Button
from gui.control_element.drop_down import DropDown
from gui.control_element.slider import Slider
from models import rover, presets
from models.rover import Rover
from utils.paths import REGULAR, get_image, get_text_file

class EditRover:
    def __init__(self, display, rover=None, algorithm=None, coordinates=[]):

        # Edit Rover Window Fields
        self.display = display
        self.rover = rover
        self.algorithm = algorithm
        self.coordinates = coordinates
        self.active = False  # Whether the popup is active
        self.font_20 = pygame.font.Font(REGULAR, 20)
        self.font_15 = pygame.font.Font(REGULAR, 15) 
        self.font_10 = pygame.font.Font(REGULAR, 12) 
        self.error_message = None
        self.selected_attr = None  # Track selected input

        self.euc_val = 0
        self.man_val = 0
        self.geo_val = 0

        self.as_val = 0
        self.lap_val = 0
        self.se_val = 0
        self.ee_val = 0

        self.heuristic_offset_y = 20

        self.heuristic_value = {
            'euclidean': self.euc_val,
            'manhattan': self.man_val,
            'geographical': self.geo_val,
            'astar': self.as_val,
            'laplacian': self.lap_val,
            'structural_entropy': self.se_val,
            'edge_entropy': self.ee_val,
        }

        self.rover_attributes = {}
        if self.rover:
            for attr, value in vars(self.rover).items():
                self.rover_attributes[attr] = str(value)  # Store as strings

        # Windows dimensions
        algo_rect_width = 600
        rov_rect_width = 300
        box_height = 500
        spacing = 10  # Space between the boxes
        total_width = algo_rect_width + rov_rect_width + spacing

        # Calculate x positions to center both windows
        start_x = (display.get_width() - total_width) // 2

        # Define rectangles for the two windows
        self.algorithm_rect = pygame.Rect(start_x, (display.get_height() - box_height) // 2, algo_rect_width, box_height)
        self.rover_rect = pygame.Rect(start_x + algo_rect_width + spacing, (display.get_height() - box_height) // 2, rov_rect_width, box_height)


        # Setting the  for UI elements
        # COLOR_UI_INACTIVE = (30,33,38)
        COLOR_UI_INACTIVE = (65, 71, 82)
        COLOR_UI_ACTIVE = "orange"
        TEXT_COLOR = "white"
        BORDER_RADIUS = 3
        UI_H = 20
        UI_W = 150
        FONT = pygame.font.Font(REGULAR, 12)
        
        # Special case for smaller open/close
        ICON_W = 25
        CLOSE_ICON = pygame.image.load(get_image('icon_close.png'))


        
        ########## Top Title Bar #############3

        self.close_button = Button("Close", COLOR_UI_INACTIVE, COLOR_UI_ACTIVE, FONT, TEXT_COLOR, BORDER_RADIUS, self.algorithm_rect.x + self.algorithm_rect.width - 40, self.algorithm_rect.y + 5, ICON_W, UI_H, CLOSE_ICON, 0.8)

        self.confirm_button = Button(None, COLOR_UI_INACTIVE, COLOR_UI_ACTIVE, FONT, TEXT_COLOR, BORDER_RADIUS, self.algorithm_rect.x + self.algorithm_rect.width - 70, self.algorithm_rect.y + 5, ICON_W, UI_H, CLOSE_ICON, 0.8)

        ####### Rover Selection Section ##########

        ROVER_OPTIONS = ["Curiosity","Perseverance", "Lunokhod1", "Lunokhod2", "Custom"]

        self.rover_drop_down = DropDown("Rover", ROVER_OPTIONS, COLOR_UI_INACTIVE, COLOR_UI_ACTIVE, COLOR_UI_INACTIVE, COLOR_UI_ACTIVE,FONT, TEXT_COLOR, 5, self.algorithm_rect.x + 30, self.algorithm_rect.y + 70, UI_W, UI_H, 150, scroll_icon_actif=True)


        ####### Algorithm Selection Section ##########

        #Algorithms

        self.astar_button = Button("A*", COLOR_UI_INACTIVE, COLOR_UI_ACTIVE, FONT, TEXT_COLOR, BORDER_RADIUS, self.algorithm_rect.x + 30, self.algorithm_rect.y + 200, UI_W, UI_H, maintain_click= True)

        self.bfs_button = Button("BFS", COLOR_UI_INACTIVE, COLOR_UI_ACTIVE, FONT, TEXT_COLOR, BORDER_RADIUS, self.algorithm_rect.x + 30, self.algorithm_rect.y + 230, UI_W, UI_H, maintain_click= True)

        self.dfs_button = Button("DFS", COLOR_UI_INACTIVE, COLOR_UI_ACTIVE, FONT, TEXT_COLOR, BORDER_RADIUS, self.algorithm_rect.x + 30, self.algorithm_rect.y + 260, UI_W, UI_H, maintain_click= True)

        # Points
        self.one_point_button = Button(None, COLOR_UI_INACTIVE, COLOR_UI_ACTIVE, FONT, TEXT_COLOR, BORDER_RADIUS, self.algorithm_rect.x + 150, self.algorithm_rect.y + 310, ICON_W, UI_H, maintain_click= True)

        self.multiple_points_button = Button(None, COLOR_UI_INACTIVE, COLOR_UI_ACTIVE, FONT, TEXT_COLOR, BORDER_RADIUS, self.algorithm_rect.x + 150, self.algorithm_rect.y + 340, ICON_W, UI_H, maintain_click= True)

        self.select_coords_button = Button("Select Coordinate(s)", COLOR_UI_INACTIVE, COLOR_UI_ACTIVE, FONT, TEXT_COLOR, BORDER_RADIUS, self.algorithm_rect.x + 30, self.algorithm_rect.y + 380, UI_W + 20, UI_H + 5)


        ####### Heuristics Selection Section ##########

        SLIDER_X = self.algorithm_rect.x + 420

        self.euclidean_slider = Slider(0.01, COLOR_UI_INACTIVE, TEXT_COLOR, COLOR_UI_ACTIVE, SLIDER_X, self.algorithm_rect.y + 190 + self.heuristic_offset_y, 100, 15)
        self.manhattan_slider = Slider(0.01, COLOR_UI_INACTIVE, TEXT_COLOR, COLOR_UI_ACTIVE, SLIDER_X, self.algorithm_rect.y + 210 + self.heuristic_offset_y, 100, 15)
        self.geographical_slider = Slider(0.01, COLOR_UI_INACTIVE, TEXT_COLOR, COLOR_UI_ACTIVE, SLIDER_X, self.algorithm_rect.y + 230 + self.heuristic_offset_y, 100, 15)
        

        self.AS_slider = Slider(0.01, COLOR_UI_INACTIVE, TEXT_COLOR, COLOR_UI_ACTIVE, SLIDER_X, self.algorithm_rect.y + 270 + self.heuristic_offset_y, 100, 15)
        self.LAP_slider = Slider(0.01, COLOR_UI_INACTIVE, TEXT_COLOR, COLOR_UI_ACTIVE, SLIDER_X, self.algorithm_rect.y + 290 + self.heuristic_offset_y, 100, 15)
        self.SE_slider = Slider(0.01, COLOR_UI_INACTIVE, TEXT_COLOR, COLOR_UI_ACTIVE, SLIDER_X, self.algorithm_rect.y + 310 + self.heuristic_offset_y, 100, 15)
        self.EE_slider = Slider(0.01, COLOR_UI_INACTIVE, TEXT_COLOR, COLOR_UI_ACTIVE, SLIDER_X, self.algorithm_rect.y + 330 + self.heuristic_offset_y, 100, 15)



################# Helper Functions ############################

    def toggle_popup(self):
        self.active = not self.active
    
    def load_preset(self, rover_name):
        print("loading preset")
        match rover_name:
            case "Curiosity":
                return presets.create_curiosity()
            case "Perseverance":
                return presets.create_perseverance()
            case "Lunokhod2":
                return presets.create_lunokhod2()
            case "Lunokhod1":
                return presets.create_lunokhod1()
            case "Custom":
                new_rover = Rover()
                return new_rover
            
    def set_rover_attributes(self, rover=None):
        """Updates the displayed attributes when a new rover is selected."""
        if rover:
            self.rover = rover  # Set the new rover
        if self.rover:
            self.rover_attributes = {attr: str(value) for attr, value in vars(self.rover).items()}
        else:
            self.rover_attributes = {}  # Clear attributes if no rover is set
    
    def reset(self):
        """Resets all fields to their default values."""
        self.rover = None
        self.algorithm = None
        self.coordinates = []
        self.error_message = None
        self.selected_attr = None
        
        # Reset heuristic values
        self.euc_val = 0
        self.man_val = 0
        self.geo_val = 0
        self.as_val = 0
        self.lap_val = 0
        self.se_val = 0
        self.ee_val = 0
        
        self.heuristic_value = {
            'euclidean': self.euc_val,
            'manhattan': self.man_val,
            'geographical': self.geo_val,
            'astar': self.as_val,
            'laplacian': self.lap_val,
            'structural_entropy': self.se_val,
            'edge_entropy': self.ee_val,
        }
        
        # Reset rover attributes
        self.rover_attributes = {}

        # Reset UI elements
        self.rover_drop_down.selected_index = -1  # No rover selected
        self.astar_button.is_clicked = False
        self.bfs_button.is_clicked = False
        self.dfs_button.is_clicked = False
        self.one_point_button.is_clicked = False
        self.multiple_points_button.is_clicked = False
        self.euclidean_slider.value = 0
        self.manhattan_slider.value = 0
        self.geographical_slider.value = 0
        self.AS_slider.value = 0
        self.LAP_slider.value = 0
        self.SE_slider.value = 0
        self.EE_slider.value = 0

    def get_window_attributes(self):
        if self.algorithm == "A*":
            return [self.rover, self.algorithm, self.coordinates, self.heuristic_value]
        else:
            return [self.rover, self.algorithm, self.coordinates]
    
    # Check for the presence of all field and more before being able to press confirm
    def check_validity(self):
        missing_fields = []

        if self.rover is None:
            missing_fields.append("rover")
        if self.algorithm is None:
            missing_fields.append("algorithm")
        if not self.coordinates:
            missing_fields.append("coordinates")
        if self.algorithm is "A*" and float(self.euc_val) <= 0 and float(self.man_val) <= 0 and float(self.geo_val) <= 0:
            return "At least one of the distance calculation heuristics must be higher than 0"


        if missing_fields:
            return f"Missing fields: {', '.join(missing_fields)}"
        
        return True
    
    #TODO: implement
    
    def select_coordinates(self):
        return [1, 42, 123]

    def update(self, events):
        if not self.active:
            return
        
        self.close_button.update(events)
        self.confirm_button.update(events)
        self.select_coords_button.update(events)
        self.euc_val = self.euclidean_slider.update(events)
        self.man_val = self.manhattan_slider.update(events)
        self.geo_val = self.geographical_slider.update(events)
        self.as_val = self.AS_slider.update(events)
        self.lap_val = self.LAP_slider.update(events)
        self.se_val = self.SE_slider.update(events)
        self.ee_val = self.EE_slider.update(events)

        algo_buttons = [self.astar_button, self.bfs_button, self.dfs_button]

        # Update all algorithm buttons and enforce exclusivity
        for button in algo_buttons:
            button.update(events)
            if button.is_clicked:
                self.algorithm = button.name
                for other_button in algo_buttons:
                    other_button.is_clicked = (other_button == button)  # Only keep the clicked one active
        
        point_buttons = [self.one_point_button, self.multiple_points_button]

        for button in point_buttons:
            button.update(events)
            if button.is_clicked:
                for other_button in point_buttons:
                    other_button.is_clicked = (other_button == button)  # Only keep the clicked one active


        rover_selection = self.rover_drop_down.update(events)
        if rover_selection >= 0:
            selected_option = self.rover_drop_down.options[rover_selection]
            preload_rover = self.load_preset(selected_option)
            self.set_rover_attributes(preload_rover)  # Update displayed attributes

        if self.close_button.is_clicked:
            self.active = False

        if self.confirm_button.is_clicked:
            self.confirm_button.is_clicked = False
            validity_check = self.check_validity()
            if validity_check is True:
                self.active = False
                attributes = self.get_window_attributes()
                print(self.get_window_attributes())
                self.reset()
                return attributes
            else:
                # Store the error message if any fields are missing
                self.error_message = validity_check
        
        if self.select_coords_button.is_clicked:
            coordinates = self.select_coordinates()
            self.coordinates = coordinates




################# Operation Functions ############################


    def draw(self, display):
        """Draws the popup window with both boxes."""
        if not self.active:
            return

        # Draw thick main popup box
        pygame.draw.rect(display, (30,33,38), self.algorithm_rect, border_radius=2)  
        pygame.draw.rect(display, (65, 71, 82), self.algorithm_rect, 1,border_radius=2)

        # Draw lean side box
        pygame.draw.rect(display, (30,33,38), self.rover_rect,border_radius=2)
        pygame.draw.rect(display, (65, 71, 82), self.rover_rect, 1, border_radius=2)


        #Horizontal lines
        #Title Bar
        pygame.draw.line(display, (65, 71, 82), (self.algorithm_rect.x, self.algorithm_rect.y + 30), (self.algorithm_rect.x + self.algorithm_rect.w, self.algorithm_rect.y + 30), 1)

        #Rover Bar
        pygame.draw.line(display, (65, 71, 82), (self.algorithm_rect.x, self.algorithm_rect.y + 135), (self.algorithm_rect.x + self.algorithm_rect.w, self.algorithm_rect.y + 135), 1)

        #Algorithm Bar
        pygame.draw.line(display, (65, 71, 82), (self.algorithm_rect.x, self.algorithm_rect.y + self.algorithm_rect.h - 70), (self.algorithm_rect.x + self.algorithm_rect.w, self.algorithm_rect.y + self.algorithm_rect.h - 70), 1)

        # pygame.draw.line(display, (65, 71, 82), (self.algorithm_rect.x, self.algorithm_rect.y + 12), (self.algorithm_rect.x + self.algorithm_rect.w, self.algorithm_rect.y + 12), 1)


        TEXT_TITLE = self.font_15.render("Rover Settings", True, "white")  
        display.blit(TEXT_TITLE, (self.algorithm_rect.x + 9, self.algorithm_rect.y + 5)) 

        TEXT_ROVER_SELECTION = self.font_20.render("Rover Selection", True, "white")  
        display.blit(TEXT_ROVER_SELECTION, (self.algorithm_rect.x + 30, self.algorithm_rect.y + 40)) 

        TEXT_ALG_FIELD = self.font_20.render("Algorithm Field", True, "white")  
        display.blit(TEXT_ALG_FIELD, (self.algorithm_rect.x + 30, self.algorithm_rect.y + 150))



        TEXT_A_POINT = self.font_15.render("One Point", True, "white")  
        display.blit(TEXT_A_POINT , (self.algorithm_rect.x + 40, self.algorithm_rect.y + 310)) 

        TEXT_MULT_POINT = self.font_15.render("Multiple Point", True, "white")
        display.blit(TEXT_MULT_POINT, (self.algorithm_rect.x + 40, self.algorithm_rect.y + 340)) 

        # Draw input fields inside thick box
        # Draw input fields inside rover_rect
        y_offset = self.rover_rect.y + 20
        for attr, value in self.rover_attributes.items():
            text_surf = self.font_15.render(f"{attr}: {value}", True, "white")
            display.blit(text_surf, (self.rover_rect.x + 20, y_offset))
            y_offset += 25


        # Draw close button
        self.close_button.draw(self.display)
        self.confirm_button.draw(self.display)
        self.rover_drop_down.draw(self.display)
        self.one_point_button.draw(self.display)
        self.multiple_points_button.draw(self.display)

        self.astar_button.draw(self.display)
        self.bfs_button.draw(self.display)
        self.dfs_button.draw(self.display)

        # Heuristic Section of the windows only shows when A* is selected.

        if self.astar_button.is_clicked:

            X = self.algorithm_rect.x + 300

            # Section Headers Display
            heuristics_text = self.font_20.render("Heuristics", True, "white")  
            display.blit(heuristics_text, (X, self.algorithm_rect.y + 150))
            distance_calc_text = self.font_15.render("Distance Calculation", True, "white")
            display.blit(distance_calc_text, (X, self.algorithm_rect.y + 180))

            # DISTANCE CALCULATION HEURISTICS

            DIST_CALC_HEURISTICS = ["Euclidean", "Manhattan", "Geographical"]
            y_offset = self.algorithm_rect.y + 190 + self.heuristic_offset_y
            for heuristic in DIST_CALC_HEURISTICS:
                text_surf = self.font_10.render(heuristic, True, "white")
                display.blit(text_surf, (X, y_offset))
                y_offset += 20

            self.euclidean_slider.draw(self.display)
            self.manhattan_slider.draw(self.display)
            self.geographical_slider.draw(self.display)

            VAL_X = self.algorithm_rect.x + 530

            euc_val_text = self.font_15.render(str(self.euc_val), True, "white")
            display.blit(euc_val_text, (VAL_X, self.algorithm_rect.y +190  + self.heuristic_offset_y))

            man_val_text = self.font_15.render(str(self.man_val), True, "white")
            display.blit(man_val_text, (VAL_X, self.algorithm_rect.y +210 + self.heuristic_offset_y))

            geo_val_text = self.font_15.render(str(self.geo_val), True, "white")
            display.blit(geo_val_text, (VAL_X, self.algorithm_rect.y +230 + self.heuristic_offset_y))



            OTHER_HEURISTICS = ["Altitude Stable", "LAP", "Solar Exposure", "Energy Efficient"]
            y_offset = self.algorithm_rect.y + 270 + self.heuristic_offset_y
            for heuristic in OTHER_HEURISTICS:
                text_surf = self.font_10.render(heuristic, True, "white")
                display.blit(text_surf, (X, y_offset))
                y_offset += 20

            self.AS_slider.draw(self.display)
            self.LAP_slider.draw(self.display)
            self.SE_slider.draw(self.display)
            self.EE_slider.draw(self.display)

            as_val_text = self.font_15.render(str(self.as_val), True, "white")
            display.blit(as_val_text, (VAL_X, self.algorithm_rect.y + 270  + self.heuristic_offset_y))

            lap_val_text = self.font_15.render(str(self.lap_val), True, "white")
            display.blit(lap_val_text, (VAL_X, self.algorithm_rect.y + 290 + self.heuristic_offset_y))

            se_val_text = self.font_15.render(str(self.se_val), True, "white")
            display.blit(se_val_text, (VAL_X, self.algorithm_rect.y + 310 + self.heuristic_offset_y))

            ee_val_text = self.font_15.render(str(self.ee_val), True, "white")
            display.blit(ee_val_text, (VAL_X, self.algorithm_rect.y + 330 + self.heuristic_offset_y))
        
        if self.multiple_points_button.is_clicked or self.one_point_button.is_clicked:
            self.select_coords_button.draw(self.display)
        
        if hasattr(self, 'error_message') and self.error_message:  
            error_text = self.font_15.render(f"! {self.error_message}", True, "orange")  
            display.blit(error_text, (self.algorithm_rect.x + 40, self.algorithm_rect.y + 450))
