import pygame

class BoundingBox:
    def __init__(self, screen, simulation, x, y, w, h, max_area):
        self.screen = screen
        self.simulation = simulation
        self.rect = pygame.Rect(x, y, w, h)
        self.active = False
        self.font = pygame.font.SysFont("arial", 13)
        self.max_area = max_area

        self.start_coord = None
        self.end_coord = None
        self.dragging = False
        self.exceeded = False  

    def get_coordinates(self):
        mpos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mpos):
            return (mpos[0] - self.rect.x, mpos[1] - self.rect.y)
        return None

    def enforce_ratio(self, width, height):
        if width == 0:
            return width, height 

        # height/width
        min_ratio = 0.8  
        max_ratio = 0.3  

        target_height = max(int(width * max_ratio), min(int(width * min_ratio), height))
        
        return width, target_height

    def draw(self):
        if self.start_coord and self.end_coord:
            drag_x = min(self.start_coord[0], self.end_coord[0]) + self.rect.x
            drag_y = min(self.start_coord[1], self.end_coord[1]) + self.rect.y
            drag_w = abs(self.end_coord[0] - self.start_coord[0])
            drag_h = abs(self.end_coord[1] - self.start_coord[1])
            
            drag_w, drag_h = self.enforce_ratio(drag_w, drag_h)
            
            dragging_box = pygame.Rect(drag_x, drag_y, drag_w, drag_h)
            color = (255, 0, 0) if self.exceeded else (200, 200, 200)
            pygame.draw.rect(self.screen, color, dragging_box, 1)

        if self.active:
            mpos = pygame.mouse.get_pos()
            coords = self.get_coordinates()
            if coords:
                text_surface = self.font.render(str(coords), True, "white")
                self.screen.blit(text_surface, (mpos[0] + 10, mpos[1] + 10))

    def update(self, events):
        mpos = pygame.mouse.get_pos()
        self.active = self.rect.collidepoint(mpos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.active and not self.simulation.active_project.selection_made:
                    self.start_coord = self.get_coordinates()
                    self.end_coord = self.start_coord
                    self.dragging = True
                    self.exceeded = False

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                if self.active and not self.simulation.active_project.selection_made:
                    new_end = self.get_coordinates()
                    if new_end:
                        new_width = abs(new_end[0] - self.start_coord[0])
                        new_height = abs(new_end[1] - self.start_coord[1])
                        new_width, new_height = self.enforce_ratio(new_width, new_height)
                        new_area = new_width * new_height

                        if new_area <= self.max_area:
                            self.end_coord = (self.start_coord[0] + new_width, self.start_coord[1] + new_height)
                            self.exceeded = False
                        else:
                            self.exceeded = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.dragging and not self.simulation.active_project.selection_made:
                    self.dragging = False
                    if self.start_coord and self.end_coord and not self.exceeded:
                        if self.simulation.active_project:
                            self.simulation.active_project.bounding_box = (
                                min(self.start_coord[0], self.end_coord[0]), 
                                min(self.start_coord[1], self.end_coord[1]), 
                                max(self.start_coord[0], self.end_coord[0]), 
                                max(self.start_coord[1], self.end_coord[1])
                            )
                            self.simulation.active_project.selection_made = True  # Mark as finalized
                            print(f"Finalized bounding box: {self.simulation.active_project.bounding_box}")
              


