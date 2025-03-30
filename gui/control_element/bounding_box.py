import pygame

class BoundingBox:
    def __init__(self, screen, simulation, x, y, w, h, max_area):
        self.screen = screen
        self.simulation = simulation
        self.rect = pygame.Rect(x, y, w, h)
        self.active = False
        self.font = pygame.font.SysFont("arial", 13)
        self.max_area = max_area

        self.coords = None
        self.start_coord = None
        self.end_coord = None
        self.dragging = False
        self.exceeded = False  

        #hold lat, long
        self.start_lat_long = None
        self.end_lat_long = None

    # # return coordinates of mouse position
    def get_coordinates(self):
        mpos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mpos):
            return (mpos[0] - self.rect.x, mpos[1] - self.rect.y)
        return None # Ignore coordinates if outside
    
    # return bound of bounding box
    def get_bounds(self):
        # return self.start_coord, self.end_coord

        return self.start_lat_long, self.end_lat_long

    # reset bound of bounding box
    def reset(self):
        self.start_coord = None
        self.end_coord = None

    def enforce_ratio(self, width, height):
        if width == 0:
            return width, height  # Avoid division by zero

        min_ratio = 0.6  # Minimum allowed aspect ratio (height/width)
        max_ratio = 0.85  # Maximum allowed aspect ratio

        # Clamp height to be within the ratio range
        target_height = max(int(width * min_ratio), min(int(width * max_ratio), height))

        # Ensure the area does not exceed max_area
        area = width * target_height
        if area > self.max_area:
            scale_factor = (self.max_area / area) ** 0.5  # Reduce both width & height proportionally
            width = int(width * scale_factor)
            target_height = int(target_height * scale_factor)

        return width, target_height



    def draw(self,coords):
        if self.start_coord and self.end_coord:
            drag_x = min(self.start_coord[0], self.end_coord[0]) 
            drag_y = min(self.start_coord[1], self.end_coord[1]) 
            drag_w = abs(self.end_coord[0] - self.start_coord[0])
            drag_h = abs(self.end_coord[1] - self.start_coord[1])
            
            drag_w, drag_h = self.enforce_ratio(drag_w, drag_h)
            
            dragging_box = pygame.Rect(drag_x, drag_y, drag_w, drag_h)
            color = (255, 0, 0) if self.exceeded else (200, 200, 200)
            pygame.draw.rect(self.screen, color, dragging_box, 1)

        if self.active:
            mpos = pygame.mouse.get_pos()
            # coord_placement = self.get_coordinates()
            if coords:
                text_surface = self.font.render(str(coords), True, "white")
                # self.screen.blit(text_surface, (mpos[0] + 10, mpos[1] + 10))
                # If mpos not close to right edge
                if mpos[0] < self.screen.get_width() - text_surface.get_width() - 30:
                     text_pos = (mpos[0] + 10, mpos[1] + 10)
                 # If mpos too close to right edge, put text on left side
                else:
                     text_pos = (mpos[0] - text_surface.get_width() - 5, mpos[1] + 10)
 
                self.screen.blit(text_surface, text_pos)

    def update(self, events, coords):
        mpos = pygame.mouse.get_pos()
        self.active = self.rect.collidepoint(mpos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.active and not self.simulation.active_project.selection_made:
                    self.start_coord = mpos
                    self.end_coord = mpos
                    self.start_lat_long = coords
                    self.dragging = True
                    self.exceeded = False

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                if self.active and not self.simulation.active_project.selection_made:
                    self.end_coord = mpos
                    new_end = mpos
                    if new_end:
                        new_x = max(0, min(new_end[0], self.rect.width))   # Clamp x within bounds
                        new_y = max(0, min(new_end[1], self.rect.height))  # Clamp y within bounds
                        new_width = abs(new_x - self.start_coord[0])
                        new_height = abs(new_y - self.start_coord[1])
                        new_width, new_height = self.enforce_ratio(new_width, new_height)
                        
                        new_area = new_width * new_height
                        if new_area <= self.max_area:
                            self.end_coord = (self.start_coord[0] + new_width, self.start_coord[1] + new_height)
                            self.exceeded = False
                        else:
                            self.exceeded = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.end_lat_long = coords
                if self.dragging and not self.simulation.active_project.selection_made:
                    self.dragging = False
                    if self.start_coord and self.end_coord and not self.exceeded:
                        if self.simulation.active_project:
                            self.simulation.active_project.bounding_box = (
                                max(0, min(self.start_coord[0], self.rect.width)), 
                                max(0, min(self.start_coord[1], self.rect.height)), 
                                max(0, min(self.end_coord[0], self.rect.width)), 
                                max(0, min(self.end_coord[1], self.rect.height))
                            )
                            self.simulation.active_project.selection_made = True  # Mark as finalized
                            print(f"Current selection of bounding box: {self.simulation.active_project.bounding_box}")
              


