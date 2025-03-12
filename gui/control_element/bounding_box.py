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
        #Returns mouse coordinates relative to the bounding box.
        mpos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mpos):  # Ensure mouse is inside the bounding box
            return (mpos[0] - self.rect.x, mpos[1] - self.rect.y)
        return None  # Ignore coordinates if outside

    def draw(self):
        #Draws the bounding box and the dragging selection if active.
        if self.start_coord and self.end_coord:
            drag_x = min(self.start_coord[0], self.end_coord[0]) + self.rect.x
            drag_y = min(self.start_coord[1], self.end_coord[1]) + self.rect.y
            drag_w = abs(self.end_coord[0] - self.start_coord[0])
            drag_h = abs(self.end_coord[1] - self.start_coord[1])

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
        #Handles events for mouse interaction.
        mpos = pygame.mouse.get_pos()
        self.active = self.rect.collidepoint(mpos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.active:
                    self.start_coord = self.get_coordinates()
                    self.end_coord = self.start_coord
                    self.dragging = True
                    self.exceeded = False  # Reset exceeded flag

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                if self.active:
                    new_end = self.get_coordinates()
                    if new_end:
                        new_width = abs(new_end[0] - self.start_coord[0])
                        new_height = abs(new_end[1] - self.start_coord[1])
                        new_area = new_width * new_height

                        if new_area <= self.max_area:
                            self.end_coord = new_end
                            self.exceeded = False
                        else:
                            self.exceeded = True  # Turn red

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging = False
                if self.start_coord and self.end_coord and not self.exceeded:
                    if self.simulation.active_project:
                        self.simulation.active_project.bounding_box = (
                            self.start_coord[0], self.start_coord[1],
                            self.end_coord[0], self.end_coord[1]
                        )
